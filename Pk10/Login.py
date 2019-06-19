# coding=utf-8
import base64
import json
import re
import time

from PIL import Image, ImageGrab
from lianzhong_code import VerifyCode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class Login:

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.lianzhong = VerifyCode()

    def login(self):
        # 登录url，详细看说明文档1
        url = 'https://qkk8.ccbenz.com/PortalUSR/index.jsp'
        host = re.findall(r'http[s]*:\/\/(.*?)\/P', url)[0]

        # with open('LZsetting.json', encoding='utf-8') as f:
        #     res = json.loads(f.read())
        # UA = res['UA']
        chrome_option = webdriver.ChromeOptions()
        # chrome_option.add_argument('user-agent=' + UA)
        # chrome_option.add_argument('--headless')
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_option.add_experimental_option("prefs", prefs)
        # self.driver = webdriver.Chrome(options=chrome_option)
        chrome_driver = './chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=chrome_driver,options=chrome_option)
        self.driver.get(url)
        while True:
            if WebDriverWait(self.driver, 30).until(
                    lambda x: x.find_element_by_xpath('//a[@class="loginBtn"]')):
                while True:
                    print(self.user, self.pwd)
                    self.driver.find_element_by_xpath('//input[@name="txtAccount"]').send_keys(self.user)
                    self.driver.find_element_by_xpath('//input[@name="txtPassword"]').send_keys(self.pwd)
                    self.driver.save_screenshot('screen.png')
                    img = self.driver.find_element_by_xpath('//img[@class="formUx-img"]')
                    s = img.location
                    print(s)

                    # 验证码坐标，提供截图给打码平台
                    captcha = self.screen_code((s['x'], s['y'], s['x'] + 57, s['y'] + 25))
                    # captcha = self.screen_code((800, 380, 800 + 57, 380 + 25))
                    self.driver.find_element_by_xpath('//input[@name="txtCheckCode"]').send_keys(captcha)
                    self.driver.find_element_by_xpath('//a[@class="loginBtn"]').click()
                    # self.driver.find_element_by_xpath('//input[@name="butLogin"]').click()
                    time.sleep(0.5)
                    try:
                        error_text = self.driver.find_element_by_xpath('//div[@id="sErrorMsg"]').text
                    except:
                        error_text = ''
                    if '验证码' in error_text or '失败' in error_text:
                        continue
                    else:
                        break
                try:
                    self.driver.switch_to_alert().accept()
                    break
                except:
                    continue
        cookies = self.driver.get_cookies()
        self.driver.close()
        cookie = ';'.join('{0}={1}'.format(temp['name'], temp['value']) for temp in cookies)
        print(cookie)
        return cookie, host

    def screen_code(self, x):
        print(x)
        img = Image.open('screen.png')
        # captcha = img.crop((503, 360, 560, 385))      # headless
        captcha = img.crop(x)
        captcha.save('captcha.png')
        with open('captcha.png', 'rb') as f:
            base64_data = base64.b64encode(f.read())
            captchaData = base64_data.decode()
        captchaType = '1038'
        try:
            res = self.lianzhong.verify_code(captchaData=captchaData, captchaType=captchaType)
        except:
            res = self.lianzhong.verify_code(captchaData=captchaData, captchaType=captchaType)
        data = json.loads(res)['data']
        print(data)
        return data

if __name__ == '__main__':
    USER = 'u-da41'
    PWD = 'dd123123'
    l = Login(USER, PWD)
    cookie, host = l.login()
    print(cookie, host)
    # l.screen_code()

    # JSESSIONID=7CA4F70AA3A2D841ED7CE78C412B5A10;sto-id-47873-PortalUSR2=CBABBDKMNOAH