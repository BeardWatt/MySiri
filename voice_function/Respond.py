"""
获取响应
"""
import requests
import time
import hashlib
import base64

URL = "http://openapi.xfyun.cn/v2/aiui"
APPID = "5f8ffba0"
API_KEY = "1395ed070bd8df20037a4effce3cf34c"
AUE = "raw"
AUTH_ID = "2894c985bf8b1111c6728db79d3479ae"
DATA_TYPE = "audio"
SAMPLE_RATE = "16000"
SCENE = "main"
RESULT_LEVEL = "complete"
LAT = "23.412548"
LNG = "116.6281044"
# 个性化参数，需转义
PERS_PARAM = "{\\\"auth_id\\\":\\\"2894c985bf8b1111c6728db79d3479ae\\\"}"
FILE_PATH = "./voice_cache/v2w.pcm"


def buildHeader():
    curTime = str(int(time.time()))
    param = "{\"result_level\":\"" + RESULT_LEVEL + "\",\"auth_id\":\"" + AUTH_ID + "\",\"data_type\":\"" + DATA_TYPE + "\",\"sample_rate\":\"" + SAMPLE_RATE + "\",\"scene\":\"" + SCENE + "\",\"lat\":\"" + LAT + "\",\"lng\":\"" + LNG + "\"}"
    # 使用个性化参数时参数格式如下：
    # param = "{\"result_level\":\"" + RESULT_LEVEL + "\",\"auth_id\":\"" + AUTH_ID + "\",\"data_type\":\"" + DATA_TYPE + "\",\"sample_rate\":\"" + SAMPLE_RATE + "\",\"scene\":\"" + SCENE + "\",\"lat\":\"" + LAT + "\",\"lng\":\"" + LNG + "\",\"pers_param\":\"" + PERS_PARAM + "\"}"
    # print(param)
    paramBase64 = base64.b64encode(param.encode('UTF-8'))
    # print(paramBase64)

    m2 = hashlib.md5()
    # m2.update(str.encode(API_KEY + curTime + bytes.decode(paramBase64)))
    m2.update(bytes(API_KEY, 'UTF-8') + bytes(curTime, 'UTF-8') + paramBase64)
    checkSum = m2.hexdigest()
    header = {
        'X-Param': paramBase64.decode('utf-8'),
        'X-CurTime': curTime,
        'X-CheckSum': checkSum,
        'X-Appid': APPID,
    }
    # print(header)
    return header


def readFile(filePath):
    binfile = open(filePath, 'rb')
    data = binfile.read()
    return data


r = requests.post(URL, headers=buildHeader(), data=readFile(FILE_PATH))
print(r.content.decode())
