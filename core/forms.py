from site import venv
from django import forms
from django.shortcuts import render, HttpResponse
from .models import *
from django_countries.fields import CountryField       
from django_countries.widgets import CountrySelectWidget
from .models import *
import string, random
import numpy as np
import os
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class RegisterForm(UserCreationForm):
    #email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={"id":"email", 'class': "form-control"}))
    class Meta:
        model = get_user_model()
        fields = ["email", "password1", "password2"]

        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        #self.fields['username'].widget.attrs['class'] = 'form-control'
        #self.fields['username'].widget.attrs['id'] = 'username'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['id'] = 'email'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['id'] = 'password1'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['id'] = 'password2'

    # def clean(self): #django'nun form methodu parola doğrulamak için

    #     email = self.cleaned_data['email']

    #     #username = self.cleaned_data.get('email')

    #     password = self.cleaned_data['password1']

    #     confirmPassword = self.cleaned_data['password2']

    #     if (email and password and confirmPassword) and (password != confirmPassword):
    #         raise forms.ValidationError(_("Passwords are not matched, please try again."))

    #     elif (email and password and confirmPassword) and (email in password):
    #         raise forms.ValidationError(_("Your password is too similar to your username, please try again."))
        
    #     elif (email and password and confirmPassword) and (len(password)<10):
    #         raise forms.ValidationError(_("Your password is too short and insecure, please try again."))
            
    #     else:
    #         module_dir = os.path.dirname(__file__)  
    #         file_path = os.path.join(module_dir, 'common-passwords.txt')   #full path to text.
    #         with open(file_path,"r") as f:
    #             for p in f.readlines():
    #                 p = p.strip()
    #                 if password == p:
    #                     raise forms.ValidationError(_("Your password is too common and insecure, please try again."))
                        
    #         values = {"email": email, "password": password}

    #         return values
        
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if UserModel.objects.filter(email=email).exists():
    #         raise forms.ValidationError(_("The email address you've chosen has been already taken, please enter another."))
    #     return email

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if UserModel.objects.filter(username=username).exists():
    #         raise forms.ValidationError(_("The username you've chosen has been already taken, please enter another."))
    #     return username
        

# UserModel = get_user_model()
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={"id":"email", 'class': "form-control"}))

    password = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={"id":"password", 'class': "form-control"}))


#company is already created for the employers, just enter the details of it
class UpdateCompanyForm(forms.Form):
    company_name = forms.CharField(required=False, max_length=120, widget=forms.TextInput(attrs={"class":"form-control",
     "placeholder":"ABC Company"}))
    establishment_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "form-control", "id":"establishment_date", 'type':'date'}))
    city_option = forms.ChoiceField(required=False, widget=forms.Select, choices=CITIES)
    state = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class": "form-control",
    "placeholder":"Hursit Bey sk", "id":"state"}))    



class UpdateResumeForm(forms.Form):
    first_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={"class":"form-control",
     "placeholder":"Ozkan"}))
    last_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={"class":"form-control",
     "placeholder":"Inonlu"}))
    nationality = CountryField(blank_label='Select Nationality').formfield(required=False, widget = CountrySelectWidget(attrs={"class": "custom-select d-block w-100"}))

    job_title = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class":"form-control",
     "placeholder":"Backend Developer"}))

class CreateJobAdvertForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control",
     "placeholder":"Frontend Dev"}))
    
    location = forms.ChoiceField(widget=forms.Select(), choices=CITIES)

    job_type = forms.ChoiceField(widget=forms.Select(), choices=JOB_TYPES)

    #industry = forms.ChoiceField(widget=forms.Select(), choices=tuple(Industry.objects.values_list('name', flat=True)))

    min_salary = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control",
     "placeholder":"1 $"}))

    max_salary = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control",
     "placeholder":"1 $"}))
    
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={"class":"form-control",
    "placeholder":" Description: We are looking for...", "rows":4}))

    is_available = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={"class":"form-check-input"}))


class UpdateJobAdvertForm(forms.Form):
    title = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    location = forms.ChoiceField(widget=forms.Select(), choices=CITIES)

    job_type = forms.ChoiceField(widget=forms.Select(), choices=JOB_TYPES)

    min_salary = forms.IntegerField(required=False, widget=forms.TextInput(attrs={"class":"form-control",
    }))

    max_salary = forms.IntegerField(required=False, widget=forms.TextInput(attrs={"class":"form-control",
     }))
    
    description = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={"class":"form-control",
    }))

    is_available = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class":"form-check-input"}))

class ForgotPasswordForm(forms.Form):
    user_email = forms.EmailField(required=False, max_length=50, widget=forms.EmailInput(attrs={ "class":"form-control", "id":"email"}))
    user_phone_no = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={ "class":"form-control", "id":"phone_no", "placeholder":"+90 548 880 25 89"}))


class EmailChangingForm(forms.Form):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={"id":"email", 'class': "form-control"}))


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={"id":"old_password", 'class': "form-control", "type":"password"}))
    new_password1 = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={"id":"new_password1", 'class': "form-control", "type":"password"}))
    new_password2 = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={"id":"new_password2", 'class': "form-control", "type":"password"}))

    class Meta:
        model=UserModel
        fields={"old_password", "new_password1", "new_password2"}
