from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response


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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/login/')
    else:
        # return render(request, 'register.html', context)
        form = UserCreationForm()
    return render(request, 'register.html', locals())
