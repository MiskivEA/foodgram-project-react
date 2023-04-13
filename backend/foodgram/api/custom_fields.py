import time

import base64
from rest_framework import serializers

from django.core.files.base import ContentFile


ALLOWED_IMAGE_TYPES = (
    "jpeg",
    "jpg",
    "png",
    "gif"
)

EMPTY_VALUES = (None, '', [], (), {})


class DecodeImageToFile(serializers.ImageField):

    def to_internal_value(self, base64_data):
        if base64_data in EMPTY_VALUES:
            return None

        if isinstance(base64_data, str) and base64_data.startswith('data:image'):
            data_info, data_str = base64_data.split(';base64,')
            data_type, format_file = data_info.split('/')

            name = str(int(time.time())) + '.' + format_file
            data = ContentFile(base64.b64decode(data_str), name=name)
            return super().to_internal_value(data)

    def to_representation(self, value):
        return value
