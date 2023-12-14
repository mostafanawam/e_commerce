from django.contrib import admin

from cart.views import send_email

# Register your models here.
from .models import *



class CategoryAdmin(admin.ModelAdmin):  
    list_display = ("id","name")
admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):  
    list_display = (
        "id",
        "name",
        "brand",
        "old_price",
        "price",
        "stock",
        "status",
        'color',
        "category"
    )

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
        'isReceived',
        "order_date"
    )
    list_filter=["customer"]

    actions = [
        # 'delivery_notify',
        'received_order'
    ]


    def received_order(self, request, queryset):
        for obj in queryset:
            if(not obj.isReceived):
                html=f"""<p>Dear Customer,</p>
                <p>Exciting news! Your pet's treats from PetsNClaws have just arrived. We hope they love them!</p>
                <p>Share your experience with us by leaving a quick review on our social media platforms. Got a cute pic? Spread the joy on Instagram, mentioning us @pets_n_claws.lb and using #PetJoy. Your pet might even become a star on our page!</p>
                <p>Thanks for choosing PetsNClaws. Here's to happy, healthy pets!</p>
                <p>Best Regards,<br>PetsNClaws Customer Service Team</p>
                """

                if(obj.customer.email):
                    email=obj.customer.email
                else:
                    email=obj.customer.user.email
                try:
                    send_email(f'PetsNClaws - Order Received',html,email)
                except Exception as e:
                    print(f"received_order:email didnt send,{e}")   
                obj.isReceived=True
                obj.save()

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
