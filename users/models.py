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
    email = models.EmailField(max_length=250, unique=True,null=True,blank=True)
    password = models.CharField(max_length=250,null=True,blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True,null=True,blank=True)
    last_login = models.DateTimeField(verbose_name='last login',auto_now_add=True,null=True,blank=True)
    is_staff = models.BooleanField(default=False,null=True,blank=True)    # admin
    is_enabled = models.BooleanField(default=True,null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password',]

    objects = UserAccountManager()

    def __str__(self):
        return f"{self.email}"
  
    
    def has_module_perms(self, app_label):
        return True

    class Meta:
        ordering = ['id']



class Customer(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,blank=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.ManyToManyField(
        "users.Address",blank=True
    )
    email=models.CharField(null=True,blank=True,max_length=100)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Customers"
        verbose_name_plural = "Customers"



# python manage.py dumpdata users.Regions --output users/fixtures/Regions.test.json
class Regions(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Regions"
        verbose_name_plural = "Regions"


class Address(models.Model):
    region=models.ForeignKey(
        Regions,
        on_delete=models.CASCADE
    )
    address=models.TextField()
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    note=models.TextField()

    def __str__(self):
        return self.address
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Address"
    
