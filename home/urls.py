from django.urls import path
from .views import  *

app_name = "home"
urlpatterns = [
    

    path('',homepage, name='home'),
    path('products/',productsPage, name='products'),
    path('search_products/',searchProducts, name='search_products'),
    path('contact-us/',contactUs, name='contactUs'),



    
]
