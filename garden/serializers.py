from rest_framework import serializers
from .models import Feature, Image, OverheadPoint, PanoramaPoint

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ['created', 'modified']
        read_only = True

class OverheadPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverheadPoint
        exclude = ['created', 'modified']
        read_only = True

class PanoramaPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanoramaPoint
        exclude = ['created', 'modified']
        read_only = True

class FeatureSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    overhead_points = OverheadPointSerializer(many=True, read_only=True)
    panorama_points = PanoramaPointSerializer(many=True, read_only=True)

    class Meta:
        model = Feature
        exclude = ['created', 'modified']
        read_only = True
