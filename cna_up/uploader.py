# -*- coding: utf-8 -*-
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from bs4 import BeautifulSoup

s = requests.Session()

def checkfile(filename):
    if not os.path.isfile(filename):
        return False
    return True

def getCRSF(content):
    soup = BeautifulSoup(content,'html.parser')
    inputs = soup.find_all("input")
    for i in inputs:
        if i['name'] == "_csrf":
            return i["value"]
        
def login(username, password):
    url = 'https://www.dorm.ccu.edu.tw/admini/site/login'
    res = s.get(url)
    csrf = getCRSF(res.content)

    login_data = {
        "_csrf": csrf,
        "LoginForm[username]": username,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]":"1",
        "login-button:": ""
    }
    res = s.post(url, data=login_data)
    if u'工讀單' not in res.text:
         return '404'
    return '200'

def upload(filename, username, password):
    url = 'https://www.dorm.ccu.edu.tw/admini/salary/index'
    res = s.get(url)
    csrf = getCRSF(res.content)
    
    if not checkfile(filename):
        return '404'

    multipart_data = MultipartEncoder(
        fields=(
                ('_csrf', csrf), 
                ('Salary[pdfFile]', ''),
                ('Salary[pdfFile]', (filename, open(filename, 'rb'), 'application/pdf')),
            )
        )
    res = s.post(url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
    return res.status_code