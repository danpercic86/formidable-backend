from pprint import pprint
from typing import Dict, List, Any, OrderedDict

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
)
from formidable.models import Application, Response, Validator
from formidable.serializers.response import (
    ResponseDetailSerializer,
    NestedResponseCreateSerializer,
)


class ApplicationDetailSerializer(ModelSerializer):
    responses = ResponseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = ID, FORM, RESPONSES
        read_only_fields = fields


class ApplicationCreateSerializer(ModelSerializer):
    responses = NestedResponseCreateSerializer(many=True)
    applicant = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Application
        exclude = CREATED, MODIFIED, STATUS, STATUS_CHANGED

    def validate(self, attrs: Dict):
        errors = {}

        for response_data in attrs[RESPONSES]:  # type: OrderedDict
            for validator in response_data[FIELD].validators.filter(
                is_enabled=True
            ):  # type: Validator
                if error := validator(response_data[VALUE]):
                    errors.update(error.detail)

        if errors:
            raise ValidationError(errors)
        return attrs

    def create(self, validated_data: Dict[str, Any]):
        pprint(validated_data)
        pprint(self.context)

        responses_data: List[Dict] = validated_data.pop(RESPONSES)
        application = Application.objects.create(**validated_data)

        Response.objects.bulk_create(
            [Response(application=application, **data) for data in responses_data]
        )

        return application
