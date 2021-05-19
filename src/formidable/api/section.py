from django.db.models import QuerySet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from formidable.models import Section
from formidable.serializers import SectionSerializer


class SectionApi(RetrieveModelMixin, GenericViewSet):
    serializer_class = SectionSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Section] = Section.objects.prefetch_related(
        "fields", "fields__choices", "fields__validators"
    )
