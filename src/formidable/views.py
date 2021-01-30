from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet

from formidable.models import FormSection, Application, Form
from formidable.serializers import (
    FormSectionSerializer,
    ResponseSerializer,
    ResponseCreateSerializer,
    FormSerializer,
)


class FormViewSet(ReadOnlyModelViewSet):
    serializer_class = FormSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Form] = Form.objects.prefetch_related("sections").all()


class FormSectionViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = FormSectionSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[FormSection] = (
        FormSection.objects.prefetch_related("fields")
        .prefetch_related("fields__choices")
        .prefetch_related("fields__validators")
        .all()
    )


@extend_schema_view(
    create=extend_schema(
        description="Create new response",
        request=ResponseCreateSerializer,
        responses={status.HTTP_201_CREATED: ResponseSerializer},
    )
)
class ResponseViewSet(ModelViewSet):
    serializer_class = ResponseSerializer
    queryset: QuerySet[Application] = Application.objects.prefetch_related(
        "fields"
    ).all()
