from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from user.models import CartUser
from .models import Product, Category


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'product_list': products,
        'categories_list': categories,
    }

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
            cart_user = CartUser.objects.create(
                user=user,
                name=user.first_name + user.last_name,
                email=user.email,
            )
            cart_user.save()
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


class CategoryDetailView(DetailView):
    model = Category
    template_name = "catalog/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        products = Product.objects.filter(category=kwargs['object'].id)
        categories = Category.objects.all()
        context['product_list'] = products
        context['categories_list'] = categories
        return context

