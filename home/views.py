from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import *
from cart.views import send_email
from settings.models import Settings
from .models import *
import django_filters

def homepage(request):
     
    products = Product.objects.filter(status__name="suggested").order_by('rank')

    gallery=Gallery.objects.all()
    brands=Brands.objects.all()

    cart = request.session.get('cart', [])
    settings=Settings.objects.get()

    sale_products=Product.objects.filter(status__name="promotion").order_by('rank')

    cats=Category.objects.all()

    total_qty=0
    for item in cart:
        total_qty+=item['qty']

    context = {
        'sale_products':sale_products,
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
    sub_category= django_filters.CharFilter(field_name='sub_category__name', lookup_expr='exact')
    class Meta:
        model = Product
        fields = ['category','brand']
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def productsPage(request):

    # categories = Category.objects.prefetch_related('subcategory_set').all()
    # print(categories)
    categories=Category.objects.all()
    # for cat in categories:
    #     for subcategory in category.subcategory_set.all

    sub_cat=SubCategory.objects.all()

    items_per_page = 12

    page= request.GET.get('page', 1)
     
    queryset=Product.objects.filter(status__listed=True).order_by('rank')
    
    filter = ProductFilter(request.GET,queryset=queryset)

    paginator = Paginator(filter.qs, items_per_page)

    try:
        paginated_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        paginated_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        paginated_items = paginator.page(paginator.num_pages)


    cart = request.session.get('cart', [])

    total_qty=0
    for item in cart:
        total_qty+=item['qty']

    settings=Settings.objects.get()
    context = {
        'products': paginated_items,
        "cart":cart,
        'total_qty':total_qty,
        'currency':settings.currency,
        "categories":categories,
        'paginated_items': paginated_items,
        'sub_cat':sub_cat
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

        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).order_by('rank')

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