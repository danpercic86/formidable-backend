from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin

from formidable.models import Application
from formidable.serializers import ApplicationCreateSerializer, \
    ApplicationDetailSerializer


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
