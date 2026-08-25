from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django_dh_map.api import admin_router, public_router, \
    PublicFeatureViewSet, InfoPageViewSet

from .serializers import FeatureOverrideSerializer, InfoPageOverrideSerializer, \
    WelcomeModalSerializer
from .models import WelcomeModal

@cache_page(settings.CACHE_SECONDS)
@api_view(["GET"])
def static_content(request):
    return Response({
        'welcome': WelcomeModalSerializer(WelcomeModal.get_solo()).data,
    })

class PublicFeatureOverrideViewSet(PublicFeatureViewSet):
    serializer_class = FeatureOverrideSerializer

class InfoPageOverrideViewSet(InfoPageViewSet):
    serializer_class = InfoPageOverrideSerializer

public_router.unregister('features')
public_router.register('features', PublicFeatureOverrideViewSet)
public_router.unregister('pages')
public_router.register('pages', InfoPageViewSet)