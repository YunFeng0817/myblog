#coding=UTF-8
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User   #用于扩展已有的用户模型
from users.models import User
import datetime
# Create your models here.

#this is information about blog owner
class storge(models.Model):
    title = models.CharField(max_length=100,unique=True,primary_key=False)     #文章标题
    introduction = models.CharField(max_length=50,default='')   #文章简介
    author = models.ForeignKey(User,primary_key=False)     #一篇日志可以对应一个作者，但一个作者可以写多个日志 ，故用foreignkey    一本书由多个作者编写，一个作者可以写很多本书，故用manytomanyField
    writeDate = models.DateTimeField(auto_now_add=True)   #写作日期
    modifyDate = models.DateTimeField(auto_now=True)   #修改日期
    words = models.CharField(max_length=10000,default='')
    #存放文件路径
    file = models.FileField(upload_to='blog')

    def was_published_recently(self):
        return self.writeDate >= timezone.now() - datetime.timedelta(days=1)

    def get(self):
        return [self.title,self.introduction,self.author,self.writeDate,self.modifyDate,self.words,self.words]

    def __str__(self):
        return self.title

    class Meta:
        abstract = True



class diary(storge):
    # 用于存放标签
    label1 = models.CharField(max_length=10,default='经历')
    label2 = models.CharField(max_length=10,default='感悟')
    label3 = models.CharField(max_length=10,default='心情')
    pass

class tech(storge):
    # 用于存放标签
    label1 = models.CharField(max_length=10,default='编程')
    label2 = models.CharField(max_length=10,default='技术')
    label3 = models.CharField(max_length=10,default='经验')
    pass

class trip(storge):
    img = models.ImageField()

class photo(models.Model):
    author = models.ForeignKey(User)
    introduction = models.CharField(max_length=50)
    img = models.ImageField(upload_to='photo')
    def __str__(self):
        return self.img.url


