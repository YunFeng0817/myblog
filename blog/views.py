#coding=UTF-8
from django.shortcuts import render,redirect,HttpResponse,Http404
from django.contrib.auth import authenticate, login,update_session_auth_hash
from django.contrib.auth import logout
from users.models import User
from django.utils.timezone import datetime
#from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
from blog import models
import os
from django.http import JsonResponse
# Create your views here.

essayModel = {u'小日记':models.diary,u'收获':models.tech,u'旅游':models.trip}
essayType = {u'小日记':'diary',u'收获':'tech',u'旅游':'trip'}

#负责页面的登录与退出动作
def loginout(request,context):
    if not request.user.is_authenticated():
        if request.method == "POST":
            blogID = request.POST['blogID']
            password = request.POST['password']
            user = authenticate(username=blogID, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session.set_expiry(1800)  #!!!设置session的过期时长 ，整数表示几秒后过期，0 表示在用户的浏览器关闭时过期，none表示永不过期
                    context['user'] = user
                    try:
                        context['author'] = models.authInformation.objects.get(author=user)
                    except:
                        pass
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
                context['user'] = None


def modelCommon(current_user,context):
    labels = models.label.objects.all()
    context['labels'] = labels
    files = models.file.objects.filter(author=current_user)
    context['files'] = files
    images = models.image.objects.filter(author=current_user)
    context['images'] = images
    return context


#负责主页面的界面
#此时也有坑  函数loginout()结束后还会继续执行之后的return render() ，导致页面密码输入错误不会得到错误提醒
def main(request,userName):
    context = {'id': userName}
    Response = loginout(request,context)
    if Response==None:
        current_user = User.objects.get(name=userName)
        if current_user:
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
            try:
                context['author'] = models.authInformation.objects.get(author=current_user)
            except:
                pass
            context = modelCommon(current_user, context)
            context['userJoin'] = current_user.date_joined
            context['userLogin'] = current_user.last_login
            return render(request, 'blog/main.html',context)
        else:
            raise Http404
    else:
        return Response

#负责小日记的链接页
def diaries(request,userName):
    context = {'contentType': '小日记', 'id': userName}
    Response = loginout(request,context)
    if Response == None:
        #获取当前登录的用户！！！
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     essay =models.diary.objects.filter(author=current_user)
        #     context['essays']=essay
        current_user = User.objects.get(name=userName)
        if current_user:
            essay = models.diary.objects.filter(author=current_user)
            context['essays'] = essay
            context = modelCommon(current_user,context)
            return render(request, 'blog/essay_list.html', context)
        else:
            raise Http404
    else:
        return Response


#负责小日记具体的某一篇日记的页面
def diary(request,userName,diaryID):
    context = {'contentType': '小日记', 'contentURL': 'diary', 'id': userName}
    Response = loginout(request,context)
    if Response == None:
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     essay = models.diary.objects.filter(author=current_user)
        #     essay = essay.get(id=diaryID)
        #     context['essay'] = essay
        current_user = User.objects.get(name=userName)
        if current_user:
            essay = models.diary.objects.filter(author=current_user)
            essay = essay.get(id=diaryID)
            context['essay'] = essay
            context = modelCommon(current_user, context)
            return render(request, 'blog/essay.html', context)
        else:
            raise Http404
    else:
        return Response


#负责显示照片的页面
def photos(request,userName):
    context = {'contentType': '照片墙', 'id': userName}
    Response = loginout(request,context)
    if Response == None:
        current_user = User.objects.get(name=userName)
        if current_user:
            images = models.image.objects.filter(author=current_user).all()
            context['images'] = images
            context = modelCommon(current_user, context)
            return render(request, 'blog/photos.html', context)
        else:
            raise Http404
    else:
        return Response

def photo(request, userName,photoID):
    context = {'contentType': '照片墙', 'contentURL': 'photo', 'id': userName}
    Response = loginout(request,context)
    if Response == None:
        current_user = User.objects.get(name=userName)
        if current_user:
            images = models.image.objects.filter(author=current_user).all()
            image = images.get(id=photoID)
            context['image'] = image
            context = modelCommon(current_user, context)
            return render(request, 'blog/showPhoto.html', context)
        else:
            raise Http404

    else:
        return Response

#负责收获的链接页
def techs(request,userName):
    context = {'contentType': '收获', 'id': userName}
    Response = loginout(request,context)
    if Response == None:
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     techs = models.tech.objects.filter(author=current_user)
        #     context['essays'] = techs
        current_user = User.objects.get(name=userName)
        if current_user:
            essay = models.tech.objects.filter(author=current_user)
            context['essays'] = essay
            context = modelCommon(current_user, context)
            return render(request, 'blog/essay_list.html', context)
        else:
            raise Http404
    else:
        return Response


#负责具体某一篇的收获内容博客
def tech(request,userName,techID):
    context = {'contentType': '收获', 'contentURL': 'tech', 'essayTitle': 'django框架', 'id': userName}
    Response = loginout(request,context)
    if Response == None:
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     techs = models.tech.objects.filter(author=current_user)
        #     tech = techs.get(id=techID)
        #     context['essay'] = tech
        current_user = User.objects.get(name=userName)
        if current_user:
            essay = models.tech.objects.filter(author=current_user)
            essay = essay.get(id=techID)
            context['essay'] = essay
            context = modelCommon(current_user, context)
            return render(request, 'blog/essay.html', context)
        else:
            raise Http404
    else:
        return Response


#负责旅游的日记链接
def trips(request,userName):
    context = {'contentType': '旅游', 'id': userName}
    Response = loginout(request,context)
    if Response == None:
        if Response == None:
            current_user = User.objects.get(name=userName)
            if current_user:
                essay = models.trip.objects.filter(author=current_user)
                context['essays'] = essay
                context = modelCommon(current_user, context)
                return render(request, 'blog/essay_list.html',context)
            else:
                raise Http404
    else:
        return Response

#负责具体的某一篇旅游记录
def trip(request,userName,tripID):
    context = {'contentType': '旅游', 'contentURL': 'trip', 'id': userName}
    Response = loginout(request,context)
    if Response == None:
        # current_user = request.user
        # if str(current_user) != 'AnonymousUser':
        #     trips = models.trip.objects.filter(author=current_user)
        #     trip = trips.get(id=tripID)
        #     context['essay'] = trip
        current_user = User.objects.get(name=userName)
        if current_user:
            essay = models.trip.objects.filter(author=current_user)
            essay = essay.get(id=tripID)
            context['essay'] = essay
            context = modelCommon(current_user, context)
            return render(request, 'blog/essay.html', context)
        else:
            raise Http404
    else:
        return Response

#增加标签的页面
def addLabels(request,current_user):
    if request.method =='POST':
        user = User.objects.get(name=current_user)
        current_user = request.user
        if current_user==user:
            label = request.POST['label']
            labelObject = models.label.objects.filter(author=current_user,name=label)
            if not labelObject:
                labelObject = models.label()
                labelObject.author = current_user
                labelObject.name = label
                labelObject.save()
                id = labelObject.id
                return JsonResponse({"response": "保存成功", "id": id})
            else:
                return HttpResponse('此标签已存在')
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
            id = fileObject.id
            #json用于返回一个类似字典的数据
            return JsonResponse({"response":"上传成功","id":id,"path":fileObject.file.url})
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
            id = imageObject.id
            return JsonResponse({"response":"上传成功","id":id,"path":imageObject.img.url})
        else:
            return HttpResponse('绘画')
    else:
        return render(request, 'blog/addImages.html')

def addEssay(request,username):
    if request.method =='POST':
        userName = User.objects.get(name=username)
        current_user = request.user
        if userName == current_user:
            type = request.POST['type']
            if type=="照片墙":
                return redirect('/id='+username+'/photo/')
            else:
                title = request.POST['title']
                introduction = request.POST['introduction']
                try:
                    id = request.POST['ContentID']
                    diary = essayModel[type].objects.get(id=id)
                except:
                    diary = essayModel[type].objects.create(author = current_user)
                diary.introduction = introduction
                diary.title = title
                #由于这些内容是可选的，所以要依次尝试
                try:
                    labels = request.POST.getlist("labels")
                    for label in labels:  #这是一个包含选项字符串的列表
                        labelObject = models.label.objects.get(id=label)
                        if labelObject not in diary.labels.all():
                            diary.labels.add(labelObject)
                    for labelObject in diary.labels.all():
                        if str(labelObject.id) not in labels:
                            diary.labels.remove(labelObject)
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
                        if fileObject not in diary.files.all():
                            diary.files.add(fileObject)
                    for fileObject in diary.files.all():
                        if str(fileObject.id) not in files:       #此处有坑  id不是字符串，而表单上传的是字符串，导致文件先上传后删除
                            diary.files.remove(fileObject)
                except:
                    pass
                try:
                    images = request.POST.getlist('images')
                    print(images)
                    for image in images:
                        imageObject = models.image.objects.get(id=image)
                        if imageObject not in diary.images.all():
                            diary.images.add(imageObject)
                    for imageObject in diary.images.all():
                        if str(imageObject.id) not in images:
                            diary.images.remove(imageObject)
                except:
                    pass
                diary.save()
                return redirect('/id='+username+'/'+essayType[type])
        else:
            return HttpResponse('非法提交')
    else:
        return HttpResponse('只支持post请求')

def deletePhoto(request,username):
    if request.method =='POST':
        userName = User.objects.get(name=username)
        current_user = request.user
        if current_user == userName:
            photoID = request.POST['photoID']
            photoObject = models.image.objects.get(id=photoID)
            #先删除对应路径的照片，后删除相应的数据库
            if os.path.isfile(photoObject.img.path):
                os.remove(photoObject.img.path)
            photoObject.delete()
            return redirect('/id='+username+'/photo/')
        else:
            return HttpResponse(u'请登录后再操作！')
    else:
        return HttpResponse(u'只支持post请求')

#负责删除各类型的博客
def deleteEssay(request,username):
    if request.method =='POST':
        userName = User.objects.get(name=username)
        current_user = request.user
        if current_user == userName:
            contentType = request.POST['contentType']
            essayID = request.POST['essayID']
            essayObject = essayModel[contentType].objects.get(id=essayID)
            essayObject.delete()
            return redirect('/id=' + username + '/'+essayType[contentType])
        else:
            return HttpResponse(u'请登录后再操作！')
    else:
        return HttpResponse(u'只支持post请求')

def modifyPassword(request,username):
    if request.method == 'POST':
        oldPassword = request.POST['oldPassword']
        user = request.user
        userName = User.objects.get(name=username)
        if user == userName:
            if userName.check_password(oldPassword):
                newPassword = request.POST['newPassword']
                userName.set_password(newPassword)
                userName.save()
                update_session_auth_hash(request, userName)
                return HttpResponse(u'修改成功')
            else:
                return HttpResponse(u'原密码错误')
        else:
            return redirect('/id='+username+'/')
    else:
        return HttpResponse(u'只支持post请求')

def addAuthorInformation(request,username):
    if request.method == 'POST':
        user = request.user
        userName = User.objects.get(name=username)
        if user == userName:
            try:
                authorObject = models.authInformation.objects.get(author=userName)
            except:
                authorObject = models.authInformation.objects.create(author=userName)
            try:
                avatar = request.FILES['avatar']
                if authorObject.avatar:
                    if os.path.isfile(authorObject.avatar.path):
                        print('remove')
                        os.remove(authorObject.avatar.path)
                authorObject.avatar = avatar
            except:
                pass
            introduction = request.POST['introduction']
            blogName = request.POST['username']
            userName.username = blogName
            authorObject.introduction = introduction
            labels = request.POST.getlist("labels")
            for label in labels:  # 这是一个包含选项字符串的列表
                labelObject = models.label.objects.get(id=label)
                if labelObject not in authorObject.labels.all():
                    authorObject.labels.add(labelObject)
            for labelObject in authorObject.labels.all():
                if str(labelObject.id) not in labels:
                    authorObject.labels.remove(labelObject)
            birthday = request.POST['birthday']
            authorObject.birthday = birthday
            authorObject.constellation = constellation(birthday)
            authorObject.save()
            userName.save()
            return redirect('/id='+username+'/')
        else:
            return redirect('/id='+username+'/')
    else:
        return HttpResponse(u'只支持post请求')

#负责从生日转换出对应的星座
def constellation(birthday):
    con = ['水平座','双鱼座','牡羊座','金牛座','双子座','巨蟹座','狮子座','处女座','天称座','天蝎座','射手座','摩羯座']
    divDate = [21,19,21,21,22,22,23,24,23,24,23,22]
    month = int(birthday[5:7])
    day = int(birthday[8:10])
    if day<divDate[month-1]:
        if month==1:
            return con[11]
        else:
            return con[month-2]
    else:
        return con[month-1]

def search(request,userName):
    if request.method == 'POST':
        context = {'id': userName}
        current_user = User.objects.get(name=userName)
        try:
            context['author'] = models.authInformation.objects.get(author=userName)
        except:
            pass
        context = modelCommon(current_user, context)
        context['userJoin'] = current_user.date_joined
        context['userLogin'] = current_user.last_login
        content = request.POST['search']
        diaries=[]
        if list(models.diary.objects.filter(title__icontains=content)) !=[]:
            diaries = list(models.diary.objects.filter(title__icontains=content))
        if list(models.diary.objects.filter(introduction__icontains=content)) != []:
            diaries.append(list(models.diary.objects.filter(introduction__icontains=content)))
        if list(models.diary.objects.filter(words__icontains=content))!=[]:
            diaries.append(list(models.diary.objects.filter(words__icontains=content)))
        if list(models.diary.objects.filter(writeDate__icontains=content))!=[]:
            diaries.append(list(models.diary.objects.filter(writeDate__icontains=content)))
        try:
            context['diaries'] = diaries
        except:
            pass
        techs = []
        if list(models.tech.objects.filter(title__icontains=content))!=[]:
            techs = list(models.tech.objects.filter(title__icontains=content))
        if list(models.tech.objects.filter(introduction__icontains=content))!=[]:
            techs.append(list(models.tech.objects.filter(introduction__icontains=content)))
        if list(models.tech.objects.filter(words__icontains=content)) !=[]:
            techs.append(list(models.tech.objects.filter(words__icontains=content)))
        if list(models.tech.objects.filter(writeDate__icontains=content))!=[]:
            techs.append(list(models.tech.objects.filter(writeDate__icontains=content)))
        try:
            context['techs'] = techs
        except:
            pass
        trips = []
        if list(models.trip.objects.filter(title__icontains=content)) != []:
            trips = list(models.trip.objects.filter(title__icontains=content))
        if list(models.trip.objects.filter(introduction__icontains=content)) != []:
            trips.append(list(models.trip.objects.filter(introduction__icontains=content)))
        if list(models.trip.objects.filter(words__icontains=content)) != []:
            trips.append(list(models.trip.objects.filter(words__icontains=content)))
        if list(models.trip.objects.filter(writeDate__icontains=content)) != []:
            trips.append(list(models.trip.objects.filter(writeDate__icontains=content)))
        try:
            context['trips'] = trips
        except:
            pass
        return render(request,'blog/main.html',context)
    else:
        return HttpResponse('支只持post请求')



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

