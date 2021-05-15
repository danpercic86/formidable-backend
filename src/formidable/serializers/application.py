from typing import Dict, List

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from formidable.constants import (
    RESPONSES,
    FORM,
    ID,
    CREATED,
    MODIFIED,
    STATUS,
    STATUS_CHANGED,
    APPLICANT,
    FIELDS,
    FIELD,
    VALUE,
)
from formidable.models import Application, Field, Response
from formidable.serializers.response import (
    ResponseDetailSerializer,
    ApplicationResponseCreateSerializer,
    ResponseSerializer,
)


class ApplicationDetailSerializer(ModelSerializer):
    responses = ResponseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = ID, FORM, RESPONSES
        read_only_fields = fields


class ApplicationCreateSerializer(ModelSerializer):
    responses = ApplicationResponseCreateSerializer(many=True)

    class Meta:
        model = Application
        exclude = CREATED, MODIFIED, STATUS, STATUS_CHANGED, APPLICANT


class ApplicationSerializer(ModelSerializer):
    responses = ResponseSerializer(many=True)

    class Meta:
        model = Application
        exclude = CREATED, MODIFIED

    def create(self, validated_data: Dict):
        fields_data: List[Dict] = validated_data.pop(FIELDS)
        for field_data in fields_data:
            form_field: Field
            if form_field := field_data.get(FIELD):
                errors = {}
                for validator in form_field.validators.filter(is_enabled=True):
                    error: ValidationError
                    if error := validator(field_data.get(VALUE), form_field):
                        errors.update(error.detail)
                if errors:
                    raise ValidationError(errors)

        response = Application.objects.create(**validated_data)
        for field_data in fields_data:
            Response.objects.create(response=response, **field_data)
        return response
