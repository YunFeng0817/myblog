#coding=UTF-8
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from blog import models
# Create your views here.

#负责页面的登录与退出动作
def loginout(request):
    if not request.user.is_authenticated():
        if request.method == "POST":
            blogID = request.POST['blogID']
            password = request.POST['password']
            user = authenticate(username=blogID, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session.set_expiry(1800)  #!!!设置session的过期时长 ，整数表示几秒后过期，0 表示在用户的浏览器关闭时过期，none表示永不过期
                else:
                    #messages.warning(request, '用户无效')
                    return HttpResponse('用户无效')
            else:
                #messages.info(request, '密码错误')    用messages的方法也可以实现提醒的功能
                return HttpResponse('密码错误')
    else:
        if request.method == 'POST':
            flag = request.POST['logout']
            if flag=='true':
                logout(request)

#负责主页面的界面
#此时也有坑  函数loginout()结束后还会继续执行之后的return render() ，导致页面密码输入错误不会得到错误提醒
def main(request):
    Response = loginout(request)
    if Response==None:
        return render(request, 'blog/main.html')
    else:
        return Response

#负责小日记的链接页
def diaries(request):
    Response = loginout(request)
    context = {'contentType':'小日记'}
    if Response == None:
        #获取当前登录的用户！！！
        current_user = request.user
        if str(current_user) != 'AnonymousUser':
            essay =models.diary.objects.filter(author=current_user)
            context['diaries']=essay
        return render(request, 'blog/essay_list.html', context)
    else:
        return Response


#负责小日记具体的某一篇日记的页面
def diary(request,diaryID):
    Response = loginout(request)
    context = {'contentType': '小日记','contentURL':'diary'}
    if Response == None:
        current_user = request.user
        if str(current_user) != 'AnonymousUser':
            essay = models.diary.objects.filter(author=current_user)
            essay = essay.filter(title=diaryID)
            context['diary'] = essay
        return render(request, 'blog/essay.html', context)
    else:
        return Response


#负责显示照片的页面
def photos(request):
    Response = loginout(request)
    context = {'contentType': '照片墙'}
    if Response == None:
        return render(request, 'blog/photos.html', context)
    else:
        return Response

#负责收获的链接页
def techs(request):
    Response = loginout(request)
    context = {'contentType': '收获'}
    if Response == None:
        return render(request, 'blog/essay_list.html', context)
    else:
        return Response


#负责具体某一篇的收获内容博客
def tech(request):
    Response = loginout(request)
    context = {'contentType': '收获','contentURL':'tech', 'essayTitle': 'django框架'}
    if Response == None:
        return render(request, 'blog/essay.html', context)
    else:
        return Response


#负责旅游的日记链接
def trips(request):
    Response = loginout(request)
    context =  {'contentType': '旅游'}
    if Response == None:
        return render(request, 'blog/essay_list.html',context)
    else:
        return Response

#负责具体的某一篇旅游记录
def trip(request):
    Response = loginout(request)
    context = {'contentType': '旅游','contentURL':'trip','essayTitle': '天津'}
    if Response == None:
        return render(request, 'blog/essay.html', context)
    else:
        return Response

#负责登录的动作 已合并到了def main中了
# def loginAction(request):
#     if request.method=="POST":
#         blogID = request.POST['blogID']
#         password = request.POST['password']
#         user = authenticate(username=blogID, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 name =user.get_short_name()
#                 return render(request,'blog/main.html',{'name':name})
#             else:
#                 messages.warning(request,'用户无效')
#                 return render(request,'blog/main.html',)
#         else:
#             messages.info(request, '密码错误')
#     return render(request,'blog/main.html',{'error':'密码错误'})


#负责登出的动作 现在已经集成到了loginout函数中了
# def logoutAction(request):
#     logout(request)
#     return redirect('/') #render(request,'blog/main.html')

