from django.contrib import admin

from cart.views import send_email

# Register your models here.
from .models import *



class CategoryAdmin(admin.ModelAdmin):  
    list_display = ("id","name")
admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):  
    list_display = ("id","name","description","price","stock","status",'color',"category")

    list_filter=["category","status"]
admin.site.register(Product,ProductAdmin)

class StatusAdmin(admin.ModelAdmin):  
    list_display = ("id","name")
admin.site.register(Status,StatusAdmin)



class OrderAdmin(admin.ModelAdmin):  
    list_display = (
        "id",
        "order_id",
        "customer",
        "total_price",
        "address",
        "order_date"
    )
    list_filter=["customer"]

    actions = ['delivery_notify']


    def delivery_notify(self, request, queryset):
        for obj in queryset:
            html=f"""
                <h3>Dear {obj.customer.first_name} {obj.customer.last_name} </h3>
                <p>Your order with id=#{obj.pk} is now with the delivery company</p>
            """
            if(obj.customer.email):
                email=obj.customer.email
            else:
                email=obj.customer.user.email
            try:
                send_email(f'PetsNClaws Order Update',html,email)
            except Exception as e:
                print(f"email didnt send,{e}")                         
admin.site.register(Order,OrderAdmin)



class OrderItemAdmin(admin.ModelAdmin):  
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
    )
    list_filter=["order","order__customer","product"]
admin.site.register(OrderItem,OrderItemAdmin)
