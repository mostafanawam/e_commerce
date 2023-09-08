from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from users.models import Customer, User

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if(email=="" or password==""):
            if(email==""):
                error_message = 'Email field is required'
                return render(request, 'login.html', {'error_message': error_message})
            if(password==""):
                error_message = 'Password field is required'
                return render(request, 'login.html', {'error_message': error_message})
        
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Replace 'home' with the appropriate URL name
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
        
    cart = request.session.get('cart', [])
    
    context = {
        'cart': cart,
    }
    return render(request, 'login.html',context)


from django.contrib.auth import logout
def user_logout(request):

    logout(request)

    return redirect("/")

def user_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        
        if(email=="" or password=="" or first_name=="" or last_name==""):
            if(email==""):
                error_message = 'Email field is required'
            if(password==""):
                error_message = 'Password field is required'
            return render(request, 'register.html', {'error_message': error_message})
            
        if(User.objects.filter(email=email).exists()):
            error_message = f'{email} is already used'
            return render(request, 'register.html', {'error_message': error_message})
        
        user = User.objects.create(
            email=email,
        )
        user.set_password(password)
        user.save()
        Customer.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name
                            
        )

        if user is not None:
            print("test")
            cart = request.session.get('cart', [])  
            context = {
                'cart': cart,
            }
            return redirect("/users/login/")  # Replace 'home' with the appropriate URL name
        
        
    cart = request.session.get('cart', [])  
    context = {
        'cart': cart,
    }
    return render(request, 'register.html',context)

