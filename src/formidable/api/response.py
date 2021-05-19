from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from formidable.models import Response
from formidable.serializers.response import NestedResponseCreateSerializer, \
    ResponseDetailSerializer


@extend_schema_view(
    create=extend_schema(
        request=NestedResponseCreateSerializer,
        responses={status.HTTP_201_CREATED: ResponseDetailSerializer},
    )
)
class NestedResponseApi(NestedViewSetMixin, ModelViewSet):
    serializer_class = NestedResponseCreateSerializer
    queryset: QuerySet[Response] = Response.objects.all()
