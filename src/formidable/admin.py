from django.contrib.admin import ModelAdmin, register

from formidable.abstractions import BaseModelAdmin
from formidable.constants import (
    CREATED,
    MODIFIED,
    NAME,
    FIELDS,
    STATUS_CHANGED,
    SECTION,
    DESCRIPTION,
    BUTTON_TEXT,
    APPLICATION,
    TYPE,
    APPLICANT,
    FORM,
    STATUS,
    FIELD,
    VALUE,
    ERRORS,
    OBSERVATIONS,
)
from formidable.forms import FieldAdminForm
from formidable.inlines import (
    ResponseInline,
    ValidatorsInline,
    FieldInline,
    SectionInline,
)
from formidable.models import (
    Field,
    Section,
    Validator,
    Choice,
    Response,
    Application,
    Form,
)


@register(Field)
class FieldAdmin(BaseModelAdmin):
    form = FieldAdminForm
    inlines = (ValidatorsInline,)
    search_fields = (NAME,)
    list_display = ("__str__", SECTION, TYPE)
    list_filter = (SECTION, TYPE, CREATED, MODIFIED)
    list_select_related = (SECTION,)


@register(Section)
class SectionAdmin(BaseModelAdmin):
    inlines = (FieldInline,)
    list_display = (
        "__str__",
        DESCRIPTION,
        BUTTON_TEXT,
    )
    list_editable = (BUTTON_TEXT,)
    list_filter = (CREATED, MODIFIED)


@register(Form)
class FormAdmin(BaseModelAdmin):
    inlines = (SectionInline,)
    list_display = ("__str__", DESCRIPTION)


@register(Choice)
class ChoiceAdmin(BaseModelAdmin):
    filter_horizontal = (FIELDS,)


@register(Application)
class ApplicationAdmin(BaseModelAdmin):
    inlines = (ResponseInline,)
    fieldsets = (
        ("General", {"fields": (STATUS, FORM, APPLICANT)}),
        ("Details", {"fields": (STATUS_CHANGED, CREATED, MODIFIED)}),
    )
    list_display = ("__str__", APPLICANT, STATUS, FORM)
    readonly_fields = (STATUS_CHANGED, CREATED, MODIFIED, APPLICANT, FORM)


@register(Validator)
class ValidatorAdmin(ModelAdmin):
    pass


@register(Response)
class ResponseAdmin(BaseModelAdmin):
    list_display = (APPLICATION, FIELD, VALUE, STATUS)
    fieldsets = (
        (
            "General",
            {"fields": (STATUS, APPLICATION, FIELD, VALUE, ERRORS, OBSERVATIONS)},
        ),
        ("Details", {"fields": (STATUS_CHANGED, CREATED, MODIFIED)}),
    )
    readonly_fields = (APPLICATION, FIELD, STATUS_CHANGED, CREATED, MODIFIED)
