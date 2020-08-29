import base64
from rest_framework import fields


class Base64CharField(fields.CharField):
    def to_representation(self, value):
        value = base64.b64encode(value)
        return super().to_representation(value)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return base64.b64decode(data)
