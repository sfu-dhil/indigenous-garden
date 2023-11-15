from django.contrib import admin
from django.db import models
from rest_framework.renderers import JSONRenderer
from django_admin_kubi.widgets import TinyMceEditorWidget
from django.utils.html import format_html

from .models import Feature, Image, OverheadPoint, PanoramaPoint, \
    EnglishName, WesternScientificName, \
    HalkomelemName, SquamishName
from .serializers import OverheadPointSerializer, PanoramaPointSerializer

def add_map_context(extra_context):
    extra_context = extra_context or {}
    extra_context['features'] = Feature.objects.prefetch_related(
        'images',
        'english_names', 'western_scientific_names',
        'halkomelem_names', 'squamish_names'
    ).order_by('number', 'id').all()
    extra_context['is_map'] = True
    overhead_points = OverheadPoint.objects.order_by('-y', 'x').all()
    extra_context['overhead_points_json'] = JSONRenderer().render(OverheadPointSerializer(overhead_points, many=True).data).decode("utf8")
    panorama_points = PanoramaPoint.objects.order_by('-pitch', 'yaw').all()
    extra_context['panorama_points_json'] = JSONRenderer().render(PanoramaPointSerializer(panorama_points, many=True).data).decode("utf8")

    return extra_context

class ImageInlineAdmin(admin.StackedInline):
    fields = [
        'image',
        ('description', 'license'),
    ]
    ordering = ['id']
    model = Image
    extra=0
    formfield_overrides = {
        models.TextField: {'widget': TinyMceEditorWidget},
    }

class EnglishNameInlineAdmin(admin.TabularInline):
    fields = [
        'name',
        'descriptor',
        'audio',
    ]
    ordering = ['id']
    model = EnglishName
    extra=0

class WesternScientificNameInlineAdmin(admin.TabularInline):
    fields = [
        'name',
        'descriptor',
        'audio',
    ]
    ordering = ['id']
    model = WesternScientificName
    extra=0

class HalkomelemNameInlineAdmin(admin.TabularInline):
    fields = [
        'name',
        'descriptor',
        'audio',
    ]
    ordering = ['id']
    model = HalkomelemName
    extra=0
    verbose_name = "hən̓q̓əmin̓əm̓ name"

class SquamishNameInlineAdmin(admin.TabularInline):
    fields = [
        'name',
        'descriptor',
        'audio',
    ]
    ordering = ['id']
    model = SquamishName
    extra=0
    verbose_name="Sḵwx̱wú7mesh Sníchim name"

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    fields = [
        ('feature_type', 'number'),
        'content',
        ('audio', 'captions'),
    ]

    list_display = ('id', 'number', '_english_names', '_western_scientific_names', '_halkomelem_names', '_squamish_names')
    list_display_links = ('id', 'number', '_english_names', '_western_scientific_names', '_halkomelem_names', '_squamish_names')
    ordering = ['number']
    search_fields = [
        'number',
        'english_names__name', 'english_names__descriptor',
        'western_scientific_names__name', 'western_scientific_names__descriptor',
        'halkomelem_names__name', 'halkomelem_names__descriptor',
        'squamish_names__name', 'squamish_names__descriptor',
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMceEditorWidget},
    }

    inlines = [
        EnglishNameInlineAdmin,
        WesternScientificNameInlineAdmin,
        HalkomelemNameInlineAdmin,
        SquamishNameInlineAdmin,
        ImageInlineAdmin,
    ]

    change_list_template = 'garden/admin/change_list.html'

    def _english_names(self, obj):
        return format_html(' <br /> '.join([str(n) for n in obj.english_names.all()]))
    _english_names.short_description = "English names"

    def _western_scientific_names(self, obj):
        return format_html(' <br /> '.join([str(n) for n in obj.western_scientific_names.all()]))
    _western_scientific_names.short_description = "Western scientific names"

    def _halkomelem_names(self, obj):
        return format_html(' <br /> '.join([str(n) for n in obj.halkomelem_names.all()]))
    _halkomelem_names.short_description = "hən̓q̓əmin̓əm̓ names"

    def _squamish_names(self, obj):
        return format_html(' <br /> '.join([str(n) for n in obj.squamish_names.all()]))
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
    list_display_links = ('id', 'feature', 'x', 'y')
    ordering = ['feature', 'x', 'y']
    list_per_page = 5

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
    list_display_links = ('id', 'feature', 'yaw', 'pitch')
    ordering = ['feature', 'yaw', 'pitch']
    list_per_page = 5

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