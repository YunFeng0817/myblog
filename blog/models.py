#coding=UTF-8
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User   #用于扩展已有的用户模型
from users.models import User
import datetime
# Create your models here.

#this is information about blog owner

#绑定在文章的文件
class file(models.Model):
    file = models.FileField(upload_to='essays/')
    addDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.url
    class Meta:
        ordering = ["-addDate"]



#这些是附属于各类型文章的标签
class label(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    addDate = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-addDate"]


#绑定在文章和照片墙上的图片
class image(models.Model):
    introduction = models.CharField(max_length=200)
    img = models.ImageField(upload_to='static/blog/')
    addDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.img.name

    class Meta:
        ordering = ["-addDate"]


#绑定在文章后面的评论
class comment(models.Model):
    author = models.ForeignKey(User,primary_key=False,blank=True)
    words = models.CharField(max_length=200)
    addDate = models.DateTimeField(auto_now_add=True)
    support_num = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.words

    def __str__(self):
        return self.words

    class Meta:
        ordering = ["-addDate"]


class storge(models.Model):
    title = models.CharField(max_length=100,unique=True,primary_key=False)     #文章标题
    introduction = models.CharField(max_length=200,default='')   #文章简介
    author = models.ForeignKey(User,primary_key=False)     #一篇日志可以只能一个作者，但一个作者可以写多个日志 ，故用foreignkey    一本书由多个作者编写，一个作者可以写很多本书，故用manytomanyField
    writeDate = models.DateTimeField(auto_now_add=True)   #写作日期
    modifyDate = models.DateTimeField(auto_now=True)   #修改日期
    labels = models.ManyToManyField(label,blank=True)
    words = models.TextField(null=True,blank=True)
    images = models.ManyToManyField(image,blank=True)
    files = models.ManyToManyField(file,blank=True)
    comments = models.ManyToManyField(comment,blank=True)
    #存放文件路径

    def get(self):
        return [self.title,self.introduction,self.author,self.writeDate,self.modifyDate,self.words,self.words]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-writeDate"]
        abstract = True



class diary(storge):
    pass

class tech(storge):
    pass

class trip(storge):
    pass


#照片墙
class photo(models.Model):
    author = models.ForeignKey(User)
    introduction = models.CharField(max_length=50)
    images = models.ManyToManyField(image)
    addDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-addDate"]
