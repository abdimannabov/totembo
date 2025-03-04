from django.contrib.auth import login, logout
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

def signin(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("index")
    else:
        messages.error(request, "Invalid username/password")
        return redirect("login")

def user_logout(request):
    logout(request)
    return redirect("login")

def user_like(request, slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=slug)
    if user:
        user_products = Like.objects.filter(user=user)
        if product in [i.product for i in user_products]:
            like_product = Like.objects.get(user=user, product=product)
            like_product.delete()
        else:
            Like.objects.create(user=user, product=product)
    next_page = request.META.get("HTTP_REFERER", "index")
    return redirect(next_page)

class LikeList(ListView):
    model = Like
    template_name = "shop/likes.html"
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user
        likes = Like.objects.filter(user=user)
        products = [i.product for i in likes]
        return products