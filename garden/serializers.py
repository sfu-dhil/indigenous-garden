from rest_framework import serializers
from .models import OverheadPoint, PanoramaPoint

class OverheadPointSerializer(serializers.ModelSerializer):
    number = serializers.SerializerMethodField()
    feature_id = serializers.SerializerMethodField()

    class Meta:
        model = OverheadPoint
        exclude = ['feature', 'created', 'modified']
        read_only = True

    def get_number(self, object):
        return object.feature.number

    def get_feature_id(self, object):
        return object.feature_id

class PanoramaPointSerializer(serializers.ModelSerializer):
    number = serializers.SerializerMethodField()
    feature_id = serializers.SerializerMethodField()

    class Meta:
        model = PanoramaPoint
        exclude = ['feature', 'created', 'modified']
        read_only = True

    def get_number(self, object):
        return object.feature.number

    def get_feature_id(self, object):
        return object.feature_id
