from django.db.models import ForeignKey, CASCADE, CharField, TextField
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from formidable.abstractions import BaseModel
from formidable.models.form import Form


class Section(TimeStampedModel, BaseModel):
    form = ForeignKey(
        Form,
        on_delete=CASCADE,
        verbose_name=_("related form"),
        related_name="sections",
        related_query_name="section",
    )
    name = CharField(_("section name"), max_length=200, blank=True, default="")
    description = TextField(
        _("section description"), max_length=500, blank=True, default=""
    )
    button_text = CharField(_("submit button text"), max_length=50, default="Submit")

    class Meta:
        db_table = "form_sections"
        verbose_name = _("form section")
        verbose_name_plural = _("form sections")
