import json
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Feature
from .schema import FeatureSchema
from garden_app.settings import CACHE_SECONDS

@cache_page(CACHE_SECONDS)
def dashboard(request):
    features = Feature.objects.prefetch_related(
        'points', 'images',
        'english_names', 'western_scientific_names',
        'halkomelem_names', 'squamish_names',
    ).order_by('number', 'id').filter(published=True).all()
    data = [FeatureSchema.from_orm(feature).dict() for feature in features]
    return render(request, 'dashboard.html', {
        'features': json.dumps(data),
        'display_options': json.dumps({}),
    })
