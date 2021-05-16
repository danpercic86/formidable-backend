from typing import Tuple

from rest_framework.serializers import ModelSerializer

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
from formidable.models import Response


class ResponseDetailSerializer(ModelSerializer):
    read_only = True

    class Meta:
        model = Response
        fields: Tuple = ID, FIELD, VALUE, ERRORS
        read_only_fields = fields


class ResponseCreateSerializer(ModelSerializer):
    class Meta:
        model = Response
        exclude: Tuple = CREATED, MODIFIED, STATUS_CHANGED, ERRORS, OBSERVATIONS, STATUS


class ApplicationResponseCreateSerializer(ResponseCreateSerializer):
    class Meta(ResponseCreateSerializer.Meta):
        exclude: Tuple = ResponseCreateSerializer.Meta.exclude + (APPLICATION,)


class ResponseSerializer(ModelSerializer):
    class Meta:
        model = Response
        exclude: Tuple = CREATED, MODIFIED, STATUS_CHANGED
