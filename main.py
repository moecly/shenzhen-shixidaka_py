import requests
import json
import urllib.parse

# URL
add_kqjl_url = "https://hrsspub.sz.gov.cn/jgxxfw/jgfw/ydfw/student/addKqjl"
get_kqdd_url = "https://hrsspub.sz.gov.cn/jgxxfw/jgfw/ydfw/student/getKqdd"
get_verity_code_url = "https://hrsspub.sz.gov.cn/jgxxfw/jgfw/get/getVerifyCode?1694162488328"

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


def get_kqdd(session):
    params = {}
    response = session.get(get_kqdd_url, headers=headers)

    # 打印响应内容
    json_data = json.loads(response.text).get('result')
    params['cnz022'] = json_data.get('sxid')
    params['cnz058'] = json_data.get('xssxglid')
    params['cnz640'] = json_data.get('data')[0]['lat']
    params['cnz641'] = json_data.get('data')[0]['lng']
    params['cnz642'] = json_data.get('data')[0]['title']

    print("params = " + str(params))

    # 对字符串进行 URL 编码
    encoded_data = urllib.parse.quote(str(params))
    url = add_kqjl_url + "?xskqjlxxDTO=" + encoded_data
    return url


def add_kqjl(sid):
    session = requests.Session()
    verity_code_sesson = session.get(get_verity_code_url)

    # 创建一个会话对象，该对象将自动处理 Cookies
    print(session.cookies)

    # 设置初始 Cookies
    initial_cookies = {
        # 'JSESSIONID': 'FChybYYMhka28IdhgIGRi4Nn_wcaOuv5B6nn4ZeD7kqU9cwOMG5l!2109771826',
        # 'custom.session': 'e21f4b60-e7d7-4371-a8b9-32aaf8ac4ac7',
        'custom.session': 'e1218b44-ab6e-43e6-ac4f-c576952f55ff',
        '_sid': sid
    }

    # # 将初始 Cookies 添加到会话中
    session.cookies.update(initial_cookies)
    print(session.cookies)
    # session.cookies.update(verity_code_sesson)

    url = get_kqdd(session)
    print("url = " + url)

    # # 打卡
    # response = session.get(url, headers=headers)

    # # 打印打卡响应内容
    # print(response.text)


def main():
    add_kqjl("41855")


main()
