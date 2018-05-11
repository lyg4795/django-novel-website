from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserForm,LoginForm

def registe_view(req):
    if req.method=='POST':
        form=UserForm(req.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            enpassword=form.cleaned_data['enpassword']
            user=authenticate(username=username,email=email,password=password)
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            context={'title':'注册','status':'成功'}
            return render(req,'redirect.html',context=context)
    else:
        form=UserForm()
    return render(req,'login/registe.html',context={'form':form,'value':'注册'})

def login_view(req):
    if req.method=='POST':
        form=LoginForm(req.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user:
                context={'title':'登录','status':'成功'}
                login(req,user)
                return render(req,'redirect.html',context=context)
            else:
                context = {'title': '登录', 'status': '失败'}
                return render(req, 'redirect.html', context=context)
    else:
        form=LoginForm()
    return render(req,'login/login.html',context={'form':form,'value':'登录'})
def logout_view(req):
    logout(req)
    context = {'title': '退出', 'status': '成功'}
    return render(req,'redirect.html',context=context)
# Create your views here.
