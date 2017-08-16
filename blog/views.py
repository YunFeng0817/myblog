from django.shortcuts import render
from blog.models import *
# Create your views here.
def main(request):
    render(request,'blog/main.html')