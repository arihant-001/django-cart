from django.urls import path, include

from . import views

urlpatterns = [
    path('<int:pk>/', views.CartDetail.as_view()),
    path('cartitem/', views.CartItemDetail.as_view()),
    path('cartitem/<int:pk>/', views.CartItemDetail.as_view()),
]