from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Member
from account.models import IncomeAndExpense, Payment, Classification, Budget, MonthBudget
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            member = Member.objects.create(user=user, create_date=datetime.now())
            MonthBudget.objects.create(budget=0, reminder=0, member=member, is_reminded=False)
            
            c1, created1 = Classification.objects.get_or_create(classification_type='food')
            c2, created2 = Classification.objects.get_or_create(classification_type='clothing')
            c3, created3 = Classification.objects.get_or_create(classification_type='housing')
            c4, created4 = Classification.objects.get_or_create(classification_type='transportation')
            c5, created5 = Classification.objects.get_or_create(classification_type='education')
            c6, created6 = Classification.objects.get_or_create(classification_type='entertainment')
            c7, created7 = Classification.objects.get_or_create(classification_type='others')
            c8, created8 = Classification.objects.get_or_create(classification_type='revenue')
            c9, created9 = Classification.objects.get_or_create(classification_type='invest_revenue')
            c10, created10 = Classification.objects.get_or_create(classification_type='other_revenue')
            Budget.objects.create(budget=0, reminder=0, classification=c1, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c2, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c3, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c4, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c5, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c6, member=member, is_reminded=False)
            Budget.objects.create(budget=0, reminder=0, classification=c7, member=member, is_reminded=False)

            p1, createdp1 = Payment.objects.get_or_create(payment_type='credit_card')
            p2, createdp2 = Payment.objects.get_or_create(payment_type='cash')
            p3, createdp3 = Payment.objects.get_or_create(payment_type='other')

            i1, createdi1 = IncomeAndExpense.objects.get_or_create(income_type='income')
            i2, createdi2 = IncomeAndExpense.objects.get_or_create(income_type='expense')

            return HttpResponseRedirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', locals())
