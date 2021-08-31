from ckeditor.fields import RichTextField
from django.db.models import CharField
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from formidable.abstractions import BaseModel


class Form(TimeStampedModel, BaseModel):
    name = CharField(_("name"), max_length=200)
    description = RichTextField(
        _("description"), max_length=5000, blank=True, default=""
    )

    class Meta:
        db_table = "forms"
        verbose_name = _("form")
        verbose_name_plural = _("forms")
