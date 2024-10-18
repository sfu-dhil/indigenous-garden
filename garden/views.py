from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.views.decorators.cache import cache_page
from .models import Feature, Point
from .serializers import FeatureSerializer
from garden_app.settings import CACHE_SECONDS

@cache_page(CACHE_SECONDS)
def dashboard(request):
    features = Feature.objects.prefetch_related(
        'points', 'images',
        'english_names', 'western_scientific_names',
        'halkomelem_names', 'squamish_names',
    ).order_by('number', 'id').filter(published=True).all()

    return render(request, 'dashboard.html', {
        'features': FeatureSerializer(features, many=True).data,
        'display_options': {},
    })
