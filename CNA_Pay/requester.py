# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from random import randint

s = requests.Session()

def login(payload={}):
    res = s.post('http://mis.cc.ccu.edu.tw/parttime/control.php',data = payload)
    if u'密碼錯誤' not in res.content.decode('utf8','ignore'):
        return '200'
    return '404'

def getAlreadyPaidDays(year,month):
    days = []
    s.get('http://mis.cc.ccu.edu.tw/parttime/sp_sel.php')
    payload = {
        'unit_cd2':'Z999',
        'sy':str(year),
        'sm':'01',
        'sd':'01',
        'ey':str(year),
        'em':'12',
        'ed':'31',
        'con_state':'9',
        'hd':'2',
        'sid':'',
        'all_go':u'送出查詢'
    }
    res = s.post('http://mis.cc.ccu.edu.tw/parttime/sp_row.php',data=payload)
    soup = BeautifulSoup(res.content,'html.parser')
    if len(month) == 1:
        month = '0'+month
    reString = '(?<=' + month + u'月)\d+(?=日)'
    return re.findall(reString,soup.text)

def addHours(year,month,days,hours):
    s.get('http://mis.cc.ccu.edu.tw/parttime/control2.php')
    
    if len(month) == 1:
        month = '0'+month
    payload={
    'yy':year,
    'mm':month,
    'dd':'16',
    'type':u'P012電子計算機中心資源管理組',
    'shour':'19',
    'smin':'00',
    'ehour':'22',
    'emin':'00',
    'workin':u'宿網諮詢',
    'sid':''
    }
    paidDays=[]
    while hours > 0:
        d = days[randint(0, len(days)-1)]
        payload['dd'] = d
        paidDays.append(d)
        days.remove(d)
        if hours >= 3:
            s.post('http://mis.cc.ccu.edu.tw/parttime/next.php',data=payload)
            hours -= 3
        elif hours >=2:
            payload['ehour'] = '21'
            if hours == 2.5:
                payload['emin'] = '30'
                hours -= 0.5
            s.post('http://mis.cc.ccu.edu.tw/parttime/next.php',data=payload)
            hours -=2
        elif hours >=1:
            payload['ehour'] = '20'
            if hours == 1.5:
                payload['emin'] = '30'
                hours -= 0.5
            s.post('http://mis.cc.ccu.edu.tw/parttime/next.php',data=payload)
            hours -=1
        elif hours >0:
            payload['ehour'] = '19'
            payload['emin'] = '30'
            s.post('http://mis.cc.ccu.edu.tw/parttime/next.php',data=payload)
            hours-=0.5
    res = s.get('http://mis.cc.ccu.edu.tw/parttime/todb.php')
    return paidDays

def submitPayment(year,month,days):
    res = s.get('http://mis.cc.ccu.edu.tw/parttime/print_sel.php')
    payload = {
    'unit_cd1':'P012',
    'sy':year,
    'sm':month,
    'sd':'01',
    'ey':year,
    'em':'12',
    'ed':'31',
    'sid':'',
    'go':'%E4%BE%9D%E6%A2%9D%E4%BB%B6%E9%81%B8%E5%87%BA%E8%B3%87%E6%96%99'
    }
    res = s.post('http://mis.cc.ccu.edu.tw/parttime/print_row.php',data=payload)

    
    #submit payment
    payload={
        'chka':'off',
        'hour_money':'133',
        'sutype':'1',
        'iswork':'0',
        'emp_type':'1',
        'agreethis':'1',
        'sid':'sqp5oi70uriohbn99tbjbhehf7',
        'go_check':'%E7%A2%BA%E5%AE%9A%E9%80%81%E5%87%BA%E4%B8%A6%E5%88%97%E5%8D%B0'
    }
    
    soup = BeautifulSoup(res.content,'html.parser')
    checkbox = 0
    totalCB = 0
    if len(month) == 1:
        month = '0'+month
    reString = '(?<=' + month + u'月)\d+(?=日)'
    for tr in soup.find_all('tr')[1:]:
        for d in re.findall(reString,tr.text):
            if d in days:
                totalCB+=1
                payload['cb_'+str(checkbox)]='1'
        checkbox+=1
        
    res = s.post('http://mis.cc.ccu.edu.tw/parttime/print_check.php',data=payload)
    seq = str(re.search(r'\d{10}',res.content).group(0))
    return seq,totalCB

def getPDF(seq,totalCB,name):
    payload = {
    'sid':'sqp5oi70uriohbn99tbjbhehf7',
    'bsn':seq,
    'ctrow':str(totalCB),
    'emp_type':'1',
    'go_check':'%E5%88%97%E5%8D%B0%E7%B0%BD%E5%88%B0%E9%80%80%E8%A1%A8'
    }
    res = s.post('http://mis.cc.ccu.edu.tw/parttime/printpdf1.php',data=payload,stream=True)
    if res.status_code == 200:
        with open(name+'.pdf','wb') as f:
            for chunk in res:
                f.write(chunk)
        return True
    else:
        return False