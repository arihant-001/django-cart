from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import Product, Category, UserProfile


def index(request):
    num_products = Product.objects.all().count()

    context = {
        'num_products': num_products,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# Product views
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"


class ProductCreateView(CreateView):
    model = Product
    template_name = "catalog/product_create.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "catalog/product_update.html"


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_delete.html"


# Product Categories views
class CategoryDetailView(DetailView):
    model = Category
    template_name = "catalog/category_detail.html"


class CategoryListView(ListView):
    model = Category
    template_name = "catalog/category_list.html"


class CategoryCreateView(CreateView):
    model = Category
    template_name = "catalog/category_create.html"


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = "catalog/category_update.html"


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "catalog/category_delete.html"


# UserProfile views
class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = "catalog/userprofile_detail.html"


class UserProfileListView(ListView):
    model = UserProfile
    template_name = "catalog/userprofile_list.html"


class UserProfileCreateView(CreateView):
    model = UserProfile
    template_name = "catalog/userprofile_create.html"


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "catalog/userprofile_update.html"


class UserProfileDeleteView(DeleteView):
    model = UserProfile
    template_name = "catalog/userprofile_delete.html"
