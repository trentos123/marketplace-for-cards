from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("card/<int:pk>/", views.detail),
    path("create/", views.create),
    path("seller/<str:username>/", views.seller_profile),

    path("add/<int:pk>/", views.add_to_cart),
    path("cart/", views.cart),
    path("remove/<int:pk>/", views.remove_from_cart),

    path("dashboard/", views.dashboard),
    path("checkout/", views.checkout),
]