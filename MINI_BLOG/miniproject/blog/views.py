from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm,LoginForm,PostFrom
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Podt
from django.contrib.auth.models import Group


# Create your views here.
def home(request):
    post=Podt.objects.all()
    return render(request,'blog/home.html',{'post':post})

def about(request):
    return render(request,'blog/about.html')


def contact(request):
    return render(request,'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        post=Podt.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':post,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

#signup
def user_signup(request):
    if request.method == "POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! You have Become an Authot')
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        
        form=SignupForm()
    
    return render(request,'blog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form=LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
            
        else:
            
            form=LoginForm()
        return render(request,'blog/login.html',{'form':form})
        
    else:
        return HttpResponseRedirect('/dashboard/')
        
  
    
    


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=PostFrom(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=Podt(title=title,desc=desc)
                pst.save()
                form=PostFrom()
                
        else:
            form=PostFrom()       
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi=Podt.objects.get(pk=id)
            form=PostFrom(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi=Podt.objects.get(pk=id)
            form=PostFrom(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
def delete(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi=Podt.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')