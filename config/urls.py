from django.contrib import admin
from django.urls import path, include
from marketplace import views as marketplace_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # marketplace
    path("", include("marketplace.urls")),

    # auth system
    path("accounts/", include("django.contrib.auth.urls")),

    # register (MAIN)
    path("register/", marketplace_views.register, name="register"),

    # OPTIONAL FIX (prevents your 404 issue)
    path("accounts/register/", marketplace_views.register),
]

# MEDIA SERVING (IMPORTANT for images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)