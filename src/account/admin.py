from django.contrib import admin
from .models import Receipt
from .models import Classification
from .models import SubClassification
from .models import Payment
from .models import IncomeAndExpense

admin.site.register(Receipt)
admin.site.register(Classification)
admin.site.register(SubClassification)
admin.site.register(Payment)
admin.site.register(IncomeAndExpense)


