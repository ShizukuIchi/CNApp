# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'cna_savemoney/index.html')

def search(request):
    username = str(request.POST.get("username", ""))
    password = str(request.POST.get("password", ""))
    # noticeList = searcher.start(username,password)
    return HttpResponse('fuck') 

def login(request):
    return HttpResponse('shit') 
    