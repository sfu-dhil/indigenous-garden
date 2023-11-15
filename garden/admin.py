from django.contrib import admin
from django.db import models
from rest_framework.renderers import JSONRenderer
from django_admin_kubi.widgets import TinyMceEditorWidget

from .models import Plant, Image, Point
from .serializers import PlantSerializer

def add_map_context(extra_context):
    extra_context = extra_context or {}
    plants = Plant.objects.prefetch_related('images', 'points').all()
    extra_context['is_map_model'] = True
    extra_context['plants_json'] = JSONRenderer().render(PlantSerializer(plants, many=True).data).decode("utf8")

    return extra_context

class ImageInlineAdmin(admin.StackedInline):
    fields = [
        ('image', 'image_url'),
        'image_license',
    ]
    ordering = ['id']
    model = Image
    extra=0

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    fields = [
        ('number', 'color'),
        ('english_names', 'english_names_audio'),
        ('english_content', 'english_content_audio'),
        ('western_scientific_names', 'western_scientific_names_audio'),
        ('halkomelem_names', 'halkomelem_names_audio'),
        ('halkomelem_content', 'halkomelem_content_audio'),
        ('squamish_names', 'squamish_names_audio'),
        ('squamish_content', 'squamish_content_audio'),
    ]

    list_display = ('id', 'number', 'english_names', 'western_scientific_names', 'halkomelem_names', 'squamish_names')
    list_display_links = ['id', 'number']
    ordering = ['number']
    formfield_overrides = {
        models.TextField: {'widget': TinyMceEditorWidget},
    }

    inlines = [ImageInlineAdmin]


    change_list_template = 'garden/admin/changelist.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['can_edit'] = True

        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    fields = [
        'plant',
        'x', 'y',
    ]

    list_display = ('id', 'plant', 'x', 'y')
    list_display_links = ['id', 'plant']
    ordering = ['plant', 'x', 'y']

    # maps
    add_form_template = 'garden/admin//add_form.html'
    change_form_template = 'garden/admin/change_form.html'
    change_list_template = 'garden/admin/changelist.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['can_edit'] = True

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['is_edit'] = True
        extra_context['edit_point_id'] = object_id

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['is_new'] = True

        return super().add_view(request, form_url, extra_context=extra_context)