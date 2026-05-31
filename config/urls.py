from django.contrib import admin
from django.urls import path, include
from marketplace import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # marketplace app
    path("", include("marketplace.urls")),

    # auth system
    path("accounts/", include("django.contrib.auth.urls")),

    # FIXED register routes
    path("accounts/register/", views.register, name="register"),
    path("register/", views.register, name="register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)