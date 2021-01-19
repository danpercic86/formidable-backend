from django.contrib.admin import ModelAdmin, StackedInline, register

from formidable.models import FormField, Form, Validator, Choice, ResponseField, Response


class BaseModelAdmin(ModelAdmin):
    list_filter = ('created', 'modified')
    readonly_fields = ('created', 'modified')


class SlugableModelAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


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
    search_fields = ("name",)


class FieldInline(StackedInline):
    model = Choice.fields.through
    extra = 0


@register(Choice)
class ChoiceAdmin(BaseModelAdmin):
    inlines = (FieldInline,)
    filter_horizontal = ("fields",)


class ResponseFieldInline(StackedInline):
    model = ResponseField
    extra = 0
    autocomplete_fields = ("field",)
    readonly_fields = ("status_changed", "created", "modified")
    verbose_name = "response"


@register(Response)
class ResponseAdmin(BaseModelAdmin):
    inlines = (ResponseFieldInline,)
    readonly_fields = ("form", "status_changed", "created", "modified")


@register(Validator)
class ValidatorAdmin(ModelAdmin):
    pass
