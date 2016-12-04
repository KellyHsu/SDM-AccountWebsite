from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^dashboard/$', views.dashboard),
    url(r'^setting/$', views.setting),
    url(r'^filter/$', views.filter),
    url(r'^createReceipt/$', views.create_receipt, name='create_receipt'),
    url(r'^createSubCategory/$', views.create_subClassification, name='create_subClassification'),
    url(r'^getNewDate/$', views.get_date, name='get_date'),
]
