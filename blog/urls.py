from django.contrib import admin
from django.conf.urls import url
from blog.views import *

urlpatterns=[
    url(r'^$',main,name='main'),
    #此url是曾用的，由于使用了ajax表单认证，此url已于上个url合并
    #url(r'^login/$',loginAction,name='loginAction'),
    #此url是曾用的，由于使用了ajax表单认证，此url已于上上个url合并
    #url(r'^logout/$',logoutAction,name='logoutAction'),
    url(r'^diary/$',diary,name='diary'),
]