from django.shortcuts import render
from blog.models import *
# Create your views here.
def main(request):
    blogOwner = blogger.objects.get(blogID='294889365')
    Name = blogOwner.blogName
    return render(request,'blog/main.html',{'name':Name})