#coding=UTF-8
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from users.models import User
from django.utils.timezone import datetime
#from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
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


def modelCommon(current_user,context):
    labels = models.label.objects.filter(author=current_user)
    context['labels'] = labels
    files = models.file.objects.filter(author=current_user)
    context['files'] = files
    images = models.image.objects.filter(author=current_user)
    context['images'] = images
    return context


#负责主页面的界面
#此时也有坑  函数loginout()结束后还会继续执行之后的return render() ，导致页面密码输入错误不会得到错误提醒
def main(request,userName):
    Response = loginout(request)
    context = {'id': userName}
    if Response==None:
        current_user = User.objects.filter(name=userName)
        time_point = datetime.datetime.now() - datetime.timedelta(days=7)
        diaries = models.diary.objects.filter(author=current_user,writeDate__gte=time_point)   # writeDate__gte表示筛选大于该时间的对象
        if not diaries:  #判断查询集是否为空的用法
            diaries = models.diary.objects.filter(author=current_user).order_by('-writeDate')[0:1]
        context['diaries'] = diaries
        techs = models.tech.objects.filter(author=current_user,writeDate__gte=time_point)
        if not techs:
            techs = models.tech.objects.filter(author=current_user).order_by('-writeDate')[0:1]
        context['techs'] = techs
        trips = models.trip.objects.filter(author=current_user,writeDate__gte=time_point)
        if not trips:
            trips = models.trip.objects.filter(author=current_user).order_by('-writeDate')[0:1]
        context['trips'] = trips
        return render(request, 'blog/main.html',context)
    else:
        return Response

#负责小日记的链接页
def diaries(request,userName):
    Response = loginout(request)
    context = {'contentType':'小日记','id':userName}
    if Response == None:
        #获取当前登录的用户！！！
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     essay =models.diary.objects.filter(author=current_user)
        #     context['essays']=essay
        current_user = User.objects.filter(name=userName)
        essay = models.diary.objects.filter(author=current_user)
        context['essays'] = essay
        context = modelCommon(current_user,context)
        return render(request, 'blog/essay_list.html', context)
    else:
        return Response


#负责小日记具体的某一篇日记的页面
def diary(request,userName,diaryID):
    Response = loginout(request)
    context = {'contentType': '小日记','contentURL':'diary','id':userName}
    if Response == None:
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     essay = models.diary.objects.filter(author=current_user)
        #     essay = essay.get(id=diaryID)
        #     context['essay'] = essay
        current_user = User.objects.filter(name=userName)
        essay = models.diary.objects.filter(author=current_user)
        essay = essay.get(id=diaryID)
        context['essay'] = essay
        context = modelCommon(current_user, context)
        return render(request, 'blog/essay.html', context)
    else:
        return Response


#负责显示照片的页面
def photos(request,userName):
    Response = loginout(request)
    context = {'contentType': '照片墙','id':userName}
    if Response == None:
        current_user = User.objects.filter(name=userName)
        images = models.image.objects.filter(author=current_user).all()
        context['images'] = images
        context = modelCommon(current_user, context)
        return render(request, 'blog/photos.html', context)
    else:
        return Response

#负责收获的链接页
def techs(request,userName):
    Response = loginout(request)
    context = {'contentType': '收获','id':userName}
    if Response == None:
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     techs = models.tech.objects.filter(author=current_user)
        #     context['essays'] = techs
        current_user = User.objects.filter(name=userName)
        essay = models.tech.objects.filter(author=current_user)
        context['essays'] = essay
        context = modelCommon(current_user, context)
        return render(request, 'blog/essay_list.html', context)
    else:
        return Response


#负责具体某一篇的收获内容博客
def tech(request,userName,techID):
    Response = loginout(request)
    context = {'contentType': '收获','contentURL':'tech', 'essayTitle': 'django框架','id':userName}
    if Response == None:
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     techs = models.tech.objects.filter(author=current_user)
        #     tech = techs.get(id=techID)
        #     context['essay'] = tech
        current_user = User.objects.filter(name=userName)
        essay = models.tech.objects.filter(author=current_user)
        essay = essay.get(id=techID)
        context['essay'] = essay
        context = modelCommon(current_user, context)
        return render(request, 'blog/essay.html', context)
    else:
        return Response


#负责旅游的日记链接
def trips(request,userName):
    Response = loginout(request)
    context =  {'contentType': '旅游','id':userName}
    if Response == None:
        if Response == None:
            current_user = User.objects.filter(name=userName)
            essay = models.trip.objects.filter(author=current_user)
            context['essays'] = essay
            context = modelCommon(current_user, context)
        return render(request, 'blog/essay_list.html',context)
    else:
        return Response

#负责具体的某一篇旅游记录
def trip(request,userName,tripID):
    Response = loginout(request)
    context = {'contentType': '旅游','contentURL':'trip','id':userName}
    if Response == None:
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     trips = models.trip.objects.filter(author=current_user)
        #     trip = trips.get(id=tripID)
        #     context['essay'] = trip
        current_user = User.objects.filter(name=userName)
        essay = models.trip.objects.filter(author=current_user)
        essay = essay.get(id=tripID)
        context['essay'] = essay
        context = modelCommon(current_user, context)
        return render(request, 'blog/essay.html', context)
    else:
        return Response

#增加标签的页面
def addLabels(request,current_user):
    if request.method =='POST':
        user = User.objects.get(name=current_user)
        current_user = request.user
        if current_user==user:
            label = request.POST['label']
            labelObject = models.label()
            labelObject.author = current_user
            labelObject.name = label
            labelObject.save()
            return HttpResponse('保存成功')
        else:
            return HttpResponse('非法访问')
    else:
        return render(request,'blog/addLabels.html')

#此处莫名的大坑 不断csrf认证错误
@csrf_exempt
def addFiles(request, current_user):
    if request.method == 'POST':
        user = User.objects.get(name=current_user)
        current_user = request.user
        if current_user == user:
            File = request.FILES['File']
            fileObject = models.file()
            fileObject.author = current_user
            fileObject.file = File
            fileObject.save()
            return HttpResponse('上传成功')
        else:
            return HttpResponse('非法访问')
    else:
        return render(request, 'blog/addFiles.html')

@csrf_exempt
def addImages(request, current_user):
    if request.method == 'POST':
        user = User.objects.get(name=current_user)
        current_user = request.user
        if current_user == user:
            Image = request.FILES['File']
            introduction = request.POST['introduction']
            imageObject = models.image()
            imageObject.author = current_user
            imageObject.img = Image
            imageObject.introduction = introduction
            imageObject.save()
            return HttpResponse('上传成功')
        else:
            return HttpResponse('非法访问')
    else:
        return render(request, 'blog/addImages.html')

def addEssay(request,userName):
    if request.method =='POST':
        username = User.objects.get(name=userName)
        current_user = request.user
        if username == current_user:
            type = request.POST['type']
            if type=="照片墙":
                return redirect('/id='+userName+'/photo/')
            else:
                title = request.POST['title']
                introduction = request.POST['introduction']
                if type == "小日记":
                    diary = models.diary.objects.create(author = current_user)
                    diary.introduction = introduction
                    diary.title = title
                    #由于这些内容是可选的，所以要依次尝试
                    try:
                        labels = request.POST.getlist("labels")
                        for label in labels:  #这是一个包含选项字符串的列表
                            labelObject = models.label.objects.get(name=label)
                            diary.labels.add(labelObject)
                    except:
                        pass
                    try:
                        words = request.POST['words']
                        diary.words = words
                    except:
                        pass
                    try:
                        files = request.POST.getlist('files')
                        for file in files:
                            fileObject = models.file.objects.get(id=file)
                            diary.files.add(fileObject)
                    except:
                        pass
                    try:
                        images = request.POST.getlist('images')
                        for image in images:
                            imageObject = models.image.objects.get(id=image)
                            diary.images.add(imageObject)
                    except:
                        pass
                    diary.save()
                elif type == "收获":
                    tech = models.tech.objects.create(author=current_user)
                    tech.introduction = introduction
                    tech.title = title
                    # 由于这些内容是可选的，所以要依次尝试
                    try:
                        labels = request.POST.getlist("labels")
                        for label in labels:  # 这是一个包含选项字符串的列表
                            labelObject = models.label.objects.get(name=label)
                            tech.labels.add(labelObject)
                    except:
                        pass
                    try:
                        words = request.POST['words']
                        tech.words = words
                    except:
                        pass
                    try:
                        files = request.POST.getlist('files')
                        for file in files:
                            fileObject = models.file.objects.get(id=file)
                            tech.files.add(fileObject)
                    except:
                        pass
                    try:
                        images = request.POST.getlist('images')
                        for image in images:
                            imageObject = models.image.objects.get(id=image)
                            tech.images.add(imageObject)
                    except:
                        pass
                    tech.save()
                elif type == "旅游":
                    trip = models.trip.objects.create(author=current_user)
                    trip.introduction = introduction
                    trip.title = title
                    # 由于这些内容是可选的，所以要依次尝试
                    try:
                        labels = request.POST.getlist("labels")
                        for label in labels:  # 这是一个包含选项字符串的列表
                            labelObject = models.label.objects.get(name=label)
                            trip.labels.add(labelObject)
                    except:
                        pass
                    try:
                        words = request.POST['words']
                        trip.words = words
                    except:
                        pass
                    try:
                        files = request.POST.getlist('files')
                        for file in files:
                            fileObject = models.file.objects.get(id=file)
                            trip.files.add(fileObject)
                    except:
                        pass
                    try:
                        images = request.POST.getlist('images')
                        for image in images:
                            imageObject = models.image.objects.get(id=image)
                            trip.images.add(imageObject)
                    except:
                        pass
                    trip.save()
                else:
                    return HttpResponse('表单类型错误')
            return redirect('/id='+userName+'/')
        else:
            return HttpResponse('非法提交')
    else:
        return HttpResponse('只支持post请求')



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

