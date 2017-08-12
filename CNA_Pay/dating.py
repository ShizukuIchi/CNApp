from calendar import monthrange
from datetime import datetime
import csv

def getChineseThisYear():
    return datetime.today().year-1911

def getThisMonthHolidaysFromFile(month,fileName):
    holidays = []
    thisMonthHolidays = []
    with open(fileName, 'r') as f:
        reader = csv.reader(f, delimiter='\n')
        holidaysDetailList = list(reader)
        for l in holidaysDetailList:
            holidays.append(l[0].split(',')[0])
    for date in holidays:
        ymd = date.split('/')
        if ymd[1] == month:
            thisMonthHolidays.append(ymd[2])
    return thisMonthHolidays

def getPayableDays(month,holidays):
    days = []
    for day in range(1,monthrange(datetime.today().year,int(month))[1]+1):
        if str(day) not in holidays:
            days.append(str(day) if (day>9) else '0'+str(day))
    
    #delete days exceeding today
    if datetime.today().month == int(month):
        for d in days[::-1]:
            if int(d) >= datetime.today().day: 
                days.remove(d)
            else:
                break
    return days
