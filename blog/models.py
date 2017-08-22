#coding=UTF-8
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User   #用于扩展已有的用户模型
from users.models import User
# Create your models here.

#this is information about blog owner
class storge(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    author = models.ForeignKey(User)     #一篇日志可以对应一个作者，但一个作者可以写多个日志 ，故用foreignkey    一本书由多个作者编写，一个作者可以写很多本书，故用manytomanyField
    writDate = models.DateField(timezone.datetime.now())

    def __int__(self):
        self.writDate = timezone.datetime.now()

    def __str__(self):
        return self.title


