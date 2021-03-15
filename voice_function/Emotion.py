#!/usr/bin/python
# -*- coding: UTF-8 -*-
import base64
import hashlib
import json
import time
import urllib.parse
import urllib.request

# 接口地址
url = "http://ltpapi.xfyun.cn/v2/sa"
# 开放平台应用ID
x_appid = "5f8ffba0"
# 开放平台应用接口秘钥
api_key = "8e3d2ddbcb61b81a0e08bbf45f840798"
# 语言文本
TEXT = "汉皇重色思倾国，御宇多年求不得。杨家有女初长成，养在深闺人未识。天生丽质难自弃，一朝选在君王侧。"


def get_emotion(TEXT: str) -> str:
    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    result = result.decode('utf-8')
    result = json.loads(result)
    print(result)
    if result['code'] == '0':
        sentiment = result['data']['sentiment']
        if sentiment == 0:
            sentiment = '中性'
        elif sentiment == 1:
            sentiment = '褒义'
        elif sentiment == -1:
            sentiment = '贬义'
        return '这是包含' + sentiment + '情感的一句话'
    else:
        return '抱歉，分析失败，请稍后再试'


if __name__ == '__main__':
    get_emotion()
