#coding=UTF-8
from django.contrib import admin
from django.conf.urls import url
from blog.views import *

urlpatterns=[
    url(r'^([^/]+)/$',main,name='main'),
    #此url是曾用的，由于使用了ajax表单认证，此url已于上个url合并
    #url(r'^login/$',loginAction,name='loginAction'),
    #此url是曾用的，由于使用了ajax表单认证，此url已于上上个url合并
    #url(r'^logout/$',logoutAction,name='logoutAction'),
    url(r'^([^/]+)/diary/$',diaries,name='diaries'),
    url(r'^([^/]+)/diary/(\d+)/$',diary,name='diary'),
    url(r'^([^/]+)/tech/$',techs,name='techs'),
    url(r'^([^/]+)/tech/(\d+)/$', tech, name='tech'),
    url(r'^([^/]+)/trip/$', trips, name='trips'),
    url(r'^([^/]+)/trip/(\d+)/$', trip, name='trip'),
    url(r'^([^/]+)/photo/$',photos,name='photos'),
    url(r'^([^/]+)/photo/(\d+)/$',photo,name='photo'),
    url(r'^([^/]+)/label/add/$',addLabels,name='addLabel'),
    url(r'^([^/]+)/file/add/$',addFiles,name='addFile'),
    url(r'^([^/]+)/image/add/$',addImages,name='addImage'),
    url(r'^([^/]+)/add/$',addEssay,name='addEssay'),
    url(r'^([^/]+)/photo/delete/$',deletePhoto,name='deletePhoto'),
    url(r'^([^/]+)/essay/delete/$',deleteEssay,name='deleteEssay'),
    url(r'^([^/]+)/changePass/$',modifyPassword,name='modifyPassword'),
    url(r'^([^/]+)/information/$',addAuthorInformation,name='addAuthorInformation'),
    url(r'^([^/]+)/search/$',search,name='search'),
]