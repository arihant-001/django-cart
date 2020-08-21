from django.urls import path, include

from . import views

urlpatterns = [
    path('<int:pk>/', views.CartView.as_view()),
    path('cartitem/', views.CartItemView.as_view()),
    path('cartitem/<int:pk>/', views.CartItemView.as_view()),
    path('updatecartitem/', views.update_cart_quantity, name='update_cart_item'),
    path('details/', views.CartItemListView.as_view(), name='cart_details'),
    path('checkout/', views.checkout, name='checkout'),
]