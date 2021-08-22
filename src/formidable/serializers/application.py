from typing import Dict, List, Any

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer

from formidable.constants import (
    RESPONSES,
    FORM,
    ID,
    CREATED,
    MODIFIED,
    STATUS,
    STATUS_CHANGED,
    FIELD,
    VALUE,
    Errors,
)
from formidable.models import Application, Response, Field
from formidable.serializers.response import (
    ResponseDetailSerializer,
    ResponseCreateSerializer,
)


class ApplicationDetailSerializer(ModelSerializer):
    responses = ResponseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = ID, FORM, RESPONSES
        read_only_fields = fields


class ApplicationCreateSerializer(ModelSerializer):
    responses = ResponseCreateSerializer(many=True)
    applicant = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Application
        exclude = CREATED, MODIFIED, STATUS, STATUS_CHANGED

    def validate(self, attrs: Dict[str, List]):
        self._check_all_fields_from_same_section(attrs[RESPONSES])
        errors = self._check_required_fields_present(attrs[RESPONSES])

        for response_data in attrs[RESPONSES]:
            errors.update(self._validate_response(response_data))

        if errors:
            raise ValidationError(errors)
        return attrs

    def create(self, validated_data: Dict[str, Any]):
        responses_data: List[Dict] = validated_data.pop(RESPONSES)
        app = Application.objects.create(**validated_data)

        responses = [Response(application=app, **data) for data in responses_data]
        Response.objects.bulk_create(responses)

        return app

    @staticmethod
    def _check_all_fields_from_same_section(responses: List[Dict]):
        section_ids = list(map(lambda response: response[FIELD].section_id, responses))
        same_section = section_ids.count(section_ids[0]) == len(section_ids)
        if same_section:
            return
        raise ValidationError({"not_same_section": Errors.NotSameSection})

    @staticmethod
    def _validate_response(data):
        errors = {}

        for validator in data[FIELD].validators.filter(is_enabled=True):
            if error := validator(data[VALUE]):
                errors.update(error.detail)

        return errors

    @staticmethod
    def _check_required_fields_present(responses: List[Dict]):
        field_ids = map(lambda response: response[FIELD].id, responses)
        required_fields = responses[0][FIELD].section.fields.filter(is_required=True)
        missing_fields: QuerySet[Field] = required_fields.exclude(id__in=field_ids)

        return {str(field): Errors.RequiredField for field in missing_fields}
