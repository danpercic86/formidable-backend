from typing import Dict, List, Any, OrderedDict
from typing import Tuple

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer, Serializer

from administration.models import User
from formidable.constants import Errors
from formidable.constants import (
    ID,
    FIELD,
    VALUE,
    ERRORS,
    CREATED,
    MODIFIED,
    STATUS_CHANGED,
    OBSERVATIONS,
    STATUS,
    APPLICATION,
)
from formidable.models import Field, Section, Application, Validator
from formidable.models import Response


class ResponseDetailSerializer(ModelSerializer):
    read_only = True

    class Meta:
        model = Response
        fields: Tuple = ID, FIELD, VALUE, ERRORS, STATUS
        read_only_fields = fields


class ResponseCreateSerializer(ModelSerializer):
    class Meta:
        model = Response
        exclude: Tuple = (
            CREATED,
            MODIFIED,
            STATUS_CHANGED,
            ERRORS,
            OBSERVATIONS,
            STATUS,
            APPLICATION,
        )


class FromRoute:
    requires_context = True

    def __init__(self, model, lookup: str):
        self.model = model
        self.lookup = lookup

    def __call__(self, serializer_field):
        value = serializer_field.context["view"].kwargs.get(self.lookup)
        return None if not value else self.model._default_manager.get(id=value)

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class NestedResponseCreateSerializer(Serializer):
    user: User = HiddenField(default=CurrentUserDefault())
    section: Section = HiddenField(default=FromRoute(Section, "_field__section"))
    responses = ResponseCreateSerializer(many=True)

    def validate(self, attrs: OrderedDict):
        _, section, responses_data = attrs.values()  # type: User, Section, List[Dict]
        fields = frozenset(map(lambda x: x[FIELD], responses_data))

        self._check_same_section(fields, section)
        errors = self._check_required_fields(fields, section)

        for data in responses_data:
            errors.update(self._validate_response(data[VALUE], data[FIELD].validators))

        if errors:
            raise ValidationError(errors)
        return attrs

    def create(self, validated_data: OrderedDict[str, Any]):
        user, section, responses = validated_data.values()  # type: User, Section, List

        app, _ = Application.objects.get_or_create(applicant=user, form=section.form)
        responses = [Response(application=app, **data) for data in responses]

        return {"responses": Response.objects.bulk_create(responses)}

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def _check_same_section(fields: frozenset[Field], section: Section) -> None:
        for field in fields:
            if field.section != section:
                raise ValidationError({"not_same_section": Errors.NotSameSection})

    @staticmethod
    def _validate_response(
        value: str, validators: QuerySet[Validator]
    ) -> Dict[str, List[ErrorDetail]]:
        errors = {}

        for validator in validators.filter(is_enabled=True):  # type: Validator
            if error := validator(value):
                errors.update(error.detail)

        return errors

    @staticmethod
    def _check_required_fields(
        fields: frozenset[Field], section: Section
    ) -> Dict[str, List[ErrorDetail]]:
        field_ids = frozenset(map(lambda field: field.id, fields))
        missing = section.fields.filter(is_required=True).exclude(id__in=field_ids)

        return {str(field): Errors.RequiredField for field in missing}


class ResponseSerializer(ModelSerializer):
    class Meta:
        model = Response
        exclude: Tuple = CREATED, MODIFIED, STATUS_CHANGED
