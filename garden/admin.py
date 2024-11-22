from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from html import unescape
from django.contrib.admin import ModelAdmin, TabularInline
from tinymce.widgets import TinyMCE

from .models import Feature, Image, Point, \
    EnglishName, WesternScientificName, \
    HalkomelemName, SquamishName
from .serializers import FeatureSerializer

class ImageInlineAdmin(TabularInline):
    fields = ['image', 'description', 'license']
    ordering = ['id']
    model = Image
    extra=0
    classes = ['collapse']

class NameInlineAdmin(TabularInline):
    fields = ['name', 'descriptor', 'audio']
    ordering = ['id']
    extra=0
    classes = ['collapse']

class EnglishNameInlineAdmin(NameInlineAdmin):
    model = EnglishName

class WesternScientificNameInlineAdmin(NameInlineAdmin):
    model = WesternScientificName

class HalkomelemNameInlineAdmin(NameInlineAdmin):
    model = HalkomelemName
    verbose_name = "hən̓q̓əmin̓əm̓ name"
    classes=['first-nations-unicode', 'collapse']

class SquamishNameInlineAdmin(NameInlineAdmin):
    model = SquamishName
    verbose_name="Sḵwx̱wú7mesh Sníchim name"
    classes=['first-nations-unicode', 'collapse']

def add_map_context(extra_context, is_edit_mode=False, point_id=None):
    extra_context = extra_context or {}
    features = Feature.objects.prefetch_related(
        'points', 'images',
        'english_names', 'western_scientific_names',
        'halkomelem_names', 'squamish_names',
    ).order_by('number', 'id').all()

    extra_context['is_map'] = True
    extra_context['features'] = FeatureSerializer(features, many=True).data
    extra_context['display_options'] = {
        'canEdit': True,
        'isEditMode': is_edit_mode,
        'editPointId': point_id,
    }

    return extra_context

@admin.register(Feature)
class FeatureAdmin(ModelAdmin):
    fields = [
        ('feature_type', 'number', 'published'),
        'content',
        ('video', 'captions'),
        'references',
    ]

    list_display = ('id', 'published', 'feature_type', 'number', '_english_names', '_western_scientific_names', '_halkomelem_names', '_squamish_names')
    list_display_links = ('id', 'published', 'feature_type', 'number', '_english_names', '_western_scientific_names', '_halkomelem_names', '_squamish_names')
    ordering = ['feature_type', 'number']
    search_fields = [
        'number',
        'english_names__name', 'english_names__descriptor',
        'western_scientific_names__name', 'western_scientific_names__descriptor',
        'halkomelem_names__name', 'halkomelem_names__descriptor',
        'squamish_names__name', 'squamish_names__descriptor',
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE},
    }

    inlines = [
        EnglishNameInlineAdmin,
        WesternScientificNameInlineAdmin,
        HalkomelemNameInlineAdmin,
        SquamishNameInlineAdmin,
        ImageInlineAdmin,
    ]

    def _english_names(self, obj):
        return mark_safe(unescape(' <br /> '.join([str(n) for n in obj.english_names.all()])))
    _english_names.short_description = "English names"

    def _western_scientific_names(self, obj):
        return mark_safe(unescape(' <br /> '.join([str(n) for n in obj.western_scientific_names.all()])))
    _western_scientific_names.short_description = "Western scientific names"

    def _halkomelem_names(self, obj):
        return mark_safe(unescape(' <br /> '.join([f"<span class='first-nations-unicode'>{n}</span>" for n in obj.halkomelem_names.all()])))
    _halkomelem_names.short_description = mark_safe("<span class='first-nations-unicode'>hən̓q̓əmin̓əm̓</span> names")

    def _squamish_names(self, obj):
        return mark_safe(unescape(' <br /> '.join([f"<span class='first-nations-unicode'>{n}</span>" for n in obj.squamish_names.all()])))
    _squamish_names.short_description = mark_safe("<span class='first-nations-unicode'>Sḵwx̱wú7mesh Sníchim</span> names")

    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context)

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Point)
class PointAdmin(ModelAdmin):
    fields = [
        'feature',
        ('x', 'y'),
    ]

    list_display = ('id', 'feature', 'x', 'y')
    list_display_links = ('id', 'feature', 'x', 'y')
    ordering = ['feature', 'x', 'y']
    autocomplete_fields = ['feature']
    list_per_page = 5

    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context)
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, True, int(object_id))
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, True)

        return super().add_view(request, form_url, extra_context=extra_context)