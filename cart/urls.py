from django.urls import path
from .views import  *

app_name = "cart"
urlpatterns = [
    

    path('',view_cart, name='cart_list'),



    path('delete/<int:id>/',remove_from_cart, name='remove_from_cart'),

    


    path('get-delivery/<str:region>/',get_delivery, name='get_delivery'),

    path('empty/',empty_cart, name='empty_cart'),
    
    path('checkout/',checkout, name='checkout'),

    path('add_to_cart/<int:product_id>/',add_to_cart, name='add_to_cart'),

    path('orders/',orders_list, name='orders_list'),
    path('orders/<str:id>/',order_details, name='order_details'),
    path('orders/<str:id>/received/',received_order, name='received_order'),
]
