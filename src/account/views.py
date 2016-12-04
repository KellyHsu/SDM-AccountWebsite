#coding=utf8 
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from account.models import Receipt, SubClassification, Payment, IncomeAndExpense, Classification
from member.models import Member
from datetime import datetime, date


def dashboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        cost_list = Receipt.objects.filter(member=member).filter(date=date.today()).filter(incomeandexpense__income_type="expense")
        print(cost_list)

    return render(request, 'dashboard.html', {"cost_list": cost_list, })


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
        # print(request.POST)
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
        rowcontent = "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'>" \
                     "" + new_receipt.subclassification.classification.classificaion_type + "- " + new_receipt.subclassification.name + "-" + new_receipt.remark + ": " + new_receipt.money + "</a></td></tr>";
    return HttpResponse(rowcontent)


def create_subClassification(request):

    if request.method == 'POST':
        print(request.POST)
        category = Classification.objects.filter(name=request.POST["category"]).first()
        member = Member.objects.filter(user__username=request.user).first()
        new_subClassification = SubClassification.objects.create(name=request.POST["newSub"], classification=category, member=member)
    return HttpResponse(new_subClassification)


def get_date(request):

    if request.method == 'POST':
        print(request.POST)
        date = datetime.strptime(request.POST["date"], "%Y/%m/%d")
        member = Member.objects.filter(user__username=request.user).first()

        cost_receipts = Receipt.objects.all().filter(date=date, member=member, incomeandexpense__income_type="expense")
        cost_rowcontent = ""
        for receipt in cost_receipts:
            cost_rowcontent = "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'>" \
                         "{0}- {1}-{2}: {3}</a></td></tr>".format(receipt.subclassification.classification.classificaion_type.encode('utf-8'),
                                                                  receipt.subclassification.name.encode('utf-8'),
                                                                  receipt.remark.encode('utf-8'), receipt.money)
    return HttpResponse(cost_rowcontent)
