from django.db.models import CharField, ForeignKey, CASCADE, Model
from django.utils.translation import gettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from simple_history.models import HistoricalRecords

from formidable.abstractions import BaseModel
from formidable.models import Field, Application


class ResponseStatuses(Model):
    STATUS = Choices(("new", _("new")), ("err", _("has errors")), ("ok", _("ok")))

    class Meta:
        abstract = True


class Response(TimeStampedModel, ResponseStatuses, StatusModel, BaseModel):
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
    history = HistoricalRecords(bases=(ResponseStatuses,))

    class Meta:
        db_table = "responses"
        verbose_name = _("response")
        verbose_name_plural = _("responses")
