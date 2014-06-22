import json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

CODE_LOGIN_SUCCESS = 1
CODE_LOGIN_NO_USER = CODE_LOGIN_SUCCESS + 1
CODE_LOGIN_ERROR_USER = CODE_LOGIN_NO_USER + 1

def login_account(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(json.dump({'code': CODE_LOGIN_SUCCESS}))
        else:
            return HttpResponse(json.dump({'code': CODE_LOGIN_ERROR_USER}))
    else:
        return HttpResponse(json.dump({'code': CODE_LOGIN_NO_USER}))
