from django.contrib import admin

# Register your models here.

from .models import *


class SettingsAdmin(admin.ModelAdmin):  
    list_display = ("id","currency","delivery","email","reciever_email","phone","instagram")
admin.site.register(Settings,SettingsAdmin)