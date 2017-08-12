# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import dating
import requester

def index(request):
    context = {}
    context['months'] = range(1,13)
    return render(request, 'CNA_Pay/index.html', context)

def login(request):
    payload = {}
    payload['staff_cd'] = str(request.POST.get("username", ""))
    payload['passwd'] = str(request.POST.get("password", ""))
    return requester.login(payload)

def pay(request):
    thisYear = dating.getChineseThisYear()

    payMonth = str(request.POST.get("month", ""))
    payHours = str(request.POST.get("hours", ""))

    holidays = dating.getThisMonthHolidaysFromFile(payMonth,'holidays.csv')
    payableDays = dating.getPayableDays(payMonth,holidays)
        
    payload = {}
    payload['staff_cd'] = str(request.POST.get("username", ""))
    payload['passwd'] = str(request.POST.get("password", ""))

    if requester.login(payload) != '200':
        return HttpResponse('incorrect username or password')

    for d in requester.getAlreadyPaidDays(thisYear,payMonth):
        if d in payableDays:
            payableDays.remove(d)

    #add hours to database get paid days list
    paidDays = requester.addHours(thisYear,payMonth,payableDays,payHours)

    #get seqenceNumber and total paid days
    sequence,days = requester.submitPayment(thisYear,payMonth,paidDays)

    #True if download pdf sucessfully
    if(requester.getPDF(sequence,days,payload['staff_cd'])):
        with open(str(request.POST.get("username", ""))+'.pdf','rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'filename='+str(request.POST.get("username", ""))+'.pdf'
            return response
    pdf.closed