from django.urls import path
from shop.views import *

urlpatterns = [
    path("", ProductView.as_view(), name="index"),
    path("category/<slug:slug>/", ProductListByCategory.as_view(), name="category"),
    path("product/<slug:slug>/", ProductDetail.as_view(), name="product"),
    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("logout/", user_logout, name="logout")
]