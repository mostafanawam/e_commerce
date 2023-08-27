from django.contrib import admin

# Register your models here.
from .models import *



class CategoryAdmin(admin.ModelAdmin):  
    list_display = ("id","name","description")
admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):  
    list_display = ("id","name","description","price","status","category")
admin.site.register(Product,ProductAdmin)

class StatusAdmin(admin.ModelAdmin):  
    list_display = ("id","name")
admin.site.register(Status,StatusAdmin)


