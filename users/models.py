from django.db import models
from datetime import datetime,timedelta

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,Group
from django.contrib.auth.models import PermissionsMixin,Permission







class UserAccountManager(BaseUserManager):
    use_in_migrations = True
    

    def create_user(self, username,email, password=None):
        if not username:
            raise ValueError("Username invalid")
        if not email:
            raise ValueError("Email invalid")

        user = self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password):
        user = self.create_user(username=username,email=email,password=password)
        # user.is_active = True
        # user.is_admin = True
        # user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user




from django.core.files.storage import default_storage
import os
from django.core.files.storage import FileSystemStorage





# python manage.py dumpdata users.user --output users/fixtures/users.test.json
class User(AbstractBaseUser, PermissionsMixin):
    """ BmUser model """

    username = models.CharField(blank=True, null=True,max_length=20,unique=True,)
    first_name = models.CharField(blank=True, null=True,max_length=50,unique=False,)
    father_name = models.CharField(blank=True, null=True,max_length=50,unique=False,)
    last_name = models.CharField(blank=True, null=True,max_length=50,unique=False)
    first_name_en = models.CharField(blank=True, null=True,max_length=50,unique=False,)
    father_name_en = models.CharField(blank=True, null=True,max_length=50,unique=False,)
    last_name_en = models.CharField(blank=True, null=True,max_length=50,unique=False)
    email = models.EmailField(max_length=250, unique=True,null=True,blank=True)
    password = models.CharField(max_length=250,null=True,blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True,null=True,blank=True)
    last_login = models.DateTimeField(verbose_name='last login',auto_now_add=True,null=True,blank=True)
    phone=models.CharField(max_length=50,null=True,blank=True,unique=True)              
    # is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False,null=True,blank=True)    # admin
    is_enabled = models.BooleanField(default=True,null=True,blank=True)
    isAdmin=models.BooleanField(default=False,null=True,blank=True)
    # upload_to=user_directory_path,
    # is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'email']

    objects = UserAccountManager()

    def __str__(self):
        if(self.fullName()):
            return f"{self.fullName()}"
        else:
            return "user"
    
    def fullName(self):
        name=""
        if(self.first_name):
            name+=self.first_name+" "

        if(self.father_name):
            name+=self.father_name+" "

        if(self.last_name):
            name+=self.last_name

        return name
    

    

    def has_module_perms(self, app_label):
        return True
    
    
    class Meta:
        ordering = ['id']



