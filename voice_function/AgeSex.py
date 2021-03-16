# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下，您可自行利用pip安装：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import ssl
import time
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket

from file_ram_convert.TokenDict import TokenDict

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

result = ''


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret

        # 设置测试音频文件
        self.AudioFile = AudioFile
        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"ent": "igr", "aue": "raw", "rate": 16000}

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/igr'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/igr " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


wsParam = Ws_Param(APPID='', APISecret='',
                   APIKey='',
                   AudioFile=r'../voice_cache/v2w.mp3')


# 收到websocket消息的处理
def on_message(ws, message):
    try:
        global result
        result = message
        # print(message)
    except Exception as e:
        print("receive msg,but parse exception:", e)
        pass


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)
    pass


# 收到websocket关闭的处理
def on_close(ws):
    # print("### closed ###")
    pass


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        frameSize = 5000  # 每一帧的音频大小
        # intervel = 0.04  # 发送音频间隔(单位:s)
        status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

        with open(wsParam.AudioFile, "rb") as fp:
            while True:
                buf = fp.read(frameSize)
                # 文件结束
                if not buf:
                    status = STATUS_LAST_FRAME
                # 第一帧处理
                # 发送第一帧音频，带business 参数
                # appid 必须带上，只需第一帧发送
                if status == STATUS_FIRST_FRAME:

                    d = {"common": wsParam.CommonArgs,
                         "business": wsParam.BusinessArgs,
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    d = json.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                    time.sleep(1)
                    break
                # 模拟音频采样间隔
                # time.sleep(intervel)
        ws.close()

    thread.start_new_thread(run, ())


def get_age_sex() -> str:
    global wsParam, result
    token_dict = TokenDict('../status_saved/aiui.npy')
    token_info = token_dict.load()
    wsParam = Ws_Param(APPID=token_info['APPID'], APISecret=token_info['APISecret'],
                       APIKey=token_info['APIKey'],
                       AudioFile=r'../voice_cache/v2w.pcm')
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    # print(result)
    result = json.loads(result)
    if result['data']['status'] == 2:
        age_result = result['data']['result']['age']['age_type']
        sex_result = result['data']['result']['gender']['gender_type']
        if age_result == '0':
            age_result = '中年'
        elif age_result == '1':
            age_result = '幼年'
        elif age_result == '2':
            age_result = '老年'
        else:
            age_result = '未知年龄'
        if sex_result == '0':
            sex_result = '女性'
        elif sex_result == '1':
            sex_result = '男性'
        else:
            sex_result = '未知性别'
        # print(age_result, sex_result)
        return '您应该是' + age_result + '、' + sex_result
    else:
        return '抱歉，分析失败，请稍后再试'


if __name__ == "__main__":
    # 测试时候在此处正确填写相关信息即可运行
    # wsParam = Ws_Param(APPID='5f8ffba0', APISecret='fb006ab543ed2b029920e07f21f5ce7e',
    #                    APIKey='38b3abe70c5866bfe6fb7c4ab36c821d',
    #                    AudioFile=r'../voice_cache/v2w.pcm')
    # websocket.enableTrace(False)
    # wsUrl = wsParam.create_url()
    # ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    # ws.on_open = on_open
    # ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    # time2 = datetime.now()
    ans = get_age_sex()
    print(ans)
