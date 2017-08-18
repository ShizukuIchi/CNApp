# -*- coding: utf-8 -*-
import telnetlib
import re

def start(username,password):
    # log in to homepage
    tn = telnetlib.Telnet('bbs.cna.ccu.edu.tw')
    content = ''
    while u"您的帳號" not in content:
        content = tn.read_very_eager().decode('big5','ignore')
    tn.write(username+'\n')

    while u"您的密碼" not in content:
        content = tn.read_very_eager().decode('big5','ignore')
    tn.write(password+'\n')

    while u"主功能表" not in content:
        content = tn.read_very_eager().decode('big5','ignore')
        if u"踢掉其他" in content:
            tn.write('Y\n')
        if u"以上為輸入密碼錯" in content:
            tn.write('Y\n')   
        if u"密碼輸入錯誤" in content or u"錯誤的使用者代號" in content:
            return "Incorrect username or password"
            
    # mailbox
    tn.write('m\n\n')

    while u"郵件選單" not in content:
        content = tn.read_very_eager().decode('big5','ignore')
    titles = re.split('\n\r',content)

    tn.write('P')
    content = ""
    while len(content)<10: 
        content = tn.read_very_eager().decode('big5','ignore')
    titles2 = re.split('\n|;5H',content)

    allTitles = titles2[1:-1]+titles[3:]
    payment = []
    notice = []
    output = ''

    for title in allTitles: 
        text = re.search(u'(.)(月|月份)(網管)?(值班|會議)(信|時間)?',title)
        if text:
            for i in range(1,6):
                if text.group(i):
                    output += text.group(i)
            if ' r ' not in title[:15] and u'備 忘 錄' not in title: 
                notice.append(output)
            output = ''
        elif u'工讀金' in title: 
            payment.append(title)
    if len(payment) > 0: 
        pay = re.search(r'\d{4}/(\d{,2})',payment[-1])
        if pay:
            notice.append(pay.group(1)+u'月工讀金')
    return notice