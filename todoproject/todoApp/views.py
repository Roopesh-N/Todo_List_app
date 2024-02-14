from django.shortcuts import render,redirect,HttpResponseRedirect
from todoApp.forms import loginForm,SignUpForm,taskform
from .models import userModel,task
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def login_view(request):
    form=loginForm()
    if request.method=='POST':
        uname=request.POST['username']#entered username
        epwd=request.POST['password']#entered password
        form=loginForm(request.POST)
        if form.is_valid():
            try:
                user = userModel.objects.get(username=uname)
                if epwd != user.password:
                    messages.error(request, "Incorrect password. Please try again.")
                else:
                    slug=user.slug
                    # print(slug)
                    return HttpResponseRedirect(reverse('homepage', args=[slug]))
            except ObjectDoesNotExist:
                messages.error(request, "User does not exist.Please try again.")
    return render(request,'todoApp/login.html',{'form':form})


def signup_view(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully, Please login")
            return redirect('login')
    return render(request,'todoApp/signup.html',{'form':form,})



def homepage_view(request,slug):
    obj=userModel.objects.get(slug=slug)
    tasks=task.objects.filter(user=obj).order_by('date')# here obj refering to user object from usermodel 

    return render(request,'todoApp/homepage.html',{'obj':obj,'tasks':tasks})

def addtask_view(request,slug):
    obj=userModel.objects.get(slug=slug)
    form=taskform()
    if request.method=='POST':
        form=taskform(request.POST)
        if form.is_valid():
            title=request.POST['title']
            description=request.POST['description']
            date=request.POST['date']
            task.objects.create(user=obj,title=title,description=description,date=date)
            return HttpResponseRedirect(reverse('homepage', args=[slug]))
    return render(request,'todoApp/addtask.html',{'form':form,'obj':obj})

def updatetask_view(request,slug,title):
    userobj=userModel.objects.get(slug=slug)
    usertask=task.objects.get(title=title, user=userobj)
    form=taskform(instance=usertask)
    if request.method=='POST':
        form=taskform(request.POST,instance=usertask)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('homepage', args=[slug]))

    return render(request,'todoapp/updatetask.html',{'form':form})

def remove_view(request,slug,title):
    userobj=userModel.objects.get(slug=slug)
    usertask=task.objects.get(title=title, user=userobj)
    print(f"Deleted {title} from todo list")
    usertask.delete()
    return HttpResponseRedirect(reverse('homepage', args=[slug]))