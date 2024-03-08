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
        uname=request.POST['username']#entered uname
        enteredpwd=request.POST['password']#entered pwd
        form=loginForm(request.POST)
        if form.is_valid():
            try:
                user = userModel.objects.get(username=uname)
                encrypted_password=user.password

                pwdstatus=passlib_encryption_verify(enteredpwd,encrypted_password)
                if pwdstatus==False:
                    messages.error(request, "Incorrect password. Please try again.")
                else:
                    slug=user.slug
                    # print(slug)
                    return HttpResponseRedirect(reverse('homepage', args=[slug]))
            except ObjectDoesNotExist:
                messages.error(request, "User does not exist.Please try again.")
    return render(request,'todoapp/login.html',{'form':form})


def signup_view(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            firstname=request.POST['firstname']
            lastname=request.POST['lastname']
            username=request.POST['username']
            password=request.POST['password']
            epwd=passlib_encryption(password)
            phone=request.POST['phone']
            email=request.POST['email']
            userModel.objects.create(firstname=firstname,lastname=lastname,username=username,password=epwd,phone=phone,email=email)
            messages.success(request,"Account created successfully, Please login")
            return redirect('login')
    return render(request,'todoapp/signup.html',{'form':form,})


from passlib.hash import pbkdf2_sha256

def passlib_encryption(raw_password):
	"""
	Here, Encryption is Using passlib Library.
	"""
	if raw_password:
		encrypted = pbkdf2_sha256.hash(raw_password)
	else:
		encrypted = None
	
	return encrypted

def passlib_encryption_verify(raw_password, enc_password):
	""" 
	@returns TRUE or FALSE 
	"""
	if raw_password and enc_password:
		# verifying the password
		response = pbkdf2_sha256.verify(raw_password, enc_password)
	else:
		response = None
	
	return response



def homepage_view(request,slug):
    obj=userModel.objects.get(slug=slug)
    tasks=task.objects.filter(user=obj).order_by('date')# here obj refering to user object from usermodel 

    return render(request,'todoapp/homepage.html',{'obj':obj,'tasks':tasks})

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
    return render(request,'todoapp/addtask.html',{'form':form,'obj':obj})

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