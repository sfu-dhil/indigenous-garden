from django.contrib import admin
from django.db import models
from rest_framework.renderers import JSONRenderer
from django_admin_kubi.widgets import TinyMceEditorWidget

from .models import Feature, Image, OverheadPoint, PanoramaPoint
from .serializers import FeatureSerializer

def add_map_context(extra_context):
    extra_context = extra_context or {}
    features = Feature.objects.prefetch_related('images', 'overhead_points', 'panorama_points').all()
    extra_context['is_map_model'] = True
    extra_context['features_json'] = JSONRenderer().render(FeatureSerializer(features, many=True).data).decode("utf8")

    return extra_context

class ImageInlineAdmin(admin.StackedInline):
    fields = [
        ('image', 'image_url'),
        'image_license',
    ]
    ordering = ['id']
    model = Image
    extra=0

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    fields = [
        ('number', 'color'),
        'feature_type',
        'audio',
        ('english_names', 'western_scientific_names'),
        ('halkomelem_names', 'squamish_names'),
        'content',
    ]

    list_display = ('id', 'number', '_english_names', '_western_scientific_names', '_halkomelem_names', '_squamish_names')
    list_display_links = ['id', 'number']
    ordering = ['number']
    formfield_overrides = {
        models.TextField: {'widget': TinyMceEditorWidget},
    }

    inlines = [ImageInlineAdmin]

    change_list_template = 'garden/admin/change_list.html'

    def _english_names(self, obj):
        return ' / '.join([
            obj._format_name(item) for item in obj.english_names
        ])
    _english_names.short_description = "English names"

    def _western_scientific_names(self, obj):
        return ' / '.join([
            obj._format_name(item) for item in obj.western_scientific_names
        ])
    _western_scientific_names.short_description = "Western scientific names"

    def _halkomelem_names(self, obj):
        return ' / '.join([
            obj._format_name(item) for item in obj.halkomelem_names
        ])
    _halkomelem_names.short_description = "hən̓q̓əmin̓əm̓ names"

    def _squamish_names(self, obj):
        return ' / '.join([
            obj._format_name(item) for item in obj.squamish_names
        ])
    _squamish_names.short_description = "Sḵwx̱wú7mesh Sníchim names"

    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['can_edit'] = True

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(OverheadPoint)
class OverheadPointAdmin(admin.ModelAdmin):
    fields = [
        'feature',
        ('x', 'y'),
    ]

    list_display = ('id', 'feature', 'x', 'y')
    list_display_links = ['id', 'feature']
    ordering = ['feature', 'x', 'y']

    # maps
    add_form_template = 'garden/admin/change_form.html'
    change_form_template = 'garden/admin/change_form.html'
    change_list_template = 'garden/admin/change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['can_edit'] = True
        extra_context['force_display'] = 'OVERHEAD'

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['is_edit'] = True
        extra_context['edit_point_id'] = object_id
        extra_context['force_display'] = 'OVERHEAD'

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['is_new'] = True
        extra_context['force_display'] = 'OVERHEAD'

        return super().add_view(request, form_url, extra_context=extra_context)

@admin.register(PanoramaPoint)
class PanoramaPointAdmin(admin.ModelAdmin):
    fields = [
        'feature',
        ('yaw', 'pitch'),
    ]

    list_display = ('id', 'feature', 'yaw', 'pitch')
    list_display_links = ['id', 'feature']
    ordering = ['feature', 'yaw', 'pitch']

    # maps
    add_form_template = 'garden/admin/change_form.html'
    change_form_template = 'garden/admin/change_form.html'
    change_list_template = 'garden/admin/change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['can_edit'] = True
        extra_context['force_display'] = 'PANORAMA'

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['is_edit'] = True
        extra_context['edit_point_id'] = object_id
        extra_context['force_display'] = 'PANORAMA'

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['is_new'] = True
        extra_context['force_display'] = 'PANORAMA'

        return super().add_view(request, form_url, extra_context=extra_context)