from rest_framework.serializers import ModelSerializer

from formidable.constants import CREATED, MODIFIED, NAME, ID
from formidable.models import Section
from formidable.serializers.field import FieldSerializer


class SectionSerializer(ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        exclude = CREATED, MODIFIED


class SectionMinimalSerializer(ModelSerializer):
    class Meta:
        model = Section
        fields = (ID, NAME)
