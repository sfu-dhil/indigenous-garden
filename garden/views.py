from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from .models import Plant
from .serializers import PlantSerializer

def index(request):
    plants = Plant.objects.prefetch_related('images', 'points').all()
    plants_json = JSONRenderer().render(PlantSerializer(plants, many=True).data).decode("utf8")

    return render(request, 'garden/index.html', {
        'plants': plants,
        'plants_json': plants_json,
    })