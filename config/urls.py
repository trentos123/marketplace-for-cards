from django.contrib import admin
from django.urls import path, include
from marketplace import views as marketplace_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # marketplace routes
    path("", include("marketplace.urls")),

    # built-in Django auth (login/logout)
    path("accounts/", include("django.contrib.auth.urls")),

    # custom register page
    path("register/", marketplace_views.register, name="register"),
]