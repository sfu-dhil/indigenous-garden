from rest_framework import serializers
from .models import Point, Feature

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        exclude = ['feature', 'created', 'modified']
        read_only = True

class FeatureSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Feature
        fields = ['id', 'feature_type', 'number', 'color', 'points']
        read_only = True


        ordering = ['-y', 'x']

    def get_color(self, object):
        if object.feature_type == Feature.FeatureTypes.FEATURE:
            return '#6495ED'

        return '#7cb341'
