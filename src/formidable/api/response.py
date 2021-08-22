from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin

from formidable.models import Response
from formidable.serializers.response import (
    NestedResponseCreateSerializer,
    ResponseDetailSerializer,
)


@extend_schema_view(
    create=extend_schema(
        request=NestedResponseCreateSerializer,
        responses={status.HTTP_201_CREATED: ResponseDetailSerializer},
    ),
    retrieve=extend_schema(
        responses={status.HTTP_200_OK: ResponseDetailSerializer},
    ),
    list=extend_schema(
        responses={status.HTTP_200_OK: ResponseDetailSerializer(many=True)},
    )
)
class NestedResponseApi(NestedViewSetMixin, DetailSerializerMixin, ModelViewSet):
    serializer_class = NestedResponseCreateSerializer
    serializer_detail_class = ResponseDetailSerializer
    queryset: QuerySet[Response] = Response.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ResponseDetailSerializer
        super().get_serializer_class()
