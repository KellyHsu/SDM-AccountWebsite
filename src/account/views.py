#coding=utf8 
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from account.models import Receipt, SubClassification, Payment, IncomeAndExpense
from member.models import Member
from datetime import datetime, date


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


def create_receipt(request):

    if request.method == 'POST':
        print(request.POST)
        subclass = SubClassification.objects.filter(name=request.POST["category"].split("-", 1)[-1]).first()
        payment = Payment.objects.filter(payment_type=request.POST["payment"]).first()
        incomeandexpense = IncomeAndExpense.objects.filter(income_type=request.POST["record_type"]).first()
        member = Member.objects.filter(user__username=request.user).first()

        new_receipt = Receipt.objects.create(money=request.POST["amount"], remark=request.POST["memo"],
                                             date=datetime.strptime(request.POST["date"], "%Y/%m/%d"),
                                             subclassification=subclass,
                                             payment=payment,
                                             incomeandexpense=incomeandexpense,
                                             member=member)
    return HttpResponse(new_receipt)


def createSubClassification(request):
    member = request.POST['user']
    #get user?
    classification = request.POST['category']
    #get category
    if classification == 'food':
        classification = 'FO'
    elif classification == 'clothing':
        classification = 'CL'
    elif classification == 'housing':
        classification = 'HO'
    elif classification == 'transportation':
        classification = 'TR'
    elif classification == 'education':
        classification = 'ED'
    elif classification == 'entertainment':
        classification = 'EN'
    elif classification == 'others':
        classification = 'OT'
    name = request.POST['SubCategory']

    account.objects.create(member=member, classification=classification, name=name)
    return render(request, 'dashboard.html', {})
