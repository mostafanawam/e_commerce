from django.contrib import admin

from .models import *

from users.forms import CustomUserCreationForm
from cart.views import send_email


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

    actions = [
        # 'delivery_notify',
        'reminder_email'
    ]
    def reminder_email(self, request, queryset):
        for obj in queryset:
            html=f"""<p>Dear Customer,</p>
                <p>We noticed you recently visited petsnclaws.com thank you for stopping by! Your pet's well-being is important to us, and we believe they deserve the best in supplements and food.</p>
                <p>If you haven't had a chance to make a purchase yet, now is the perfect time! Our selection is tailored to enhance your pet's health and happiness.</p>
                <p>Explore our website again and treat your furry friend to something special. Remember, we're here to make your pet parenting journey enjoyable and worry-free.</p>
                <p>Visit petsnclaws.com now and make your pet's day extraordinary!</p>
                <p>Thanks for choosing PetsNClaws. Here's to happy, healthy pets!</p>
                <p>Best Regards,<br>PetsNClaws Customer Service Team</p>
                """
            if(obj.email):
                email=obj.email
            else:
                email=obj.user.email
            try:
                send_email(f'PetsNClaws - Reminder',html,email)
            except Exception as e:
                print(f"received_order:email didnt send,{e}")   
  
admin.site.register(Customer,CustomerAdmin)
