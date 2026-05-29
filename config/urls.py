from django.contrib import admin
from django.urls import path, include
from marketplace import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),
    path("card/<int:pk>/", views.card_detail, name="card_detail"),

    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("orders/", views.orders, name="orders"),

    path("seller/<str:username>/", views.seller_profile, name="seller_profile"),

    path("ajax/add/<int:pk>/", views.ajax_add_to_cart, name="ajax_add_to_cart"),

    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)