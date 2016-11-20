from __future__ import unicode_literals

from django.db import models
from member.models import Member


class Receipt(models.Model):
    money = models.IntegerField()
    remark = models.CharField(max_length=100)
    date = models.DateField()
    subclassification = models.ForeignKey('SubClassification', on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    incomeandexpense = models.ForeignKey('IncomeAndExpense', on_delete=models.CASCADE)

class Classification(models.Model):
    CLASSIFICATION_TYPE = (
        ('FO', 'food'),
        ('CL', 'clothing'),
        ('HO', 'housing'),
        ('TR', 'transportation'),
        ('ED', 'education'),
        ('EN', 'entertainment'),
        ('OT', 'others'),
    )
    classificaion_type = models.CharField(max_length=2, choices=CLASSIFICATION_TYPE)

class SubClassification(models.Model):
    name = models.CharField(max_length=100)
    classification = models.ForeignKey('Classification', on_delete=models.CASCADE)
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)

class Payment(models.Model):
    PAYMENT_TYPE = (
        ('CR', 'credit_card'),
        ('CA', 'cash'),
    )
    payment_type = models.CharField(max_length=2, choices=PAYMENT_TYPE)

class IncomeAndExpense(models.Model):
    INCOME_TYPE = (
        ('IN', 'income'),
        ('EX', 'expense'),
    )
    income_type = models.CharField(max_length=2, choices=INCOME_TYPE)

    
