from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^dashboard/$', views.dashboard),
    url(r'^setting/$', views.setting),
    url(r'^filter/$', views.filter),
    url(r'^createReceipt/$', views.create_receipt, name='create_receipt'),
    url(r'^createSubCategory/$', views.create_subClassification, name='create_subClassification'),
    url(r'^getNewDate/$', views.get_date, name='get_date'),
    url(r'^changePassword/$', views.change_password, name='change_password'),
    url(r'^createCyclicalExpenditure/$', views.create_cyclicalExpenditure, name='create_cyclicalExpenditure'),
    url(r'^deleteCyclicalExpenditure/$', views.delete_cyclicalExpenditure, name='delete_cyclicalExpenditure'),
    url(r'^updateCyclicalExpenditureIsreminded/$', views.update_cyclicalExpenditure_isreminded, name='update_cyclicalExpenditure_isreminded'),
    url(r'^updateBudget/$', views.update_budget, name='update_budget'),
    url(r'^updateBudgetReminder/$', views.update_budget_reminder, name='update_budget_reminder'),
    url(r'^updateBudgetIsreminded/$', views.update_budget_isreminded, name='update_budget_isreminded'),
    url(r'^updateMonthBudget/$', views.update_month_budget, name='update_month_budget'),
    url(r'^updateMonthBudgetReminder/$', views.update_month_budget_reminder, name='update_month_budget_reminder'),
    url(r'^updateMonthBudgetIsreminded/$', views.update_month_budget_isreminded, name='update_month_budget_isreminded'),
]
