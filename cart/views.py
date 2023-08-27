from django.shortcuts import render

# Create your views here.



from django.shortcuts import render, redirect
from django.http import JsonResponse
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
        'id': product.id,
        'title': product.name,
        'price': str(product.price),
    })
    request.session.modified = True
    
    return HttpResponse(len(cart))

def view_cart(request):
    cart = request.session.get('cart', [])
    total = sum(float(item['price']) for item in cart)
    
    context = {
        'cart': cart,
        'total': total,
    }
    return render(request, 'view_cart.html', context)
