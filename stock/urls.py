from django.conf.urls import *
from django.conf.urls import url
from django.urls import path


from . import views

urlpatterns = [
    path('', views.main, name='login'),
    path('index', views.index, name='index'),
    path(r'signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'signup/account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),
]