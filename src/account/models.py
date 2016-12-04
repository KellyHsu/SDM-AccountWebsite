from __future__ import unicode_literals
from django.db import models


class Receipt(models.Model):
    money = models.IntegerField()
    remark = models.CharField(max_length=100)
    date = models.DateField()
    subclassification = models.ForeignKey('SubClassification', on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    incomeandexpense = models.ForeignKey('IncomeAndExpense', on_delete=models.CASCADE)
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)


class Classification(models.Model):
    CLASSIFICATION_TYPE = (
        ('food', 'food'),
        ('clothing', 'clothing'),
        ('housing', 'housing'),
        ('transportation', 'transportation'),
        ('education', 'education'),
        ('entertainment', 'entertainment'),
        ('others', 'others'),
    )
    classificaion_type = models.CharField(max_length=20, choices=CLASSIFICATION_TYPE)

    def __unicode__(self):
        return self.classificaion_type


class SubClassification(models.Model):
    name = models.CharField(max_length=100)
    classification = models.ForeignKey('Classification', on_delete=models.CASCADE)
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_TYPE = (
        ('credit_card', 'credit_card'),
        ('cash', 'cash'),
        ('other', 'other'),
    )
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)

    def __unicode__(self):
        return self.payment_type


class IncomeAndExpense(models.Model):
    INCOME_TYPE = (
        ('income', 'income'),
        ('expense', 'expense'),
    )
    income_type = models.CharField(max_length=10, choices=INCOME_TYPE)

    def __unicode__(self):
        return self.income_type


class CyclicalExpenditure(models.Model):
    name = models.CharField(max_length=100)
    expenditure_date = models.DateField()
    reminder_date = models.DateField()
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)


class Budget(models.Model):
    budget = models.IntegerField()
    reminder = models.IntegerField()
    classification = models.ForeignKey('Classification', on_delete=models.CASCADE)
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)
