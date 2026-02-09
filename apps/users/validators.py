import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UppercaseValidator:
    """Exige pelo menos uma letra maiúscula."""

    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _('A senha deve conter pelo menos uma letra maiúscula.'),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _('Sua senha deve conter pelo menos uma letra maiúscula.')


class LowercaseValidator:
    """Exige pelo menos uma letra minúscula."""

    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _('A senha deve conter pelo menos uma letra minúscula.'),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _('Sua senha deve conter pelo menos uma letra minúscula.')


class SpecialCharacterValidator:
    """Exige pelo menos um caractere especial."""

    def validate(self, password, user=None):
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>\-_=+\[\]\\\/~`]', password):
            raise ValidationError(
                _('A senha deve conter pelo menos um caractere especial (!@#$%&* etc.).'),
                code='password_no_special',
            )

    def get_help_text(self):
        return _('Sua senha deve conter pelo menos um caractere especial (!@#$%&* etc.).')
