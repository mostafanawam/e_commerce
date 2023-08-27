from django.db import models

# Create your models here.
from django.db import models





# python manage.py dumpdata cart.Status --output cart/fixtures/Status.test.json
class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"



# python manage.py dumpdata cart.Category --output cart/fixtures/Category.test.json
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categories"
        verbose_name_plural = "Categories"


def uploadedform(object,filename):
    try:
        import pathlib
        file_extension = pathlib.Path(filename).suffix
        return f'products/{object.name}/{object.name}{file_extension}'

    except Exception as e:
        print(f"error uploading id to minio,{e}")
        

from django_resized import ResizedImageField

# python manage.py dumpdata cart.Product --output cart/fixtures/Product.test.json
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    image=ResizedImageField(null=True,blank=True,upload_to=uploadedform)
    status=models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True,blank=True,default=1
    )
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Products"

class Order(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)