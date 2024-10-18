"""
URL configuration for garden_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.views.decorators.cache import cache_control
from django.contrib.staticfiles.views import serve
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from .views import UnfoldPasswordResetView, UnfoldPasswordResetDoneView, UnfoldPasswordResetConfirmView, UnfoldPasswordResetCompleteView

urlpatterns = [
    # health check ping endpoint
    path('health_check/', include('health_check.urls')),

    # admin password reset endpoints (from https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#adding-a-password-reset-feature)
    path('admin/password_reset/', UnfoldPasswordResetView.as_view(), name="admin_password_reset"),
    path('admin/password_reset/done/', UnfoldPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', UnfoldPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', UnfoldPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # admin site endpoints
    path('admin/', admin.site.urls),

    # main garden map endpoints
    path('', include("garden.urls")),

    # django-async-upload endpoints
    path('admin_async_upload/', include("admin_async_upload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        view=cache_control(no_cache=True, must_revalidate=True)(serve),
    )
    # nginx serving media files
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)