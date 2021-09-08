from django.db.models import ForeignKey, CASCADE, Model
from django.utils.translation import gettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from simple_history.models import HistoricalRecords

from administration.models import User
from formidable.abstractions import BaseModel
from formidable.models.form import Form


class ApplicationStatusesModel(Model):
    STATUS = Choices(("new", _("new")), ("err", _("has errors")), ("ok", _("ok")))

    class Meta:
        abstract = True


class Application(TimeStampedModel, ApplicationStatusesModel, StatusModel, BaseModel):
    applicant = ForeignKey(
        User,
        verbose_name=_("applicant"),
        on_delete=CASCADE,
        related_name="applications",
        related_query_name="application",
    )
    form = ForeignKey(
        Form,
        verbose_name=_("form"),
        on_delete=CASCADE,
        related_name="applications",
        related_query_name="application",
    )
    history = HistoricalRecords(bases=(ApplicationStatusesModel,))

    def __str__(self):
        return str(self.applicant) + " - " + str(self.form)

    class Meta:
        db_table = "applications"
        verbose_name = _("application")
        verbose_name_plural = _("applications")
