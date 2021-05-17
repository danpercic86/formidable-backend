from pprint import pprint
from typing import Dict, List, Union

from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer

from administration.models import User
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
from formidable.models import Application, Response, Validator, Form, Field
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

    def validate(
        self,
        attrs: Dict[str, Union[List[Dict[str, Union[str, Field]]], User, Form, str]],
    ):
        errors = {}
        pprint(attrs)

        for response_data in attrs.get(RESPONSES):
            for validator in response_data.get(FIELD).validators.filter(
                is_enabled=True
            ):  # type: Validator
                if error := validator(response_data.get(VALUE)):
                    errors.update(error.detail)

        if errors:
            raise ValidationError(errors)
        return attrs

    def create(
        self, validated_data: Dict[str, Union[Form, List[Dict[str, Union[str, Field]]]]]
    ):
        print("Serializer create")
        pprint(validated_data)
        pprint(self.context)

        responses_data = validated_data.pop(RESPONSES)
        application = Application.objects.create(**validated_data)

        for response_data in responses_data:
            Response.objects.create(application=application, **response_data)

        return application
