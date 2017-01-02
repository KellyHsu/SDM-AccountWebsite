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

    @property
    def sub_category_name(self):
        return self.subclassification.name

    @property
    def category_name(self):
        return self.subclassification.classification.classification_type
    
    @property
    def payment_type(self):
        return self.payment.payment_type
    
    @property
    def income_or_expense(self):
        return self.incomeandexpense.income_type

class Classification(models.Model):
    CLASSIFICATION_TYPE = (
        ('food', 'food'),
        ('clothing', 'clothing'),
        ('housing', 'housing'),
        ('transportation', 'transportation'),
        ('education', 'education'),
        ('entertainment', 'entertainment'),
        ('others', 'others'),
        ('general_revenue', 'general_revenue'),
        ('invest_revenue', 'invest_revenue'),
        ('other_revenue', 'other_revenue'),
    )
    classification_type = models.CharField(max_length=20, choices=CLASSIFICATION_TYPE)

    def __unicode__(self):
        return self.classification_type


class SubClassification(models.Model):
    name = models.CharField(max_length=100)
    classification = models.ForeignKey('Classification', on_delete=models.CASCADE)
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)
    exist = models.BooleanField(default=True)

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
    REMIND_TYPE = (
        ('month', 'month'),
        ('week', 'week'),
    )
    name = models.CharField(max_length=100)
    expenditure_type = models.CharField(max_length=10, choices=REMIND_TYPE, default='month')
    expenditure_date = models.IntegerField()
    reminder_type = models.CharField(max_length=10, choices=REMIND_TYPE, default='month')
    reminder_date = models.IntegerField()
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)
    is_reminded = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Budget(models.Model):
    budget = models.IntegerField()
    reminder = models.IntegerField()
    classification = models.ForeignKey('Classification', on_delete=models.CASCADE)
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)
    is_reminded = models.BooleanField(default=False)


class MonthBudget(models.Model):
    budget = models.IntegerField()
    reminder = models.IntegerField()
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)
    is_reminded = models.BooleanField(default=False)

class Notification(models.Model):
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    NOTIFICATION_TYPE = (
        ('budget', 'budget'),
        ('periodic', 'periodic')
    )
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE, default='budget')
    item_name = models.CharField(max_length=100, default='item')
    create_date = models.DateField(auto_now_add=True)
