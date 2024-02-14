from django import forms
from todoApp.models import userModel,task
from django.core import validators
from datetime import date

class loginForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=userModel
        fields=('username','password')

class SignUpForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    reenter_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=userModel
        fields=('firstname','lastname','username','password','phone','email')

    def clean(self):
        total_data=super().clean()
        fname=total_data['firstname']
        lname=total_data['lastname']
        uname=total_data['username']
        pwd=total_data['password']
        rpwd=total_data['reenter_password']
        email=total_data['email']
        phone=total_data['phone']

        if len(fname)<3:
            raise forms.ValidationError("Minimum Length of the first name should be 3 characters")
        
        if uname==fname :
            raise forms.ValidationError("username couldn't be same as firstname")
        if pwd!=rpwd:
            raise forms.ValidationError("Both passwords should match")
        if pwd==uname:
            raise forms.ValidationError("Please choose different password")
        if len(str(phone))<8:
            raise forms.ValidationError("Please enter correct phone number")


class taskform(forms.ModelForm):
    class Meta:
        model=task
        fields=('title','description','date')

    def clean(self):
        total_data=super().clean()
        date=total_data['date']
        todays_date=date.today()
        if date<todays_date:
            raise forms.ValidationError("Enter future date")

