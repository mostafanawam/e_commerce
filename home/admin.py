from django.contrib import admin
from .models import *
# Register your models here.


class GalleryAdmin(admin.ModelAdmin):  
    list_display = ("id","name")
admin.site.register(Gallery,GalleryAdmin)


class BrandsAdmin(admin.ModelAdmin):  
    list_display = ("id","name")
admin.site.register(Brands,BrandsAdmin)

class ContactUsAdmin(admin.ModelAdmin):  
    list_display = ("id","name","email","subject")
admin.site.register(ContactUs,ContactUsAdmin)



class SocialLinksAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'link',
        'icon',
        'color'
    )
admin.site.register(SocialLinks, SocialLinksAdmin)