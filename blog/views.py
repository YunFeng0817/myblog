from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from blog.models import *
# Create your views here.

#负责主页的视图
def main(request):
    if not request.user.is_authenticated():
        return render(request,'blog/main.html',)
    else:
        user = request.user
        name = user.username
        # request_context = RequestContext(request,{'name':'您是访客'})
        return render(request,'blog/main.html',{'name':name})

#负责登录的动作
def loginAction(request):
    if request.method=="POST":
        blogID = request.POST['blogID']
        password = request.POST['password']
        user = authenticate(username=blogID, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                name =user.get_short_name()
                return render(request,'blog/main.html',{'name':name})
            else:
                messages.warning(request,'用户无效')
                return render(request,'blog/main.html',)
        else:
            messages.info(request, '密码错误')
    return render(request,'blog/main.html',{'error':'密码错误'})

#负责登出的动作
def logoutAction(request):
    logout(request)
    return redirect('/') #render(request,'blog/main.html')