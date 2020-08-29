from django.urls import path, include
from . import views

urlpatterns = [
    path('update_cart/', views.update_cart_quantity, name='update_cart'),
    path('cart_quantity/', views.get_cart_quantity),
    path('details/', views.cart_details, name='cart_details'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_order/', views.process_order),
]