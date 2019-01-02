# -- coding: utf-8 --
import requests
# import re

## input your pwd and account
uaserName='XXXXXXXXXXXXXXXXXXXXXXX'
pwd='XXXXXXXXXXXXXXXXXXXXX'

url='http://2.2.2.2/ac_portal/login.php'
# print r.text
login_data = {
            'opr':'pwdLogin',
            'userName':uaserName,
            'pwd':pwd,
            'rememberPwd':0
    }
headers_base = {
        'Accept': '*/*','Accept-Encoding': 'gzip, deflate','Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Host': '2.2.2.2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36', 
        'Referer': 'http://2.2.2.2/ac_portal/default/pc.html?tabs=pwd'
}

session = requests.session()

content = session.post(url, headers = headers_base, data = login_data)
content.encoding='utf-8'

print content.text