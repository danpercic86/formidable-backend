from rest_framework.serializers import ModelSerializer

from formidable.constants import (
    CREATED,
    MODIFIED,
    FIELDS,
    IS_ENABLED,
    DESCRIPTION,
    FIELD,
    FORM_SECTION,
    NAME,
    FORM,
    ID,
    RESPONSES,
    VALUE,
    ERRORS,
)
from formidable.models import (
    FormField,
    Choice,
    Validator,
    FormSection,
    Form,
    Application,
    Response,
)


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        exclude = CREATED, MODIFIED, FIELDS


class ValidatorSerializer(ModelSerializer):
    class Meta:
        model = Validator
        exclude = FIELD, DESCRIPTION, IS_ENABLED


class FormFieldSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    validators = ValidatorSerializer(many=True, read_only=True)

    class Meta:
        model = FormField
        exclude = CREATED, MODIFIED, FORM_SECTION


class FormSectionSerializer(ModelSerializer):
    fields = FormFieldSerializer(many=True, read_only=True)

    class Meta:
        model = FormSection
        exclude = CREATED, MODIFIED


class FormSectionMinimalSerializer(ModelSerializer):
    class Meta:
        model = FormSection
        fields = ("id", NAME)


class FormSerializer(ModelSerializer):
    sections = FormSectionMinimalSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        exclude = CREATED, MODIFIED


class ResponseDetailSerializer(ModelSerializer):
    read_only = True

    class Meta:
        model = Response
        fields = ID, FIELD, VALUE, ERRORS
        read_only_fields = fields


class ApplicationDetailSerializer(ModelSerializer):
    responses = ResponseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = ID, FORM, RESPONSES
        read_only_fields = fields
