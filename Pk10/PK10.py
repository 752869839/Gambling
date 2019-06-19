# coding=utf-8
import json
import threading
import time
from Login import Login
import requests


class PK10:

    def __init__(self, cookie, host):
        self.cookie = cookie
        self.host = host

    def pk10(self):
        """
        pk10数据接口，根据host变化，就是登录的url
        :return:
        """
        headers = {
            "Host": self.host,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": self.cookie,
        }
        url = "https://" + self.host + "/USR/API/Result/getNewResultNumber.jsp?txtCBID=CBBJPK10&txtTime="
        try:
            res = requests.get(url=url, headers=headers, verify=False)
            # print(res)

            # 获取请求到的json数据，取出对应的数据
            res_data = res.json()
            issue = res_data['issue']['displayofficialissue']
            data_list = [
                res_data['result']['ball1'],
                res_data['result']['ball2'],
                res_data['result']['ball3'],
                res_data['result']['ball4'],
                res_data['result']['ball5'],
                res_data['result']['ball6'],
                res_data['result']['ball7'],
                res_data['result']['ball8'],
                res_data['result']['ball9'],
                res_data['result']['ball10'],
            ]
            result = {'issue': issue, 'data': data_list}
            print(result)

            # 将获取到的数据存储
            with open('pk10.txt', 'a', encoding='utf-8') as f:
                f.write(json.dumps(result) + '\n')
        except Exception as e:

            # 如果请求出现异常，重新更换用户登录获取cookie
            # 此处用txt文档实现的循环队列， 确保每个用户轮流使用
            with open('user.txt', 'r') as f:
                users = f.readlines()
            user_data = users[0].replace('\n', '')
            user_end = users[1:] + [users[0]]
            with open('user.txt', 'w') as f:
                f.writelines(user_end)
            user = user_data.split('@')[0]
            pwd = user_data.split('@')[1]
            self.cookie, self.host= Login(user, pwd).login()
            headers = {
                "Host": self.host,
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cookie": self.cookie,
            }
            res = requests.get(url=url, headers=headers, verify=False)
            print(res)
            res_data = res.json()
            issue = res_data['issue']['displayofficialissue']
            data_list = [
                res_data['result']['ball1'],
                res_data['result']['ball2'],
                res_data['result']['ball3'],
                res_data['result']['ball4'],
                res_data['result']['ball5'],
                res_data['result']['ball6'],
                res_data['result']['ball7'],
                res_data['result']['ball8'],
                res_data['result']['ball9'],
                res_data['result']['ball10'],
            ]
            result = {'issue': issue, 'data': data_list}
            print(result)
            with open('pk10.txt', 'a', encoding='utf-8') as f:
                f.write(json.dumps(result) + '\n')

    def bai_jia_le(self):
        """
        百家乐数据接口
        :return:
        """
        url = "https://" + self.host + "/USR/API/GameState/CBCCBCR/getCBCCBCRGameStateData.jsp?"
        for room in range(1, 49):
            headers =  {
                "Host": self.host,
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cookie": self.cookie,
            }
            # time.sleep(3)
            try:
                # 伪造参数，获取每个房间的数据
                params = {
                    "txtCBID": "CBCCBCR",
                    "txtBCRType": "NC",
                    "txtRoom": room,
                    "txtGetGameStateData": "true",
                    "txtTime": '',
                }
                res = requests.get(url=url, params=params, headers=headers, verify=False)
                print(res)
                # print(res.text)

                # 获取返回的json数据，解析
                res_data = res.json()
                issue = res_data['issue']
                start_times = res_data['starttimes']
                close_time = res_data['closetime']
                data_list_en = {
                    '1': res_data['lastresult1'],
                    '2': res_data['lastresult2'],
                    '3': res_data['lastresult3'],
                    '4': res_data['lastresult4'],
                    '5': res_data['lastresult5'],
                    '6': res_data['lastresult6'],
                }

                # 根据对应的数据替换成常见牌面
                data_list_cn = {
                    '1': res_data['lastresult1'].replace(
                        'h', '红桃').replace('d', '方块').replace('c', '梅花').replace('s', '黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '2': res_data['lastresult2'].replace(
                        'h', '红桃').replace('d', '方块').replace('c', '梅花').replace('s', '黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '3': res_data['lastresult3'].replace(
                        'h', '红桃').replace('d', '方块').replace('c', '梅花').replace('s', '黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '4': res_data['lastresult4'].replace(
                        'h', '红桃').replace('d', '方块').replace('c', '梅花').replace('s', '黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '5': res_data['lastresult5'].replace(
                        'h', '红桃').replace('d', '方块').replace('c', '梅花').replace('s', '黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '6': res_data['lastresult6'].replace(
                        'h', '红桃').replace('d', '方块').replace('c', '梅花').replace('s', '黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                }
                result = {
                    'room': room,
                    'issue': issue,
                    'start_times': start_times,
                    'close_time': close_time,
                    'data_en': data_list_en,
                    'data_cn': data_list_cn,
                }
                print(result)

                # 将获取的数据保存
                with open('baijile.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(result, ensure_ascii=False) + '\n')
            except Exception as e:
                print(e)

                # 如果请求出现异常，重新更换用户登录获取cookie
                # 此处用txt文档实现的循环队列， 确保每个用户轮流使用
                with open('user.txt', 'r') as f:
                    users = f.readlines()
                user_data = users[0].replace('\n', '')
                user_end = users[1:] + [users[0]]
                with open('user.txt', 'w') as f:
                    f.writelines(user_end)
                user = user_data.split('@')[0]
                pwd = user_data.split('@')[1]
                self.cookie = Login(user, pwd).login()
                headers =  {
                    "Host": self.host,
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": UA,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": self.cookie,
                }
                params = {
                    "txtCBID": "CBCCBCR",
                    "txtBCRType": "NC",
                    "txtRoom": room,
                    "txtGetGameStateData": "true",
                    "txtTime": '',
                }
                res = requests.get(url=url, params=params, headers=headers, verify=False)
                print(res)
                # print(res.text)
                res_data = res.json()
                issue = res_data['issue']
                start_times = res_data['starttimes']
                close_time = res_data['closetime']
                data_list_en = {
                    '1': res_data['lastresult1'],
                    '2': res_data['lastresult2'],
                    '3': res_data['lastresult3'],
                    '4': res_data['lastresult4'],
                    '5': res_data['lastresult5'],
                    '6': res_data['lastresult6'],
                }
                data_list_cn = {
                    '1': res_data['lastresult1'].replace(
                        'h', r'红桃').replace('d', r'方块').replace('c', r'梅花').replace('s', r'黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '2': res_data['lastresult2'].replace(
                        'h', r'红桃').replace('d', r'方块').replace('c', r'梅花').replace('s', r'黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '3': res_data['lastresult3'].replace(
                        'h', r'红桃').replace('d', r'方块').replace('c', r'梅花').replace('s', r'黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '4': res_data['lastresult4'].replace(
                        'h', r'红桃').replace('d', r'方块').replace('c', r'梅花').replace('s', r'黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '5': res_data['lastresult5'].replace(
                        'h', r'红桃').replace('d', r'方块').replace('c', r'梅花').replace('s', r'黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                    '6': res_data['lastresult6'].replace(
                        'h', r'红桃').replace('d', r'方块').replace('c', r'梅花').replace('s', r'黑桃').replace(
                        '11', 'J').replace('12', 'Q').replace('13', 'K'),
                }
                result = {
                    'room': room,
                    'issue': issue,
                    'start_times': start_times,
                    'close_time': close_time,
                    'data_en': data_list_en,
                    'data_cn': data_list_cn,
                }
                print(result)
                with open('baijile.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(result, ensure_ascii=False) + '\n')

    def thread_pk10(self):
        # 使用线程等待，定时执行任务， 等待时间PK10_WAIT_TIME
        self.pk10()
        threading.Timer(PK10_WAIT_TIME, self.thread_pk10).start()

    def thread_bjl(self):
        # 使用线程等待，定时执行任务， 等待时间BJL_WAIT_TIME
        self.bai_jia_le()
        threading.Timer(BJL_WAIT_TIME, self.thread_bjl).start()

    def run(self):
        # 开启多线程，执行程序，将pk10 和百家乐同时进行
        thread_list = [
            threading.Thread(target=self.thread_pk10),
            threading.Thread(target=self.thread_bjl)
        ]
        for i in thread_list:
            i.start()

if __name__ == '__main__':
    # 从配置未见取出等待时间数据，以及User—Agent
    with open('LZsetting.json', encoding='utf-8') as f:
        res = json.loads(f.read())
    PK10_WAIT_TIME = res['PK10_TIME_WAIT']
    BJL_WAIT_TIME = res['BAIJIALE_TIME_WAIT']
    UA = res['UA']

    # 取出用户，替换换行符，通过关键字符@分割获取账号和密码
    with open('user.txt', 'r') as f:
        users = f.readlines()
    user_data = users[0].replace('\n', '')
    user_end = users[1:] + [users[0]]
    with open('user.txt', 'w') as f:
        f.writelines(user_end)
    user = user_data.split('@')[0]
    pwd = user_data.split('@')[1]
    # print(user, pwd)

    # 初次获取cookie和host
    cookie, host = Login(user, pwd).login()

    # 实例化类对象，并传入参数
    pk = PK10(cookie, host)

    # 开始执行程序
    pk.run()