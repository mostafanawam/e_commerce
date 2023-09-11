from django.db import models

# python manage.py dumpdata settings.Settings --output settings/fixtures/Settings.test.json
class Settings(models.Model):
    currency=models.CharField(max_length=5,default='$')
    delivery=models.DecimalField(decimal_places=2,max_digits=5,default=3)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    reciever_email=models.EmailField(max_length=50)
    admin_link=models.CharField(max_length=50,null=True,blank=True)
    # def __str__(self):
    #     return self.name

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"