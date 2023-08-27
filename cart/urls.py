from django.urls import path
from .views import  *

app_name = "cart"
urlpatterns = [
    

    path('',view_cart, name='cart_list'),


    path('products/',product_list, name='product_list'),

    path('product/<int:product_id>/',product_details, name='product_details'),
    
    path('add_to_cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    
]
