from ckeditor.fields import RichTextField
from django.db.models import CharField, ImageField
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from formidable.abstractions import BaseModel, OrderableModel
from formidable.utils import get_upload_path


class Form(TimeStampedModel, OrderableModel, BaseModel):
    name = CharField(_("name"), max_length=200)
    description = RichTextField(max_length=5000, blank=True, default="")
    avatar = ImageField(upload_to=get_upload_path, blank=True, null=True)
    image = ImageField(upload_to=get_upload_path, blank=True, null=True)
    history = HistoricalRecords()

    class Meta(OrderableModel.Meta):
        db_table = "forms"
        verbose_name = _("form")
        verbose_name_plural = _("forms")
