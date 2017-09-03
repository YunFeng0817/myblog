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
    url(r'^id=([^/]+)/photo/(\d+)/$',photo,name='photo'),
    url(r'^id=([^/]+)/label/add/$',addLabels,name='addLabel'),
    url(r'^id=([^/]+)/file/add/$',addFiles,name='addFile'),
    url(r'^id=([^/]+)/image/add/$',addImages,name='addImage'),
    url(r'^id=([^/]+)/add/$',addEssay,name='addEssay'),
    url(r'^id=([^/]+)/photo/delete/$',deletePhoto,name='deletePhoto'),
    url(r'^id=([^/]+)/essay/delete/$',deleteEssay,name='deleteEssay'),
    url(r'^id=([^/]+)/changePass/$',modifyPassword,name='modifyPassword'),
    url(r'^id=([^/]+)/information/$',addAuthorInformation,name='addAuthorInformation'),
    url(r'^id=([^/]+)/search/$',search,name='search'),
]