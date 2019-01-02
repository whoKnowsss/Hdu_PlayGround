#coding=utf-8
#-*- coding: UTF-8 -*- 
import requests
import os
import time
import re
class ConnectWeb(object):
    def __init__(self):
        self.username = "#################"
        self.password = "#################"
        self.url = "http://2.2.2.2/ac_portal/login.php"

    def connect_baidu(self):   #检测目前是否联网
        try:
            requests.get("http://www.baidu.com", timeout=2)
            return 1
        except:
            return 0

    def login(self):  #模拟上网验证
        try:
            login_data = {
                'opr':'pwdLogin',
                'userName':self.username,
                'pwd':self.password,
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
            content = session.post(self.url, headers = headers_base, data = login_data)
            content.encoding='utf-8'
            print content.text
        except Exception as e:
            print(str(e))

    def disconnect(self):   # 断开wifi
        os.system("netsh wlan disconnect")

    def wifis_nearby(self): # 查询附近wifi
        os.system('netsh interface set interface name="WLAN" admin=disable')
        p = os.popen("netsh wlan show all")
        content = p.read().decode("GB2312", "ignore")
        temp = re.findall(u"(SSID.*\n.*Network type.*\n.*\u8eab\u4efd\u9a8c\u8bc1.*\n.*\u52a0\u5bc6.*\n.*BSSID.*\n)",
                       content)
        result = []
        for i in temp:
            name = re.findall(u"SSID.*:(.*)\n", i)[0].replace(" ", "")
            result.append(name)
        return result

    def connect_wifi(self, name=None): #连接wifi
        os.system("netsh wlan connect name=%s" % name)

    def checking(self): # 一直检测是否有断网，如果断网则重新连接
        while 1:
            try:
                if not self.connect_baidu():
                    self.login()
            except:
                pass
            time.sleep(10)


if __name__ == "__main__":
    test = ConnectWeb()
    print test.wifis_nearby()
    # test.checking()