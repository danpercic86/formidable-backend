from django.db.models import ForeignKey, CASCADE
from django.utils.translation import gettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel

from administration.models import User
from formidable.abstractions import BaseModel
from formidable.models.form import Form


class Application(TimeStampedModel, StatusModel, BaseModel):
    STATUS = Choices(("new", _("new")), ("err", _("has errors")), ("ok", _("ok")))
    applicant = ForeignKey(
        User,
        verbose_name=_("applicant"),
        on_delete=CASCADE,
        related_name="applications",
        related_query_name="application",
    )
    form = ForeignKey(
        Form,
        verbose_name=_("form this response belongs to"),
        on_delete=CASCADE,
        related_name="applications",
        related_query_name="application",
    )

    class Meta:
        db_table = "applications"
        verbose_name = _("application")
        verbose_name_plural = _("applications")
