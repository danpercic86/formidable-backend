import re

from django.db.models import TextChoices, IntegerChoices
from django.utils.translation import gettext as _
from rest_framework.exceptions import ErrorDetail


class FieldTypes(TextChoices):
    TEXT = "text", _("text")
    EMAIL = "email", _("email")
    URL = "url", _("url")
    FILE = "file", _("file")
    # integer is actually "number" type with "step = 1"
    INTEGER = "integer", _("integer")
    # decimal is "number" type with "step = 0.01"
    DECIMAL = "decimal", _("decimal")
    PHONE = "tel", _("phone number")
    DATE = "date", _("date")
    TIME = "time", _("time")
    DATETIME = "datetime", _("datetime")
    # for these 3 types, there must be at least one choice provided
    RADIO = "radio", _("radio")
    CHECKBOX = "checkbox", _("checkbox")
    SELECT = "select", _("select")


class ValidatorTypes(TextChoices):
    MIN = "min", _("Minimum value (applies to number inputs only)")
    MAX = "max", _("Maximum value (applies to number inputs only)")
    MIN_LENGTH = "minlength", _("Minimum length")
    MAX_LENGTH = "maxlength", _("Maximum length")
    EMAIL = "email", _("Email")
    REGEX = "pattern", _("Regular expression")


class RegexFlags(IntegerChoices):
    INSENSITIVE = re.I, _("case-insensitive")
    MULTILINE = re.M, _("multiline")
    DOTALL = re.S, _("dotall")
    UNICODE = re.U, _("unicode")


class Codes:
    REQUIRED_FIELD = "required_field"
    NOT_SAME_SECTION = "not_same_section"


class Errors:
    REQUIRED_FIELD = {"string": "This field is required!", "code": Codes.REQUIRED_FIELD}
    RequiredField = ErrorDetail(**REQUIRED_FIELD)
    NOT_SAME_SECTION = {
        "string": "There is a mix of responses for fields from different sections",
        "code": Codes.NOT_SAME_SECTION,
    }
    NotSameSection = ErrorDetail(**NOT_SAME_SECTION)


CREATED = "created"
MODIFIED = "modified"
NAME = "name"
SLUG = "slug"
DESCRIPTION = "description"
BUTTON_TEXT = "button_text"
SECTION = "section"
TYPE = "type"
PLACEHOLDER = "placeholder"
DEPENDENT_FIELD = "dependent_field"
DEPENDENT_VALUE = "dependent_value"
FIELD = "field"
FIELDS = "fields"
CONSTRAIN = "constraint"
MESSAGE = "message"
IS_ENABLED = "is_enabled"
INVERSE_MATCH = "inverse_match"
FLAGS = "flags"
STATUS = "status"
STATUS_CHANGED = "status_changed"
VALUE = "value"
RESPONSE = "response"
ERRORS = "errors"
OBSERVATIONS = "observations"
APPLICATION = "application"
CHOICES = "choices"
APPLICANT = "applicant"
FORM = "form"
ID = "id"
RESPONSES = "responses"
SECTIONS = "sections"
IS_REQUIRED = "is_required"

CREATED_MODIFIED = (
    "Created / Modified",
    {
        "fields": (CREATED, MODIFIED),
        "classes": ("collapse",),
        "description": "Info about the time this entry was added here or updated",
    },
)
