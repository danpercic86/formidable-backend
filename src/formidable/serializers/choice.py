from rest_framework.serializers import ModelSerializer

from formidable.constants import CREATED, MODIFIED, FIELDS
from formidable.models import Choice


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        exclude = CREATED, MODIFIED, FIELDS
