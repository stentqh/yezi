#!/usr/bin/env python3
# -*- utf-8 -*-
import time
import json
import random

import requests

class XingShi(object):
    """"幸识爬虫"""
    def __init__(self):
        self.login_url = "https://api.cijian.link/public/_login"
        self.sms_login_url = "https://api.cijian.link/public/_login-by-msg?phone={phone}&vsCode={vCode}"
        self.like_url = "https://api.cijian.link/users/like"
        self.init_friend_url = "https://api.cijian.link/friends/init"
        self.session = requests.Session()
        self.session.headers = {
            'platform': '1',
            'version': '1.4.7.1',
            'model': 'Redmi_Redmi Note 8 Pro',
            'deviceid': '',
            'network': '2',
            'channel': 'UMENG_CHANNEL',
            'androidid': '843ccf8a5c210292',
            'macaddress': '',
            'user-agent': 'okhttp/3.14.7',
        }

    def is_json(self, s):
        """判断字符串是否可以转换为字典(json)"""
        try:
            json.loads(s)
            return True
        except ValueError as e:
            print(f"ValueError: {e}")
            print("Failed to convert json. String is...")
            print(s)
            return False

    def parseData(self, text):
        data = {
            "uid": text["data"][0]["id"],
            "nickname": text["data"][0]["nickName"],
            "content": [i.get("content") for i in text["data"][0]["userCards"] if not (not i.get("content")) and i.get("content") != "null"]
        }
        if data["content"]:
            data["content"] = data["content"][0]
        print("="*50)
        print(f"uid:{data['uid']}\n昵称:{data['nickname']}\n{data['content']}")
        print("="*50)
        return data["uid"]

    def send_msg(self, phone):
        """发送验证码短信"""
        self.session.get(f"https://api.cijian.link/public/_send-msg?phone={phone}")

    def login(self, phone, password="", code="", sex=0, birthData=0, lt=1):
        """登陆函数"""
        if lt == 1:
            req = self.session.get(self.sms_login_url.format(phone=phone, vCode=code))
        elif lt == 2:
            data = {
                "birthData": birthData,
                "password": password,
                "phone": phone,
                "sex": sex
            }
            self.session.headers["content-type"] = "application/json; charset=UTF-8"
            req = self.session.post(self.login_url, data=data)
            self.session.headers.pop("content-type")
        if self.is_json(req.text):
            data = req.json()
            if data.get("data"):
                if data["data"].get("userInfo"):
                    userInfo = data["data"]["userInfo"]
                    uid = userInfo.get("id")
                    nickName = userInfo.get("nickName")
                    sex = "男" if userInfo.get("sex") == 0 else "女"
                    print(f"""{'='*10} Login Sucess {'='*10}
UID: {uid}
昵称: {nickName}
性别: {sex}
{'='*34}""")
                    self.session.headers["x-token"] = req.json().get("data").get("token")
                else:
                    print("userInfo not found.")
                    print(f"[Info] {data['data']}")
            else:
                print("Login data not found.")
                print(f"[Info] {data}")
        else:
            return
    def like(self):
        n = 0
        while n < 1000:
            #break
            req = self.session.get(self.init_friend_url)
            uid = self.parseData(req.json())
            #if uid in uids: continue
            #uids.append(uid)
            data = {"uid":uid, "count":random.randint(3,9)}
            self.session.post(self.like_url, data=data)
            #time.sleep(random.randint(1,8))
            n += 1
       
if __name__ == "__main__":
    xingshi = XingShi()
    print("Login type:\n1.SMS login\n2.Password login[TODO]")
    login_type = input(">>> ")
    phone = input("[Phone]: ")
    if login_type == "1":
        xingshi.send_msg(phone)
        code = input("[Code] ")
        xingshi.login(phone, code=code)
    elif login_type == "2":
        password = input("[Password] ")
        xingshi.login(phone, password=password, lt=2)
    else:
        print("[Error] input error. Please input 1 or 2")
        exit()
    xingshi.like()
