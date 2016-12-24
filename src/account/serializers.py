from django.contrib.auth.models import User
from member.models import Member
from account.models import Receipt, SubClassification, Payment, IncomeAndExpense, Classification, CyclicalExpenditure, \
    Budget, MonthBudget
from rest_framework import serializers

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'user', 'create_date')