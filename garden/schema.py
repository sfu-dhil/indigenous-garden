from ninja import ModelSchema, Field
from typing import List, Optional

from .models import Feature, Image, Point, Name


class NameSchema(ModelSchema):
    class Meta:
        model = Name
        fields = [
            'name', 'descriptor', 'audio'
        ]

class PointSchema(ModelSchema):
    class Meta:
        model = Point
        fields = [
            'id', 'x', 'y'
        ]

class ImageSchema(ModelSchema):
    class Meta:
        model = Image
        fields = [
            'id', 'image', 'thumbnail', 'description', 'license'
        ]

class FeatureSchema(ModelSchema):
    english_names: List[NameSchema] = []
    western_scientific_names: List[NameSchema] = []
    halkomelem_names: List[NameSchema] = []
    squamish_names: List[NameSchema] = []
    points: List[PointSchema] = []
    images: List[ImageSchema] = []

    class Meta:
        model = Feature
        fields = [
            'id', 'feature_type', 'number', 'video', 'captions', 'content', 'references',
        ]