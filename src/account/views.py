from django.shortcuts import render
from django.http import HttpResponseRedirect


def dashboard(request):
    if not request.user.is_authenticated():
       return HttpResponseRedirect('/login/')
    return render(request, 'dashboard.html', {})

def filter(request):
  	return render(request, 'filter.html', {})
