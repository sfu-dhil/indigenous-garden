from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from polymorphic.contrib.drf.serializers import PolymorphicSerializer

from django_dh_map.serializers import FeatureSerializer, InfoPageSerializer, \
    ContentBlockPolymorphicSerializer

from .models import ContentBlockMultilingualLabels, ContentBlockMultilingualLabel, \
    WelcomeModal, WelcomeModalContent


class ContentBlockMultilingualLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlockMultilingualLabel
        fields = ['id', 'language', 'label', 'descriptor', 'audio']

class ContentBlockMultilingualLabelsSerializer(serializers.ModelSerializer):
    labels = ContentBlockMultilingualLabelSerializer(many=True)
    class Meta:
        model = ContentBlockMultilingualLabels
        fields = ['id', 'labels']

class ContentBlockPolymorphicOverrideSerializer(ContentBlockPolymorphicSerializer):
    def __init__(self, *args, **kwargs):
        self.model_serializer_mapping[ContentBlockMultilingualLabels] = ContentBlockMultilingualLabelsSerializer
        super().__init__(*args, **kwargs)

class FeatureOverrideSerializer(FeatureSerializer):
    content_blocks = ContentBlockPolymorphicOverrideSerializer(many=True)

class InfoPageOverrideSerializer(InfoPageSerializer):
    content_blocks = ContentBlockPolymorphicOverrideSerializer(many=True)



class WelcomeModalContentSerializer(serializers.ModelSerializer):
    content_blocks = ContentBlockPolymorphicOverrideSerializer(many=True)
    class Meta:
        model = WelcomeModalContent
        fields = ['content_blocks']

class WelcomeModalSerializer(serializers.ModelSerializer):
    content_item = WelcomeModalContentSerializer()
    class Meta:
        model = WelcomeModal
        fields = ['title', 'display', 'close_button_label', 'content_item']