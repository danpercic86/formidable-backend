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


def _bitwise_or(lhs: int, rhs: int):
    return lhs | rhs


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

    def __call__(self, value: str) -> Optional[ValidationError]:
        """
        Validate that the input contains (or does *not* contain, if
        inverse_match is True) a match for the regular expression.
        """
        if not isinstance(value, str):
            return ValidationError(f"'{value}' must be a string!")

        validate_attr = getattr(self, "_validate_" + self.type, None)

        return validate_attr(value) if validate_attr else None

    def _validate_regex(self, value: str) -> Optional[ValidationError]:
        flags = reduce(_bitwise_or, list(map(int, str(self.flags).split(","))), 0)
        regex = _lazy_re_compile(self.constraint, flags)
        regex_matches = regex.search(value)
        invalid_input = regex_matches if self.inverse_match else not regex_matches

        return self._error() if invalid_input else None

    def _validate_minlength(self, value: str) -> Optional[ValidationError]:
        if len(value) < int(self.constraint):
            details = f"'{self.field}' must have minimum {self.constraint} characters!"
            return self._error(default_message=details)
        return None

    def _validate_maxlength(self, value: str) -> Optional[ValidationError]:
        if len(value) > int(self.constraint):
            details = f"'{self.field}' must have maximum {self.constraint} characters!"
            return self._error(default_message=details)
        return None

    def _error(self, default_message="Something went wrong!") -> ValidationError:
        message = self.message if self.message else default_message
        return ValidationError({"error": message, "field": self.field_id})
