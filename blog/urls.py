from django.contrib import admin
from django.conf.urls import url
from blog.views import *

urlpatterns=[
    url(r'^$',main,name='main'),
    #url(r'^login/$',loginAction,name='loginAction'),
    url(r'^logout/$',logoutAction,name='logoutAction')
]