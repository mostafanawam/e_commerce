from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import *
from cart.views import send_email
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