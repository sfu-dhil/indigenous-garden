from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.db import models
from django.utils.safestring import mark_safe
from rest_framework.renderers import JSONRenderer
from html import unescape
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import display

from .models import Feature, Image, Point, \
    EnglishName, WesternScientificName, \
    HalkomelemName, SquamishName
from .serializers import FeatureSerializer

# override the Auth User and Group models to use unfold UI theme
admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

class ImageInlineAdmin(StackedInline):
    fields = [('image', 'description', 'license')]
    ordering = ['id']
    model = Image
    extra=0

class NameInlineAdmin(TabularInline):
    fields = ['name', 'descriptor', 'audio']
    ordering = ['id']
    extra=0

class EnglishNameInlineAdmin(NameInlineAdmin):
    model = EnglishName

class WesternScientificNameInlineAdmin(NameInlineAdmin):
    model = WesternScientificName

class HalkomelemNameInlineAdmin(NameInlineAdmin):
    model = HalkomelemName
    verbose_name = "hən̓q̓əmin̓əm̓ name"
    classes=['first-nations-unicode']

    # def formfield_for_dbfield(self, db_field, request, **kwargs):
    #     field = super().formfield_for_dbfield(db_field, request, **kwargs)
    #     if db_field.name == "name":
    #         field.widget.attrs["style"] = 'font-family: "First Nations Unicode" !important;'
    #     return field

class SquamishNameInlineAdmin(NameInlineAdmin):
    model = SquamishName
    verbose_name="Sḵwx̱wú7mesh Sníchim name"
    classes=['first-nations-unicode']

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
        'published',
        ('feature_type', 'number'),
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
        models.TextField: {'widget': WysiwygWidget},
    }

    inlines = [
        EnglishNameInlineAdmin,
        WesternScientificNameInlineAdmin,
        HalkomelemNameInlineAdmin,
        SquamishNameInlineAdmin,
        ImageInlineAdmin,
    ]

    @display(description="English names")
    def _english_names(self, obj):
        return mark_safe(unescape(' <br /> '.join([str(n) for n in obj.english_names.all()])))

    @display(description="Western scientific names")
    def _western_scientific_names(self, obj):
        return mark_safe(unescape(' <br /> '.join([str(n) for n in obj.western_scientific_names.all()])))

    @display(description=mark_safe(unescape("<span class='first-nations-unicode'>hən̓q̓əmin̓əm̓</span> names")))
    def _halkomelem_names(self, obj):
        return mark_safe(unescape(' <br /> '.join([f"<span class='first-nations-unicode'>{n}</span>" for n in obj.halkomelem_names.all()])))

    @display(description=mark_safe(unescape("<span class='first-nations-unicode'>Sḵwx̱wú7mesh Sníchim</span> names")))
    def _squamish_names(self, obj):
        return mark_safe(unescape(' <br /> '.join([f"<span class='first-nations-unicode'>{n}</span>" for n in obj.squamish_names.all()])))

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