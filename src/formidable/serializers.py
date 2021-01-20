from typing import List, Dict

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from formidable.models import ResponseField, Response, FormField, Choice, Validator, Form
from formidable.model_fields import *


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        exclude = CREATED, MODIFIED, FIELDS


class ValidatorSerializer(ModelSerializer):
    class Meta:
        model = Validator
        exclude = FIELD, DESCRIPTION, IS_ENABLED


class FormFieldSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    validators = ValidatorSerializer(many=True, read_only=True)

    class Meta:
        model = FormField
        exclude = CREATED, MODIFIED, FORM


class FormSerializer(ModelSerializer):
    fields = FormFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        exclude = CREATED, MODIFIED


class ResponseFieldSerializer(ModelSerializer):
    class Meta:
        model = ResponseField
        exclude = CREATED, MODIFIED, RESPONSE, STATUS_CHANGED


class ResponseSerializer(ModelSerializer):
    fields = ResponseFieldSerializer(many=True)

    class Meta:
        model = Response
        exclude = CREATED, MODIFIED

    def create(self, validated_data: Dict):
        fields_data: List[Dict] = validated_data.pop(FIELDS)
        for field_data in fields_data:
            form_field: FormField
            if form_field := field_data.get(FIELD):
                errors = {}
                for validator in form_field.validators.filter(is_enabled=True):
                    error: ValidationError
                    if error := validator(field_data.get(VALUE), form_field):
                        errors.update(error.detail)
                if errors:
                    raise ValidationError(errors)

        response = Response.objects.create(**validated_data)
        for field_data in fields_data:
            ResponseField.objects.create(response=response, **field_data)
        return response


class ResponseFieldCreateSerializer(ModelSerializer):
    class Meta:
        model = ResponseField
        exclude = (
            CREATED,
            MODIFIED,
            RESPONSE,
            STATUS_CHANGED,
            ERRORS,
            OBSERVATIONS,
            STATUS,
        )


class ResponseCreateSerializer(ModelSerializer):
    fields = ResponseFieldCreateSerializer(many=True)

    class Meta:
        model = Response
        exclude = CREATED, MODIFIED, STATUS, STATUS_CHANGED
