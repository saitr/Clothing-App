from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from cloudinary.models import CloudinaryField
import secrets
# Create your models here.

#Common Fields for every table

class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=False,null=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False,null=False)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = models.CharField(max_length=250,null=True,blank=True,unique=True)
    password = models.CharField(max_length=100,null=False,blank=False)
    phone_number = models.IntegerField(null=True,blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=250)
    jwt_token = models.CharField(max_length=250,unique=True,null=True)
    token = models.CharField(max_length=100,unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    display_picture = CloudinaryField('Display Picture',null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS =['username','phone_number']
    class Meta:
        db_table = 'User'
    
    # function to create a token 
    def save_token(self, *args, **kwargs):
        if not self.token:
            # generate new token if none exists
            self.token = secrets.token_urlsafe(32)

        super().save(*args, **kwargs)

    
    def update_token(self):
        self.token = None
        self.token_created = None
        self.token_expires = None
        self.save()
