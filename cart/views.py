from django.shortcuts import render, redirect
from django.http import JsonResponse
from settings.models import Settings
from users.models import Address, Customer, Regions
from .models import Order, OrderItem, Product
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
    if(len(cart)==0):
        return redirect("/products/")
    if(request.method == 'POST'):
        user=None
        if request.user.is_authenticated:
            user=request.user
        else:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']

            phone = request.POST['phone']
            region=request.POST['region']
            address=request.POST['address']

            note = request.POST['note']

        
            region=Regions.objects.get(id=region)
            
            customer=Customer.objects.create(
                user=user,
                first_name=firstname,
                last_name=lastname,
                phone_number=phone
            )
            address=Address.objects.create(
                region=region,
                address=address,
                note=note
            )
            customer.address.add(address)
            order_id=generate_random_id()
            order=Order.objects.create(
                total_price=total_price,
                customer=customer,
                address=address,
                order_id=order_id
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=Product.objects.get(id=item['id']),
                    quantity=item['qty'],
                )
            if 'cart'  in request.session:
                del request.session['cart']

            success = f'ORDER submitted'

            from datetime import datetime
            context={
                "success":success,
                "date": datetime.now().strftime("%b %d, %Y"),
                "order_id":order_id,
                "address":f"{region.name},{address}"
            }
            return render(request, 'checkout.html', context)

    settings=Settings.objects.get()

    regions=Regions.objects.all()
    context = {
        'cart': cart,
        'total_price': total_price,
        "settings":settings,
        "grand_total":Decimal(total_price)+settings.delivery,
        'regions':regions,
    }
        
    return render(request, 'checkout.html', context)



import random
import string

def generate_random_id(length=10):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id