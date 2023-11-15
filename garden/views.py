from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from .models import Feature, OverheadPoint, PanoramaPoint
from .serializers import OverheadPointSerializer, PanoramaPointSerializer

def index(request):
    features = Feature.objects.prefetch_related(
        'images',
        'english_names', 'western_scientific_names',
        'halkomelem_names', 'squamish_names',
    ).order_by('number', 'id').all()

    overhead_points = OverheadPoint.objects.order_by('-y', 'x').all()
    overhead_points_json = JSONRenderer().render(OverheadPointSerializer(overhead_points, many=True).data).decode("utf8")
    panorama_points = PanoramaPoint.objects.order_by('-pitch', 'yaw').all()
    panorama_points_json = JSONRenderer().render(PanoramaPointSerializer(panorama_points, many=True).data).decode("utf8")

    return render(request, 'garden/index.html', {
        'features': features,
        'overhead_points_json': overhead_points_json,
        'panorama_points_json': panorama_points_json,
    })
