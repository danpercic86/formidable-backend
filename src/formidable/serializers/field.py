from typing import Tuple

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from administration.models import User
from formidable.constants import CREATED, MODIFIED, SECTION, ID, VALUE, ERRORS, STATUS
from formidable.models import Field, Response
from formidable.serializers.choice import ChoiceSerializer
from formidable.serializers.validator import ValidatorSerializer


class ResponseSerializer(ModelSerializer):
    class Meta:
        model = Response
        fields: Tuple = ID, VALUE, ERRORS, STATUS
        read_only_fields = fields


class FieldSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    validators = ValidatorSerializer(many=True, read_only=True)
    response = SerializerMethodField()

    class Meta:
        model = Field
        exclude = CREATED, MODIFIED, SECTION

    def get_response(self, field: Field):
        user: User = self.context["request"].user
        response = field.responses.filter(application__applicant=user).first()
        return ResponseSerializer(response).data
