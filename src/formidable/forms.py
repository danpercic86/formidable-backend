from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm, ModelMultipleChoiceField

from formidable.constants import CHOICES
from formidable.models import Choice, FormField


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
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields[CHOICES].initial = self.instance.choices.all()

    def save(self, commit=True):
        form_field: FormField = super().save(commit=False)

        if commit:
            form_field.save()

        if form_field.pk:
            form_field.choices.set(self.cleaned_data[CHOICES])
            self.save_m2m()

        return form_field
