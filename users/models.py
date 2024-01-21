from django.db import models
from django.conf import settings
from django.shortcuts import reverse, redirect
from django.utils import timezone
from django_countries.fields import CountryField  
import string
import random
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):

    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True) 

    is_employer = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)

    has_resume = models.BooleanField(default=False)
    has_company = models.BooleanField(default=False)

