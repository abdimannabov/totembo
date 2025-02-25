from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from shop.forms import LoginForm, RegisterForm
from shop.models import *
from django.contrib import messages

class ProductView(ListView):
    model = Product
    template_name = "shop/index.html"
    context_object_name = "categories"
    extra_context = {
        "title": "Totembo"
    }

    def get_queryset(self):
        categories = Category.objects.all()
        data = []
        for category in categories:
            products = category.products.all()
            data.append({
                "title": category.title,
                "products": products
            })
        return data

class ProductListByCategory(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop/category.html"
    paginate_by = 4
    extra_context = {
        "title":"Category"
    }

    def get_queryset(self):
        sort_field = self.request.GET.get("sort")
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = category.products.all()
        if sort_field:
            products = products.order_by(sort_field)
        return products

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = product.title
        products = Product.objects.all()
        data = []
        while len(data) < 4:
            from random import randint
            random_int = randint(0, len(products)-1)
            product = products[random_int]
            if product not in data:
                data.append(product)
        context['products'] = data
        return context

def user_login(request):
    context = {
        'title':"Auth User",
        "login_form":LoginForm()
    }
    return render(request, 'shop/login.html', context)

def user_register(request):
    context = {
        'title':"Auth User",
        "register_form":RegisterForm()
    }
    return render(request, 'shop/register.html', context)

def signup(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request, "Successfully created")
        return redirect("login")
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())
        return redirect("register")