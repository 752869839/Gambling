# coding: utf-8
"""
LZsetting.json

    这里是个人软件配置信息
    {
        "msg": "软件配置信息和用户信息",
        "ID": "用户软件ID",
        "Secret": "用户软件Secret",
        "UserName": "用户账号",
        "PassWord": "用户密码"
    }


使用说明：

verify_code：识别验证码借口
    参数：
        captchaData：验证码参数
            目前只支持 /9j/4AAQSkZJRgABAQAAAQABAAD//gA7......YUUUUAFFFFAH//Z
        captchaType: 验证码类型

    {
        "code":0,
        "data":"58F4K",
        "id":"20190214:000000000025750641035",
        "msg":"",
        "text":"当code不为0时，使用id返回调用error_code申请错误！"
    }

error_code: 验证码识别错误, 申请返回点数
    参数：
        captchaId：识别验证码，网站返回ID

check_lianzhong：检查当前用户的剩余点数以及可用点数
    {
        "code":0,
        "user_points":998,
        "available_points":998,
        "lock_points":0,
        "msg":"user_points:用户总点数, available_points:可用点数, lock_points:锁定点数"
    }

"""


import json
import requests
from requests.exceptions import Timeout
from useragent import randomUA, UA_TYPE_DESKTOP


class VerifyCode:

    def __init__(self):
        self.session = requests.session()
        self.session.headers['User-Agent'] = randomUA(UA_TYPE_DESKTOP)
        self.session.verify = False
        self.session.headers.update({
            'Host': 'v2-api.jsdama.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'text/json'
        })

        # 读取配置信息
        with open('LZsetting.json', 'r', encoding='utf-8') as f:
            s = f.read()
        setting = json.loads(s)

        self.id = setting['ID']
        self.secret = setting['Secret']
        self.user = setting['UserName']
        self.pwd = setting['PassWord']

    def verify_code(self, captchaData, captchaType):
        """
        验证验证码信息
        :return:
        """
        url = 'https://v2-api.jsdama.com/upload'
        data = {
            'softwareId': self.id,
            'softwareSecret': self.secret,
            'username': self.user,
            'password': self.pwd,
            'captchaData': captchaData,
            'captchaType': captchaType,
            'captchaMinLength': 0,
            'captchaMaxLength': 0,
            'workerTiosId': 0,
        }
        try:
            res = self.session.post(url=url, data=json.dumps(data), timeout=30)
            res_data = json.loads(res.text)
            print(res_data)
            code = res_data['code']
            data = res_data['data']['recognition']
            id = res_data['data']['captchaId']
            msg = res_data['message']
        except Timeout:
            code = 400
            data = ''
            id = id
            msg = '连接超时，检查网络重新请求，无需申请错误'

        text = '当code不为0时，使用id返回调用error_code申请错误！'
        return json.dumps({
            'code': code,
            'data': data,
            'id': id,
            'msg': msg,
            'text': text
        })

    def error_code(self, captchaId):
        """
        申请错误，返回点数，减少支出
        :param id:
        :return:
        """
        url = 'https://v2-api.jsdama.com/report-error'
        data = {
            'softwareId': self.id,
            'softwareSecret': self.secret,
            'username': self.user,
            'password': self.pwd,
            'captchaId': captchaId
        }
        try:
            res = self.session.post(url=url, data=json.dumps(data), timeout=5)
            result = res.text
        except Timeout:
            result = json.dumps({'code': 400, 'msg': '连接超时'})
        return result

    def check_lianzhong(self):
        """
        检查当前账户剩余点数
        :return:
        """
        url = 'https://v2-api.jsdama.com/check-points'
        data = {
            'softwareId': self.id,
            'softwareSecret': self.secret,
            'username': self.user,
            'password': self.pwd,
        }
        try:
            res = self.session.post(url=url, data=json.dumps(data), timeout=5)
            print(res.text)
            response = json.loads(res.text)
            code = response['code']
            msg = response['message']
            if not code == 0:
                result = {'code': code, 'msg': msg}
            else:
                available_points = response['data']['availablePoints']
                user_points = response['data']['userPoints']
                lock_points = response['data']['lockPoints']
                result = {
                    'code': code,
                    'user_points': user_points,
                    'available_points': available_points,
                    'lock_points': lock_points,
                    'msg': 'user_points:用户总点数, available_points:可用点数, lock_points:锁定点数'
                }
        except Timeout:
            result = {'code': 400, 'msg': '请求连接超时'}

        return json.dumps(result)

    def download_img(self):
        pass


if __name__ == '__main__':
    v = VerifyCode()
    captchaData = '/9j/4AAQSkZJRgABAQAAAQABAAD//gA7Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZyBJSkcgSlBFRyB2NjIpLCBxdWFsaXR5ID0gOTAK/9sAQwADAgIDAgIDAwMDBAMDBAUIBQUEBAUKBwcGCAwKDAwLCgsLDQ4SEA0OEQ4LCxAWEBETFBUVFQwPFxgWFBgSFBUU/9sAQwEDBAQFBAUJBQUJFA0LDRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU/8AAEQgAKACWAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A+3aKKK5D6gKKKKACiivDrLTfGPizxl4xn0LxfLpEVlfLFHaTwCeF8oCRyQV59K1hDnvd2sTKVuh7jRXDfDvQPGuk3l9N4s8QW+rpIoW3htogix88k/KOfxNYZ8Yar47+Jmr+GNL1Q6Hp+jxKbiaKJHnuJDjhS2QqjPUDNP2d20nououbTVHqtFeG6X8abvw1r2u+GL5z4i1C21CGx02ZMI07SZykhHAKEcmvRPD/AI2v7zxHJoWs6BPpN6IjPFPHJ59tMgODiQAYbn7pH4mnKjOOrBTTOuqG9vrbTbWS5u7iK1toxl5pnCIo9yeBWB8QvFj+EPDdxdW0IutSkVks7Y/8tJNpOT/sqAWPsprC+But3fi/4XabfatMb+6uDL5zygHf856jpj2qVTfJzvYfMr8p2ul63p+txPJp97b3saHDNBIHAPvirteLfsyW0UGn+LmhjWOJtZmCKowAoJAA/CvaaKsFTm4oIvmVwrAu/FDXNzLZaJa/2rdRMYpp1kVba1kH8Mr5zu4PyoGI43bdyk8n4x+JumPdx6Va3E98bgER22kO/wBqvmHVYpEICKP4pNw6MAcg4S1t/iPqltFFYx6J4O05VCQxPG11PHGRxlQQgdAOmSpJ68VaptK8tPX+rkuXRHomn/a/scf27yftRyXFvnYOeACeTgYGeM4zgZwIr7WrDTLqztru7it7i9kMVtE7ANMwGSFHfArgz8MfE99ldR+I2rtC3DJYQRWzBTyQHAJBz0bqBxW34T+Ffh7wfePqFtbS3mrygCbVNQma4uZT/eLMcAnPO0DNS4wWvNf0/wCCO77HXUUUViWFFFFABRRRQAVwmp/BnQb+7vbyC41XS727kMslxp+oSRNuIxkAHb+ld3XCTa54v8NeIL7+0dLGu6BKS1pLpKZuYf8AYkQkbvqDWtNy15XYmVuqOQ8AeMNd8KfFa7+H2v6g+tW7QG50/UZ/9cVC7sOe/AYZ9V96zte8Cr8TvFmo+IPA+oSaHc2pa3m1aJmCXkwGCigEcDoX+mM9a2dA8B6x4t+IeteNdXtX0XfZtYaZaSMDNGpUqZHwSAeW4z/F7U74YxeMPh94Sh8NyeETfS2TOIruG9ijilVmLBjuOR1xjBPHSu1yUXzQa5rK+1vPyMEr6S2PBde1yXTvEfhu1g8PwaR4k0DU0iuZY3LJdSMwKM2Tkk7GySe/XpX1d4T8cSasY7LWtOl0HWSCBbXHCz46tE3RhwTjqO9eD/GX4b3vh/wre+L9UmifXrzWLa4kS3z5dugDhUUnrywyfYV9I6jpOm+K9KSK/tY7y1mUOFcdM4III5H4VOJcZQjKPn/X4mtCybjP/gnm954v0TV59Z17U9UtbaxSCbT9JjllGZcgiSVR33MNox2X3rk/gF8SF0H4YWVmuhaxqUiTSRq9nal43kY5VA2cc+p4Hc11Gr/BlPCFvPd+CLVBfzMUW0nSJ4hnPzb3GVA9iT0FN+GHhDxr8JvBd1p722m62ke6a3traVo5t55IZmG0jjjH/wCpKdN02rdVYbpvmXK77/1r+h5F8MPjPP4S0TUdIg8P315eaxfzC3mgnETeY/CqhKtlgxGeuODz0r1Hw/4J+KXijTTa+KPEo0bTptyywWYR7xoyCNplA2g8jJA/Kua8BfC7Utf+E+reGtTsX03XLS7a/sL4SKyrPwQNyklSCMEHB5Br0n4P/Fi28baRFp+pzxWnim0Jgu7GVgkjunBdVPUcZOOnNbVpr3pUkt9evozGMWnyz0Oq8HeBdH8C2UkGlWxSSch7m6lbfNcv3eRj1JJJ7DJOAK36KK8xtyd2dCVtEFFFFSMKKKKACiiigAooooAKKKKACiiigDjviN8MbL4l2MdpqGoX9tbJg+RbShY2YHIZlI5IrW8IeH7nwxpMenz6pNqsUIVIJLhFEioBgBiuA31wKKKvnk48t9CeVXubdFFFQUZ99o0dzP8Aa4H+yX4AAuEH3wOiyDjeuex9TgjOazFubTSroTatp1vZ3K5xqUUOYmz334zGT6N3IAZjRRSemqOygvbTVKe34o6OiiimcYUUUUAFFFFAH//Z'
    captchaType = '1038'
    print(v.verify_code(captchaData=captchaData, captchaType=captchaType))
    # id = '20190214:000000000025751528630'
    # print(v.error_code(captchaId=id))
    print(v.check_lianzhong())


