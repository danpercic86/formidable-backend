from django.contrib.admin import StackedInline, TabularInline

from formidable.constants import (
    FIELD,
    STATUS_CHANGED,
    CREATED,
    MODIFIED,
    NAME,
    TYPE,
    PLACEHOLDER,
    DEPENDENT_FIELD,
    DEPENDENT_VALUE,
    CHOICES,
)
from formidable.forms import FormFieldAdminForm
from formidable.models import FormField, Validator, Response, FormSection


class FormSectionInline(TabularInline):
    model = FormSection
    extra = 0


class FormFieldInline(StackedInline):
    form = FormFieldAdminForm
    model = FormField
    extra = 0
    fieldsets = (
        (
            None,
            {
                "fields": (
                    TYPE,
                    NAME,
                    PLACEHOLDER,
                    (DEPENDENT_FIELD, DEPENDENT_VALUE),
                    CHOICES,
                )
            },
        ),
    )


class ValidatorsInline(StackedInline):
    model = Validator
    extra = 0


class ResponseInline(StackedInline):
    model = Response
    extra = 0
    autocomplete_fields = (FIELD,)
    readonly_fields = (STATUS_CHANGED, CREATED, MODIFIED)
