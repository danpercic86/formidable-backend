from functools import reduce
from typing import Optional

from django.db.models import (
    ForeignKey,
    CASCADE,
    CharField,
    BooleanField,
    CheckConstraint,
    Q,
)
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from formidable.abstractions import BaseModel
from formidable.constants import ValidatorTypes, RegexFlags
from formidable.models import Field


class Validator(BaseModel):
    field = ForeignKey(
        Field,
        on_delete=CASCADE,
        verbose_name=_("field to validate"),
        related_name="validators",
        related_query_name="validator",
    )
    type = CharField(
        _("type"), max_length=10, choices=ValidatorTypes.choices, default=None
    )
    constraint = CharField(_("constraint"), max_length=500)
    message = CharField(_("message"), max_length=500, default="", blank=True)
    description = CharField(_("description"), max_length=500, default="", blank=True)
    is_enabled = BooleanField(_("is enabled"), default=True)
    inverse_match = BooleanField(_("inverse match"))
    flags = CharField(
        _("flags"), choices=RegexFlags.choices, default="", max_length=5, blank=True
    )

    class Meta:
        db_table = "validators"
        verbose_name = _("validator")
        verbose_name_plural = _("validators")
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

    def __call__(self, value: Optional[str], field: Field) -> Optional[ValidationError]:
        """
        Validate that the input contains (or does *not* contain, if
        inverse_match is True) a match for the regular expression.
        """
        validate_attr = getattr(self, "_validate_" + self.type, None)
        return validate_attr(value, field) if validate_attr else None

    def _validate_regex(self, value: str, field: Field) -> Optional[ValidationError]:
        flags = reduce(
            lambda a, b: a | b, list(map(int, str(self.flags).split(","))), 0
        )
        regex = _lazy_re_compile(self.constraint, flags)
        regex_matches = regex.search(str(value))
        invalid_input = regex_matches if self.inverse_match else not regex_matches

        return self._error(field_id=field.id) if invalid_input else None

    def _validate_minlength(
        self, value: str, field: Field
    ) -> Optional[ValidationError]:
        if not isinstance(value, str):
            return self._error(f"'{value}' must be a string!")

        return (
            self._error(
                f"'{field}' must have minimum {self.constraint} characters!",
                field.id,
            )
            if len(value) < int(self.constraint)
            else None
        )

    def _validate_maxlength(
        self, value: str, field: Field
    ) -> Optional[ValidationError]:
        if not isinstance(value, str):
            return self._error(f"'{value}' must be a string!")

        return (
            self._error(
                f"'{field}' must have maximum {self.constraint} characters!",
                field.id,
            )
            if len(value) > int(self.constraint)
            else None
        )

    def _error(
        self, default="Something went wrong!", field_id: int = None
    ) -> ValidationError:
        message = default if field_id is None else self._message(default)
        details = message if field_id is None else {"error": message, "field": field_id}
        return ValidationError(details)

    def _message(self, default="Something went wrong!") -> str:
        return self.message if self.message else default
