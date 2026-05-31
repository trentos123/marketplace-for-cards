from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as marketplace_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("marketplace.urls")),

    path("accounts/", include("django.contrib.auth.urls")),

    path("register/", marketplace_views.register, name="register"),
]

# MEDIA FIX (THIS WAS MISSING/WRONG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)