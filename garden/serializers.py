from rest_framework import serializers
from .models import Feature, Image, Point


class NameSerializer(serializers.Serializer):
    name = serializers.CharField()
    descriptor = serializers.CharField()
    audio = serializers.FileField()

    class Meta:
        read_only = True

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'x', 'y']
        read_only = True

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'thumbnail', 'description', 'license']
        read_only = True

class FeatureSerializer(serializers.ModelSerializer):
    english_names = NameSerializer(many=True, read_only=True)
    western_scientific_names = NameSerializer(many=True, read_only=True)
    halkomelem_names = NameSerializer(many=True, read_only=True)
    squamish_names = NameSerializer(many=True, read_only=True)
    points = PointSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Feature
        fields = [
            'id', 'feature_type', 'number', 'video', 'captions', 'content',
            'english_names', 'western_scientific_names', 'halkomelem_names', 'squamish_names',
            'points', 'images',
        ]
        read_only = True