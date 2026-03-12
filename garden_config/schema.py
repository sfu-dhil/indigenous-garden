from ninja import Schema, ModelSchema, Field
from typing import List, Optional

from .models import WelcomePopup, History, ResidentialSchools, \
    ContextualEthicalFraming, RelationalInterconnectedTeachings, \
    Acknowledgements, AcknowledgementsContentBlock


class WelcomePopupSchema(ModelSchema):
    class Meta:
        model = WelcomePopup
        fields = [
            'heading',
            'heading_halkomelem', 'heading_halkomelem_audio',
            'heading_squamish', 'heading_squamish_audio',
            'image', 'thumbnail', 'image_caption',
            'content',
        ]

class HistorySchema(ModelSchema):
    class Meta:
        model = History
        fields = [
            'heading', 'content_1', 'content_2', 'content_3', 'content_4', 'content_5',
        ]

class ResidentialSchoolsSchema(ModelSchema):
    class Meta:
        model = ResidentialSchools
        fields = [
            'heading',
            'image', 'thumbnail', 'image_caption',
            'content',
        ]

class ContextualEthicalFramingSchema(ModelSchema):
    class Meta:
        model = ContextualEthicalFraming
        fields = [
            'heading', 'content',
        ]

class RelationalInterconnectedTeachingsSchema(ModelSchema):
    class Meta:
        model = RelationalInterconnectedTeachings
        fields = [
            'heading', 'content',
        ]

class AcknowledgementsContentBlockSchema(ModelSchema):
    class Meta:
        model = AcknowledgementsContentBlock
        fields = [
            'heading', 'list', 'content',
        ]
class AcknowledgementsSchema(ModelSchema):
    content_blocks: List[AcknowledgementsContentBlockSchema] = []

    class Meta:
        model = Acknowledgements
        fields = [
            'heading', 'content',
        ]
