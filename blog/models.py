from django.db import models
from django.utils import timezone
# Create your models here.

#this is information about blog owner
class blogger(models.Model):
    blogID = models.CharField(max_length=30,primary_key=True)      #set the key
    blogName = models.CharField(max_length=30)
    createTime = models.DateField(timezone.datetime.now())

    def __str__(self):
        return self.blogID


class blogs(models):
    title = models.CharField(max_length=100)
    content = models.CharField
    author = models.ForeignKey(blogger)     #一篇日志可以对应一个作者，但一个作者可以写多个日志 ，故用foreignkey    一本书由多个作者编写，一个作者可以写很多本书，故用manytomanyField
    writDate = models.DateField

    def __init__(self):
        self.writDate = timezone.datetime.now()

    def __str__(self):
        return self.title


