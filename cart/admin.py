from django.contrib import admin

from cart.views import send_email
from settings.models import Settings

# Register your models here.
from .models import *



class CategoryAdmin(admin.ModelAdmin):  
    list_display = ("id","name")
admin.site.register(Category,CategoryAdmin)


from import_export import resources

from import_export.admin import ImportExportModelAdmin
class MyModelResource(resources.ModelResource):
    class Meta:
        model = Product
        
        
class ProductAdmin(ImportExportModelAdmin):  
    resource_class = MyModelResource
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

class SubCategoryAdmin(admin.ModelAdmin):  
    list_display = ("id","category",'name')
admin.site.register(SubCategory,SubCategoryAdmin)


class OrderItemInline(admin.TabularInline):  # or admin.StackedInline for more vertical layout
    model = OrderItem
    extra = 0  # Number of empty forms shown by default
    readonly_fields = ('product', 'quantity')  # optional, make fields read-only if needed
    can_delete = False  # optional, prevent deleting from inline

class OrderAdmin(admin.ModelAdmin):  
    list_display = (
        "id",
        "order_id",
        "customer",
        "total_price",
        'delivery',
        "address",
        'isReceived',
        "order_date"
    )
    list_filter=["customer"]
    inlines = [OrderItemInline]  # ✅ Add this line

    actions = [
        # 'delivery_notify',
        'received_order'
    ]


    def received_order(self, request, queryset):
        settings=Settings.objects.get()
        instagram=settings.instagram
        for obj in queryset:
            if(not obj.isReceived):
                html=f"""<p>Dear Customer,</p>
                <p>Exciting news! Your pet's treats from PetsNClaws have just arrived. We hope they love them!</p>
                <p>Share your experience with us by leaving a quick review on our social media platforms. Got a cute pic? Spread the joy on Instagram, mentioning us @{instagram} and using #PetJoy. Your pet might even become a star on our page!</p>
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

