from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from nested_admin.nested import NestedStackedInline
from nested_admin.polymorphic import NestedPolymorphicModelAdmin, NestedStackedPolymorphicInline

from django_dh_map.models import InfoPage, Feature
from django_dh_map.admin import DjangoDhMapAdminMixin, ContentBlockInline, IconInline, SortableHiddenMixinTinyMceFix, \
    InfoPageAdmin, FeatureAdmin

from .models import WelcomeModal, WelcomeModalContent, \
    ContentBlockMultilingualLabels, ContentBlockMultilingualLabel


class FixSingletonModelMixin():
    # Fix user message success vs info
    def response_change(self, request, obj):
        msg = _("{obj} was changed successfully.").format(obj=force_str(obj))
        if "_continue" in request.POST:
            self.message_user(request, msg + " " + _("You may edit it again below."), messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect("../../")

class ContentBlockOverrideInline(ContentBlockInline):
    class ContentBlockMultilingualLabelsInline(SortableHiddenMixinTinyMceFix, NestedStackedPolymorphicInline.Child):
        model = ContentBlockMultilingualLabels
        fields = ['position']

        class ContentBlockMultilingualLabelInline(SortableHiddenMixinTinyMceFix, NestedStackedInline):
            model = ContentBlockMultilingualLabel
            min_num = 1
            extra = 0
            classes = ['collapse']
            fields = [('language', 'label', 'descriptor'), ('_audio_tag', 'original'), 'position']
            readonly_fields = ['_audio_tag']
            def _audio_tag(self, obj):
                return mark_safe(f'<audio src="{obj.audio.url}" controls preload="metadata" />') if obj.audio else 'N/A'
            _audio_tag.short_description = 'Preview'

        inlines = [ContentBlockMultilingualLabelInline]

    def get_child_inlines(self):
        return (*super().get_child_inlines(), self.ContentBlockMultilingualLabelsInline,)

admin.site.unregister(InfoPage)
@admin.register(InfoPage)
class InfoPageOverrideAdmin(InfoPageAdmin):
    inlines = [ContentBlockOverrideInline]

admin.site.unregister(Feature)
@admin.register(Feature)
class FeatureOverrideAdmin(FeatureAdmin):
    inlines = [
        IconInline,
        ContentBlockOverrideInline
    ]

class WelcomeModalContentInline(NestedStackedInline):
    model = WelcomeModalContent
    min_num = 0
    max_num = 1
    extra = 0
    inlines = [ContentBlockOverrideInline]

@admin.register(WelcomeModal)
class WelcomeModalAdmin(DjangoDhMapAdminMixin, FixSingletonModelMixin, SingletonModelAdmin, NestedPolymorphicModelAdmin):
    fields = ['title', 'display', 'close_button_label']
    inlines = [WelcomeModalContentInline]