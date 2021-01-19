from typing import List, Dict

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from formidable.models import ResponseField, Response, FormField, Choice, Validator, Form


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        exclude = "created", "modified", "fields"


class ValidatorSerializer(ModelSerializer):
    class Meta:
        model = Validator
        exclude = "field", "description", "is_enabled"


class FormFieldSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    validators = ValidatorSerializer(many=True, read_only=True)

    class Meta:
        model = FormField
        exclude = "created", "modified", "form"


class FormSerializer(ModelSerializer):
    fields = FormFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        exclude = "created", "modified"


class ResponseFieldSerializer(ModelSerializer):
    class Meta:
        model = ResponseField
        exclude = "created", "modified", "response", "status_changed"


class ResponseSerializer(ModelSerializer):
    fields = ResponseFieldSerializer(many=True)

    class Meta:
        model = Response
        exclude = "created", "modified"

    def create(self, validated_data: Dict):
        fields_data: List[Dict] = validated_data.pop("fields")
        for field_data in fields_data:
            form_field: FormField
            if form_field := field_data.get("field"):
                errors = {}
                for validator in form_field.validators.filter(is_enabled=True):
                    error: ValidationError
                    if error := validator(field_data.get("value"), form_field):
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
            "created",
            "modified",
            "response",
            "status_changed",
            "errors",
            "observations",
            "status",
        )


class ResponseCreateSerializer(ModelSerializer):
    fields = ResponseFieldCreateSerializer(many=True)

    class Meta:
        model = Response
        exclude = "created", "modified", "status", "status_changed"
