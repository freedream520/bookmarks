import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from accounts.forms import *
from django.shortcuts import render, render_to_response, get_object_or_404
from bookmark_base.models import Freindship

CODE_LOGIN_SUCCESS = 1
CODE_LOGIN_NO_USER = CODE_LOGIN_SUCCESS + 1
CODE_LOGIN_ERROR_USER = CODE_LOGIN_NO_USER + 1
CODE_REGISTER_SUCCESS = CODE_LOGIN_ERROR_USER + 1
CODE_REGISTER_ERROR = CODE_REGISTER_SUCCESS + 1

def login(request):
    if request.user_agent.is_mobile:
        if request.method == 'GET':
            context = RequestContext(request, {
                'form': AuthenticationForm(request)
            })
            return render_to_response('registration/mobile_login.html', context)
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                response = HttpResponse(json.dumps({'code': CODE_LOGIN_SUCCESS}))
                response.set_cookie("user", user.pk)
                return response
            else:
                return HttpResponse(json.dumps({'code': CODE_LOGIN_NO_USER}))
    else:
        return HttpResponseRedirect('/accounts/pc_login')

def register_success(request):
    variables = RequestContext(request, {
        'stub': 'stub'
    })
    return render_to_response('reg_success.html', variables)


def add_user(request):
    if request.method == 'POST':
        form = RegisteForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/accounts/register_success')
    else:
        form = RegisteForm()
        variables = RequestContext(request, {
            'form': form
        })
    return render_to_response('registration/registe.html', variables)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.post['email']
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        return HttpResponse(json.dumps({'code': CODE_REGISTER_SUCCESS, 'msg': 'register success'}))
    else:
        form = RegisteForm()
        variables = RequestContext(request, {
            'form': form
        })
    return render_to_response('registration/registe.html', variables)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-id')
    if request.user.is_authenticated():
        is_friend = Freindship.objects.filter(
            fromuser=request.user,
            touser=user)
    else:
        is_friend = False
    variables = RequestContext(request, {
        'bookmarks': bookmarks,
        'username': username,
        'show_tags': True,
        'show_user': False,
        'show_edit': username == request.user.username,
        'is_friend': is_friend,
        })
    return render_to_response('user_page.html', variables)