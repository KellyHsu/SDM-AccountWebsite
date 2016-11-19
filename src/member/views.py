from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect


def login(request):

    # check whether already login
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    # get login form info
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')

    # check authenticate
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        # user exist and is active
        auth.login(request, user)
        return HttpResponseRedirect('/dashboard/')
    else:
        context = {}
        return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


def register(request):
    pass
