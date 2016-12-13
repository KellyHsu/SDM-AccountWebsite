# coding=utf8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from account.models import Receipt, SubClassification, Payment, IncomeAndExpense, Classification, CyclicalExpenditure, \
    Budget, MonthBudget
from member.models import Member
from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from django.db.models import Q, Sum
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

        periodic_notification_list = periodicItemDateCheck(member)

        total_expense = get_total(cost_list)
        total_income = get_total(revenue_list)

    return render(request, 'dashboard.html',
                  {"cost_list": cost_list, "revenue_list": revenue_list, "food_list": food_list,
                   "clothing_list": clothing_list, "housing_list": housing_list,
                   "transportation_list": transportation_list, "education_list": education_list,
                   "entertainment_list": entertainment_list, "others_list": others_list,
                   "general_revenue_list": general_revenue_list, "invest_revenue_list": invest_revenue_list,
                   "other_revenue_list": other_revenue_list, "periodic_notification_list": periodic_notification_list,
                   "periodic_notification_count": len(periodic_notification_list),
                   "total_expense": total_expense, "total_income": total_income})


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
                                            "budget_food": budget_food, "budget_clothing": budget_clothing,
                                            "budget_housing": budget_housing,
                                            "budget_transportation": budget_transportation,
                                            "budget_education": budget_education,
                                            "budget_entertainment": budget_entertainment, "budget_other": budget_other,
                                            "month_budget": month_budget, "food_list": food_list,
                                            "clothing_list": clothing_list, "housing_list": housing_list,
                                            "transportation_list": transportation_list,
                                            "education_list": education_list,
                                            "entertainment_list": entertainment_list, "others_list": others_list})


def filter(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        # currentDate = datetime.now()
        # receipts = Receipt.objects.filter(member=member,date__date=datetime.date(currentDate.year, currentDate.month, currentDate.day))
        member = Member.objects.filter(user__username=request.user).first()
        receipts = Receipt.objects.filter(member=member, date=date.today())
        currentDate = datetime.strftime(datetime.now(), '%Y/%m/%d')
        totalCost = Receipt.objects.filter(member=member, date=date.today(),
                                           incomeandexpense__income_type="expense").aggregate(Sum('money'))
        totalIncome = Receipt.objects.filter(member=member, date=date.today(),
                                             incomeandexpense__income_type="income").aggregate(Sum('money'))
        # print type(str(totalIncome['money__sum']))
        if str(totalIncome['money__sum']) == "None":
            income = 0
        else:
            income = int(totalIncome['money_sum'])
        if str(totalCost['money__sum']) == "None":
            cost = 0
        else:
            cost = int(totalCost['money__sum'])
        balance = income - cost
        print balance, type(balance)
    return render(request, 'filter.html',
                  {"member": member, "receipts": receipts, "title": currentDate, "totalCost": cost,
                   "totalIncome": income, "balance": balance})


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

        if incomeandexpense.income_type == 'expense':
            receipt_list = Receipt.objects.filter(member=member, date=date.today(),
                                                  incomeandexpense__income_type="expense")
        else:
            receipt_list = Receipt.objects.filter(member=member, date=date.today(),
                                                  incomeandexpense__income_type="income")

        total_value = get_total(receipt_list)

        cost_rowcontent = ""
        if new_receipt.remark:
            cost_rowcontent += "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'> " \
                               "{0}-{1}-{2}: {3}</a><span style='float: right; margin-right: 10px; " \
                               "color: #9D9D9D;'></span></td></tr>".format(
                new_receipt.subclassification.classification.classification_type.encode('utf-8'),
                new_receipt.subclassification.name.encode('utf-8'),
                new_receipt.remark.encode('utf-8'), new_receipt.money)
        else:
            cost_rowcontent += "<tr><td><span class='glyphicon glyphicon-file text-success'></span><a href='#'> " \
                               "{0}-{1}: {2}</a><span style='float: right; margin-right: 10px; " \
                               "color: #9D9D9D;'></span></td></tr>".format(
                new_receipt.subclassification.classification.classification_type.encode('utf-8'),
                new_receipt.subclassification.name.encode('utf-8'),
                new_receipt.money)

        classification = classNameTranslate_zhtwToen(request.POST["category"].split("-")[0].encode('utf-8'))
        category = Classification.objects.filter(classification_type=classification).first()
        category_budget_instance = Budget.objects.filter(classification=category, member=member).first()
        month_budget_instance = MonthBudget.objects.filter(member=member).first()

        # 只有支出才要計算預算
        monthly_budget_check_result = ""
        class_budget_check_result = ""
        if incomeandexpense.income_type == 'expense':
            # check month budget setting
            if month_budget_instance and month_budget_instance.is_reminded:
                monthly_budget_check_result = budget_calculate(member)
            # check category budget setting
            if category_budget_instance and category_budget_instance.is_reminded:
                class_budget_check_result = classification_budget_calculate(member, classification)

        message = {"rowcontent": cost_rowcontent, "total_value": total_value,
                   "budget_check": {"monthly": monthly_budget_check_result, "class": class_budget_check_result}}

    return HttpResponse(json.JSONEncoder().encode(message))


def delete_receipt(request):
    if request.method == 'POST':
        print(request.POST)

        # delete receipt
        member = Member.objects.filter(user__username=request.user).first()
        classification = Classification.objects.filter(classification_type=request.POST["category"]).first()
        subclass = SubClassification.objects.filter(name=request.POST["subcategory"], member=member,
                                                    classification=classification).first()
        receipt = Receipt.objects.filter(money=request.POST["amount"], remark=request.POST["memo"],
                                         date=datetime.strptime(request.POST["date"], "%Y/%m/%d"),
                                         subclassification=subclass, member=member).first()
        if receipt is not None:
            receipt.delete()

        # recount total
        incomeandexpense = IncomeAndExpense.objects.filter(income_type=request.POST["record_type"]).first()
        if incomeandexpense.income_type == 'expense':
            receipt_list = Receipt.objects.filter(member=member, date=date.today(),
                                                  incomeandexpense__income_type="expense")
        else:
            receipt_list = Receipt.objects.filter(member=member, date=date.today(),
                                                  incomeandexpense__income_type="income")
        total_value = get_total(receipt_list)

    return HttpResponse(total_value)


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
            rowcontent = '<button type="button" class="btn btn-link {0}" id="sec-category">' \
                         '{1}</button>'.format(new_subclass.classification.classification_type +
                                               "_list", new_subclass.name.encode('utf-8'))

        return HttpResponse(rowcontent)


# 用來把英文分類換成中文
def classNameTranslate_enTozhtw(name):
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


# 用來把中文分類換成英文
def classNameTranslate_zhtwToen(name):
    return {
        '食': "food",
        '衣': "clothing",
        '住': "housing",
        '行': "transportation",
        '育': "education",
        '樂': "entertainment",
        '收入': "general_revenue",
        '投資': "invest_revenue",
        '其他': "other_revenue",
        '其': "others"
    }.get(name, "other")


def get_date(request):
    if request.method == 'POST':
        print(request.POST)
        date = datetime.strptime(request.POST["date"], "%Y/%m/%d")
        member = Member.objects.filter(user__username=request.user).first()

        cost_receipts = Receipt.objects.all().filter(date=date, member=member, incomeandexpense__income_type="expense")
        cost_rowcontent = ""
        for receipt in cost_receipts:
            className = classNameTranslate_enTozhtw(
                receipt.subclassification.classification.classification_type.encode('utf-8'))
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

        revenue_receipts = Receipt.objects.all().filter(date=date, member=member,
                                                        incomeandexpense__income_type="income")
        revenue_rowcontent = ""
        for receipt in revenue_receipts:
            className = classNameTranslate_enTozhtw(
                receipt.subclassification.classification.classification_type.encode('utf-8'))

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

        jsonResult = {'cost': cost_rowcontent, 'revenue': revenue_rowcontent}

    return HttpResponse(json.JSONEncoder().encode(jsonResult))


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
            repeated_name = "nameRepeated"
            print(repeated_name)
            return HttpResponse(repeated_name)
        else:
            new_cyclicalExpenditure = CyclicalExpenditure.objects.create(name=request.POST["name"],
                                                                         expenditure_date=request.POST[
                                                                             "expenditure_date"],
                                                                         expenditure_type=request.POST[
                                                                             "expenditure_type"],
                                                                         reminder_type=request.POST["reminder_type"],
                                                                         reminder_date=request.POST["reminder_date"],
                                                                         member=member, is_reminded=False)
    return HttpResponse(new_cyclicalExpenditure)


def update_cyclicalExpenditure(request):
    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        cyclicalExpenditure = CyclicalExpenditure.objects.filter(name=request.POST["name"], member=member).first()
        print(member)
        print(cyclicalExpenditure)
        if cyclicalExpenditure is not None:
            cyclicalExpenditure.expenditure_date = request.POST["expenditure_date"]
            cyclicalExpenditure.expenditure_type = request.POST["expenditure_type"]
            cyclicalExpenditure.reminder_type = request.POST["reminder_type"]
            cyclicalExpenditure.reminder_date = request.POST["reminder_date"]
            cyclicalExpenditure.save()
    return HttpResponse(cyclicalExpenditure)


def delete_cyclicalExpenditure(request):
    if request.method == 'POST':
        print(request.POST)
        names = request.POST.getlist("deltArr[]", "None")
        member = Member.objects.filter(user__username=request.user).first()
        print(names)
        print(member)
        cyclicalExpenditure = CyclicalExpenditure.objects.filter(
            reduce(lambda x, y: x | y, [Q(name=item) for item in names]), member=member)
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
            budget_instance.budget = budget
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
            budget_instance.reminder = reminder
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
            budget_instance.is_reminded = isreminded
            budget_instance.save()
    return HttpResponse(budget_instance)


def update_month_budget(request):
    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        month_budget = request.POST["month_budget"]
        month_budget_instance = MonthBudget.objects.filter(member=member).first()
        if month_budget_instance is not None:
            month_budget_instance.budget = month_budget
            month_budget_instance.save()
    return HttpResponse()


def update_month_budget_reminder(request):
    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        reminder = request.POST["month_reminder"]
        month_budget_instance = MonthBudget.objects.filter(member=member).first()
        if month_budget_instance is not None:
            month_budget_instance.reminder = reminder
            month_budget_instance.save()
    return HttpResponse()


def update_month_budget_isreminded(request):
    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        isreminded = request.POST["isreminded"]
        month_budget_instance = MonthBudget.objects.filter(member=member).first()
        if month_budget_instance is not None:
            month_budget_instance.is_reminded = isreminded
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
            rowcontent = '<button type="button" class="btn btn-link btn-md sub-category">{0}</button>'.format(
                new_subclass.name.encode('utf-8'))

        return HttpResponse(rowcontent)


def delete_subClassification_in_settingPage(request):
    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        delsub = SubClassification.objects.filter(name=request.POST["name"], member=member).delete()
        return HttpResponse(delsub)


# 計算當月的各項預算和總預算是否有超過上限
def budget_calculate(member):
    monthly_budget = MonthBudget.objects.filter(member=member).first()
    # 以月為範圍做查詢
    currentDate = datetime.now()
    if (currentDate.month == 2):
        dayOfMonth = 28
    elif (currentDate.month == 4 or currentDate.month == 6 or currentDate.month == 9 or currentDate.month == 11):
        dayOfMonth = 30
    else:
        dayOfMonth = 31

    startDay = date(currentDate.year, currentDate.month, 1)
    lastDay = date(currentDate.year, currentDate.month, dayOfMonth)

    receipt = Receipt.objects.all().filter(date__range=[startDay, lastDay], member=member,
                                           incomeandexpense__income_type="expense")

    sumOfExpense = 0
    for entry in receipt:
        sumOfExpense += entry.money

    alertMessage = ""
    monthlyBudget = monthly_budget.budget
    alertThreshold = monthly_budget.reminder

    # 如果有設定預算且超過
    if (monthlyBudget > 0 and sumOfExpense > monthlyBudget):
        alertMessage = "警告：本月花費已超過當月預算"
    elif (alertThreshold > 0 and sumOfExpense > alertThreshold):
        alertMessage = "警告：本月花費已超過 {0}".format(alertThreshold.encode('utf-8'))
    else:
        alertMessage = "正常"

    return alertMessage


# 計算分類支出是否有超過預算上限
def classification_budget_calculate(member, classification):
    c1 = Classification.objects.filter(classification_type=classification).first()
    budget_Object = Budget.objects.filter(member=member, classification=c1).first()

    # 以月為範圍做查詢
    currentDate = datetime.now()
    if (currentDate.month == 2):
        dayOfMonth = 28
    elif (currentDate.month == 4 or currentDate.month == 6 or currentDate.month == 9 or currentDate.month == 11):
        dayOfMonth = 30
    else:
        dayOfMonth = 31

    startDay = date(currentDate.year, currentDate.month, 1)
    lastDay = date(currentDate.year, currentDate.month, dayOfMonth)

    # 把所有子分類撈出來，才能查Recepit
    subClass_list = SubClassification.objects.filter(member=member, classification=c1)

    # 把該月所有的該主分類的支出receipt加總
    sumOfExpense = 0
    for subclass in subClass_list:
        receipt = Receipt.objects.all().filter(date__range=[startDay, lastDay], member=member,
                                               subclassification=subclass, incomeandexpense__income_type="expense")
        for entry in receipt:
            sumOfExpense += entry.money

    alertMessage = ""
    classBudget = budget_Object.budget
    classBudgetThreshold = budget_Object.reminder
    classification = classNameTranslate_enTozhtw(classification)
    print(classification)
    if (classBudget > 0 and sumOfExpense > classBudget):
        alertMessage = "警告：本月{0}分類花費已超過當月預算".format(classification)
    elif (classBudgetThreshold > 0 and sumOfExpense > classBudgetThreshold):
        alertMessage = "警告：本月{0}分類花費已超過 {1}".format(classification, classBudgetThreshold)
    else:
        alertMessage = "正常"

    return alertMessage


def getreceipt_week(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        today = date.today()
        weekday = today.weekday()
        if weekday == 2:
            startDay = today - timedelta(days=3)
            endDay = today + timedelta(days=3)
        else:
            forward = today + timedelta(days=1)
            while forward.weekday() != 2:
                forward = forward + timedelta(days=1)
            dateForward = forward
            backward = today - timedelta(days=1)
            while backward.weekday() != 2:
                backward = backward - timedelta(days=1)
            dateBackward = backward
            diff1 = today - dateBackward
            diff2 = dateForward - today
            if diff1 < diff2:
                startDay = dateBackward - timedelta(days=3)
                endDay = dateBackward + timedelta(days=3)
            else:
                startDay = dateForward - timedelta(days=3)
                endDay = dateForward + timedelta(days=3)
        receipts = Receipt.objects.filter(member=member, date__range=[startDay, endDay])
        week = datetime.strftime(startDay, '%Y/%m/%d') + "-" + datetime.strftime(endDay, '%Y/%m/%d')

        totalCost = Receipt.objects.filter(member=member, date__range=[startDay, endDay],
                                           incomeandexpense__income_type="expense").aggregate(Sum('money'))
        totalIncome = Receipt.objects.filter(member=member, date__range=[startDay, endDay],
                                             incomeandexpense__income_type="income").aggregate(Sum('money'))
        # print type(str(totalIncome['money__sum']))
        if str(totalIncome['money__sum']) == "None":
            income = 0
        else:
            income = int(totalIncome['money_sum'])
        if str(totalCost['money__sum']) == "None":
            cost = 0
        else:
            cost = int(totalCost['money__sum'])
        balance = income - cost
        print balance, type(balance)
    return render(request, 'filter.html',
                  {"member": member, "receipts": receipts, "title": week, "totalCost": cost, "totalIncome": income,
                   "balance": balance})


def getreceipt_mon(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        currentDate = datetime.now()
        title = datetime.strftime(currentDate, "%Y/%m")
        receipts = Receipt.objects.filter(date__month=currentDate.month, member=member)
        totalCost = Receipt.objects.filter(member=member, date__month=currentDate.month,
                                           incomeandexpense__income_type="expense").aggregate(Sum('money'))
        totalIncome = Receipt.objects.filter(member=member, date__month=currentDate.month,
                                             incomeandexpense__income_type="income").aggregate(Sum('money'))
        # print type(str(totalIncome['money__sum']))
        if str(totalIncome['money__sum']) == "None":
            income = 0
        else:
            income = int(totalIncome['money_sum'])
        if str(totalCost['money__sum']) == "None":
            cost = 0
        else:
            cost = int(totalCost['money__sum'])
        balance = income - cost
        print balance, type(balance)
    return render(request, 'filter.html',
                  {"member": member, "receipts": receipts, "title": title, "totalCost": cost, "totalIncome": income,
                   "balance": balance})


def getreceipt_yr(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        currentDate = datetime.now()
        yr = str(currentDate.year)
        receipts = Receipt.objects.filter(date__year=currentDate.year, member=member)
        totalCost = Receipt.objects.filter(member=member, date__year=currentDate.year,
                                           incomeandexpense__income_type="expense").aggregate(Sum('money'))
        totalIncome = Receipt.objects.filter(member=member, date__year=currentDate.year,
                                             incomeandexpense__income_type="income").aggregate(Sum('money'))
        # print type(str(totalIncome['money__sum']))
        if str(totalIncome['money__sum']) == "None":
            income = 0
        else:
            income = int(totalIncome['money_sum'])
        if str(totalCost['money__sum']) == "None":
            cost = 0
        else:
            cost = int(totalCost['money__sum'])
        balance = income - cost
        print balance, type(balance)
    return render(request, 'filter.html',
                  {"member": member, "receipts": receipts, "title": yr, "totalCost": cost, "totalIncome": income,
                   "balance": balance})


def backwardtime(request):
    if request.method == 'POST':
        # print(request.POST)
        print type(request.POST["pageHeader_date"]), request.POST["sign"]
        member = Member.objects.filter(user__username=request.user).first()
        if request.POST["sign"] == "day":
            pageHeader_date = datetime.strptime(request.POST["pageHeader_date"], "%Y/%m/%d")
            if request.POST["id"] == "btn_left":
                target = pageHeader_date - timedelta(days=1)
            else:
                target = pageHeader_date + timedelta(days=1)
            receipts = Receipt.objects.filter(member=member, date=target)
            targetOutput = datetime.strftime(target, '%Y/%m/%d')
            totalCost = Receipt.objects.filter(member=member, date=target,
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date=target,
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))
        elif request.POST["sign"] == "week":
            temp = request.POST["pageHeader_date"].split('-')
            print temp[0], temp[1]
            temp[0] = datetime.strptime(temp[0], "%Y/%m/%d")
            temp[1] = datetime.strptime(temp[1], "%Y/%m/%d")
            if request.POST["id"] == "btn_left":
                targetStart = temp[0] - timedelta(days=7)
                targetEnd = temp[1] - timedelta(days=7)
            else:
                targetStart = temp[0] + timedelta(days=7)
                targetEnd = temp[1] + timedelta(days=7)
            receipts = Receipt.objects.filter(member=member, date__range=[targetStart, targetEnd])
            targetOutput = datetime.strftime(targetStart, '%Y/%m/%d') + "-" + datetime.strftime(targetEnd, '%Y/%m/%d')
            totalCost = Receipt.objects.filter(member=member, date__range=[targetStart, targetEnd],
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date__range=[targetStart, targetEnd],
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))
        elif request.POST["sign"] == "month":
            if request.POST["id"] == "btn_left":
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y/%m") - timedelta(days=365 / 12)
            else:
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y/%m") + timedelta(days=365 / 12)
            receipts = Receipt.objects.filter(date__month=target.month, member=member)
            targetOutput = datetime.strftime(target, '%Y/%m')
            totalCost = Receipt.objects.filter(member=member, date__month=target.month,
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date__month=target.month,
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))
        else:
            if request.POST["id"] == "btn_left":
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y") - timedelta(days=365)
            else:
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y") + timedelta(days=365)
            receipts = Receipt.objects.filter(date__year=target.year, member=member)
            targetOutput = datetime.strftime(target, '%Y')
            totalCost = Receipt.objects.filter(member=member, date__year=target.year,
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date__year=target.year,
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))

        if str(totalIncome['money__sum']) == "None":
            income = 0
        else:
            income = int(totalIncome['money_sum'])
        if str(totalCost['money__sum']) == "None":
            cost = 0
        else:
            cost = int(totalCost['money__sum'])
        print income, cost
        balance = income - cost
        print balance, type(balance)
        print targetOutput
        table = ""
        print len(receipts), type(receipts)
        for receipt in receipts:
            print type(
                receipt.subclassification.classification.classification_type), receipt.subclassification.classification.classification_type
            table += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td>" \
                     "<td>{6}</td><td>{7}</td></tr>".format(
                receipt.subclassification.classification.classification_type.encode('utf-8'),
                receipt.subclassification.name.encode('utf-8'), receipt.remark.encode('utf-8'),
                receipt.incomeandexpense,
                receipt.payment, receipt.date, receipt.money, receipt.member)
            print table
        jsonResult = {'tableContent': table, 'title': targetOutput, 'balance': balance, 'income': income, 'cost': cost}
    return HttpResponse(json.JSONEncoder().encode(jsonResult))


# 檢查是否有週期性項目的日期到了要提醒使用者
def periodicItemDateCheck(member):
    periodicItemList = CyclicalExpenditure.objects.all().filter(member=member)
    notification_list = []

    for entry in periodicItemList:
        if entry.is_reminded:
            if entry.reminder_type == 'week':
                if entry.reminder_date == date.today().isoweekday():
                    payingTimeTitle = ""
                    payingTimeContent = ""

                    if entry.expenditure_date >= entry.reminder_date:
                        payingTimeTitle = "本週"
                    else:
                        payingTimeTitle = "下週"
                    weekday = {
                        1: "星期一",
                        2: "星期二",
                        3: "星期三",
                        4: "星期四",
                        5: "星期五",
                        6: "星期六",
                        7: "星期日"
                    }
                    payingTimeContent = weekday.get(entry.expenditure_date, "星期天")

                    message = "繳費提醒：{0}須於{1}{2}進行繳費".format(entry.name.encode('utf-8'), payingTimeTitle,
                                                            payingTimeContent)
                    notification_list.append(message)

            else:
                if entry.reminder_date == date.today().day:
                    payingTimeTitle = ""
                    payingTimeContent = ""
                    if entry.expenditure_date >= entry.reminder_date:
                        payingTimeTitle = "本月"
                    else:
                        payingTimeTitle = "下個月"
                    payingTimeContent = str(entry.expenditure_date) + "號"

                    message = "繳費提醒：{0}須於{1}{2}進行繳費".format(entry.name.encode('utf-8'), payingTimeTitle,
                                                            payingTimeContent)
                    notification_list.append(message)

                    # end if-else 'week'
                    # end if is_reminded

    return notification_list


def get_total(receipt_list):
    total = 0
    for receipt in receipt_list:
        total += receipt.money

    return total
