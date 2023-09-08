from django.contrib import admin

# Register your models here.
from .models import *



class CategoryAdmin(admin.ModelAdmin):  
    list_display = ("id","name","description")
admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):  
    list_display = ("id","name","description","price","status","category")

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
