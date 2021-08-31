from django.db.models import CharField, ForeignKey, CASCADE
from django.utils.translation import gettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel

from formidable.abstractions import BaseModel
from formidable.models import Field, Application


class Response(TimeStampedModel, StatusModel, BaseModel):
    STATUS = Choices(("new", _("new")), ("err", _("has errors")), ("ok", _("ok")))

    value = CharField(_("value"), max_length=500)
    field = ForeignKey(
        Field,
        on_delete=CASCADE,
        verbose_name=_("field"),
        related_name="responses",
        related_query_name="response",
    )
    application = ForeignKey(
        Application,
        on_delete=CASCADE,
        verbose_name=_("application"),
        related_name="responses",
        related_query_name="response",
    )
    errors = CharField(_("errors"), max_length=500, default="", blank=True)
    observations = CharField(_("observations"), max_length=500, default="", blank=True)

    class Meta:
        db_table = "responses"
        verbose_name = _("response")
        verbose_name_plural = _("responses")
