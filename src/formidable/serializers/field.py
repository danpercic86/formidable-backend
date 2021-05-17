from rest_framework.serializers import ModelSerializer

from formidable.constants import CREATED, MODIFIED, SECTION
from formidable.models import Field
from formidable.serializers.choice import ChoiceSerializer
from formidable.serializers.validator import ValidatorSerializer


class FieldSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    validators = ValidatorSerializer(many=True, read_only=True)

    class Meta:
        model = Field
        exclude = CREATED, MODIFIED, SECTION
