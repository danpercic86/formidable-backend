from django.contrib.admin import StackedInline

from formidable.model_fields import FIELD, STATUS_CHANGED, CREATED, MODIFIED
from formidable.models import FormField, Validator, Response


class FormFieldInline(StackedInline):
    model = FormField
    extra = 0


class ValidatorsInline(StackedInline):
    model = Validator
    extra = 0


class ResponseInline(StackedInline):
    model = Response
    extra = 0
    autocomplete_fields = (FIELD,)
    readonly_fields = (STATUS_CHANGED, CREATED, MODIFIED)
