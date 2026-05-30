from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("card/<int:pk>/", views.detail, name="detail"),
    path("create/", views.create, name="create"),
    path("seller/<str:username>/", views.seller_profile, name="seller_profile"),

    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),

    # ✅ FIX: missing pages
    path("dashboard/", views.dashboard, name="dashboard"),
    path("checkout/", views.checkout, name="checkout"),
]