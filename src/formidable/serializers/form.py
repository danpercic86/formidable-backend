from rest_framework.serializers import ModelSerializer

from formidable.constants import ID, NAME, DESCRIPTION, SECTIONS
from formidable.models import Form
from formidable.serializers.section import SectionMinimalSerializer


class FormSerializer(ModelSerializer):
    sections = SectionMinimalSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        exclude = "created", "modified"


class FormDetailSerializer(ModelSerializer):
    sections = SectionMinimalSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = ID, NAME, DESCRIPTION, SECTIONS
        read_only_fields = fields
