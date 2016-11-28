from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^dashboard/$', views.dashboard),
    url(r'^setting/$', views.setting),
    url(r'^filter/$', views.filter),
]
