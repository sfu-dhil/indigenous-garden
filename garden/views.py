from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from .models import Feature, Point
from .serializers import FeatureSerializer

def index(request):
    features = Feature.objects.prefetch_related(
        'images',
        'english_names', 'western_scientific_names',
        'halkomelem_names', 'squamish_names', 'points',
    ).order_by('number', 'id').filter(published=True).all()
    feature_points_json = JSONRenderer().render(FeatureSerializer(features, many=True).data).decode("utf8")

    return render(request, 'garden/index.html', {
        'features': features.all(),
        'feature_points_json': feature_points_json,
    })
