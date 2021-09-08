from typing import Tuple

from django.contrib.admin import ModelAdmin, register
from simple_history.admin import SimpleHistoryAdmin

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
    IS_ENABLED,
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
    exclude = ("order_index", "button_text")


@register(Form)
class FormAdmin(BaseModelAdmin, SimpleHistoryAdmin):
    inlines = (SectionInline,)
    exclude = ("order_index",)
    list_display = ("__str__", "description", "created", "modified")
    list_filter: Tuple[str, ...] = ("created", "modified")
    readonly_fields: Tuple[str, ...] = ("created", "modified")


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
    list_display = ("__str__", FIELD, TYPE, "constraint", IS_ENABLED)


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
