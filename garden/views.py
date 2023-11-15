from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from .models import Feature
from .serializers import FeatureSerializer

def index(request):
    features = Feature.objects.prefetch_related('images', 'overhead_points', 'panorama_points').all()
    features_json = JSONRenderer().render(FeatureSerializer(features, many=True).data).decode("utf8")

    return render(request, 'garden/index.html', {
        'features': features,
        'features_json': features_json,
    })