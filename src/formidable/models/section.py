from ckeditor.fields import RichTextField
from django.db.models import ForeignKey, CASCADE, CharField
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from formidable.abstractions import BaseModel, OrderableModel
from formidable.models.form import Form


class Section(TimeStampedModel, OrderableModel, BaseModel):
    form = ForeignKey(
        Form,
        on_delete=CASCADE,
        verbose_name=_("form"),
        related_name="sections",
        related_query_name="section",
    )
    name = CharField(_("name"), max_length=200, blank=True, default="")
    description = RichTextField(
        _("description"), max_length=1000, blank=True, default=""
    )
    button_text = CharField(_("submit button text"), max_length=50, default="Submit")

    class Meta(OrderableModel.Meta):
        db_table = "form_sections"
        verbose_name = _("section")
        verbose_name_plural = _("sections")
