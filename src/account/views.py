from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from account.models import Receipt, SubClassification, Payment, IncomeAndExpense, Classification, CyclicalExpenditure, \
    Budget, MonthBudget
from member.models import Member
from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from django.db.models import Q, Sum
import json
from bokeh.plotting import figure, output_file, show
from bokeh.charts import Bar, Donut, output_file, show
from bokeh.layouts import row
from bokeh.embed import components
import pandas as pd
from pandas.compat import StringIO
from bokeh.charts.attributes import ColorAttr, CatAttr


def dashboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        cost_list = Receipt.objects.filter(member=member, date=date.today(), incomeandexpense__income_type="expense")
        revenue_list = Receipt.objects.filter(member=member, date=date.today(), incomeandexpense__income_type="income")

        food_list = SubClassification.objects.filter(member=member, classification=1, exist=True)
        clothing_list = SubClassification.objects.filter(member=member, classification=2, exist=True)
        housing_list = SubClassification.objects.filter(member=member, classification=3, exist=True)
        transportation_list = SubClassification.objects.filter(member=member, classification=4, exist=True)
        education_list = SubClassification.objects.filter(member=member, classification=5, exist=True)
        entertainment_list = SubClassification.objects.filter(member=member, classification=6, exist=True)
        others_list = SubClassification.objects.filter(member=member, classification=7, exist=True)

        c8 = Classification.objects.filter(classification_type='general_revenue').first()
        c9 = Classification.objects.filter(classification_type='invest_revenue').first()
        c10 = Classification.objects.filter(classification_type='other_revenue').first()
        general_revenue_list = SubClassification.objects.filter(member=member, classification=c8, exist=True)
        invest_revenue_list = SubClassification.objects.filter(member=member, classification=c9, exist=True)
        other_revenue_list = SubClassification.objects.filter(member=member, classification=c10, exist=True)

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
        food_list = SubClassification.objects.filter(member=member, classification=c1, exist=True)
        c2 = Classification.objects.filter(classification_type='clothing').first()
        clothing_list = SubClassification.objects.filter(member=member, classification=c2, exist=True)
        c3 = Classification.objects.filter(classification_type='housing').first()
        housing_list = SubClassification.objects.filter(member=member, classification=c3, exist=True)
        c4 = Classification.objects.filter(classification_type='transportation').first()
        transportation_list = SubClassification.objects.filter(member=member, classification=c4, exist=True)
        c5 = Classification.objects.filter(classification_type='education').first()
        education_list = SubClassification.objects.filter(member=member, classification=c5, exist=True)
        c6 = Classification.objects.filter(classification_type='entertainment').first()
        entertainment_list = SubClassification.objects.filter(member=member, classification=c6, exist=True)
        c7 = Classification.objects.filter(classification_type='others').first()
        others_list = SubClassification.objects.filter(member=member, classification=c7, exist=True)
        c8 = Classification.objects.filter(classification_type='general_revenue').first()
        general_revenue_list = SubClassification.objects.filter(member=member, classification=c8, exist=True)
        c9 = Classification.objects.filter(classification_type='invest_revenue').first()
        invest_revenue_list = SubClassification.objects.filter(member=member, classification=c9, exist=True)
        c10 = Classification.objects.filter(classification_type='other_revenue').first()
        other_revenue_list = SubClassification.objects.filter(member=member, classification=c10, exist=True)

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
                                            "entertainment_list": entertainment_list, "others_list": others_list,
                                            "general_revenue_list": general_revenue_list, "invest_revenue_list": invest_revenue_list,
                                            "other_revenue_list": other_revenue_list})


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
            income = int(totalIncome['money__sum'])
        if str(totalCost['money__sum']) == "None":
            cost = 0
        else:
            cost = int(totalCost['money__sum'])
        balance = income - cost
        print balance, type(balance)
    return render(request, 'filter.html',
                  {"member": member, "receipts": receipts, "title": currentDate, "totalCost": cost,
                   "totalIncome": income, "balance": balance})


def chart(request):
    
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
        week = datetime.strftime(startDay, '%Y/%m/%d') + "-" + datetime.strftime(endDay, '%Y/%m/%d')
        cost_sun = Receipt.objects.filter(member=member, date=startDay, incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_mon = Receipt.objects.filter(member=member, date=startDay+timedelta(days=1), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_tue = Receipt.objects.filter(member=member, date=startDay+timedelta(days=2), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_wed = Receipt.objects.filter(member=member, date=startDay+timedelta(days=3), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_thu = Receipt.objects.filter(member=member, date=startDay+timedelta(days=4), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_fri = Receipt.objects.filter(member=member, date=startDay+timedelta(days=5), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_sat = Receipt.objects.filter(member=member, date=endDay, incomeandexpense__income_type="expense").aggregate(Sum('money'))
        if str(cost_sun['money__sum']) == "None":
            cost_sun = 0
        else:
            cost_sun = int(cost_sun['money__sum'])
        if str(cost_mon['money__sum']) == "None":
            cost_mon = 0
        else:
            cost_mon = int(cost_mon['money__sum'])
        if str(cost_tue['money__sum']) == "None":
            cost_tue = 0
        else:
            cost_tue = int(cost_tue['money__sum'])
        if str(cost_wed['money__sum']) == "None":
            cost_wed = 0
        else:
            cost_wed = int(cost_wed['money__sum'])
        if str(cost_thu['money__sum']) == "None":
            cost_thu = 0
        else:
            cost_thu = int(cost_thu['money__sum'])
        if str(cost_fri['money__sum']) == "None":
            cost_fri = 0
        else:
            cost_fri = int(cost_fri['money__sum'])
        if str(cost_sat['money__sum']) == "None":
            cost_sat = 0
        else:
            cost_sat = int(cost_sat['money__sum'])

        income_sun = Receipt.objects.filter(member=member, date=startDay, incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_mon = Receipt.objects.filter(member=member, date=startDay+timedelta(days=1), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_tue = Receipt.objects.filter(member=member, date=startDay+timedelta(days=2), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_wed = Receipt.objects.filter(member=member, date=startDay+timedelta(days=3), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_thu = Receipt.objects.filter(member=member, date=startDay+timedelta(days=4), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_fri = Receipt.objects.filter(member=member, date=startDay+timedelta(days=5), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_sat = Receipt.objects.filter(member=member, date=endDay, incomeandexpense__income_type="income").aggregate(Sum('money'))
        if str(income_sun['money__sum']) == "None":
            income_sun = 0
        else:
            income_sun = int(income_sun['money__sum'])
        if str(income_mon['money__sum']) == "None":
            income_mon = 0
        else:
            income_mon = int(income_mon['money__sum'])
        if str(income_tue['money__sum']) == "None":
            income_tue = 0
        else:
            income_tue = int(income_tue['money__sum'])
        if str(income_wed['money__sum']) == "None":
            income_wed = 0
        else:
            income_wed = int(income_wed['money__sum'])
        if str(income_thu['money__sum']) == "None":
            income_thu = 0
        else:
            income_thu = int(income_thu['money__sum'])
        if str(income_fri['money__sum']) == "None":
            income_fri = 0
        else:
            income_fri = int(income_fri['money__sum'])
        if str(income_sat['money__sum']) == "None":
            income_sat = 0
        else:
            income_sat = int(income_sat['money__sum'])

        data = {
            'week': ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            'dollar': [cost_sun, cost_mon, cost_tue, cost_wed, cost_thu, cost_fri, cost_sat, income_sun, income_mon, income_tue, income_wed, income_thu, income_fri, income_sat],
            'origin':['expense','expense','expense','expense','expense','expense','expense',
                      'income','income','income','income','income','income','income']
        }
        bar2 = Bar(data, label=CatAttr(columns=['week'], sort=False,), values='dollar', plot_height=400, responsive=True, group='origin')
        script2, div2 = components(bar2)

        #AAPL = pd.read_csv(
        #    "http://ichart.yahoo.com/table.csv?s=AAPL&a=0&b=1&c=2000&d=0&e=1&f=2010",
        #    parse_dates=['Date']
        #)
        #print(AAPL)
        s = """Date,Close
        """+datetime.strftime(startDay, '%Y/%m/%d')+""","""+str(cost_sun)+"""
        """+datetime.strftime(startDay+timedelta(days=1), '%Y/%m/%d')+""","""+str(cost_mon)+"""
        """+datetime.strftime(startDay+timedelta(days=2), '%Y/%m/%d')+""","""+str(cost_tue)+"""
        """+datetime.strftime(startDay+timedelta(days=3), '%Y/%m/%d')+""","""+str(cost_wed)+"""
        """+datetime.strftime(startDay+timedelta(days=4), '%Y/%m/%d')+""","""+str(cost_thu)+"""
        """+datetime.strftime(startDay+timedelta(days=5), '%Y/%m/%d')+""","""+str(cost_fri)+"""
        """+datetime.strftime(endDay, '%Y/%m/%d')+""","""+str(cost_sat)+""" """
        print(s)
        AAPL = pd.read_csv(StringIO(s),parse_dates=['Date'])
        print(AAPL)
        # create a new plot with a datetime axis type
        p = figure(plot_height=400, responsive=True, x_axis_type="datetime")

        p.line(AAPL['Date'], AAPL['Close'], color='navy', alpha=0.5)

        # add renderers
        #p.circle(aapl_dates, aapl, size=4, color='darkgrey', alpha=0.2, legend='close')
        #p.line(aapl_dates, aapl_avg, color='navy', legend='avg')
    
        # NEW: customize by setting attributes
        ##p.title.text = "AAPL One-Month Average"
        p.legend.location = "top_left"
        p.grid.grid_line_alpha=0
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Dollar'
        p.ygrid.band_fill_color="olive"
        p.ygrid.band_fill_alpha = 0.1
        script, div = components(p)
        print(div)

        #p = figure()
        #p.circle([1,2], [3,4])
        #script, div = components(p)
        #print(script)
        #print(div)
        #show(p)

        ###Classification's drop down menu###
        oldest_receipt = Receipt.objects.filter(member=member).order_by('date').first()
        #print(oldest_receipt.date)
        if oldest_receipt is not None:
            oldest_y = int(datetime.strftime(oldest_receipt.date, '%Y'))
            oldest_m = int(datetime.strftime(oldest_receipt.date, '%m'))
            today_y = int(datetime.strftime(today, '%Y'))
            today_m = int(datetime.strftime(today, '%m'))
            month_list=[]
            first=1

            while oldest_y != today_y+1:
                m=1
                if oldest_y == today_y:
                    while m != today_m+1:
                        month_list.append(str(oldest_y)+" - "+str(m).zfill(2))
                        m = m + 1
                else:
                    if first == 1:
                        m=oldest_m
                    while m != 13:
                        month_list.append(str(oldest_y)+" - "+str(+m).zfill(2))
                        m = m + 1
                oldest_y = oldest_y + 1
                first = first + 1
            print(month_list)
        else:
            month_list=[]

    return render(request, 'chart.html',{"title": week, "the_script": script, "the_div": div, "script_bar": script2, "div_bar": div2, "month_list": month_list})


def create_receipt(request):
    if request.method == 'POST':
        print(request.POST)
        receipt_id = None
        if request.POST.get('whick_receipt', False):
            receipt_id = int(request.POST["whick_receipt"].partition("receipt")[-1])

        subclass = SubClassification.objects.filter(name=request.POST["category"].split("-", 1)[-1]).first()
        payment = Payment.objects.filter(payment_type=request.POST["payment"]).first()
        incomeandexpense = IncomeAndExpense.objects.filter(income_type=request.POST["record_type"]).first()
        member = Member.objects.filter(user__username=request.user).first()
        new_receipt, created = Receipt.objects.update_or_create(member=member, id=receipt_id,
                                                                defaults={"money": request.POST["amount"],
                                                                          "remark": request.POST["memo"],
                                                                          "date": datetime.strptime(request.POST["date"], "%Y/%m/%d"),
                                                                          "subclassification": subclass, "payment": payment,
                                                                          "incomeandexpense":incomeandexpense,
                                                                          "member": member})

        if incomeandexpense.income_type == 'expense':
            receipt_list = Receipt.objects.filter(member=member, date=datetime.strptime(request.POST["date"], "%Y/%m/%d"),incomeandexpense__income_type="expense")
        else:
            receipt_list = Receipt.objects.filter(member=member, date=datetime.strptime(request.POST["date"], "%Y/%m/%d"), incomeandexpense__income_type="income")

        total_value = get_total(receipt_list)

        cost_rowcontent = ""
        if new_receipt.remark:
            cost_rowcontent += "<tr class='receipt{0}'><td><span class='glyphicon glyphicon-file text-success'></span>" \
                               "<a class='receipt_info' href='#'>{1}-{2}-{3}: {4}</a><span style='float: right; margin-right: 10px; " \
                               "color: #9D9D9D;'></span></td></tr>".format(
                new_receipt.id,
                new_receipt.subclassification.classification.classification_type.encode('utf-8'),
                new_receipt.subclassification.name.encode('utf-8'),
                new_receipt.remark.encode('utf-8'), new_receipt.money)
        else:
            cost_rowcontent += "<tr class='receipt{0}'><td><span class='glyphicon glyphicon-file text-success'></span>" \
                               "<a class='receipt_info' href='#'>{1}-{2}: {3}</a><span style='float: right; margin-right: 10px; " \
                               "color: #9D9D9D;'></span></td></tr>".format(
                new_receipt.id,
                new_receipt.subclassification.classification.classification_type.encode('utf-8'),
                new_receipt.subclassification.name.encode('utf-8'),
                new_receipt.money)

        classification = classNameTranslate_zhtwToen(request.POST["category"].split("-")[0].encode('utf-8'))
        category = Classification.objects.filter(classification_type=classification).first()
        category_budget_instance = Budget.objects.filter(classification=category, member=member).first()
        month_budget_instance = MonthBudget.objects.filter(member=member).first()

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
    # return 0


def delete_receipt(request):
    if request.method == 'POST':
        print(request.POST)
        receipt_id = int(request.POST["whick_receipt"].strip("receipt"))

        # delete receipt
        member = Member.objects.filter(user__username=request.user).first()
        receipt = Receipt.objects.filter(member=member, id=receipt_id).first()
        if receipt is not None:
            receipt.delete()

        # recount total
        receipt_type = receipt.incomeandexpense.income_type
        if receipt_type == 'expense':
            receipt_list = Receipt.objects.filter(member=member, date=date.today(),
                                                  incomeandexpense__income_type="expense")
        else:
            receipt_list = Receipt.objects.filter(member=member, date=date.today(),
                                                  incomeandexpense__income_type="income")
        total_value = get_total(receipt_list)

        message = {"total_value": total_value, "receipt_type": receipt_type}
    return HttpResponse(json.JSONEncoder().encode(message))


def modify_receipt(request):
    if request.method == 'POST':
        print(request.POST)
        receipt_id = int(request.POST["whick_receipt"].strip("receipt"))

        # delete receipt
        member = Member.objects.filter(user__username=request.user).first()
        receipt = Receipt.objects.filter(member=member, id=receipt_id).first()

        class_name = classNameTranslate_enTozhtw(receipt.subclassification.classification.classification_type)
        classification_detail = class_name.decode("utf8") + "-" + receipt.subclassification.name
        message = {"money": receipt.money, "remark": receipt.remark, "classification_detail": classification_detail,
                   "payment": receipt.payment.payment_type, "incomeandexpense": receipt.incomeandexpense.income_type,
                   "receipt_id": "receipt"+str(receipt.id)}
        print(message)
    return HttpResponse(json.JSONEncoder().encode(message))
    # return 0


def create_subClassification(request):
    if request.method == 'POST':
        print(request.POST)
        category = Classification.objects.filter(classification_type=request.POST["category"]).first()
        member = Member.objects.filter(user__username=request.user).first()
        new_subclass, created = SubClassification.objects.get_or_create(member=member, classification=category,
                                                                        name=request.POST["newSub"],
                                                                        defaults={'name': request.POST["newSub"]})
        if not new_subclass.exist:
            SubClassification.objects.filter(member=member, id=new_subclass.id).update(exist=True)
            created = True

        rowcontent = ""
        if created:
            rowcontent = '<button type="button" class="btn btn-link {0}" id="sec-category">' \
                         '{1}</button>'.format(new_subclass.classification.classification_type +
                                               "_list", new_subclass.name.encode('utf-8'))
        message = {"rowcontent": rowcontent, "created": created}
        return HttpResponse(json.JSONEncoder().encode(message))


def classNameTranslate_enTozhtw(name):
    return {
        'food': "food",
        'clothing': "clothing",
        'housing': "housing",
        'transportation': "transportation",
        'education': "education",
        'entertainment': "entertainment",
        'general_revenue': "general_revenue",
        'invest_revenue': "invest_revenue",
        'other_revenue': "other_revenue",
        'others': "others"
    }.get(name, "default")


def classNameTranslate_zhtwToen(name):
    return {
        'food': "food",
        'clothing': "clothing",
        'housing': "housing",
        'transportation': "transportation",
        'education': "education",
        'entertainment': "entertainment",
        'general_revenue': "general_revenue",
        'invest_revenue': "invest_revenue",
        'other_revenue': "other_revenue",
        'others': "others"
    }.get(name, "default")


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
                cost_rowcontent += "<tr class='receipt{0}'><td><span class='glyphicon glyphicon-file text-success'>" \
                                   "</span><a class='receipt_info' href='#'>{1}-{2}-{3}: {4}</a><span style='float: right; " \
                                   "margin-right: 10px; color: #9D9D9D;'></span></td></tr>".format(
                    receipt.id, className, receipt.subclassification.name.encode('utf-8'),
                    receipt.remark.encode('utf-8'), receipt.money)
            else:
                cost_rowcontent += "<tr class='receipt{0}'><td><span class='glyphicon glyphicon-file text-success'>" \
                                   "</span><a class='receipt_info' href='#'>{1}-{2}: {3}</a><span style='float: right; margin-right: 10px; " \
                                   "color: #9D9D9D;'></span></td></tr>".format(receipt.id, className,
                                                                               receipt.subclassification.name.encode('utf-8'),
                                                                               receipt.money)
        revenue_receipts = Receipt.objects.all().filter(date=date, member=member,
                                                        incomeandexpense__income_type="income")
        revenue_rowcontent = ""
        for receipt in revenue_receipts:
            className = classNameTranslate_enTozhtw(
                receipt.subclassification.classification.classification_type.encode('utf-8'))

            if receipt.remark:
                revenue_rowcontent += "<tr class='receipt{0}'><td><span class='glyphicon glyphicon-file text-success'></span><a class='receipt_info' href='#'>" \
                                      "{1}-{2}-{3}: {4}</a><span style='float: right; margin-right: 10px; color: #9D9D9D;'>" \
                                      "</span></td></tr>".format(receipt.id, className,
                                                                 receipt.subclassification.name.encode('utf-8'),
                                                                 receipt.remark.encode('utf-8'), receipt.money)
            else:
                revenue_rowcontent += "<tr class='receipt{0}'><td><span class='glyphicon glyphicon-file text-success'></span><a class='receipt_info' href='#'>" \
                                      "{1}-{2}: {3}</a><span style='float: right; margin-right: 10px; color: #9D9D9D;'>" \
                                      "</span></td></tr>".format(receipt.id, className,
                                                                 receipt.subclassification.name.encode('utf-8'),
                                                                 receipt.money)
                                                                 
        total_expense = get_total(cost_receipts)
        total_income = get_total(revenue_receipts)

        jsonResult = {'cost': cost_rowcontent, 'revenue': revenue_rowcontent, "total_expense": total_expense, "total_income": total_income}

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

        if not new_subclass.exist:
            SubClassification.objects.filter(member=member, id=new_subclass.id).update(exist=True)
            created = True

        rowcontent = ""
        if created:
            rowcontent = '<button type="button" class="btn btn-link btn-md sub-category">{0}</button>'.format(
                new_subclass.name.encode('utf-8'))
        message = {"rowcontent": rowcontent, "created": created}
        return HttpResponse(json.JSONEncoder().encode(message))


def delete_subClassification_in_settingPage(request):
    if request.method == 'POST':
        print(request.POST)
        member = Member.objects.filter(user__username=request.user).first()
        delsub = SubClassification.objects.filter(name=request.POST["name"], member=member).update(exist=False)
        return HttpResponse(delsub)


def budget_calculate(member):
    monthly_budget = MonthBudget.objects.filter(member=member).first()
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

    if (monthlyBudget > 0 and sumOfExpense > monthlyBudget):
        alertMessage = "Warning"
    elif (alertThreshold > 0 and sumOfExpense > alertThreshold):
        alertMessage = "Warning {0}".format(alertThreshold)
    else:
        alertMessage = "Normal"

    return alertMessage


def classification_budget_calculate(member, classification):
    c1 = Classification.objects.filter(classification_type=classification).first()
    budget_Object = Budget.objects.filter(member=member, classification=c1).first()

    currentDate = datetime.now()
    if (currentDate.month == 2):
        dayOfMonth = 28
    elif (currentDate.month == 4 or currentDate.month == 6 or currentDate.month == 9 or currentDate.month == 11):
        dayOfMonth = 30
    else:
        dayOfMonth = 31

    startDay = date(currentDate.year, currentDate.month, 1)
    lastDay = date(currentDate.year, currentDate.month, dayOfMonth)

    subClass_list = SubClassification.objects.filter(member=member, classification=c1)

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
        alertMessage = "Warning {0}".format(classification)
    elif (classBudgetThreshold > 0 and sumOfExpense > classBudgetThreshold):
        alertMessage = "Warning {0}  {1}".format(classification, classBudgetThreshold)
    else:
        alertMessage = "Normal"

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
            income = int(totalIncome['money__sum'])
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
            income = int(totalIncome['money__sum'])
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
            income = int(totalIncome['money__sum'])
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
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y/%m") - timedelta(days=365/12)
            else:
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y/%m") + timedelta(days=31)
            receipts = Receipt.objects.filter(date__year=target.year, date__month=target.month, member=member)
            targetOutput = datetime.strftime(target, '%Y/%m')
            totalCost = Receipt.objects.filter(member=member, date__year=target.year, date__month=target.month,
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date__year=target.year, date__month=target.month,
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))
        else:
            if request.POST["id"] == "btn_left":
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y")
                target = datetime(year=target.year - 1 , month=target.month, day=target.day)
            else:
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y")
                target = datetime(year=target.year + 1 , month=target.month, day=target.day)
            receipts = Receipt.objects.filter(date__year=target.year, member=member)
            targetOutput = datetime.strftime(target, '%Y')
            totalCost = Receipt.objects.filter(member=member, date__year=target.year,
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date__year=target.year,
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))

        if str(totalIncome['money__sum']) == "None":
            income = 0
        else:
            income = int(totalIncome['money__sum'])
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
            # print type(
            #     receipt.subclassification.classification.classification_type), receipt.subclassification.classification.classification_type
            # table += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td>" \
            #          "<td>{6}</td><td style='display: none'>{7}</td></tr>".format(
            #     receipt.subclassification.classification.classification_type.encode('utf-8'),
            #     receipt.subclassification.name.encode('utf-8'), receipt.remark.encode('utf-8'),
            #     receipt.incomeandexpense,
            #     receipt.payment, receipt.date, receipt.money, receipt.id)
            table += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td>" \
                     "<td>{6}</td><td style='width: 12%'>" \
                     "<button type='button' class='btn btn-danger btn-sm' value='{7}' title='delete'>" \
                     "delete</button>&nbsp;<button type='button' class='btn btn-danger btn-sm'" \
                     " value='{8}' title='modify'>modify</button></td></tr>".format(
                receipt.subclassification.classification.classification_type.encode('utf-8'),
                receipt.subclassification.name.encode('utf-8'), receipt.remark.encode('utf-8'),
                receipt.incomeandexpense,
                receipt.payment, receipt.date, receipt.money, receipt.id, receipt.id)
            # print table
        jsonResult = {'tableContent': table, 'title': targetOutput, 'balance': balance, 'income': income, 'cost': cost}
    return HttpResponse(json.JSONEncoder().encode(jsonResult))


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
                        payingTimeTitle = "This week"
                    else:
                        payingTimeTitle = "Next week"
                    weekday = {
                        1: "Monday",
                        2: "Tuesday",
                        3: "Wednesday",
                        4: "Thursday",
                        5: "Friday",
                        6: "Saturday",
                        7: "Sunday"
                    }
                    payingTimeContent = weekday.get(entry.expenditure_date, "Sunday")

                    message = "Notifications: {0} {1}{2}".format(entry.name.encode('utf-8'), payingTimeTitle,
                                                            payingTimeContent)
                    notification_list.append(message)

            else:
                if entry.reminder_date == date.today().day:
                    payingTimeTitle = ""
                    payingTimeContent = ""
                    if entry.expenditure_date >= entry.reminder_date:
                        payingTimeTitle = "This month"
                    else:
                        payingTimeTitle = "Next month"
                    payingTimeContent = str(entry.expenditure_date)

                    message = "Notifications: {0} {1}{2}".format(entry.name.encode('utf-8'), payingTimeTitle,
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

def filterdelrecord(request):
    if request.method == 'POST':
        print request.POST["id"],type(request.POST["id"])
        member = Member.objects.filter(user__username=request.user).first()
        receipt = Receipt.objects.filter(id=int(request.POST["id"]))
        if receipt is not None:
            print(receipt)
            receipt.delete()
            a = "OK"
            print a
        if request.POST["sign"] == "day":
            target = datetime.strptime(request.POST["pageHeader_date"], "%Y/%m/%d")
            new_receipts = Receipt.objects.filter(member=member, date=target)
            totalCost = Receipt.objects.filter(member=member, date=target,
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date=target,
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))
        elif request.POST["sign"] == "week":
            temp = request.POST["pageHeader_date"].split('-')
            print temp[0], temp[1]
            temp[0] = datetime.strptime(temp[0], "%Y/%m/%d")
            temp[1] = datetime.strptime(temp[1], "%Y/%m/%d")
            new_receipts = Receipt.objects.filter(member=member, date__range=[temp[0], temp[1]])
            totalCost = Receipt.objects.filter(member=member, date__range=[temp[0], temp[1]],
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date__range=[temp[0], temp[1]],
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))
        elif request.POST["sign"] == "month":
            target = datetime.strptime(request.POST["pageHeader_date"], "%Y/%m")
            new_receipts = Receipt.objects.filter(date__year=target.year, date__month=target.month, member=member)
            totalCost = Receipt.objects.filter(member=member, date__year=target.year, date__month=target.month,
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date__year=target.year, date__month=target.month,
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))
        else:
            target = datetime.strptime(request.POST["pageHeader_date"], "%Y")
            new_receipts = Receipt.objects.filter(date__year=target.year, member=member)
            targetOutput = datetime.strftime(target, '%Y')
            totalCost = Receipt.objects.filter(member=member, date__year=target.year,
                                               incomeandexpense__income_type="expense").aggregate(Sum('money'))
            totalIncome = Receipt.objects.filter(member=member, date__year=target.year,
                                                 incomeandexpense__income_type="income").aggregate(Sum('money'))
        if str(totalIncome['money__sum']) == "None":
            income = 0
        else:
            income = int(totalIncome['money__sum'])
        if str(totalCost['money__sum']) == "None":
            cost = 0
        else:
            cost = int(totalCost['money__sum'])
        print income, cost
        balance = income - cost
        print balance, type(balance)
        table = ""
        print len(new_receipts), type(new_receipts)
        for receipt in new_receipts:
            table += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td>" \
                     "<td>{6}</td><td style='width: 12%'>" \
                     "<button type='button' class='btn btn-danger btn-sm' value='{7}' title='delete'>" \
                     "delete</button>&nbsp;<button type='button' class='btn btn-danger btn-sm'" \
                     " value='{8}' title='modify'>modify</button></td></tr>".format(
                receipt.subclassification.classification.classification_type.encode('utf-8'),
                receipt.subclassification.name.encode('utf-8'), receipt.remark.encode('utf-8'),
                receipt.incomeandexpense,
                receipt.payment, receipt.date, receipt.money, receipt.id, receipt.id)
        jsonResult = {'tableContent': table, 'balance': balance, 'income': income, 'cost': cost, 'answer': a}
    return HttpResponse(json.JSONEncoder().encode(jsonResult))


def backwardchart(request):
    if request.method == 'POST':
        print(request.POST)
        print type(request.POST["pageHeader_date"]), request.POST["sign"]
        member = Member.objects.filter(user__username=request.user).first()
        
        if request.POST["sign"] == "week":
            temp = request.POST["pageHeader_date"].split('-')
            #print temp[0], temp[1]
            temp[0] = datetime.strptime(temp[0], "%Y/%m/%d")
            temp[1] = datetime.strptime(temp[1], "%Y/%m/%d")
            if request.POST["id"] == "btn_left":
                targetStart = temp[0] - timedelta(days=7)
                targetEnd = temp[1] - timedelta(days=7)
            else:
                targetStart = temp[0] + timedelta(days=7)
                targetEnd = temp[1] + timedelta(days=7)

            targetOutput = datetime.strftime(targetStart, '%Y/%m/%d') + "-" + datetime.strftime(targetEnd, '%Y/%m/%d')
            print targetOutput
            cost_sun = Receipt.objects.filter(member=member, date=targetStart, incomeandexpense__income_type="expense").aggregate(Sum('money'))
            cost_mon = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=1), incomeandexpense__income_type="expense").aggregate(Sum('money'))
            cost_tue = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=2), incomeandexpense__income_type="expense").aggregate(Sum('money'))
            cost_wed = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=3), incomeandexpense__income_type="expense").aggregate(Sum('money'))
            cost_thu = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=4), incomeandexpense__income_type="expense").aggregate(Sum('money'))
            cost_fri = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=5), incomeandexpense__income_type="expense").aggregate(Sum('money'))
            cost_sat = Receipt.objects.filter(member=member, date=targetEnd, incomeandexpense__income_type="expense").aggregate(Sum('money'))
            if str(cost_sun['money__sum']) == "None":
                cost_sun = 0
            else:
                cost_sun = int(cost_sun['money__sum'])
            if str(cost_mon['money__sum']) == "None":
                cost_mon = 0
            else:
                cost_mon = int(cost_mon['money__sum'])
            if str(cost_tue['money__sum']) == "None":
                cost_tue = 0
            else:
                cost_tue = int(cost_tue['money__sum'])
            if str(cost_wed['money__sum']) == "None":
                cost_wed = 0
            else:
                cost_wed = int(cost_wed['money__sum'])
            if str(cost_thu['money__sum']) == "None":
                cost_thu = 0
            else:
                cost_thu = int(cost_thu['money__sum'])
            if str(cost_fri['money__sum']) == "None":
                cost_fri = 0
            else:
                cost_fri = int(cost_fri['money__sum'])
            if str(cost_sat['money__sum']) == "None":
                cost_sat = 0
            else:
                cost_sat = int(cost_sat['money__sum'])

            income_sun = Receipt.objects.filter(member=member, date=targetStart, incomeandexpense__income_type="income").aggregate(Sum('money'))
            income_mon = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=1), incomeandexpense__income_type="income").aggregate(Sum('money'))
            income_tue = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=2), incomeandexpense__income_type="income").aggregate(Sum('money'))
            income_wed = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=3), incomeandexpense__income_type="income").aggregate(Sum('money'))
            income_thu = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=4), incomeandexpense__income_type="income").aggregate(Sum('money'))
            income_fri = Receipt.objects.filter(member=member, date=targetStart+timedelta(days=5), incomeandexpense__income_type="income").aggregate(Sum('money'))
            income_sat = Receipt.objects.filter(member=member, date=targetEnd, incomeandexpense__income_type="income").aggregate(Sum('money'))
            if str(income_sun['money__sum']) == "None":
                income_sun = 0
            else:
                income_sun = int(income_sun['money__sum'])
            if str(income_mon['money__sum']) == "None":
                income_mon = 0
            else:
                income_mon = int(income_mon['money__sum'])
            if str(income_tue['money__sum']) == "None":
                income_tue = 0
            else:
                income_tue = int(income_tue['money__sum'])
            if str(income_wed['money__sum']) == "None":
                income_wed = 0
            else:
                income_wed = int(income_wed['money__sum'])
            if str(income_thu['money__sum']) == "None":
                income_thu = 0
            else:
                income_thu = int(income_thu['money__sum'])
            if str(income_fri['money__sum']) == "None":
                income_fri = 0
            else:
                income_fri = int(income_fri['money__sum'])
            if str(income_sat['money__sum']) == "None":
                income_sat = 0
            else:
                income_sat = int(income_sat['money__sum'])


            data = {
                'week': ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', ],
                'dollar': [cost_sun, cost_mon, cost_tue, cost_wed, cost_thu, cost_fri, cost_sat, income_sun, income_mon, income_tue, income_wed, income_thu, income_fri, income_sat],
                'origin':['expense','expense','expense','expense','expense','expense','expense',
                      'income','income','income','income','income','income','income']
            }
            bar2 = Bar(data, label=CatAttr(columns=['week'], sort=False,), values='dollar', plot_height=400, responsive=True, group='origin')
            script2, div2 = components(bar2)

            s = """Date,Close
            """+datetime.strftime(targetStart, '%Y/%m/%d')+""","""+str(cost_sun)+"""
            """+datetime.strftime(targetStart+timedelta(days=1), '%Y/%m/%d')+""","""+str(cost_mon)+"""
            """+datetime.strftime(targetStart+timedelta(days=2), '%Y/%m/%d')+""","""+str(cost_tue)+"""
            """+datetime.strftime(targetStart+timedelta(days=3), '%Y/%m/%d')+""","""+str(cost_wed)+"""
            """+datetime.strftime(targetStart+timedelta(days=4), '%Y/%m/%d')+""","""+str(cost_thu)+"""
            """+datetime.strftime(targetStart+timedelta(days=5), '%Y/%m/%d')+""","""+str(cost_fri)+"""
            """+datetime.strftime(targetEnd, '%Y/%m/%d')+""","""+str(cost_sat)+""" """
            AAPL = pd.read_csv(StringIO(s),parse_dates=['Date'])
            p = figure(plot_height=400, responsive=True, x_axis_type="datetime")
            p.line(AAPL['Date'], AAPL['Close'], color='navy', alpha=0.5)
            p.legend.location = "top_left"
            p.grid.grid_line_alpha=0
            p.xaxis.axis_label = 'Date'
            p.yaxis.axis_label = 'Dollar'
            p.ygrid.band_fill_color="olive"
            p.ygrid.band_fill_alpha = 0.1
            script, div = components(p)
        elif request.POST["sign"] == "month":
            time = request.POST["pageHeader_date"]
            if request.POST["id"] == "btn_left":
                targetTime = datetime.strptime(time, "%Y/%m") - timedelta(days=365/12)
            else:
                targetTime = datetime.strptime(time, "%Y/%m") + timedelta(days=31)
            targetOutput = datetime.strftime(targetTime, '%Y/%m')
            day = int(datetime.strftime(targetTime, "%d"))
            mon = int(datetime.strftime(targetTime, "%m"))
            yr = int(datetime.strftime(targetTime, "%Y"))
            if (mon == 1) or (mon == 3) or (mon == 5) or (mon == 7) or (mon == 8) or (mon == 10) or (mon == 12):
                monsday = 31
            elif (yr % 4 == 0) and (mon == 2):
                monsday = 29
            elif (yr % 4 != 0) and (mon == 2):
                monsday = 28
            else:
                monsday = 30
            startDay = targetTime - timedelta(days=day-1)
            list_cost=[]
            for i in range(monsday):
                cost = Receipt.objects.filter(member=member, date=startDay+timedelta(days=i), incomeandexpense__income_type="expense").aggregate(Sum('money'))
                if str(cost['money__sum']) == "None":
                    cost = 0
                else:
                    cost = cost['money__sum']
                list_cost.append(cost)

            list_income=[]
            for i in range(monsday):
                income = Receipt.objects.filter(member=member, date=startDay+timedelta(days=i), incomeandexpense__income_type="income").aggregate(Sum('money'))
                if str(income['money__sum']) == "None":
                    income = 0
                else:
                    income = income['money__sum']
                list_income.append(income)

            mon_origin_cost=[]
            mon_origin_income=[]
            mon_day=[]
            mon_day_double=[]
            mon_dollar=[]
            for i in range(monsday):
                mon_day.append(i+1)
                mon_origin_cost.append('expense')
                mon_origin_income.append('income')
            list_cost_income = list_cost
            list_cost_income.extend(list_income)
            mon_day.extend(mon_day)
            mon_origin = mon_origin_cost
            mon_origin.extend(mon_origin_income)
            print(mon_day)
            print(list_cost_income)
            print(mon_origin)
            data = {
                'mon': mon_day,
                'dollar': list_cost_income,
                'origin': mon_origin
            }
            bar2 = Bar(data, label=CatAttr(columns=['mon'], sort=False,), values='dollar', plot_height=400, responsive=True, group='origin')
            script2, div2 = components(bar2)

            s = """Date,Cost
            """
            for i in range(monsday):
                s = s + datetime.strftime(startDay+timedelta(days=i), '%Y/%m/%d')+","+str(list_cost[i])+"""
                """

            print(s)
            AAPL = pd.read_csv(StringIO(s),parse_dates=['Date'])
            print(AAPL)
            p = figure(plot_height=400, responsive=True, x_axis_type="datetime")
            p.line(AAPL['Date'], AAPL['Cost'], color='navy', alpha=0.5)
            p.legend.location = "top_left"
            p.grid.grid_line_alpha=0
            p.xaxis.axis_label = 'Date'
            p.yaxis.axis_label = 'Dollar'
            p.ygrid.band_fill_color="olive"
            p.ygrid.band_fill_alpha = 0.1
            script, div = components(p)
        elif request.POST["sign"] == "year":
            if request.POST["id"] == "btn_left":
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y")
                target = datetime(year=target.year - 1 , month=target.month, day=target.day)
            else:
                target = datetime.strptime(request.POST["pageHeader_date"], "%Y")
                target = datetime(year=target.year + 1 , month=target.month, day=target.day)
            targetOutput = datetime.strftime(target, '%Y')
            currentDate = target
            list_cost=[]
            for i in range(12):
                cost = Receipt.objects.filter(member=member, date__year=currentDate.year, date__month=(i+1), incomeandexpense__income_type="expense").aggregate(Sum('money'))
                if str(cost['money__sum']) == "None":
                    cost = 0
                else:
                    cost = cost['money__sum']
                list_cost.append(cost)

            list_income=[]
            for i in range(12):
                income = Receipt.objects.filter(member=member, date__year=currentDate.year, date__month=(i+1), incomeandexpense__income_type="income").aggregate(Sum('money'))
                if str(income['money__sum']) == "None":
                    income = 0
                else:
                    income = income['money__sum']
                list_income.append(income)

            yr_origin_cost=[]
            yr_origin_income=[]
            yr_day=[]
            yr_day_double=[]
            yr_dollar=[]
            for i in range(12):
                yr_day.append(i+1)
                yr_origin_cost.append('expense')
                yr_origin_income.append('income')
            list_cost_income = list_cost
            list_cost_income.extend(list_income)
            yr_day.extend(yr_day)
            yr_origin = yr_origin_cost
            yr_origin.extend(yr_origin_income)
            print(yr_day)
            print(list_cost_income)
            print(yr_origin)
            data = {
                'year': yr_day,
                'dollar': list_cost_income,
                'origin': yr_origin
            }
            bar2 = Bar(data, label=CatAttr(columns=['year'], sort=False,), values='dollar', plot_height=400, responsive=True, group='origin')
            script2, div2 = components(bar2)

            yr = int(datetime.strftime(currentDate, "%Y"))
            print(yr)
            yr_date = date(year=yr, month=1, day=1)
            s = """Date,Cost
            """
            while yr_date != date(year=yr, month=12, day=31):
                yr_cost = Receipt.objects.filter(member=member, date=yr_date, incomeandexpense__income_type="expense").aggregate(Sum('money'))
                if str(yr_cost['money__sum']) == "None":
                    yr_cost = 0
                else:
                    yr_cost = yr_cost['money__sum']
                s = s + datetime.strftime(yr_date, '%Y/%m/%d')+","+str(yr_cost)+"""
                """
                yr_date = yr_date + timedelta(days=1)
        

            AAPL = pd.read_csv(StringIO(s),parse_dates=['Date'])
            p = figure(plot_height=400, responsive=True, x_axis_type="datetime")
            p.line(AAPL['Date'], AAPL['Cost'], color='navy', alpha=0.5)
            p.legend.location = "top_left"
            p.grid.grid_line_alpha=0
            p.xaxis.axis_label = 'Date'
            p.yaxis.axis_label = 'Dollar'
            p.ygrid.band_fill_color="olive"
            p.ygrid.band_fill_alpha = 0.1
            script, div = components(p)

        jsonResult = { 'title': targetOutput, "the_script": script, "the_div": div, "script_bar": script2, "div_bar": div2}
    return HttpResponse(json.JSONEncoder().encode(jsonResult))



def get_week_chart(request):
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
        week = datetime.strftime(startDay, '%Y/%m/%d') + "-" + datetime.strftime(endDay, '%Y/%m/%d')
        cost_sun = Receipt.objects.filter(member=member, date=startDay, incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_mon = Receipt.objects.filter(member=member, date=startDay+timedelta(days=1), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_tue = Receipt.objects.filter(member=member, date=startDay+timedelta(days=2), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_wed = Receipt.objects.filter(member=member, date=startDay+timedelta(days=3), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_thu = Receipt.objects.filter(member=member, date=startDay+timedelta(days=4), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_fri = Receipt.objects.filter(member=member, date=startDay+timedelta(days=5), incomeandexpense__income_type="expense").aggregate(Sum('money'))
        cost_sat = Receipt.objects.filter(member=member, date=endDay, incomeandexpense__income_type="expense").aggregate(Sum('money'))
        if str(cost_sun['money__sum']) == "None":
            cost_sun = 0
        else:
            cost_sun = int(cost_sun['money__sum'])
        if str(cost_mon['money__sum']) == "None":
            cost_mon = 0
        else:
            cost_mon = int(cost_mon['money__sum'])
        if str(cost_tue['money__sum']) == "None":
            cost_tue = 0
        else:
            cost_tue = int(cost_tue['money__sum'])
        if str(cost_wed['money__sum']) == "None":
            cost_wed = 0
        else:
            cost_wed = int(cost_wed['money__sum'])
        if str(cost_thu['money__sum']) == "None":
            cost_thu = 0
        else:
            cost_thu = int(cost_thu['money__sum'])
        if str(cost_fri['money__sum']) == "None":
            cost_fri = 0
        else:
            cost_fri = int(cost_fri['money__sum'])
        if str(cost_sat['money__sum']) == "None":
            cost_sat = 0
        else:
            cost_sat = int(cost_sat['money__sum'])

        income_sun = Receipt.objects.filter(member=member, date=startDay, incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_mon = Receipt.objects.filter(member=member, date=startDay+timedelta(days=1), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_tue = Receipt.objects.filter(member=member, date=startDay+timedelta(days=2), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_wed = Receipt.objects.filter(member=member, date=startDay+timedelta(days=3), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_thu = Receipt.objects.filter(member=member, date=startDay+timedelta(days=4), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_fri = Receipt.objects.filter(member=member, date=startDay+timedelta(days=5), incomeandexpense__income_type="income").aggregate(Sum('money'))
        income_sat = Receipt.objects.filter(member=member, date=endDay, incomeandexpense__income_type="income").aggregate(Sum('money'))
        if str(income_sun['money__sum']) == "None":
            income_sun = 0
        else:
            income_sun = int(income_sun['money__sum'])
        if str(income_mon['money__sum']) == "None":
            income_mon = 0
        else:
            income_mon = int(income_mon['money__sum'])
        if str(income_tue['money__sum']) == "None":
            income_tue = 0
        else:
            income_tue = int(income_tue['money__sum'])
        if str(income_wed['money__sum']) == "None":
            income_wed = 0
        else:
            income_wed = int(income_wed['money__sum'])
        if str(income_thu['money__sum']) == "None":
            income_thu = 0
        else:
            income_thu = int(income_thu['money__sum'])
        if str(income_fri['money__sum']) == "None":
            income_fri = 0
        else:
            income_fri = int(income_fri['money__sum'])
        if str(income_sat['money__sum']) == "None":
            income_sat = 0
        else:
            income_sat = int(income_sat['money__sum'])

        data = {
            'week': ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', ],
            'dollar': [cost_sun, cost_mon, cost_tue, cost_wed, cost_thu, cost_fri, cost_sat, income_sun, income_mon, income_tue, income_wed, income_thu, income_fri, income_sat],
            'origin':['expense','expense','expense','expense','expense','expense','expense',
                      'income','income','income','income','income','income','income']
        }
        bar2 = Bar(data, label=CatAttr(columns=['week'], sort=False,), values='dollar', plot_height=400, responsive=True, group='origin')
        script2, div2 = components(bar2)

        s = """Date,Close
        """+datetime.strftime(startDay, '%Y/%m/%d')+""","""+str(cost_sun)+"""
        """+datetime.strftime(startDay+timedelta(days=1), '%Y/%m/%d')+""","""+str(cost_mon)+"""
        """+datetime.strftime(startDay+timedelta(days=2), '%Y/%m/%d')+""","""+str(cost_tue)+"""
        """+datetime.strftime(startDay+timedelta(days=3), '%Y/%m/%d')+""","""+str(cost_wed)+"""
        """+datetime.strftime(startDay+timedelta(days=4), '%Y/%m/%d')+""","""+str(cost_thu)+"""
        """+datetime.strftime(startDay+timedelta(days=5), '%Y/%m/%d')+""","""+str(cost_fri)+"""
        """+datetime.strftime(endDay, '%Y/%m/%d')+""","""+str(cost_sat)+""" """
        print(s)
        AAPL = pd.read_csv(StringIO(s),parse_dates=['Date'])
        print(AAPL)
        # create a new plot with a datetime axis type
        p = figure(plot_height=400, responsive=True, x_axis_type="datetime")
        p.line(AAPL['Date'], AAPL['Close'], color='navy', alpha=0.5)
        p.legend.location = "top_left"
        p.grid.grid_line_alpha=0
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Dollar'
        p.ygrid.band_fill_color="olive"
        p.ygrid.band_fill_alpha = 0.1
        script, div = components(p)

        jsonResult = {"title": week, "the_script": script, "the_div": div, "script_bar": script2, "div_bar": div2 }
    return HttpResponse(json.JSONEncoder().encode(jsonResult))

def get_mon_chart(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        currentDate = datetime.now()
        print(currentDate)
        title = datetime.strftime(currentDate, "%Y/%m")
        day = int(datetime.strftime(currentDate, "%d"))
        mon = int(datetime.strftime(currentDate, "%m"))
        yr = int(datetime.strftime(currentDate, "%Y"))
        if (mon == 1) or (mon == 3) or (mon == 5) or (mon == 7) or (mon == 8) or (mon == 10) or (mon == 12):
            monsday = 31
        elif (yr % 4 == 0) and (mon == 2):
            monsday = 29
        elif (yr % 4 != 0) and (mon == 2):
            monsday = 28
        else:
            monsday = 30
        startDay = currentDate - timedelta(days=day-1)
        list_cost=[]
        for i in range(monsday):
            cost = Receipt.objects.filter(member=member, date=startDay+timedelta(days=i), incomeandexpense__income_type="expense").aggregate(Sum('money'))
            if str(cost['money__sum']) == "None":
                cost = 0
            else:
                cost = cost['money__sum']
            list_cost.append(cost)

        list_income=[]
        for i in range(monsday):
            income = Receipt.objects.filter(member=member, date=startDay+timedelta(days=i), incomeandexpense__income_type="income").aggregate(Sum('money'))
            if str(income['money__sum']) == "None":
                income = 0
            else:
                income = income['money__sum']
            list_income.append(income)

        mon_origin_cost=[]
        mon_origin_income=[]
        mon_day=[]
        mon_day_double=[]
        mon_dollar=[]
        for i in range(monsday):
            mon_day.append(i+1)
            mon_origin_cost.append('expense')
            mon_origin_income.append('income')
        list_cost_income = list_cost
        list_cost_income.extend(list_income)
        mon_day.extend(mon_day)
        mon_origin = mon_origin_cost
        mon_origin.extend(mon_origin_income)
        print(mon_day)
        print(list_cost_income)
        print(mon_origin)
        data = {
            'mon': mon_day,
            'dollar': list_cost_income,
            'origin': mon_origin
        }
        bar2 = Bar(data, label=CatAttr(columns=['mon'], sort=False,), values='dollar', plot_height=400, responsive=True, group='origin')
        script2, div2 = components(bar2)

        s = """Date,Cost
        """
        for i in range(monsday):
            s = s + datetime.strftime(startDay+timedelta(days=i), '%Y/%m/%d')+","+str(list_cost[i])+"""
            """

        print(s)
        AAPL = pd.read_csv(StringIO(s),parse_dates=['Date'])
        print(AAPL)
        p = figure(plot_height=400, responsive=True, x_axis_type="datetime")
        p.line(AAPL['Date'], AAPL['Cost'], color='navy', alpha=0.5)
        p.legend.location = "top_left"
        p.grid.grid_line_alpha=0
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Dollar'
        p.ygrid.band_fill_color="olive"
        p.ygrid.band_fill_alpha = 0.1
        script, div = components(p)

        jsonResult = { 'title': title, "the_script": script, "the_div": div, "script_bar": script2, "div_bar": div2}
    return HttpResponse(json.JSONEncoder().encode(jsonResult))


def get_yr_chart(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        currentDate = datetime.now()
        print(currentDate)
        title = datetime.strftime(currentDate, "%Y")
        list_cost=[]
        for i in range(12):
            cost = Receipt.objects.filter(member=member, date__year=currentDate.year, date__month=(i+1), incomeandexpense__income_type="expense").aggregate(Sum('money'))
            if str(cost['money__sum']) == "None":
                cost = 0
            else:
                cost = cost['money__sum']
            list_cost.append(cost)

        list_income=[]
        for i in range(12):
            income = Receipt.objects.filter(member=member, date__year=currentDate.year, date__month=(i+1), incomeandexpense__income_type="income").aggregate(Sum('money'))
            if str(income['money__sum']) == "None":
                income = 0
            else:
                income = income['money__sum']
            list_income.append(income)

        yr_origin_cost=[]
        yr_origin_income=[]
        yr_day=[]
        yr_day_double=[]
        yr_dollar=[]
        for i in range(12):
            yr_day.append(i+1)
            yr_origin_cost.append('expense')
            yr_origin_income.append('income')
        list_cost_income = list_cost
        list_cost_income.extend(list_income)
        yr_day.extend(yr_day)
        yr_origin = yr_origin_cost
        yr_origin.extend(yr_origin_income)
        print(yr_day)
        print(list_cost_income)
        print(yr_origin)
        data = {
            'year': yr_day,
            'dollar': list_cost_income,
            'origin': yr_origin
        }
        bar2 = Bar(data, label=CatAttr(columns=['year'], sort=False,), values='dollar', plot_height=400, responsive=True, group='origin')
        script2, div2 = components(bar2)

        yr = int(datetime.strftime(currentDate, "%Y"))
        print(yr)
        yr_date = date(year=yr, month=1, day=1)
        s = """Date,Cost
        """
        while yr_date != date(year=yr, month=12, day=31):
            yr_cost = Receipt.objects.filter(member=member, date=yr_date, incomeandexpense__income_type="expense").aggregate(Sum('money'))
            if str(yr_cost['money__sum']) == "None":
                yr_cost = 0
            else:
                yr_cost = yr_cost['money__sum']
            s = s + datetime.strftime(yr_date, '%Y/%m/%d')+","+str(yr_cost)+"""
            """
            yr_date = yr_date + timedelta(days=1)
        

        AAPL = pd.read_csv(StringIO(s),parse_dates=['Date'])
        p = figure(plot_height=400, responsive=True, x_axis_type="datetime")
        p.line(AAPL['Date'], AAPL['Cost'], color='navy', alpha=0.5)
        p.legend.location = "top_left"
        p.grid.grid_line_alpha=0
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Dollar'
        p.ygrid.band_fill_color="olive"
        p.ygrid.band_fill_alpha = 0.1
        script, div = components(p)

        jsonResult = { 'title': title, "the_script": script, "the_div": div, "script_bar": script2, "div_bar": div2}
    return HttpResponse(json.JSONEncoder().encode(jsonResult))



def get_category_chart(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        currentDate = datetime.now()
        print(currentDate)
        title = datetime.strftime(currentDate, "%Y")
        list_cost=[]
        list_cost_classification=[]
        list_income_classification=[]
        list_cost_classification_default=['food','clothing','housing','transportation','education','entertainment', 'others']
        list_income_classification_default=['general_revenue','invest_revenue','other_revenue']
        for i in range(7):
            cost = Receipt.objects.filter(member=member, subclassification__classification__classification_type=list_cost_classification_default[i], incomeandexpense__income_type="expense").aggregate(Sum('money'))
            if str(cost['money__sum']) == "None":
                cost = 0
            else:
                cost = cost['money__sum']
                list_cost.append(cost)
                list_cost_classification.append(list_cost_classification_default[i])
        if len(list_cost_classification) == 0:
            list_cost_classification.append("none")
            list_cost.append(0)
        list_income=[]
        for i in range(3):
            income = Receipt.objects.filter(member=member, subclassification__classification__classification_type=list_income_classification_default[i], incomeandexpense__income_type="income").aggregate(Sum('money'))
            if str(income['money__sum']) == "None":
                income = 0
            else:
                income = income['money__sum']
                list_income.append(income)
                list_income_classification.append(list_income_classification_default[i])
        if len(list_income_classification) == 0:
            list_income_classification.append("none")
            list_income.append(0)
        ####Pie chart####
        #expense
        data3 = pd.Series(list_cost, index=list_cost_classification)
        pie_chart = Donut(data3)
        pie_chart.title.text = "Expense"
        pie_chart.height=430
        pie_chart.width=430
        # pie_chart.sizing_mode="scale_width"
        script3, div3 = components(pie_chart)

        #income
        data4 = pd.Series(list_income, index=list_income_classification)
        pie_chart_in = Donut(data4)
        pie_chart_in.title.text = "Income"
        pie_chart_in.height=430
        pie_chart_in.width=430
        # pie_chart_in.sizing_mode="scale_width"
        script4, div4 = components(pie_chart_in)

        #expense
        name = SubClassification.objects.filter(member=member)
        #print(name)
        sub_list_name=[]
        sub_list=[]
        for i in range(len(name)):
            #print(name[i].name)
            sub = Receipt.objects.filter(member=member, subclassification=name[i], incomeandexpense__income_type="expense").aggregate(Sum('money'))
            if str(sub['money__sum']) == "None":
                sub = 0
            else:
                sub = sub['money__sum']
                sub_list_name.append(name[i].name.encode('utf-8'))
                sub_list.append(sub)
        if len(sub_list_name) == 0:
            sub_list_name.append("none")
            sub_list.append(0)
        print(sub_list)
        print(sub_list_name)
        data5 = pd.Series(sub_list, index=sub_list_name)
        pie_chart_sub = Donut(data5)
        pie_chart_sub.title.text = "Subclass Expense"
        pie_chart_sub.height=430
        pie_chart_sub.width=430
        # pie_chart_sub.sizing_mode="scale_width"
        script5, div5 = components(pie_chart_sub)

        #income
        name_in = SubClassification.objects.filter(member=member)
        #print(name)
        sub_list_name_in=[]
        sub_list_in=[]
        for i in range(len(name_in)):
            #print(name[i].name)
            sub_in = Receipt.objects.filter(member=member, subclassification=name_in[i], incomeandexpense__income_type="income").aggregate(Sum('money'))
            if str(sub_in['money__sum']) == "None":
                sub_in = 0
            else:
                sub_in = sub_in['money__sum']
                sub_list_name_in.append(name_in[i].name.encode('utf-8'))
                sub_list_in.append(sub_in)
        if len(sub_list_name_in) == 0:
            sub_list_name_in.append("none")
            sub_list_in.append(0)
        data6 = pd.Series(sub_list_in, index=sub_list_name_in)
        pie_chart_sub_in = Donut(data6)
        pie_chart_sub_in.title.text = "Subclass Income"
        pie_chart_sub_in.height=430
        pie_chart_sub_in.width=430
        # pie_chart_sub_in.sizing_mode="scale_width"
        script6, div6 = components(pie_chart_sub_in)


        jsonResult = { 'title': title, "script_pie": script3, "div_pie": div3, "script_pie_in": script4, "div_pie_in": div4, "script_pie_sub": script5, "div_pie_sub": div5, "script_pie_sub_in": script6, "div_pie_sub_in": div6}
    return HttpResponse(json.JSONEncoder().encode(jsonResult))


def get_specific_category_chart(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        member = Member.objects.filter(user__username=request.user).first()
        currentDate = datetime.strptime(request.POST["pageHeader_date"],'%Y/%m')
        #print(currentDate)
        list_cost=[]
        list_cost_classification=[]
        list_income_classification=[]
        list_cost_classification_default=['food','clothing','housing','transportation','education','entertainment', 'others']
        list_income_classification_default=['general_revenue','invest_revenue','other_revenue']
        for i in range(7):
            cost = Receipt.objects.filter(member=member, date__year=currentDate.year, date__month=currentDate.month, subclassification__classification__classification_type=list_cost_classification_default[i], incomeandexpense__income_type="expense").aggregate(Sum('money'))
            if str(cost['money__sum']) == "None":
                cost = 0
            else:
                cost = cost['money__sum']
                list_cost.append(cost)
                list_cost_classification.append(list_cost_classification_default[i])
        if len(list_cost_classification) == 0:
            list_cost_classification.append("none")
            list_cost.append(0)
        list_income=[]
        for i in range(3):
            income = Receipt.objects.filter(member=member, date__year=currentDate.year, date__month=currentDate.month, subclassification__classification__classification_type=list_income_classification_default[i], incomeandexpense__income_type="income").aggregate(Sum('money'))
            if str(income['money__sum']) == "None":
                income = 0
            else:
                income = income['money__sum']
                list_income.append(income)
                list_income_classification.append(list_income_classification_default[i])
        if len(list_income_classification) == 0:
            list_income_classification.append("none")
            list_income.append(0)
        
        ####Pie chart####
        #expense
        data3 = pd.Series(list_cost, index=list_cost_classification)
        pie_chart = Donut(data3)
        pie_chart.title.text = "Expense"
        pie_chart.height=430
        pie_chart.width=430
        # pie_chart.sizing_mode="scale_width"
        script3, div3 = components(pie_chart)

        #income
        data4 = pd.Series(list_income, index=list_income_classification)
        pie_chart_in = Donut(data4)
        pie_chart_in.title.text = "Income"
        pie_chart_in.height=430
        pie_chart_in.width=430
        # pie_chart_in.sizing_mode="scale_width"
        script4, div4 = components(pie_chart_in)

        #expense
        name = SubClassification.objects.filter(member=member)
        #print(name)
        sub_list_name=[]
        sub_list=[]
        for i in range(len(name)):
            #print(name[i].name)
            sub = Receipt.objects.filter(member=member, date__year=currentDate.year, date__month=currentDate.month, subclassification=name[i], incomeandexpense__income_type="expense").aggregate(Sum('money'))
            if str(sub['money__sum']) == "None":
                sub = 0
            else:
                sub = sub['money__sum']
                sub_list_name.append(name[i].name.encode('utf-8'))
                sub_list.append(sub)
        if len(sub_list_name) == 0:
            sub_list_name.append("none")
            sub_list.append(0)
        print(sub_list)
        print(sub_list_name)
        data5 = pd.Series(sub_list, index=sub_list_name)
        pie_chart_sub = Donut(data5)
        pie_chart_sub.title.text = "Subclass Expense"
        pie_chart_sub.height=430
        pie_chart_sub.width=430
        # pie_chart_sub.sizing_mode="scale_width"
        script5, div5 = components(pie_chart_sub)

        #income
        name_in = SubClassification.objects.filter(member=member)
        #print(name)
        sub_list_name_in=[]
        sub_list_in=[]
        for i in range(len(name_in)):
            #print(name[i].name)
            sub_in = Receipt.objects.filter(member=member, date__year=currentDate.year, date__month=currentDate.month, subclassification=name_in[i], incomeandexpense__income_type="income").aggregate(Sum('money'))
            if str(sub_in['money__sum']) == "None":
                sub_in = 0
            else:
                sub_in = sub_in['money__sum']
                sub_list_name_in.append(name_in[i].name.encode('utf-8'))
                sub_list_in.append(sub_in)
        if len(sub_list_name_in) == 0:
            sub_list_name_in.append("none")
            sub_list_in.append(0)
        data6 = pd.Series(sub_list_in, index=sub_list_name_in)
        pie_chart_sub_in = Donut(data6)
        pie_chart_sub_in.title.text = "Subclass Income"
        pie_chart_sub_in.height=430
        pie_chart_sub_in.width=430
        # pie_chart_sub_in.sizing_mode="scale_width"
        script6, div6 = components(pie_chart_sub_in)


        jsonResult = { "script_pie": script3, "div_pie": div3, "script_pie_in": script4, "div_pie_in": div4, "script_pie_sub": script5, "div_pie_sub": div5, "script_pie_sub_in": script6, "div_pie_sub_in": div6}
    return HttpResponse(json.JSONEncoder().encode(jsonResult))

