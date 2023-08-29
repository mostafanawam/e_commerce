from django.shortcuts import render

# Create your views here.
from cart.models import *
from .models import *


def homepage(request):
     
    products = Product.objects.filter(status__name="suggested")

    gallery=Gallery.objects.all()
    brands=Brands.objects.all()
    context = {
        'products': products,
        'gallery':gallery,
        'brands':brands
    }
    return render(request, 'home.html',context)

def productsPage(request):
    return render(request, 'products.html')

