from django.db.models import QuerySet
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin

from formidable.models import Form
from formidable.serializers import FormSerializer
from formidable.serializers.form import FormDetailSerializer


class FormApi(DetailSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = FormSerializer
    serializer_detail_class = FormDetailSerializer
    permission_classes = (AllowAny,)
    queryset: QuerySet[Form] = Form.objects.all()
    queryset_detail = Form.objects.prefetch_related("sections")
