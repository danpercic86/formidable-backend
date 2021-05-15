from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from formidable.models import FormSection, Application, Form, Response
from formidable.serializers import (
    FormSectionSerializer,
    ApplicationSerializer,
    ApplicationCreateSerializer,
    FormSerializer, ResponseSerializer,
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
        request=ApplicationCreateSerializer,
        responses={status.HTTP_201_CREATED: ApplicationSerializer},
    )
)
class ApplicationViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = ApplicationSerializer
    queryset: QuerySet[Application] = Application.objects.prefetch_related(
        "responses__field"
    ).all()


class ResponseViewSet(NestedViewSetMixin, ModelViewSet, GenericViewSet):
    serializer_class = ResponseSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Response] = Response.objects.all()
