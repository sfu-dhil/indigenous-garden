from django.contrib import admin
from django.db import models
from rest_framework.renderers import JSONRenderer
from django_admin_kubi.widgets import TinyMceEditorWidget
from django.utils.html import format_html

from .models import Feature, Image, Point, \
    EnglishName, WesternScientificName, \
    HalkomelemName, SquamishName
from .serializers import FeatureSerializer

def add_map_context(extra_context):
    extra_context = extra_context or {}
    features = Feature.objects.prefetch_related(
        'images',
        'english_names', 'western_scientific_names',
        'halkomelem_names', 'squamish_names', 'points'
    ).order_by('feature_type', 'number', 'id').all()

    extra_context['is_map'] = True
    extra_context['features'] = features
    extra_context['feature_points_json'] = JSONRenderer().render(FeatureSerializer(features, many=True).data).decode("utf8")

    return extra_context

class ImageInlineAdmin(admin.StackedInline):
    fields = [
        'image',
        ('description', 'license'),
    ]
    ordering = ['id']
    model = Image
    extra=0

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
    classes=['first-nations-unicode']

    # def formfield_for_dbfield(self, db_field, request, **kwargs):
    #     field = super().formfield_for_dbfield(db_field, request, **kwargs)
    #     if db_field.name == "name":
    #         field.widget.attrs["style"] = 'font-family: "First Nations Unicode" !important;'
    #     return field

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
    classes=['first-nations-unicode']

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    fields = [
        ('published', 'feature_type', 'number'),
        'content',
        ('video', 'captions'),
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
        models.TextField: {'widget': TinyMceEditorWidget},
    }

    inlines = [
        EnglishNameInlineAdmin,
        WesternScientificNameInlineAdmin,
        HalkomelemNameInlineAdmin,
        SquamishNameInlineAdmin,
        ImageInlineAdmin,
    ]

    def _english_names(self, obj):
        return format_html(' <br /> '.join([str(n) for n in obj.english_names.all()]))
    _english_names.short_description = "English names"

    def _western_scientific_names(self, obj):
        return format_html(' <br /> '.join([str(n) for n in obj.western_scientific_names.all()]))
    _western_scientific_names.short_description = "Western scientific names"

    def _halkomelem_names(self, obj):
        return format_html(' <br /> '.join([f"<span class='first-nations-unicode'>{n}</span>" for n in obj.halkomelem_names.all()]))
    _halkomelem_names.short_description = format_html("<span class='first-nations-unicode'>hən̓q̓əmin̓əm̓</span> names")

    def _squamish_names(self, obj):
        return format_html(' <br /> '.join([f"<span class='first-nations-unicode'>{n}</span>" for n in obj.squamish_names.all()]))
    _squamish_names.short_description = format_html("<span class='first-nations-unicode'>Sḵwx̱wú7mesh Sníchim</span> names")

    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['can_edit'] = True

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
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
        extra_context['can_edit'] = True
        extra_context['force_display'] = 'MAP'

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['is_edit'] = True
        extra_context['edit_point_id'] = object_id
        extra_context['force_display'] = 'MAP'

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context)
        extra_context['is_new'] = True
        extra_context['force_display'] = 'MAP'

        return super().add_view(request, form_url, extra_context=extra_context)