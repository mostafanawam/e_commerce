from django.shortcuts import render

# Create your views here.
from cart.models import *
from settings.models import Settings
from .models import *


def homepage(request):
     
    products = Product.objects.filter(status__name="suggested")

    gallery=Gallery.objects.all()
    brands=Brands.objects.all()

    cart = request.session.get('cart', [])
    settings=Settings.objects.get()
    
    context = {
        'products': products,
        'gallery':gallery,
        'brands':brands,
        "cart":cart,
        'delivery':int(settings.delivery),
        'currency':settings.currency
    }
    return render(request, 'home.html',context)

def productsPage(request):

    categories=Category.objects.all()

    products_list={}

    for category in categories:
        products = Product.objects.filter(status__listed=True,category=category)
        if(products.count()> 0):
            products_list[category.name]=products

    cart = request.session.get('cart', [])
    context = {
        'products': products_list,
        "cart":cart,
        # "categories":categories
    }

    return render(request, 'products.html',context)

def contactUs(request):
    cart = request.session.get('cart', [])
    context = {
        "cart":cart,
    }

    return render(request, 'contact_us.html',context)


from django.db.models import Q
def searchProducts(request):
    if request.method == 'POST':
        query = request.POST['query']

        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))


        cart = request.session.get('cart', [])
        context = {
            'products': products,
            "cart":cart,
            "query":query
        }

        return render(request, 'search_products.html',context)