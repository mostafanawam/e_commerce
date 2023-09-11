from django.contrib import admin

from .models import *

from users.forms import CustomUserCreationForm


admin.site.unregister(Group)
class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fields = [
        'email','password','is_staff','is_superuser','is_enabled'
    ]
    list_display = (
        'id',
        'email',
        'is_staff',
        'is_enabled',
        'is_superuser',
        'last_login',
    ) 
    list_filter = ('is_staff',)
admin.site.register(User, UserAdmin)



class AddressAdmin(admin.ModelAdmin):  
    list_display = (
        "id",
        "region",
        "address",
        "phone_number",
        "note"
    )
admin.site.register(Address,AddressAdmin)

class RegionsAdmin(admin.ModelAdmin):  
    list_display = (
        "id",
        "name",

    )
admin.site.register(Regions,RegionsAdmin)



class CustomerAdmin(admin.ModelAdmin):  
    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
        # "address"

    )
admin.site.register(Customer,CustomerAdmin)
