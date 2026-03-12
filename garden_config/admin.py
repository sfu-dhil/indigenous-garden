from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from django.contrib.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from adminsortable2.admin import SortableTabularInline, SortableAdminBase
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils.encoding import force_str
from django.contrib import messages

from .models import WelcomePopup, History, ResidentialSchools, \
    ContextualEthicalFraming, RelationalInterconnectedTeachings, \
    Acknowledgements, AcknowledgementsContentBlock

# Admin Panel Items
class AcknowledgementsContentBlockInline(SortableTabularInline):
    fields = ['heading', 'list', 'content', 'order']
    model = AcknowledgementsContentBlock
    extra = 0

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

# Admin Panel Items
@admin.register(WelcomePopup)
class WelcomePopupAdmin(SingletonModelAdmin):
    fields = [
        'heading',
        ('heading_halkomelem', 'heading_halkomelem_audio'),
        ('heading_squamish', 'heading_squamish_audio'),
        ('_thumbnail_image_tag', 'image', 'image_caption'),
        'content',
    ]
    readonly_fields = ['_thumbnail_image_tag']

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    def _thumbnail_image_tag(self, obj):
        return mark_safe(f'<img src="{obj.thumbnail.url}" style="max-width: 800px; max-height: 450px" />') if obj.thumbnail else ''
    _thumbnail_image_tag.short_description = 'Thumbnail Preview'

    # Fix user message success vs info
    def response_change(self, request, obj):
        msg = _("{obj} was changed successfully.").format(obj=force_str(obj))
        if "_continue" in request.POST:
            self.message_user(request, msg + " " + _("You may edit it again below."), messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect("../../")


@admin.register(History)
class HistoryAdmin(SingletonModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    # Fix user message success vs info
    def response_change(self, request, obj):
        msg = _("{obj} was changed successfully.").format(obj=force_str(obj))
        if "_continue" in request.POST:
            self.message_user(request, msg + " " + _("You may edit it again below."), messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect("../../")

@admin.register(ResidentialSchools)
class ResidentialSchoolsAdmin(SingletonModelAdmin):
    fields = [
        'heading',
        ('_thumbnail_image_tag', 'image', 'image_caption'),
        'content',
    ]
    readonly_fields = ['_thumbnail_image_tag']

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    def _thumbnail_image_tag(self, obj):
        return mark_safe(f'<img src="{obj.thumbnail.url}" style="max-width: 800px; max-height: 450px" />') if obj.thumbnail else ''
    _thumbnail_image_tag.short_description = 'Thumbnail Preview'

    # Fix user message success vs info
    def response_change(self, request, obj):
        msg = _("{obj} was changed successfully.").format(obj=force_str(obj))
        if "_continue" in request.POST:
            self.message_user(request, msg + " " + _("You may edit it again below."), messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect("../../")

@admin.register(ContextualEthicalFraming)
class ContextualEthicalFramingAdmin(SingletonModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    # Fix user message success vs info
    def response_change(self, request, obj):
        msg = _("{obj} was changed successfully.").format(obj=force_str(obj))
        if "_continue" in request.POST:
            self.message_user(request, msg + " " + _("You may edit it again below."), messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect("../../")

@admin.register(RelationalInterconnectedTeachings)
class RelationalInterconnectedTeachingsAdmin(SingletonModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    # Fix user message success vs info
    def response_change(self, request, obj):
        msg = _("{obj} was changed successfully.").format(obj=force_str(obj))
        if "_continue" in request.POST:
            self.message_user(request, msg + " " + _("You may edit it again below."), messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect("../../")

@admin.register(Acknowledgements)
class AcknowledgementsAdmin(SortableAdminBase, SingletonModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE,
        },
    }

    inlines = [
        AcknowledgementsContentBlockInline,
    ]

    # Fix user message success vs info
    def response_change(self, request, obj):
        msg = _("{obj} was changed successfully.").format(obj=force_str(obj))
        if "_continue" in request.POST:
            self.message_user(request, msg + " " + _("You may edit it again below."), messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect("../../")