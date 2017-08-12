# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {}
    context['months'] = range(1,13)
    return render(request, 'CNA_Pay/index.html', context)

def login(request):
    if str(request.POST.get("username", "")) == '123' and str(request.POST.get("password", "")) == '123':
        return HttpResponse('200')
    else:
        return HttpResponse('404')

def pay(request):
    return HttpResponse('username='+str(request.POST.get("username", ""))+' password='+str(request.POST.get("password", ""))+' hours='+str(request.POST.get("hours", ""))+' month='+str(request.POST.get("month", "")))