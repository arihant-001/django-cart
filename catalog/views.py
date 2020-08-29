from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import Product, Category, UserProfile


def index(request):
    products = Product.objects.all()
    # if 'cart_id' not in request.session:
    #     if request.user.is_authenticated:
    #         cart = Cart(owner=request.user)
    #     else:
    #         cart = Cart()
    #     cart.save()
    #     request.session['cart_id'] = cart.id
    #     request.session['cart_count'] = cart.get_total_items()
    #     request.session.is_modified = True

    context = {
        'product_list': products
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print("method is post")
        if form.is_valid():
            print("form  is valid")
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect('index')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request=request,
                          template_name="registration/register.html",
                          context={"form": form})
    form = UserCreationForm
    return render(request=request, template_name="registration/register.html", context={"form": form})


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"


class ProductListView(ListView):
    model = Product
    paginate_by = 10
    template_name = "catalog/product_list.html"

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


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
