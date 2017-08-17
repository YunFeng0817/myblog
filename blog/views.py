from django.shortcuts import render
from blog.models import *
# Create your views here.
def main(request):
    return render(request,'blog/basic.html')