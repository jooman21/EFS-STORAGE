
from django.core.exceptions import ValidationError
import re



class MinimumLengthValidator(object):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ("This password is too short. It must contain at least %(min_length)d characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return (
            "Your password must contain at least %(min_length)d characters."
        ) % {'min_length': self.min_length}


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                ("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                ("The password must contain at least 1 symbol: " 
               ),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return (
            "Your password must contain at least 1 symbol: " 
            # "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )