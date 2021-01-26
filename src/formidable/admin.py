from django.contrib.admin import ModelAdmin, register

from formidable.abstractions import BaseModelAdmin
from formidable.forms import FormFieldAdminForm
from formidable.inlines import ResponseInline, ValidatorsInline, FormFieldInline
from formidable.constants import (
    CREATED,
    MODIFIED,
    NAME,
    FIELDS,
    STATUS_CHANGED,
    FORM,
    DESCRIPTION,
    BUTTON_TEXT,
    APPLICATION,
    TYPE,
)
from formidable.models import FormField, Form, Validator, Choice, Response, Application


@register(FormField)
class FormFieldAdmin(BaseModelAdmin):
    form = FormFieldAdminForm
    inlines = (ValidatorsInline,)
    search_fields = (NAME,)
    list_display = ('__str__', FORM, TYPE)
    list_filter = (FORM, TYPE, CREATED, MODIFIED)
    list_select_related = (FORM,)


@register(Form)
class FormAdmin(BaseModelAdmin):
    inlines = (FormFieldInline,)
    list_display = (
        '__str__',
        DESCRIPTION,
        BUTTON_TEXT,
    )
    list_editable = (BUTTON_TEXT,)
    list_filter = (CREATED, MODIFIED)


@register(Choice)
class ChoiceAdmin(BaseModelAdmin):
    filter_horizontal = (FIELDS,)


@register(Application)
class ApplicationAdmin(BaseModelAdmin):
    inlines = (ResponseInline,)
    readonly_fields = (FORM, STATUS_CHANGED, CREATED, MODIFIED)


@register(Validator)
class ValidatorAdmin(ModelAdmin):
    pass


@register(Response)
class ResponseAdmin(BaseModelAdmin):
    readonly_fields = (APPLICATION, STATUS_CHANGED, CREATED, MODIFIED)
