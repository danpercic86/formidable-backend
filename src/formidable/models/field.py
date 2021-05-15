from django.db.models import (
    CharField,
    ForeignKey,
    CASCADE,
    CheckConstraint,
    Q,
)
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from formidable.abstractions import BaseModel
from formidable.constants import FieldTypes
from formidable.models.section import Section


class Field(TimeStampedModel, BaseModel):
    name = CharField(_("field name"), max_length=100)
    form_section = ForeignKey(
        Section,
        on_delete=CASCADE,
        verbose_name=_("related form section"),
        related_name="fields",
        related_query_name="field",
    )
    type = CharField(
        _("type"), max_length=50, choices=FieldTypes.choices, default=FieldTypes.TEXT
    )
    placeholder = CharField(_("placeholder"), max_length=200, default="", blank=True)
    dependent_field = ForeignKey(
        "Field",
        on_delete=CASCADE,
        verbose_name=_("depends on"),
        related_name="dependents",
        related_query_name="dependent",
        limit_choices_to={
            "type__in": [FieldTypes.SELECT, FieldTypes.CHECKBOX, FieldTypes.RADIO]
        },
        null=True,
        blank=True,
    )
    dependent_value = CharField(_("with value"), max_length=200, default="", blank=True)

    class Meta:
        db_table = "fields"
        verbose_name = _("field")
        verbose_name_plural = _("fields")
        constraints = [
            CheckConstraint(
                name="field_type_valid",
                check=Q(type__in=FieldTypes.values),
            )
        ]
