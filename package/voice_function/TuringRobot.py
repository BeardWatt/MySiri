import json
import urllib.request

from package.file_ram_convert.TokenDict import TokenDict


class TuringRobot:
    api_url = "http://openapi.tuling123.com/openapi/api/v2"
    text_input = ""
    apiKey = ""

    req = {
        "perception":
            {
                "inputText":
                    {
                        "text": text_input
                    },

                "selfInfo":
                    {
                        "location":
                            {
                                "city": "汕头",
                                "province": "广东",
                                "street": "大学路"
                            }
                    }
            },

        "userInfo":
            {
                "apiKey": apiKey,
                "userId": "OnlyUseAlphabet"
            }
    }

    def __init__(self, text_input: str):
        self.text_input = text_input
        self.req["perception"]["inputText"]["text"] = text_input
        token_loader = TokenDict('../status_saved/turingRobot.npy')
        token_info = token_loader.load()
        self.apiKey = token_info
        self.req["userInfo"]["apiKey"] = token_info["APIKey"]

    def get_respond(self) -> str:
        # print(req)
        # 将字典格式的req编码为utf8
        req = json.dumps(self.req).encode('utf8')
        # print(req)

        http_post = urllib.request.Request(self.api_url, data=req, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(http_post)
        response_str = response.read().decode('utf8')
        # print(response_str)
        response_dic = json.loads(response_str)
        # print(response_dic)

        intent_code = response_dic['intent']['code']
        results_text = response_dic['results'][0]['values']['text']
        # print('Turing的回答：')
        # print('code：' + str(intent_code))
        # print('text：' + results_text)
        return results_text


if __name__ == '__main__':
    turing_robot = TuringRobot('我是谁')
    respond_text = turing_robot.get_respond()
    print(respond_text)
