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
    path("logout/", user_logout, name="logout"),
    path("user_like/<slug:slug>/", user_like, name="user_like"),
    path("like_list/", LikeList.as_view(), name="like_list"),
    path("cart/", cart, name="cart"),
    path("to_cart/<int:product_id>/<str:action>/", to_cart, name="to_cart"),
    path("success/", success_payment, name="success"),
    path("cancel/", cancel_payment, name="cancel"),
    path("payment/", payment, name="payment")
]