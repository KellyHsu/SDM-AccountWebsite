from django.contrib import admin
from .models import Receipt, Classification, SubClassification, Payment,IncomeAndExpense


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('member', 'subclassification', 'money', 'date', 'payment', "remark")
    ordering = ('-date',)
    # search with member, subclassification, payment
    search_fields = ('member__user__username', 'subclassification__name', 'payment__payment_type')
    date_hierarchy = 'date'


class SubClassificationAdmin(admin.ModelAdmin):
    list_display = ('member', 'classification', 'name')


class ClassificationAdmin(admin.ModelAdmin):
    ordering = ('classificaion_type',)


class PaymentAdmin(admin.ModelAdmin):
    ordering = ('payment_type',)


class IncomeAndExpenseAdmin(admin.ModelAdmin):
    ordering = ('income_type',)

admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(SubClassification, SubClassificationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(IncomeAndExpense, IncomeAndExpenseAdmin)
