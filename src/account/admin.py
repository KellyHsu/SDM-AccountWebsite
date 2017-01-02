from django.contrib import admin
from .models import Receipt, Classification, SubClassification, Payment,IncomeAndExpense,CyclicalExpenditure,Budget,MonthBudget,Notification


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('member', 'subclassification', 'money', 'date', 'payment', "remark")
    ordering = ('-date',)
    # search with member, subclassification, payment
    search_fields = ('member__user__username', 'subclassification__name', 'payment__payment_type')
    date_hierarchy = 'date'


class SubClassificationAdmin(admin.ModelAdmin):
    list_display = ('member', 'classification', 'name', "exist")


class ClassificationAdmin(admin.ModelAdmin):
    ordering = ('classification_type',)


class PaymentAdmin(admin.ModelAdmin):
    ordering = ('payment_type',)


class IncomeAndExpenseAdmin(admin.ModelAdmin):
    ordering = ('income_type',)


class CyclicalExpenditureAdmin(admin.ModelAdmin):
    ordering = ('is_reminded',)


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('member', 'classification', 'budget', 'reminder', 'is_reminded')


class MonthBudgetAdmin(admin.ModelAdmin):
    list_display = ('member', 'budget', 'reminder', 'is_reminded')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('member', 'message', 'is_read', 'is_deleted', 'type', 'item_name', 'create_date')

admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(SubClassification, SubClassificationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(IncomeAndExpense, IncomeAndExpenseAdmin)
admin.site.register(CyclicalExpenditure, CyclicalExpenditureAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(MonthBudget, MonthBudgetAdmin)
admin.site.register(Notification, NotificationAdmin)
