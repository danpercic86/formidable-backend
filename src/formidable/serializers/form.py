from rest_framework.serializers import ModelSerializer

from formidable.constants import CREATED, MODIFIED
from formidable.models import Form
from formidable.serializers.section import SectionMinimalSerializer


class FormSerializer(ModelSerializer):
    sections = SectionMinimalSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        exclude = CREATED, MODIFIED
