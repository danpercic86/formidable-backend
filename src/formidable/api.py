from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin

from formidable.models import Section, Application, Form, Response
from formidable.serializers import (
    ApplicationCreateSerializer,
)
from formidable.serializers import (
    SectionSerializer,
    FormSerializer,
    ApplicationDetailSerializer,
)
from formidable.serializers.form import FormDetailSerializer
from formidable.serializers.response import (
    NestedResponseCreateSerializer,
    ResponseDetailSerializer,
)


class FormApi(DetailSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = FormSerializer
    serializer_detail_class = FormDetailSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Form] = Form.objects.none()
    queryset_detail = Form.objects.prefetch_related("sections").only(
        *FormDetailSerializer.Meta.fields[:2]
    )


class SectionApi(RetrieveModelMixin, GenericViewSet):
    serializer_class = SectionSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Section] = Section.objects.prefetch_related(
        "fields", "fields__choices", "fields__validators"
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
class ApplicationApi(
    NestedViewSetMixin,
    DetailSerializerMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = ApplicationCreateSerializer
    serializer_detail_class = ApplicationDetailSerializer
    queryset: QuerySet[Application] = Application.objects.all()
    queryset_detail = (
        Application.objects.only(*ApplicationDetailSerializer.Meta.fields)
        .prefetch_related("responses")
        .select_related("responses__field")
    )
    # to be removed
    permission_classes = (AllowAny,)


@extend_schema_view(
    create=extend_schema(
        request=NestedResponseCreateSerializer(many=True),
        responses={status.HTTP_201_CREATED: ResponseDetailSerializer},
    )
)
class ResponseApi(NestedViewSetMixin, ModelViewSet):
    serializer_class = NestedResponseCreateSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Response] = Response.objects.all()
