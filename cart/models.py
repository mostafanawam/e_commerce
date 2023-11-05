from django.db import models
from django_resized import ResizedImageField

from home.models import Brands


# python manage.py dumpdata cart.Status --output cart/fixtures/Status.test.json
class Status(models.Model):
    name = models.CharField(max_length=100)
    listed=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"


def uploadCat(object,filename):
    try:
        import pathlib
        file_extension = pathlib.Path(filename).suffix
        return f'categories/{object.name}{file_extension}'

    except Exception as e:
        print(f"error uploading id to minio,{e}")

# python manage.py dumpdata cart.Category --output cart/fixtures/Category.static.json
class Category(models.Model):
    name = models.CharField(max_length=100)
    image=ResizedImageField(upload_to=uploadCat,null=True,blank=True)

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
        



TEXT_COLOR = [
        ('green', 'green'),
        ('text-black', 'text-black'),
        ('text-white', 'text-white'),
]


# python manage.py dumpdata cart.Product --output cart/fixtures/Product.test.json
class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,null=True,blank=True)
    image=ResizedImageField(upload_to=uploadedform)
    status=models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        default=1
    )
    stock = models.IntegerField()
    color=models.CharField(max_length=50, choices=TEXT_COLOR,default='text-black')
    brand=models.ForeignKey(
        Brands,
        on_delete=models.PROTECT,
        null=True,blank=True

    )
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Products"



class Order(models.Model):
    order_id=models.CharField(max_length=15)
    customer = models.ForeignKey(
        "users.Customer", on_delete=models.PROTECT,
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address= models.ForeignKey(
        "users.Address", on_delete=models.PROTECT
    )
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.order_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()

