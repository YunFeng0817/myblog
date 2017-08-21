from django.contrib import admin
from django.conf.urls import url
from blog.views import *

urlpatterns=[
    url(r'^$',main,name='main'),
    #此url是曾用的，由于使用了ajax表单认证，此url已于上个url合并
    #url(r'^login/$',loginAction,name='loginAction'),
    #此url是曾用的，由于使用了ajax表单认证，此url已于上上个url合并
    #url(r'^logout/$',logoutAction,name='logoutAction'),
    url(r'^diary/$',diaries,name='diaries'),
    url(r'^diary/1/$',diary,name='diary'),
    url(r'^tech/$',techs,name='techs'),
    url(r'^tech/1/$', tech, name='tech'),
    url(r'^trips/$', trips, name='trips'),
    url(r'^trip/1/$', techs, name='trip'),
    url(r'^photo/$',photos,name='photos'),

]