from django.contrib import admin
from django.urls import path, include
from marketplace import views as marketplace_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # marketplace routes
    path("", include("marketplace.urls")),

    # built-in auth
    path("accounts/", include("django.contrib.auth.urls")),

    # register
    path("register/", marketplace_views.register, name="register"),
]

# MEDIA FILES (ONLY FOR DEV / DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)