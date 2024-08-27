from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from .models import Feature, Point
from .serializers import PointSerializer

def index(request):
    features = Feature.objects.prefetch_related(
        'images',
        'english_names', 'western_scientific_names',
        'halkomelem_names', 'squamish_names',
    ).order_by('number', 'id').all()

    points = Point.objects.order_by('-y', 'x').all()
    points_json = JSONRenderer().render(PointSerializer(points, many=True).data).decode("utf8")

    return render(request, 'garden/index.html', {
        'features': features,
        'points_json': points_json,
    })
