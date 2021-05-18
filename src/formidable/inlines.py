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
    IS_REQUIRED,
)
from formidable.forms import FieldAdminForm
from formidable.models import Field, Validator, Response, Section


class SectionInline(TabularInline):
    model = Section
    extra = 0


class FieldInline(StackedInline):
    form = FieldAdminForm
    model = Field
    extra = 0
    fieldsets = (
        (
            None,
            {
                "fields": (
                    TYPE,
                    NAME,
                    PLACEHOLDER,
                    IS_REQUIRED,
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
