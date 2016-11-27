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

def createReceipt(request):
	member = request.POST['user']
	#get user?
	money = request.POST['amount']
	remark = request.POST['memo']
	date = request.POST['datepicker1']
	subclassification = request.POST['costCategory'] 
	#only need sub category
	payment = request.POST['payment']
	if payment == 'cash':
		payment = 'CR'
	elif payment == 'credit-card':
		payment = 'CA'
	elif payment == 'other':
		payment = 'OT'
	
	incomeandexpense = request.POST['recordType']
	if incomeandexpense == 'cost':
		incomeandexpense = 'EX'
	elif incomeandexpense == 'revenue':
		incomeandexpense = 'IN'

	account.objects.create(member=member, usermoney=money, remark=remark, date=date, subclassification=subclassification, payment=payment, incomeandexpense=incomeandexpense)
	return render(request, 'dashboard.html', {})

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

    