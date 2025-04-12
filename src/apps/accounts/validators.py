from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    """
    Validator to ensure the username contains only letters, numbers
    and ./_ characters.
    """

    regex = r"^[a-zA-Z0-9_]+\Z"
    message = _(
        "Enter a valid username. It may contain only  letters, numbers and"
        " _ character."
    )
    code = "invalid_username_character"
    flags = 0


class MinLengthUsernameValidator(validators.MinValueValidator):
    """
    Validator to ensure that the username is of a minimum length.
    """

    message = _(
        "The username must contain at least %(limit_value)d characters."
    )
    code = "min_username_length"

    def clean(self, x: str) -> int:
        return len(x)
