from django.shortcuts import render, redirect
from django.http import JsonResponse
from settings.models import Settings
from users.models import Address, Customer, Regions
from users.tasks import send_email
from .models import Order, OrderItem, Product
from django.http import HttpResponse



def orders_list(request):
    if request.user.is_authenticated:

        orders=Order.objects.all().order_by('-order_date')

        context={
            "orders":orders,
        }
        return render(request, 'orders_list.html', context)
    return HttpResponse("you need to be logged in")

def order_details(request, id):
    if request.user.is_authenticated:

        try:
            order=Order.objects.get(order_id=id)
        except:
            return HttpResponse(f"order with id={id} not found")
        items=OrderItem.objects.filter(order=order)

        context={
            "order":order,
            "items":items,
        }
        return render(request, 'order_details.html', context)
    
    return HttpResponse("you need to be logged in")
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if 'cart' not in request.session:
        request.session['cart'] = []
    
    cart = request.session['cart']

    product_found=False
    for item in cart:
        if item['id'] == product_id:
            item['qty'] += 1  # Increment the quantity by 1
            item['total_price']=float(item['qty'])*float(item['price'])
            product_found = True
            break

    if not product_found:
        cart.append({
            'id': product.pk,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'image': product.image.url,
            'qty':1,
            'total_price':str(product.price)
        })
    request.session.modified = True

    total_qty=0
    for item in cart:
        total_qty+=item['qty']
    return HttpResponse(total_qty)

def view_cart(request):
    cart = request.session.get('cart', [])
    total_price = sum(float(item['total_price']) for item in cart)
    
    settings=Settings.objects.get()

    total_qty=0
    for item in cart:
        total_qty+=item['qty']

    context = {
        'total_qty':total_qty,
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


from datetime import datetime
from decimal import Decimal


def checkout(request):
        
    cart = request.session.get('cart', [])
    total_price = sum(float(item['total_price']) for item in cart)
    if(len(cart)==0):
        return redirect("/products/")
    settings=Settings.objects.get()

    if(request.method == 'POST'):
        user=None
        if request.user.is_authenticated:
            user=request.user
            address_type = request.POST.get('type')
            customer=Customer.objects.get(user=request.user)
            if(address_type=="choose"):
                # auth ,select from saved address
                selected_address = request.POST.get('selected_address')
            
                address=Address.objects.get(pk=int(selected_address))

                
                order_id=generate_random_id()
                order=Order.objects.create(
                    total_price=total_price,
                    customer=customer,
                    address=address,
                    order_id=order_id
                )
                for item in cart:
                    product=Product.objects.get(id=item['id'])
                    product.stock=product.stock-item['qty']
                    product.save()
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['qty'],
                    )
                if 'cart'  in request.session:
                    del request.session['cart']

         

                html_customer=f"""
                    <p>Dear Customer,</p>
                    <p>Thank you for choosing PetsNClaws for your pet's nutritional needs! We are delighted to inform you that your order has been successfully processed and is now on its way.</p>
                    <br>
                    <p>Order Number:{order.order_id}</p>
                    <p>Total:${total_price}</p>
                    <p>You will receive it within 2 to 3 days</p>
                    <br>
                    <p>If you have any questions or concerns about your order, please feel free to contact our customer service team at {settings.email} or +961 3 743061. We are here to assist you!</p>
                    <p>Thank you once again for choosing PetsNClaws for your pet's nutrition. We look forward to being a part of your pet's wellness journey.</p>
                    <p>Best Regards,<br>PetsNClaws Customer Service Team</p>
                    """
            
                try:
                    if(request.user.email):
                        email=request.user.email
                    else:
                        email=customer.email
                    send_email.apply_async(args=(f'PetsNClaws - Order Confirmation',html_customer,email),countdown=120)
                except Exception as e:
                    print(f"email didnt send,{e}")


                try:
                    html=f"""
                    <h3>New Order  from {customer.first_name} {customer.last_name} </h3>
                    <p>Hello Dear,<br> You have new order with id=#{order.order_id} <br>total price={total_price}$<br>Delivery address= {address.region.name},{address.address}</p>
                    <p>For more details <a style="color:red" href='{settings.admin_link}/cart/orders/{order.order_id}/' >click here</a></p>
                    """
                    send_email.delay(f'PetsNClaws - New Order',html,settings.reciever_email)
                except Exception as e:
                    print(f"email didnt send,{e}")


                context={
                    "success":'success',
                    "date": datetime.now().strftime("%b %d, %Y"),
                    "order_id":order_id,
                    "address":f"{address.region.name},{address.address}"
                }
                return JsonResponse(context)
            else:
                # auth but new address
                phone = request.POST['phone']
                region=request.POST['region']
                address=request.POST['address']
                note = request.POST['note']
                region=Regions.objects.get(id=region)

                address=Address.objects.create(
                    region=region,
                    address=address,
                    note=note,
                    phone_number=phone
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
                    product=Product.objects.get(id=item['id'])
                    product.stock=product.stock-item['qty']
                    product.save()
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['qty'],
                    )
                if 'cart'  in request.session:
                    del request.session['cart']
                context={
                    "success":'success',
                    "date": datetime.now().strftime("%b %d, %Y"),
                    "order_id":order_id,
                    "address":f"{region.name},{address}"
                }


                html_customer=f"""
                    <p>Dear Customer,</p>
                    <p>Thank you for choosing PetsNClaws for your pet's nutritional needs! We are delighted to inform you that your order has been successfully processed and is now on its way.</p>
                    <br>
                    <p>Order Number:{order.order_id}</p>
                    <p>Total:${total_price}</p>
                    <p>You will receive it within 2 to 3 days</p>
                    <br>
                    <p>If you have any questions or concerns about your order, please feel free to contact our customer service team at {settings.email} or +961 3 743061. We are here to assist you!</p>
                    <p>Thank you once again for choosing PetsNClaws for your pet's nutrition. We look forward to being a part of your pet's wellness journey.</p>
                    <p>Best Regards,<br>PetsNClaws Customer Service Team</p>
                    """
                
                try:
                    if(request.user.email):
                        email=request.user.email
                    else:
                        email=customer.email
                
                    send_email.apply_async(args=(f'PetsNClaws - Order Confirmation',html_customer,email),countdown=120)
                except Exception as e:
                    print(f"email didnt send,{e}")


                try:
                    html=f"""
                    <h3>New Order  from {customer.first_name} {customer.last_name} </h3>
                    <p>Hello Dear,<br> You have new order with id=#{order.order_id} <br>total price={total_price}$<br>Delivery address= {region.name},{address}</p>
                    <p>For more details <a style="color:red" href='{settings.admin_link}/cart/orders/{order.order_id}/' >click here</a></p>
                    """
                    send_email.delay(f'PetsNClaws - New Order',html,settings.reciever_email)
                except Exception as e:
                    print(f"email didnt send,{e}")




                return JsonResponse(context)
        else:
            # not auth
            firstname = request.POST.get('firstname')
            lastname = request.POST['lastname']
            email = request.POST['email']
            phone = request.POST['phone']
            region=request.POST['region']
            address=request.POST['address']

            note = request.POST['note']

        
            region=Regions.objects.get(id=region)
            
            customer=Customer.objects.create(
                user=user,
                first_name=firstname,
                last_name=lastname,
                email=email
            )
            address=Address.objects.create(
                region=region,
                address=address,
                note=note,
                phone_number=phone
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
                product=Product.objects.get(id=item['id'])
                product.stock=product.stock-item['qty']
                product.save()
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['qty'],
                )
            if 'cart'  in request.session:
                del request.session['cart']



            html_customer=f"""
                <p>Dear Customer,</p>
                <p>Thank you for choosing PetsNClaws for your pet's nutritional needs! We are delighted to inform you that your order has been successfully processed and is now on its way.</p>
                 <br>
                <p>Order Number:{order.order_id}</p>
                 <p>Total:${total_price}</p>
                <p>You will receive it within 2 to 3 days</p>
                <br>
                 <p>If you have any questions or concerns about your order, please feel free to contact our customer service team at {settings.email} or +961 3 743061. We are here to assist you!</p>
                 <p>Thank you once again for choosing PetsNClaws for your pet's nutrition. We look forward to being a part of your pet's wellness journey.</p>
                  <p>Best Regards,<br>PetsNClaws Customer Service Team</p>
                """
            try:
                send_email.apply_async(args=(f'PetsNClaws - Order Confirmation',html_customer,email),countdown=120)
            except Exception as e:
                print(f"email didnt send,{e}")

            html=f"""
                <h3>New Order  from {firstname} {lastname} </h3>
                <p>You have new order with id=#{order.order_id} <br>total price={total_price}$<br>Delivery address= {region.name},{address}</p>
                    <p>For more details <a style="color:red" href='{settings.admin_link}/cart/orders/{order.order_id}/' >click here</a></p>
            """
            try:
                send_email.delay(f'PetsNClaws - New Order',html,settings.reciever_email)
            except Exception as e:
                print(f"email didnt send,{e}")

            context={
                "success":'success',
                "date": datetime.now().strftime("%b %d, %Y"),
                "order_id":order_id,
                "address":f"{region.name},{address}"
            }
            return JsonResponse(context)


    address=None
    if request.user.is_authenticated:
        address=Customer.objects.get(user=request.user).address.all()

    regions=Regions.objects.all()

    total_qty=0
    for item in cart:
        total_qty+=item['qty']

    context = {
        'total_qty':total_qty,
        'cart': cart,
        'total_price': total_price,
        "settings":settings,
        "grand_total":(Decimal(total_price)+settings.delivery).quantize(Decimal('0.00')),
        'regions':regions,
        'address':address
    }
        
    return render(request, 'checkout.html', context)



import random
import string

def generate_random_id(length=10):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id





