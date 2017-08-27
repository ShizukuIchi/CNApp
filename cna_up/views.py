# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import uploader

def index(request):
    return render(request, 'cna_up/index.html')

def login(request):
    username = str(request.POST.get("username", ""))
    password = str(request.POST.get("password", ""))
    return HttpResponse(uploader.login(username, password))

def upload(request):
    filename = str(request.POST.get("filename", ""))
    username = str(request.POST.get("username", ""))
    password = str(request.POST.get("password", ""))
    return HttpResponse(uploader.upload(filename+'.pdf', username, password))
