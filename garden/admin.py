import json
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from html import unescape
from django.contrib.admin import ModelAdmin, TabularInline
from tinymce.widgets import TinyMCE
from django_rq import enqueue
from django.contrib import messages

from .models import Feature, Image, Point, \
    Location1PanoramaPoint, Location2PanoramaPoint, Location3PanoramaPoint, \
    EnglishName, WesternScientificName, \
    HalkomelemName, SquamishName
from .schema import FeatureSchema

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

def add_map_context(extra_context, lock_view=None, is_edit_mode=False, point_id=None):
    extra_context = extra_context or {}
    features = Feature.objects.prefetch_related(
        'points', 'images',
        'location_1_panorama_points', 'location_2_panorama_points', 'location_3_panorama_points',
        'english_names', 'western_scientific_names',
        'halkomelem_names', 'squamish_names',
    ).order_by('number', 'id').all()
    data = [FeatureSchema.from_orm(feature).dict() for feature in features]

    extra_context['is_map'] = True
    extra_context['features'] = json.dumps(data)
    extra_context['display_options'] = json.dumps({
        'lockView': lock_view,
        'canEdit': True,
        'isEditMode': is_edit_mode,
        'editPointId': point_id,
    })

    return extra_context

@admin.register(Feature)
class FeatureAdmin(ModelAdmin):
    fields = [
        ('feature_type', 'number', 'published'),
        'video_original',
        'content',
        'references',
    ]

    list_display = ('id', 'published', 'feature_type', 'number', '_english_names', '_western_scientific_names', '_halkomelem_names', '_squamish_names', '_video_status')
    list_display_links = ('id', 'published', 'feature_type', 'number', '_english_names', '_western_scientific_names', '_halkomelem_names', '_squamish_names', '_video_status')
    ordering = ['feature_type', 'number']
    search_fields = [
        'number',
        'english_names__name', 'english_names__descriptor',
        'western_scientific_names__name', 'western_scientific_names__descriptor',
        'halkomelem_names__name', 'halkomelem_names__descriptor',
        'squamish_names__name', 'squamish_names__descriptor',
    ]
    actions = ['generate_thumbnail', 'generate_dash', 'generate_thumbnails_vtt']
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

    @admin.action(description="(Re)Generate video thumbnail for selected Features")
    def generate_thumbnail(self, request, queryset):
        from .tasks import task_video_thumbnail_generator
        job_count = 0
        for feature in queryset:
            if feature.has_video_original():
                enqueue(task_video_thumbnail_generator, feature.pk)
                job_count+=1
        self.message_user(
            request,
            f'Created {job_count} jobs to generate video thumbnails for features.',
            messages.SUCCESS,
        )

    @admin.action(description="(Re)Generate video streams for selected Features")
    def generate_dash(self, request, queryset):
        from .tasks import task_video_dash_generator
        job_count = 0
        for feature in queryset:
            if feature.has_video_original():
                enqueue(task_video_dash_generator, feature.pk)
                job_count+=1
        self.message_user(
            request,
            f'Created {job_count} jobs to generate video streams for features.',
            messages.SUCCESS,
        )

    @admin.action(description="(Re)Generate video VTT thumbnails for selected Features")
    def generate_thumbnails_vtt(self, request, queryset):
        from .tasks import task_video_thumbnails_vtt_generator
        job_count = 0
        for feature in queryset:
            if feature.has_video_original():
                enqueue(task_video_thumbnails_vtt_generator, feature.pk)
                job_count+=1
        self.message_user(
            request,
            f'Created {job_count} jobs to generate VTT video thumbnails for features.',
            messages.SUCCESS,
        )

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

    def _video_status(self, obj):
        success = '<strong><span style="color: green">✓<span></strong>'
        failure = '<strong><span style="color: red">x<span></strong>'
        return mark_safe(f'''
            Original video: {success if obj.has_video_original() else failure}<br />
            Streamable video: {success if obj.has_video() else failure}<br />
            Poster thumbnail: {success if obj.has_video_thumbnail() else failure}<br />
            Preview thumbnails: {success if obj.has_video_thumbnails_vtt() else failure}
        ''')
    _video_status.short_description = "Video Status"



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
        extra_context = add_map_context(extra_context, lock_view='overhead')
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='overhead', is_edit_mode=True, point_id=int(object_id))
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='overhead', is_edit_mode=True)
        return super().add_view(request, form_url, extra_context=extra_context)

class PanoramaPointAdmin(ModelAdmin):
    fields = [
        'feature',
        ('yaw', 'pitch'),
    ]

    list_display = ('id', 'feature', 'yaw', 'pitch')
    list_display_links = ('id', 'feature', 'yaw', 'pitch')
    ordering = ['feature', '-pitch', 'yaw']
    autocomplete_fields = ['feature']
    list_per_page = 5

@admin.register(Location1PanoramaPoint)
class Location1PanoramaPointAdmin(PanoramaPointAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='panorama_location_1')
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='panorama_location_1', is_edit_mode=True, point_id=int(object_id))
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='panorama_location_1', is_edit_mode=True)
        return super().add_view(request, form_url, extra_context=extra_context)

@admin.register(Location2PanoramaPoint)
class Location2PanoramaPointAdmin(PanoramaPointAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='panorama_location_2')
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='panorama_location_2', is_edit_mode=True, point_id=int(object_id))
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='panorama_location_2', is_edit_mode=True)
        return super().add_view(request, form_url, extra_context=extra_context)

@admin.register(Location3PanoramaPoint)
class Location3PanoramaPointAdmin(PanoramaPointAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='panorama_location_3')
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='panorama_location_3', is_edit_mode=True, point_id=int(object_id))
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = add_map_context(extra_context, lock_view='panorama_location_3', is_edit_mode=True)
        return super().add_view(request, form_url, extra_context=extra_context)