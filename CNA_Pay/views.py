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
    return HttpResponse(requester.login(payload))

def pay(request):
    thisYear = dating.getChineseThisYear()

    payMonth = str(request.POST.get("month", ""))
    payHours = float(request.POST.get("hours", ""))

    holidays = dating.getThisMonthHolidaysFromFile(payMonth,'holidays.json')
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
    paidDays, leftHours = requester.addHours(thisYear,payMonth,payableDays,payHours)
    if leftHours > 0:
        return HttpResponse('Fail to add hours: ' + str(leftHours) + ' hours remained, please declare your salary manually.')

    #get seqenceNumber and total paid days
    sequence,days = requester.submitPayment(thisYear,payMonth,paidDays)
    if sequence is False:
        return HttpResponse('Fail to add hours.')

    #True if download pdf sucessfully
    if(requester.getPDF(sequence,days,payload['staff_cd'])):
        with open(str(request.POST.get("username", ""))+'.pdf','rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'filename='+str(request.POST.get("username", ""))+'.pdf'
            return response
    pdf.closed

 