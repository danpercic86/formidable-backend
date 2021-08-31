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
    BUTTON_TEXT,
    STATUS,
    VALUE,
    ERRORS,
    OBSERVATIONS,
)
from formidable.forms import FieldAdminForm
from formidable.models import Field, Validator, Response, Section


class SectionInline(TabularInline):
    model = Section
    extra = 0
    exclude = (BUTTON_TEXT, "order_index")


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
    fieldsets = (
        (None, {"fields": (STATUS, FIELD, VALUE, ERRORS, OBSERVATIONS)}),
        (
            "Details",
            {"fields": (STATUS_CHANGED, CREATED, MODIFIED), "classes": ("collapse",)},
        ),
    )
    readonly_fields = (STATUS_CHANGED, CREATED, MODIFIED, FIELD)
