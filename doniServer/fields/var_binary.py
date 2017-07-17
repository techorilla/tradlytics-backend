from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models

import binascii


def validate_hex(value):
    if value is None:
        return
    if not isinstance(value, basestring):
        raise ValidationError(_('Not a string!'))
    for c in value:
        if c not in '01234567890abcdefABCDEF':
            raise ValidationError(_('"%s" is not a hex string!') % value)


class VarBinaryField(models.Field):
    description = _('Vector of bytes (up to %(max_length)s)')

    def __init__(self, *args, **kwargs):
        super(VarBinaryField, self).__init__(*args, **kwargs)
        # self.validators.append(validate_hex)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        # return value.encode("utf-8")
        # return value
        # value = binascii.b2a_hex(value)
        return value

    def get_prep_value(self, value):
        if value is None:
            return None
        return value.encode('hex')

    def db_type(self, connection):
            return 'longtext COLLATE utf8mb4_unicode_ci'