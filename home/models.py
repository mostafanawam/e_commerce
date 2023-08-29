from django.db import models

# Create your models here.

from django_resized import ResizedImageField




def uploadedform(object,filename):
    try:
        import pathlib
        file_extension = pathlib.Path(filename).suffix
        return f'gallery/{object.name}{file_extension}'

    except Exception as e:
        print(f"error uploading gallery,{e}")

def uploadbrand(object,filename):
    try:
        import pathlib
        file_extension = pathlib.Path(filename).suffix
        return f'brands/{object.name}{file_extension}'

    except Exception as e:
        print(f"error uploading brand,{e}")


class Gallery(models.Model):
    name=models.CharField(max_length=100)
    image = ResizedImageField(upload_to=uploadedform)

    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Gallery"


class Brands(models.Model):
    name=models.CharField(max_length=100)
    image = ResizedImageField(upload_to=uploadbrand)
    
    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = "Brands"
        verbose_name_plural = "Brands"