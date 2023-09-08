from django.shortcuts import render, redirect
from django.http import JsonResponse
from settings.models import Settings
from .models import Product



def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', [])
    context = {
        'products': products,
        'cart_count': len(cart),
    }
    return render(request, 'product_list.html', context)



def product_details(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.session.get('cart', [])

    context = {
        'product': product,
        'cart_count': len(cart),
    }
    return render(request, 'product_details.html', context)


from django.http import HttpResponse

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if 'cart' not in request.session:
        request.session['cart'] = []
    
    cart = request.session['cart']
    cart.append({
        'id': product.pk,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'image': product.image.url,
        'qty':1
    })
    request.session.modified = True
    
    return HttpResponse(len(cart))

def view_cart(request):
    cart = request.session.get('cart', [])
    total_price = sum(float(item['price']) for item in cart)
    
    settings=Settings.objects.get()
    context = {
        'cart': cart,
        'total_price': total_price,
        "settings":settings
    }
    return render(request, 'view_cart.html', context)

def empty_cart(request):
    if(request.method == 'POST'):
        if 'cart'  in request.session:
            del request.session['cart']

        return redirect('/cart')

def remove_from_cart(request,id):
    cart = request.session.get('cart', [])

    # Remove the item at the specified index
    del cart[id-1]

    # Update the session with the modified cart
    request.session['cart'] = cart

    return redirect('/cart')


from decimal import Decimal
def checkout(request):
    cart = request.session.get('cart', [])
    total_price = sum(float(item['price']) for item in cart)
    
    settings=Settings.objects.get()

    context = {
        'cart': cart,
        'total_price': total_price,
        "settings":settings,
        "grand_total":Decimal(total_price)+settings.delivery
    }
        
    return render(request, 'checkout.html', context)