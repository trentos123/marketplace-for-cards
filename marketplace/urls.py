from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("cart/", views.cart, name="cart"),

    # LOGIN (THIS IS IMPORTANT)
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]