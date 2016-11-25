from django.shortcuts import render
from django.http import HttpResponseRedirect


def dashboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    return render(request, 'dashboard.html', {})

def setting(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	return render(request, 'setting.html', {})

def filter(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	return render(request, 'filter.html', {})
