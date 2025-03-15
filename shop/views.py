from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from shop.forms import LoginForm, RegisterForm, CustomerForm, AddressForm
from shop.models import *
from django.contrib import messages
from shop.utils import get_cart_data, CartForUser
import stripe

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

def cart(request):
    cart_info = get_cart_data(request)

    context = {
        "products":cart_info["products"],
        "order":cart_info["order"],
        "total_quantity":cart_info["cart_total_quantity"],
        "total_price": cart_info["cart_total_price"],
        "customer_form":CustomerForm(),
        "address_form":AddressForm(),
        "title":"Cart"
    }
    return render(request, "shop/cart.html", context)

def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForUser(request, product_id, action)
        return redirect("cart")
    else:
        messages.error(request, "You are not authenticated!")
        return redirect("login")

def payment(request):
    from config import settings
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForUser(request)
        cart_info = user_cart.get_cart_info()
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.name = customer_form.cleaned_data['name']
            customer.email = customer_form.cleaned_data['email']
        address_form = AddressForm(data=request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()
        total_price = cart_info["cart_total_price"]
        total_quantity = cart_info["cart_total_quantity"]
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data":{
                        "currency":"usd",
                        "product_data":{
                            'name':"products of TOTEMBO"
                        },
                        "unit_amount":int(total_price)
                    },
                    "quantity":total_quantity
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("cancel"))
        )
    return redirect(session.url, 303)

def success_payment(request):
    return render(request, "shop/success.html")

def cancel_payment(request):
    return render(request, "shop/cancel.html")