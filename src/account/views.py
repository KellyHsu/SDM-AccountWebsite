#coding=utf8 
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from account.models import Receipt, SubClassification, Payment, IncomeAndExpense, Classification, CyclicalExpenditure, Budget, MonthBudget
from member.models import Member
from datetime import datetime, date
from django.contrib.auth.models import User
from django.db.models import Q
import json


def dashboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        cost_list = Receipt.objects.filter(member=member, date=date.today(), incomeandexpense__income_type="expense")
        revenue_list = Receipt.objects.filter(member=member, date=date.today(), incomeandexpense__income_type="income")

        food_list = SubClassification.objects.filter(member=member, classification=1)
        clothing_list = SubClassification.objects.filter(member=member, classification=2)
        housing_list = SubClassification.objects.filter(member=member, classification=3)
        transportation_list = SubClassification.objects.filter(member=member, classification=4)
        education_list = SubClassification.objects.filter(member=member, classification=5)
        entertainment_list = SubClassification.objects.filter(member=member, classification=6)
        others_list = SubClassification.objects.filter(member=member, classification=7)


        c8 = Classification.objects.filter(classification_type='general_revenue').first()
        c9 = Classification.objects.filter(classification_type='invest_revenue').first()
        c10 = Classification.objects.filter(classification_type='other_revenue').first()
        general_revenue_list = SubClassification.objects.filter(member=member, classification=c8)
        invest_revenue_list = SubClassification.objects.filter(member=member, classification=c9)
        other_revenue_list = SubClassification.objects.filter(member=member, classification=c10)

        print(invest_revenue_list)
    return render(request, 'dashboard.html', {"cost_list": cost_list, "revenue_list": revenue_list, "food_list": food_list,
                                              "clothing_list": clothing_list, "housing_list": housing_list,
                                              "transportation_list": transportation_list, "education_list": education_list,
                                              "entertainment_list": entertainment_list, "others_list": others_list,
                                              "general_revenue_list": general_revenue_list, "invest_revenue_list": invest_revenue_list,
                                              "other_revenue_list": other_revenue_list})


def setting(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        
        c1 = Classification.objects.filter(classification_type='food').first()
        food_list = SubClassification.objects.filter(member=member, classification=c1)
        print(food_list)
        c2 = Classification.objects.filter(classification_type='clothing').first()
        clothing_list = SubClassification.objects.filter(member=member, classification=c2)
        c3 = Classification.objects.filter(classification_type='housing').first()
        housing_list = SubClassification.objects.filter(member=member, classification=c3)
        c4 = Classification.objects.filter(classification_type='transportation').first()
        transportation_list = SubClassification.objects.filter(member=member, classification=c4)
        c5 = Classification.objects.filter(classification_type='education').first()
        education_list = SubClassification.objects.filter(member=member, classification=c5)
        c6 = Classification.objects.filter(classification_type='entertainment').first()
        entertainment_list = SubClassification.objects.filter(member=member, classification=c6)
        c7 = Classification.objects.filter(classification_type='others').first()
        others_list = SubClassification.objects.filter(member=member, classification=c7)
        
        month_budget = MonthBudget.objects.filter(member=member).first()      
        
        budget_food = Budget.objects.filter(member=member, classification=c1).first()
        budget_clothing = Budget.objects.filter(member=member, classification=c2).first()
        budget_housing = Budget.objects.filter(member=member, classification=c3).first()
        budget_transportation = Budget.objects.filter(member=member, classification=c4).first()
        budget_education = Budget.objects.filter(member=member, classification=c5).first()
        budget_entertainment = Budget.objects.filter(member=member, classification=c6).first()
        budget_other = Budget.objects.filter(member=member, classification=c7).first()
        
        cyclicalExpenditure_list = CyclicalExpenditure.objects.filter(member=member)

    return render(request, 'setting.html', {"member": member, "cyclicalExpenditure_list": cyclicalExpenditure_list,
                                            "budget_food": budget_food, "budget_clothing": budget_clothing, "budget_housing": budget_housing, "budget_transportation": budget_transportation,
                                            "budget_education": budget_education, "budget_entertainment": budget_entertainment, "budget_other": budget_other,
                                            "month_budget": month_budget, "food_list": food_list,
                                            "clothing_list": clothing_list, "housing_list": housing_list,
                                            "transportation_list": transportation_list, "education_list": education_list,
                                            "entertainment_list": entertainment_list, "others_list": others_list})


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

        cost_rowcontent = ""
        if new_receipt.remark:
            cost_rowcontent += "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'> " \
                               "{0}-{1}-{2}: {3}</a></td></tr>".format(new_receipt.subclassification.classification.classification_type.encode('utf-8'),
                                                                       new_receipt.subclassification.name.encode('utf-8'),
                                                                       new_receipt.remark.encode('utf-8'), new_receipt.money)
        else:
            cost_rowcontent += "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'> " \
                               "{0}-{1}: {2}</a></td></tr>".format(new_receipt.subclassification.classification.classification_type.encode('utf-8'),
                                                                   new_receipt.subclassification.name.encode('utf-8'),
                                                                   new_receipt.money)
    return HttpResponse(cost_rowcontent)


def delete_receipt(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        classification = Classification.objects.filter(classification_type=request.POST["category"]).first()
        subclass = SubClassification.objects.filter(name=request.POST["subcategory"], member=member, classification=classification).first()
        receipt = Receipt.objects.filter(money=request.POST["amount"], remark=request.POST["memo"],
                                        date=datetime.strptime(request.POST["date"], "%Y/%m/%d"),
                                        subclassification=subclass, member=member)
        if receipt is not None:
            # print(receipt)
            receipt.delete()
    return HttpResponse(receipt)


def create_subClassification(request):

    if request.method == 'POST':
        print(request.POST)
        category = Classification.objects.filter(classification_type=request.POST["category"]).first()
        member = Member.objects.filter(user__username=request.user).first()
        new_subclass, created = SubClassification.objects.get_or_create(member=member, classification=category,
                                                                        name=request.POST["newSub"],
                                                                        defaults={'name': request.POST["newSub"]})
        rowcontent = ""
        if created:
            rowcontent='<button type="button" class="btn btn-link {0}" id="sec-category">' \
                       '{1}</button>'.format(new_subclass.classification.classification_type +
                                             "_list", new_subclass.name.encode('utf-8'))

        return HttpResponse(rowcontent)


def classNameTranslate(name):
    return {
        'food': "食",
        'clothing': "衣",
        'housing': "住",
        'transportation': "行",
        'education': "育",
        'entertainment': "樂",
        'general_revenue': "收入",
        'invest_revenue': "投資",
        'other_revenue': "其他",
        'others': "其"
    }.get(name, "預設")


def get_date(request):

    if request.method == 'POST':
        print(request.POST)
        date = datetime.strptime(request.POST["date"], "%Y/%m/%d")
        member = Member.objects.filter(user__username=request.user).first()

        cost_receipts = Receipt.objects.all().filter(date=date, member=member, incomeandexpense__income_type="expense")
        cost_rowcontent = ""
        for receipt in cost_receipts:
            className = classNameTranslate(receipt.subclassification.classification.classification_type.encode('utf-8'))
            
            if receipt.remark:
                cost_rowcontent += "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'>" \
                            "{0}-{1}-{2}: {3}</a><span style='float: right; margin-right: 10px; color: #9D9D9D;'>" \
                                   "</span></td></tr>".format(className,
                                                                    receipt.subclassification.name.encode('utf-8'),
                                                                    receipt.remark.encode('utf-8'), receipt.money)
            else:
                cost_rowcontent += "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'>" \
                                   "{0}-{1}: {2}</a><span style='float: right; margin-right: 10px; color: #9D9D9D;'>" \
                                   "</span></td></tr>".format(className,
                                                                       receipt.subclassification.name.encode('utf-8'),
                                                                       receipt.money)

        revenue_receipts = Receipt.objects.all().filter(date=date, member=member, incomeandexpense__income_type="income")
        revenue_rowcontent = ""
        for receipt in revenue_receipts:
            className = classNameTranslate(receipt.subclassification.classification.classification_type.encode('utf-8'))

            if receipt.remark:
                revenue_rowcontent += "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'>" \
                            "{0}-{1}-{2}: {3}</a><span style='float: right; margin-right: 10px; color: #9D9D9D;'>" \
                                   "</span></td></tr>".format(className,
                                                                    receipt.subclassification.name.encode('utf-8'),
                                                                    receipt.remark.encode('utf-8'), receipt.money)
            else:
                revenue_rowcontent += "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'>" \
                                   "{0}-{1}: {2}</a><span style='float: right; margin-right: 10px; color: #9D9D9D;'>" \
                                   "</span></td></tr>".format(className,
                                                                       receipt.subclassification.name.encode('utf-8'),
                                                                       receipt.money)

        jsonResult = {'cost': cost_rowcontent , 'revenue': revenue_rowcontent}


    return HttpResponse( json.JSONEncoder().encode(jsonResult) )



def change_password(request):

    if request.method == 'POST':
        print(request.POST)
        user = User.objects.get(username=request.user)
        user.set_password(request.POST["new_password"])
        user.save()

    return HttpResponse(user)


def create_cyclicalExpenditure(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        cyclicalExpenditure = CyclicalExpenditure.objects.filter(name=request.POST["name"], member=member).first()
        if cyclicalExpenditure is not None:
            repeated_name="nameRepeated"
            print(repeated_name)
            return HttpResponse(repeated_name)
        else:
            new_cyclicalExpenditure = CyclicalExpenditure.objects.create(name=request.POST["name"], expenditure_date=request.POST["expenditure_date"],
                                             expenditure_type=request.POST["expenditure_type"], reminder_type=request.POST["reminder_type"],
                                             reminder_date=request.POST["reminder_date"], member=member,is_reminded=False)
    return HttpResponse(new_cyclicalExpenditure)


def update_cyclicalExpenditure(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        cyclicalExpenditure = CyclicalExpenditure.objects.filter(name=request.POST["name"], member=member).first()
        print(member)
        print(cyclicalExpenditure)
        if cyclicalExpenditure is not None:
            cyclicalExpenditure.expenditure_date=request.POST["expenditure_date"]
            cyclicalExpenditure.expenditure_type=request.POST["expenditure_type"]
            cyclicalExpenditure.reminder_type=request.POST["reminder_type"]
            cyclicalExpenditure.reminder_date=request.POST["reminder_date"]
            cyclicalExpenditure.save()
    return HttpResponse(cyclicalExpenditure)


def delete_cyclicalExpenditure(request):

    if request.method == 'POST':
        print(request.POST)
        names = request.POST.getlist("deltArr[]","None")
        member = Member.objects.filter(user__username=request.user).first()
        print(names)
        print(member)
        cyclicalExpenditure = CyclicalExpenditure.objects.filter(reduce(lambda x, y: x | y, [Q(name=item) for item in names]), member=member)
        if cyclicalExpenditure is not None:
            print(cyclicalExpenditure)
            cyclicalExpenditure.delete()
    return HttpResponse(cyclicalExpenditure)


def update_cyclicalExpenditure_isreminded(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        cyclicalExpenditure = CyclicalExpenditure.objects.filter(name=request.POST["name"], member=member).first()
        isreminded = request.POST["isreminded"]
        if cyclicalExpenditure is not None:
            cyclicalExpenditure.is_reminded = isreminded
            cyclicalExpenditure.save()
    return HttpResponse(cyclicalExpenditure)


def update_budget(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        print(member)
        budget = request.POST["budget"]
        category = Classification.objects.filter(classification_type=request.POST["category"]).first()
        budget_instance = Budget.objects.filter(classification=category, member=member).first()
        if budget_instance is not None:
            budget_instance.budget=budget
            budget_instance.save()
    return HttpResponse(budget_instance)


def update_budget_reminder(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        reminder = request.POST["reminder"]
        category = Classification.objects.filter(classification_type=request.POST["category"]).first()
        budget_instance = Budget.objects.filter(classification=category, member=member).first()
        if budget_instance is not None:
            budget_instance.reminder=reminder
            budget_instance.save()
    return HttpResponse(budget_instance)


def update_budget_isreminded(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        print(member)
        isreminded = request.POST["isreminded"]
        category = Classification.objects.filter(classification_type=request.POST["category"]).first()
        budget_instance = Budget.objects.filter(classification=category, member=member).first()
        if budget_instance is not None:
            budget_instance.is_reminded=isreminded
            budget_instance.save()
    return HttpResponse(budget_instance)


def update_month_budget(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        month_budget = request.POST["month_budget"]
        month_budget_instance = MonthBudget.objects.filter(member=member).first()
        if month_budget_instance is not None:
            month_budget_instance.budget=month_budget
            month_budget_instance.save()
    return HttpResponse()


def update_month_budget_reminder(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        reminder = request.POST["month_reminder"]
        month_budget_instance = MonthBudget.objects.filter(member=member).first()
        if month_budget_instance is not None:
            month_budget_instance.reminder=reminder
            month_budget_instance.save()
    return HttpResponse()


def update_month_budget_isreminded(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        isreminded = request.POST["isreminded"]
        month_budget_instance = MonthBudget.objects.filter(member=member).first()
        if month_budget_instance is not None:
            month_budget_instance.is_reminded=isreminded
            month_budget_instance.save()
    return HttpResponse()


def create_subClassification_in_settingPage(request):

    if request.method == 'POST':
        print(request.POST)
        category = Classification.objects.filter(classification_type=request.POST["category"]).first()
        member = Member.objects.filter(user__username=request.user).first()
        new_subclass, created = SubClassification.objects.get_or_create(member=member, classification=category,
                                                                        name=request.POST["newSub"],
                                                                        defaults={'name': request.POST["newSub"]})
        rowcontent = ""
        if created:
            rowcontent='<button type="button" class="btn btn-link btn-md sub-category">{0}</button>'.format(new_subclass.name.encode('utf-8'))

        return HttpResponse(rowcontent)


def delete_subClassification_in_settingPage(request):

    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        delsub = SubClassification.objects.filter(name=request.POST["name"], member=member).delete()
        return HttpResponse(delsub)