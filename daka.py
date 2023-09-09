import requests
import json
import urllib.parse
import ddddocr
import base64

class daka:
    def __init__(self):
        self.session = requests.Session()

    def get_kqdd(self):
        params = {}
        response = self.session.get(self.get_kqdd_url)

        # 打印响应内容
        json_data = json.loads(response.text).get('result')
        params['cnz022'] = json_data.get('sxid')
        params['cnz058'] = json_data.get('xssxglid')
        params['cnz640'] = json_data.get('data')[0]['lat']
        params['cnz641'] = json_data.get('data')[0]['lng']
        params['cnz642'] = json_data.get('data')[0]['title']

        # 对字符串进行 URL 编码
        encoded_data = urllib.parse.quote(str(params))
        url = self.add_kqjl_url + "?xskqjlxxDTO=" + encoded_data
        return url


    def add_kqjl(self, sid):
        # 设置初始 Cookies
        initial_cookies = {
            # 'JSESSIONID': 'FChybYYMhka28IdhgIGRi4Nn_wcaOuv5B6nn4ZeD7kqU9cwOMG5l!2109771826',
            # 'custom.session': 'e21f4b60-e7d7-4371-a8b9-32aaf8ac4ac7',
            '_sid': sid
        }

        # 将初始 Cookies 添加到会话中
        self.session.cookies.update(initial_cookies)
        url = self.get_kqdd()

        # 打卡
        response = self.session.get(url, headers=self.headers)

        # 打印打卡响应内容
        print('-------------------------------------------')
        print('sid: ' + sid)
        resp_json = json.loads(response.text)
        if resp_json['status'] == 200:
            print(' 打卡成功')
        else:
            print(resp_json['message'])

        print('-------------------------------------------')
    
    def login(self, username, password):
        self.session.headers.update(self.headers)
        response = self.session.get(self.get_verity_code_url)
        ocr = ddddocr.DdddOcr()
        verity_code = ocr.classification(response.content)
        print('-------------------------------------------')
        print("verity code: " + verity_code)
        print('-------------------------------------------')

        response = self.session.get(self.get_hash_url)
        hash = json.loads(response.text)['result']['hash']

        name = username + hash
        pawd = password + hash
        name = base64.b64encode(name.encode('utf-8'))
        pawd = base64.b64encode(pawd.encode('utf-8'))
        name = name.decode('utf-8')
        pawd = pawd.decode('utf-8')

        params = {
            'loginInfo': {
                'loginName': name,
                'password': pawd,
                'captcha': verity_code
            }
        }

        params = {
            'loginInfo': '{' + '"loginName":' + '"' + str(params['loginInfo']['loginName']) + '"' + ',' + '"password":' + '"' + str(params['loginInfo']['password']) + '"' + ',' + '"captcha":' + '"' + str(params['loginInfo']['captcha']) + '"' + '}'
        }

        response = self.session.post(url=self.login_url, params=params)
        resp_json = json.loads(response.text)
        print('-------------------------------------------')
        if resp_json['result']['status'] != 3:
            print('login err')
            print('err msg: ')
            print(resp_json)
            print('-------------------------------------------')
            return False

        print('login success')
        print('-------------------------------------------')
        return True

    # URL
    add_kqjl_url = 'https://hrsspub.sz.gov.cn/jgxxfw/jgfw/ydfw/student/addKqjl'
    get_kqdd_url = 'https://hrsspub.sz.gov.cn/jgxxfw/jgfw/ydfw/student/getKqdd'
    get_verity_code_url = 'https://hrsspub.sz.gov.cn/jgxxfw/jgfw/get/getVerifyCode?1694162488328'
    get_hash_url = 'https://hrsspub.sz.gov.cn/jgxxfw/jgfw/ggww/hash?loginInfo%5Bhash%5D=lkjh12'
    login_url = 'https://hrsspub.sz.gov.cn/jgxxfw/jgfw/suumLogin'

    # 设置请求头，包括Cookie等
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6",
        "Connection": "keep-alive",
        "Host": "hrsspub.sz.gov.cn",
        "Referer": "https://hrsspub.sz.gov.cn/jgxxfw/yidong/student/kq/xskq.html",
        "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

def main():
    dk = daka()
    while True:
        ret = dk.login('', '')
        if ret == True:
            break
    dk.add_kqjl('')

main()