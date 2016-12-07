from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Member
from account.models import Classification, Budget, MonthBudget
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            member = Member.objects.create(user=user, create_date=datetime.now())
            MonthBudget.objects.create(budget=0, reminder=0, member=member, is_reminded=False)
            
            c1 = Classification.objects.filter(classification_type='food').first()
            c2 = Classification.objects.filter(classification_type='clothing').first()
            c3 = Classification.objects.filter(classification_type='housing').first()
            c4 = Classification.objects.filter(classification_type='transportation').first()
            c5 = Classification.objects.filter(classification_type='education').first()
            c6 = Classification.objects.filter(classification_type='entertainment').first()
            c7 = Classification.objects.filter(classification_type='others').first()
            Budget.objects.create(budget=0, reminder=0, classification=c1, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c2, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c3, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c4, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c5, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c6, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c7, member=member, is_reminded=False)

            return HttpResponseRedirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', locals())
