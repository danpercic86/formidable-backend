from django.contrib.admin import ModelAdmin, StackedInline, register

from formidable.model_fields import (
    CREATED,
    MODIFIED,
    SLUG,
    NAME,
    FIELDS,
    FIELD,
    STATUS_CHANGED,
    FORM,
)
from formidable.models import FormField, Form, Validator, Choice, ResponseField, Response


class BaseModelAdmin(ModelAdmin):
    list_filter = (CREATED, MODIFIED)
    readonly_fields = (CREATED, MODIFIED)


class SlugableModelAdmin(ModelAdmin):
    prepopulated_fields = {SLUG: (NAME,)}


class FormFieldInline(StackedInline):
    model = FormField
    extra = 0


@register(Form)
class FormAdmin(BaseModelAdmin):
    inlines = (FormFieldInline,)


class ChoicesInline(StackedInline):
    model = FormField.choices.through
    extra = 0


class ValidatorsInline(StackedInline):
    model = Validator
    extra = 0


@register(FormField)
class FormFieldAdmin(BaseModelAdmin):
    inlines = (ChoicesInline, ValidatorsInline)
    search_fields = (NAME,)


class FieldInline(StackedInline):
    model = Choice.fields.through
    extra = 0


@register(Choice)
class ChoiceAdmin(BaseModelAdmin):
    inlines = (FieldInline,)
    filter_horizontal = (FIELDS,)


class ResponseFieldInline(StackedInline):
    model = ResponseField
    extra = 0
    autocomplete_fields = (FIELD,)
    readonly_fields = (STATUS_CHANGED, CREATED, MODIFIED)
    verbose_name = "response"


@register(Response)
class ResponseAdmin(BaseModelAdmin):
    inlines = (ResponseFieldInline,)
    readonly_fields = (FORM, STATUS_CHANGED, CREATED, MODIFIED)


@register(Validator)
class ValidatorAdmin(ModelAdmin):
    pass
