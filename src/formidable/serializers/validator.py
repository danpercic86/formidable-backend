from rest_framework.serializers import ModelSerializer

from formidable.constants import FIELD, DESCRIPTION, IS_ENABLED
from formidable.models import Validator


class ValidatorSerializer(ModelSerializer):
    class Meta:
        model = Validator
        exclude = FIELD, DESCRIPTION, IS_ENABLED
