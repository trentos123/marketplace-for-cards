from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("card/<int:pk>/", views.detail, name="detail"),

    # CART
    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),

    # CHECKOUT
    path("checkout/", views.checkout, name="checkout"),
    path("payment-success/", views.payment_success, name="payment_success"),

    # WEBHOOK
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),

    # AUTH
    path("register/", views.register, name="register"),
]