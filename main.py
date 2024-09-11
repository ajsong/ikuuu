# -*- coding: utf-8 -*-
import json
import requests
import os
from urllib import parse

#账户
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
DOMAIN = os.environ["DOMAIN"]
TG_TOKEN = os.environ["TG_TOKEN"]
TG_CHAT_ID = os.environ["TG_CHAT_ID"]

class SSPANEL:
    name = "SSPANEL"

    def __init__(self, check_item):
        self.check_item = check_item

    def url_encode(self, string):
        return parse.quote(string, safe='', encoding=None, errors=None)

    def sign(self, email, password, url):
        email = email.replace("@", "%40")
        try:
            session = requests.session()
            session.get(url=url, verify=False)
            login_url = url + "/auth/login"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
            post_data = "email=" + email + "&passwd=" + password + "&code="
            post_data = post_data.encode()
            session.post(login_url, post_data, headers=headers, verify=False)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Referer": url + "/user",
            }
            response = session.post(url + "/user/checkin", headers=headers, verify=False)
            msg = response.json().get("msg")
        except Exception as e:
            msg = "签到失败"
        return msg

    def main(self):
        email = self.check_item.get("email")
        password = self.check_item.get("password")
        url = self.check_item.get("url")
        token = self.check_item.get("token")
        chat = self.check_item.get("chat")
        sign_msg = self.sign(email=email, password=password, url=url)
        msg = [
            {"name": "帐号信息", "value": email},
            {"name": "签到信息", "value": f"{sign_msg}"},
        ]
        msg = "iKuuu自动签到\n" + "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        print(msg)

        try:
            tg_url = "https://api.telegram.org/bot" + token + "/sendmessage?chat_id=" + chat + "&parse_mode=HTML&text=" + self.url_encode(msg)
            session = requests.session()
            session.get(url=tg_url, verify=False)
        except Exception as e:
            print(e)
        
        return msg



if __name__ == "__main__":
    _check_item = {'email': EMAIL, 'password': PASSWORD, 'url': DOMAIN, 'token': TG_TOKEN, 'chat': TG_CHAT_ID}
    SSPANEL(check_item=_check_item).main()
