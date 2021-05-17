from django.db.models import CharField, TextField
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from formidable.abstractions import BaseModel


class Form(TimeStampedModel, BaseModel):
    name = CharField(_("name"), max_length=200)
    description = TextField(_("description"), max_length=500, blank=True, default="")

    class Meta:
        db_table = "forms"
        verbose_name = _("form")
        verbose_name_plural = _("forms")
