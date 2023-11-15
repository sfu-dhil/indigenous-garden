from rest_framework import serializers
from .models import Plant, Image, Point

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        exclude = ['created', 'modified']
        read_only = True

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ['created', 'modified']
        read_only = True

class PlantSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        exclude = ['created', 'modified']
        read_only = True
