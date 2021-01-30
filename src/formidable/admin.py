from django.contrib.admin import ModelAdmin, register

from formidable.abstractions import BaseModelAdmin
from formidable.forms import FormFieldAdminForm
from formidable.inlines import (
    ResponseInline,
    ValidatorsInline,
    FormFieldInline,
    FormSectionInline,
)
from formidable.constants import (
    CREATED,
    MODIFIED,
    NAME,
    FIELDS,
    STATUS_CHANGED,
    FORM_SECTION,
    DESCRIPTION,
    BUTTON_TEXT,
    APPLICATION,
    TYPE,
)
from formidable.models import (
    FormField,
    FormSection,
    Validator,
    Choice,
    Response,
    Application,
    Form,
)


@register(FormField)
class FormFieldAdmin(BaseModelAdmin):
    form = FormFieldAdminForm
    inlines = (ValidatorsInline,)
    search_fields = (NAME,)
    list_display = ("__str__", FORM_SECTION, TYPE)
    list_filter = (FORM_SECTION, TYPE, CREATED, MODIFIED)
    list_select_related = (FORM_SECTION,)


@register(FormSection)
class FormSectionAdmin(BaseModelAdmin):
    inlines = (FormFieldInline,)
    list_display = (
        "__str__",
        DESCRIPTION,
        BUTTON_TEXT,
    )
    list_editable = (BUTTON_TEXT,)
    list_filter = (CREATED, MODIFIED)


@register(Form)
class FormAdmin(BaseModelAdmin):
    inlines = (FormSectionInline,)
    list_display = ("__str__", DESCRIPTION)


@register(Choice)
class ChoiceAdmin(BaseModelAdmin):
    filter_horizontal = (FIELDS,)


@register(Application)
class ApplicationAdmin(BaseModelAdmin):
    inlines = (ResponseInline,)
    readonly_fields = (STATUS_CHANGED, CREATED, MODIFIED)


@register(Validator)
class ValidatorAdmin(ModelAdmin):
    pass


@register(Response)
class ResponseAdmin(BaseModelAdmin):
    readonly_fields = (APPLICATION, STATUS_CHANGED, CREATED, MODIFIED)
