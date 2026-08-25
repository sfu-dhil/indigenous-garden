from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.conf import settings

from . import views
from .api import admin_router, public_router, static_content

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('api/content', static_content),
    # override django_dh_map api endpoints with custom items
    path('api/admin/', include(admin_router.urls)),
    path('api/', include(public_router.urls)),
]