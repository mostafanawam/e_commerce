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


from datetime import datetime
from decimal import Decimal


def checkout(request):
        
    cart = request.session.get('cart', [])
    total_price = sum(float(item['price']) for item in cart)
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
                <p>Your order has been processed</p>
                 <p>Order Number:{order.order_id}</p>
                 <p>Total price:{total_price}$</p>
                <p>You will receive it within 2-3 days</p>
                """
            
                try:
                    send_email(f'PetsNClaws Order',html_customer,user.email)
                except Exception as e:
                    print(f"email didnt send,{e}")


                try:
                    html=f"""
                    <h3>New Order  from {firstname} {lastname} </h3>
                    <p>Hello Dear,<br> You have new order with id=#{order.order_id} <br>total price={total_price}$<br>Delivery address= {region.name},{address}</p>
                    <p>For more details <a style="color:red" href='{settings.admin_link}/cart/orderitem/?order__id__exact={order.pk}' >click here</a></p>
                    """
                    send_email(f'PetsNClaws New Order',html,settings.reciever_email)
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
                <p>Your order has been processed</p>
                 <p>Order Number:{order.order_id}</p>
                 <p>Total price:{total_price}$</p>
                <p>You will receive it within 2-3 days</p>
                """
                try:
                    send_email(f'PetsNClaws Order',html_customer,user.email)
                except Exception as e:
                    print(f"email didnt send,{e}")


                try:
                    html=f"""
                    <h3>New Order  from {firstname} {lastname} </h3>
                    <p>Hello Dear,<br> You have new order with id=#{order.order_id} <br>total price={total_price}$<br>Delivery address= {region.name},{address}</p>
                    <p>For more details <a style="color:red" href='{settings.admin_link}/cart/orderitem/?order__id__exact={order.pk}' >click here</a></p>
                    """
                    send_email(f'PetsNClaws New Order',html,settings.reciever_email)
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
                <p>Your order has been processed</p>
                 <p>Order Number:{order.order_id}</p>
                 <p>Total price:{total_price}$</p>
                <p>You will receive it within 2-3 days</p>
                """
            try:
                send_email(f'PetsNClaws Order',html_customer,email)
            except Exception as e:
                print(f"email didnt send,{e}")

            html=f"""
                <h3>New Order  from {firstname} {lastname} </h3>
                <p>You have new order with id=#{order.order_id} <br>total price={total_price}$<br>Delivery address= {region.name},{address}</p>
                <p>For more details <a style="color:red" href='{settings.admin_link}/cart/orderitem/?order__id__exact={order.pk}' >click here</a></p>
            """
            try:
                send_email(f'PetsNClaws New Order',html,settings.reciever_email)
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
    context = {
        'cart': cart,
        'total_price': total_price,
        "settings":settings,
        "grand_total":Decimal(total_price)+settings.delivery,
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





import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings.models import Settings



def send_email(subject,html,reciever_email):
    settings=Settings.objects.get()
    gmail_user =settings.email
    gmail_password = settings.password  # Use your App Password if you have 2FA enabled

    # Email details
    subject = subject

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = reciever_email
    msg['Subject'] = subject

    msg.attach(MIMEText(html, "html"))

    email_string = msg.as_string()

    # Connect to Gmail's SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Enable TLS (Transport Layer Security)
        
        # Log in to your Gmail account
        server.login(gmail_user, gmail_password)
        
        # Send the email
        server.sendmail(gmail_user,reciever_email,email_string)

    print('Email sent successfully!')