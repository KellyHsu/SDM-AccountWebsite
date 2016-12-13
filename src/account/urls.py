from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^dashboard/$', views.dashboard),
    url(r'^setting/$', views.setting),
    url(r'^filter/$', views.filter),
    url(r'^createReceipt/$', views.create_receipt, name='create_receipt'),
    url(r'^deleteReceipt/$', views.delete_receipt, name='delete_receipt'),
    url(r'^createSubCategory/$', views.create_subClassification, name='create_subClassification'),
    url(r'^getNewDate/$', views.get_date, name='get_date'),
    url(r'^changePassword/$', views.change_password, name='change_password'),
    url(r'^createCyclicalExpenditure/$', views.create_cyclicalExpenditure, name='create_cyclicalExpenditure'),
    url(r'^updateCyclicalExpenditure/$', views.update_cyclicalExpenditure, name='update_cyclicalExpenditure'),
    url(r'^deleteCyclicalExpenditure/$', views.delete_cyclicalExpenditure, name='delete_cyclicalExpenditure'),
    url(r'^updateCyclicalExpenditureIsreminded/$', views.update_cyclicalExpenditure_isreminded, name='update_cyclicalExpenditure_isreminded'),
    url(r'^updateBudget/$', views.update_budget, name='update_budget'),
    url(r'^updateBudgetReminder/$', views.update_budget_reminder, name='update_budget_reminder'),
    url(r'^updateBudgetIsreminded/$', views.update_budget_isreminded, name='update_budget_isreminded'),
    url(r'^updateMonthBudget/$', views.update_month_budget, name='update_month_budget'),
    url(r'^updateMonthBudgetReminder/$', views.update_month_budget_reminder, name='update_month_budget_reminder'),
    url(r'^updateMonthBudgetIsreminded/$', views.update_month_budget_isreminded, name='update_month_budget_isreminded'),
    url(r'^createSubClassificationInSettingPage/$', views.create_subClassification_in_settingPage, name='create_subClassification_in_settingPage'),
    url(r'^deleteSubClassificationInSettingPage/$', views.delete_subClassification_in_settingPage, name='delete_subClassification_in_settingPage'),
    url(r'^countForMaxBudget/$', views.budget_calculate, name='budget_calculate'),
    url(r'^getReceiptByWeek/$', views.getreceipt_week, name='getreceipt_week'),
    url(r'^getReceiptByMon/$', views.getreceipt_mon, name='getreceipt_mon'),
    url(r'^getReceiptByYr/$', views.getreceipt_yr, name='getreceipt_yr'),
    url(r'^backwardTime/$', views.backwardtime, name='backwardtime'),
    url(r'^countClassBudget/$', views.classification_budget_calculate, name='classification_budget_calculate'),
    url(r'^filterDelRecord/$', views.filterdelrecord, name='filterdelrecord'),
]
