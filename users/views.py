from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

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
            return redirect('/products')  # Replace 'home' with the appropriate URL name
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

    cart = request.session.get('cart', [])
    context = {
        'cart': cart,
    }
    return render(request, 'login.html',context)

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        if(email=="" or password==""):
            if(email==""):
                error_message = 'Email field is required'
            if(password==""):
                error_message = 'Password field is required'
            return render(request, 'login.html', {'error_message': error_message})
        
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/products')  # Replace 'home' with the appropriate URL name
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})

    cart = request.session.get('cart', [])  
    context = {
        'cart': cart,
    }
    return render(request, 'register.html',context)

