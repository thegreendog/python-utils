"""JSON specific serializers"""
from django.core.files.base import File
from django.core.serializers.json import DjangoJSONEncoder


class DjangoWithFileJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode Files
    """

    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, File):
            return str(o)
        else:
            return super().default(o)
