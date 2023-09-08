from django.contrib import admin

from .models import *

from users.forms import CustomUserCreationForm


admin.site.unregister(Group)
class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fields = [
        'first_name','last_name',
        # 'phone',
        'email','password','is_staff','is_superuser','is_enabled'
    ]
    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_enabled',
        # 'phone',
        # 'is_active',
        'is_superuser',
        'last_login',
    ) 
    list_filter = ('is_staff',)
admin.site.register(User, UserAdmin)
