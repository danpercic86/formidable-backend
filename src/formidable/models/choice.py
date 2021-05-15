from django.db.models import ManyToManyField, CharField
from django.utils.translation import gettext as _

from model_utils.models import TimeStampedModel

from formidable.abstractions import BaseModel
from formidable.constants import FieldTypes
from formidable.models.field import Field


class Choice(TimeStampedModel, BaseModel):
    name = CharField(_("choice name"), max_length=300)
    fields = ManyToManyField(
        Field,
        verbose_name=_("fields"),
        related_name="choices",
        related_query_name="choice",
        limit_choices_to={
            "type__in": [FieldTypes.SELECT, FieldTypes.CHECKBOX, FieldTypes.RADIO]
        },
    )

    class Meta:
        db_table = "choices"
        verbose_name = _("choice")
        verbose_name_plural = _("choices")
