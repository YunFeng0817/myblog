#coding=UTF-8
from django.contrib import admin
from django.conf.urls import url
from blog.views import *

urlpatterns=[
    url(r'^id=([^/]+)/$',main,name='main'),
    #此url是曾用的，由于使用了ajax表单认证，此url已于上个url合并
    #url(r'^login/$',loginAction,name='loginAction'),
    #此url是曾用的，由于使用了ajax表单认证，此url已于上上个url合并
    #url(r'^logout/$',logoutAction,name='logoutAction'),
    url(r'^id=([^/]+)/diary/$',diaries,name='diaries'),
    url(r'^id=([^/]+)/diary/(\d+)/$',diary,name='diary'),
    url(r'^id=([^/]+)/tech/$',techs,name='techs'),
    url(r'^id=([^/]+)/tech/(\d+)/$', tech, name='tech'),
    url(r'^id=([^/]+)/trip/$', trips, name='trips'),
    url(r'^id=([^/]+)/trip/(\d+)/$', trip, name='trip'),
    url(r'^id=([^/]+)/photo/$',photos,name='photos'),

]