from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from formidable.models import Form, Application
from formidable.serializers import (
    FormSerializer,
    ResponseSerializer,
    ResponseCreateSerializer,
)


class FormViewSet(ModelViewSet):
    serializer_class = FormSerializer
    queryset: QuerySet[Form] = Form.objects.prefetch_related("fields").all()


@extend_schema_view(
    create=extend_schema(
        description="Create new response",
        auth=[],
        request=ResponseCreateSerializer,
        responses={status.HTTP_201_CREATED: ResponseSerializer},
    )
)
class ResponseViewSet(ModelViewSet):
    serializer_class = ResponseSerializer
    queryset: QuerySet[Application] = Application.objects.prefetch_related("fields").all()
