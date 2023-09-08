from django.urls import path
from .views import  *

app_name = "cart"
urlpatterns = [
    

    path('',view_cart, name='cart_list'),



    path('delete/<int:id>/',remove_from_cart, name='remove_from_cart'),

    
    path('empty/',empty_cart, name='empty_cart'),
    
    path('checkout/',checkout, name='checkout'),

    path('add_to_cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    
]
