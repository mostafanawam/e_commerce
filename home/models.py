from django.db import models

# Create your models here.

from django_resized import ResizedImageField




def uploadedform(object,filename):
    try:
        # import pathlib
        # file_extension = pathlib.Path(filename).suffix
        return f'gallery/{filename}'

    except Exception as e:
        print(f"error uploading id to minio,{e}")


class Gallery(models.Model):
    image = ResizedImageField(null=True,blank=True,upload_to=uploadedform)

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Gallery"