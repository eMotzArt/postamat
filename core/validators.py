from gettext import ngettext

from django.core.exceptions import ValidationError


class IsNumbersIncluded:
    """
    Validate that the password have numbers inside.
    """

    def validate(self, password, user=None):
        if password.isalpha():
            raise ValidationError('Password must include at least one digit',
                                  code="password_not_include_digits",
                                  )


class DomainValidator:
    """
    Validate that the email is in available domains.
    """

    def __init__(self):
        self.available_domains = [
            'yandex.ru',
            'mail.ru',
        ]

    def validate(self, email):
        name, domain = email.split('@')
        if domain not in self.available_domains:
            raise ValidationError('Email domain is not supported',
                                  code="email_domain_is_not_supported",
                                  )
