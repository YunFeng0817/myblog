from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from blog.models import *
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
def main(request):
    loginout(request)
    return render(request, 'blog/main.html')

#负责小日记的链接页
def diaries(request):
    loginout(request)
    return render(request, 'blog/essay_list.html')

def diary(request):
    loginout(request)
    return render(request, 'blog/essay.html')

def photos(request):
    loginout(request)
    return render(request,'blog/photos.html')

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

