from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("card/<int:pk>/", views.detail, name="detail"),
    path("create/", views.create, name="create"),

    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),

    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    path("ajax/add-to-cart/<int:pk>/", views.ajax_add_to_cart, name="ajax_add_to_cart"),
    ]