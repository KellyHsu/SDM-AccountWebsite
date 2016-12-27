from django.contrib.auth.models import User
from member.models import Member
from account.models import Receipt, SubClassification, Payment, IncomeAndExpense, Classification, CyclicalExpenditure, \
    Budget, MonthBudget
from rest_framework import serializers

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'user', 'create_date')


class ReceiptSerializer(serializers.ModelSerializer):
    #sub = SubClassificationSerializer(source='SubClassification_set')
    sub_category_name = serializers.ReadOnlyField()

    class Meta:
        model = Receipt
        fields = ('money', 'remark', 'date', 'category_name', 'sub_category_name', 'payment_type', 'income_or_expense')

