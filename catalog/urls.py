from django.urls import path, include

from . import views

# Product Urls
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]

urlpatterns += [
    path('register/', views.register, name='register'),
]

