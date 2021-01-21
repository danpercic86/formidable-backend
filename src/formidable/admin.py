from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm, ModelMultipleChoiceField

from formidable.abstractions import BaseModelAdmin
from formidable.inlines import ResponseInline, ValidatorsInline, FormFieldInline
from formidable.model_fields import (
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
    CHOICES,
)
from formidable.models import FormField, Form, Validator, Choice, Response, Application


class FormFieldAdminForm(ModelForm):
    choices = ModelMultipleChoiceField(
        queryset=Choice.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=Choice._meta.verbose_name_plural, is_stacked=False
        ),
    )

    class Meta:
        model = FormField
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields[CHOICES].initial = self.instance.choices.all()

    def save(self, commit=True):
        form_field: FormField = super().save(commit=False)

        if commit:
            form_field.save()

        if form_field.pk:
            form_field.choices = self.cleaned_data[CHOICES]
            self.save_m2m()

        return form_field


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
