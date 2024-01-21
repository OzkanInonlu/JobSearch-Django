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

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]