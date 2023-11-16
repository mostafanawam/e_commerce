from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import *
from cart.views import send_email
from settings.models import Settings
from .models import *
import django_filters

def homepage(request):
     
    products = Product.objects.filter(status__name="suggested")

    gallery=Gallery.objects.all()
    brands=Brands.objects.all()

    cart = request.session.get('cart', [])
    settings=Settings.objects.get()


    cats=Category.objects.all()

    total_qty=0
    for item in cart:
        total_qty+=item['qty']

    context = {
        'products': products,
        'gallery':gallery,
        'brands':brands,
        "cart":cart,
        'delivery':settings.delivery,
        'currency':settings.currency,
        'total_qty':total_qty,
        'cats':cats
    }
    return render(request, 'home.html',context)



class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='exact')
    brand= django_filters.CharFilter(field_name='brand__name', lookup_expr='exact')
    class Meta:
        model = Product
        fields = ['category','brand']

def productsPage(request):

    categories=Category.objects.all()
    
    filter = ProductFilter(request.GET, queryset=Product.objects.filter(status__listed=True))
    cart = request.session.get('cart', [])

    total_qty=0
    for item in cart:
        total_qty+=item['qty']

    settings=Settings.objects.get()
    context = {
        'products': filter.qs,
        "cart":cart,
        'total_qty':total_qty,
        'currency':settings.currency,
        "categories":categories
    }
    return render(request, 'products.html',context)

def contactUs(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact_us=ContactUs.objects.create(
            name=fullname,
            email=email,
            subject=subject,
            message=message
        )
        try:
            settings=Settings.objects.get()
            html_message=f"""
                <h3>Hello Dear, <br> 
                You have a new message from {fullname} having the email: {email}<br>
                message subject:{subject} <br>
                Message content:{message}<br>
                <a style="color:#83B641" href="{settings.admin_link}/home/contactus/{contact_us.pk}/change/" >Click here</a> for more details
                </h3>
            """
            send_email(f"New Message from {fullname}",html_message,settings.reciever_email)
        except Exception as e:
            print(f"email didnt send,{e}")

        context={
            "success":'success',
        }
        return JsonResponse(context)
    cart = request.session.get('cart', [])

    total_qty=0
    for item in cart:
        total_qty+=item['qty']

    context = {
        "cart":cart,
        'total_qty':total_qty
    }

    return render(request, 'contact_us.html',context)


from django.db.models import Q
def searchProducts(request):
    if request.method == 'POST':
        query = request.POST['query']

        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

        cart = request.session.get('cart', [])
        total_qty=0
        for item in cart:
            total_qty+=item['qty']
            
        settings=Settings.objects.get()
        context = {
        'total_qty':total_qty,
            'products': products,
            "cart":cart,
            "query":query,
                    'currency':settings.currency,

        }

        return render(request, 'search_products.html',context)
    
def productDetails(request,pk):


    cart = request.session.get('cart', [])
    total_qty=0
    for item in cart:
        total_qty+=item['qty']

    product=Product.objects.get(pk=pk)
    settings=Settings.objects.get()

    description=product.description.split("\n")
    context = {
        'total_qty':total_qty,
        "cart":cart,
        'product':product,
        'currency':settings.currency,
        'description':description

    }

    return render(request, 'product_details.html',context)
    # for category in categories:
    #     products = Product.objects.filter(status__listed=True,category=category)
    #     if(products.count()> 0):
    #         products_list[category.name]=products