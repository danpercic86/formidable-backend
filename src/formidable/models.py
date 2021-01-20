from typing import AnyStr, Optional

from django.db.models import (
    Model,
    SlugField,
    CharField,
    TextField,
    ForeignKey,
    CASCADE,
    ManyToManyField,
    CheckConstraint,
    Q,
    BooleanField,
)
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from rest_framework.exceptions import ValidationError

from formidable.constants import FieldTypes, ValidatorTypes, RegexFlags


class SlugableModel(Model):
    slug = SlugField(unique=True, db_index=True)

    class Meta:
        abstract = True


class BaseModel(Model):
    class Meta:
        abstract = True

    def get_change_url(self) -> AnyStr:
        from django.urls import reverse_lazy

        return reverse_lazy(
            f"admin:{self._meta.app_label}_{self._meta.model_name}_change",
            args=[str(self.id)],
        )

    @property
    def href(self):
        """
        Use this property in admin dashboard to show this object's name as html anchor
        that redirects to object's edit page
        @return:
        """
        from django.utils.html import format_html

        return format_html(f"<a href='{self.get_change_url()}'>{self}</a>")


class Form(TimeStampedModel, BaseModel):
    name = CharField(_("form name"), max_length=200)
    description = TextField(_("form description"), max_length=500, blank=True, default="")
    button_text = CharField(_("submit button text"), max_length=50)


class FormField(TimeStampedModel, BaseModel):
    form = ForeignKey(
        Form,
        on_delete=CASCADE,
        verbose_name=_("form this filed belongs to"),
        related_name="fields",
        related_query_name="field",
    )
    name = CharField(_("field name"), max_length=100)
    type = CharField(
        _("field type"), max_length=50, choices=FieldTypes.choices, default=FieldTypes.TEXT
    )
    placeholder = CharField(_("placeholder"), max_length=200, default="", blank=True)
    dependent_field = ForeignKey(
        "FormField",
        verbose_name=_("depends on"),
        on_delete=CASCADE,
        related_name="dependents",
        related_query_name="dependent",
        limit_choices_to={"type__in": [FieldTypes.SELECT, FieldTypes.CHECKBOX, FieldTypes.RADIO]},
        null=True,
        blank=True,
    )
    dependent_value = CharField(_("with value"), max_length=200, default="", blank=True)

    # for IDE autocomplete purposes only
    choices: ManyToManyField

    class Meta:
        db_table = "fields"
        constraints = [
            CheckConstraint(
                name="form_field_type_valid",
                check=Q(type__in=FieldTypes.values),
            )
        ]


class Choice(TimeStampedModel, BaseModel):
    name = CharField(_("choice name"), max_length=300)
    fields = ManyToManyField(
        FormField,
        verbose_name=_('"select" form fields'),
        related_name="choices",
        related_query_name="choice",
        limit_choices_to={"type__in": [FieldTypes.SELECT, FieldTypes.CHECKBOX, FieldTypes.RADIO]},
    )

    class Meta:
        db_table = "choices"


class Validator(BaseModel):
    requires_context = True

    field = ForeignKey(
        FormField,
        verbose_name=_("field to validate"),
        related_name="validators",
        related_query_name="validator",
        on_delete=CASCADE,
    )
    type = CharField(max_length=10, choices=ValidatorTypes.choices, default=None)
    constraint = CharField(max_length=500)
    message = CharField(max_length=500, default="", blank=True)
    description = CharField(max_length=500, default="", blank=True)
    is_enabled = BooleanField(default=True)
    inverse_match = BooleanField()
    flags = CharField(choices=RegexFlags.choices, default="", max_length=5, blank=True)

    class Meta:
        db_table = "validators"
        constraints = [
            CheckConstraint(
                name="validator_type_valid",
                check=Q(type__in=ValidatorTypes.values),
            ),
            CheckConstraint(
                name="validator_flag_valid",
                check=Q(flags__in=[""] + RegexFlags.values),
            ),
        ]

    def __call__(self, value: AnyStr, field: FormField) -> Optional[ValidationError]:
        """
        Validate that the input contains (or does *not* contain, if
        inverse_match is True) a match for the regular expression.
        """
        if validate_attr := getattr(self, "validate_" + self.type, None):
            return validate_attr(value, field)
        return None

    def validate_regex(self, value: AnyStr, field: FormField) -> Optional[ValidationError]:
        flags: int = 0
        for flag in str(self.flags).split(","):
            flags |= int(flag)
        regex = _lazy_re_compile(self.constraint, flags)
        regex_matches = regex.search(str(value))
        invalid_input = regex_matches if self.inverse_match else not regex_matches
        if invalid_input:
            return ValidationError(
                {
                    "error": self.message,
                    "field": field.id,
                }
            )
        return None

    def validate_minlength(self, value: AnyStr, field: FormField) -> Optional[ValidationError]:
        if not isinstance(value, str):
            return ValidationError(f"'{value}' must be a string!")
        if len(value) < int(self.constraint):
            return ValidationError(
                {
                    "error": self.message
                    if self.message
                    else f"'{field}' must have minimum {self.constraint} characters!",
                    "field": field.id,
                }
            )
        return None

    def validate_maxlength(self, value: AnyStr, field: FormField) -> Optional[ValidationError]:
        if not isinstance(value, str):
            return ValidationError(f"'{value}' must be a string!")
        if len(value) > int(self.constraint):
            return ValidationError(
                {
                    "error": self.message
                    if self.message
                    else f"'{field}' must have maximum {self.constraint} characters!",
                    "field": field.id,
                }
            )
        return None


class Response(TimeStampedModel, StatusModel, BaseModel):
    STATUS = Choices(("new", _("new")), ("err", _("has errors")), ("ok", _("ok")))
    form = ForeignKey(
        Form, verbose_name=_("form this response belongs to"), on_delete=CASCADE, null=True
    )


class ResponseField(TimeStampedModel, StatusModel, BaseModel):
    STATUS = Choices(("new", _("new")), ("err", _("has errors")), ("ok", _("ok")))

    value = CharField(_("value"), max_length=500)
    field = ForeignKey(
        FormField, verbose_name=_("field this response belongs to"), on_delete=CASCADE
    )
    response = ForeignKey(
        Response,
        verbose_name=_("application this response belongs to"),
        on_delete=CASCADE,
        related_name="fields",
        related_query_name="field",
    )
    errors = CharField(_("errors"), max_length=500, default="", blank=True)
    observations = CharField(_("observations"), max_length=500, default="", blank=True)
