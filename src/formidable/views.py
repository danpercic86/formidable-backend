from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin

from formidable.models import Section, Application, Form, Response
from formidable.serializers.request import (
    ApplicationCreateSerializer,
    ApplicationSerializer,
    ResponseSerializer,
)
from formidable.serializers.response import (
    FormSectionSerializer,
    FormSerializer,
    ApplicationDetailSerializer,
)


class FormViewSet(ReadOnlyModelViewSet):
    serializer_class = FormSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Form] = Form.objects.prefetch_related("sections").all()


class FormSectionViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = FormSectionSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Section] = (
        Section.objects.prefetch_related("fields")
        .prefetch_related("fields__choices")
        .prefetch_related("fields__validators")
        .all()
    )


@extend_schema_view(
    create=extend_schema(
        description="Create new response",
        request=ApplicationCreateSerializer,
        responses={status.HTTP_201_CREATED: ApplicationDetailSerializer},
    ),
    retrieve=extend_schema(
        responses={status.HTTP_200_OK: ApplicationDetailSerializer},
    ),
    update=extend_schema(
        request=ApplicationCreateSerializer,
        responses={status.HTTP_200_OK: ApplicationDetailSerializer},
    ),
    partial_update=extend_schema(
        request=ApplicationCreateSerializer,
        responses={status.HTTP_200_OK: ApplicationDetailSerializer},
    ),
)
class ApplicationViewSet(
    NestedViewSetMixin,
    DetailSerializerMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = ApplicationSerializer
    serializer_detail_class = ApplicationDetailSerializer
    queryset: QuerySet[Application] = Application.objects.all()
    queryset_detail = (
        Application.objects.only(*ApplicationDetailSerializer.Meta.fields)
        .prefetch_related("responses")
        .select_related("responses__field")
    )

    # to be removed
    permission_classes = (AllowAny,)


class ResponseViewSet(NestedViewSetMixin, ModelViewSet, GenericViewSet):
    serializer_class = ResponseSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Response] = Response.objects.all()
