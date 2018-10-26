"""
Generic datetime utils

Links that helped:
https://github.com/encode/django-rest-framework/blob/3.8.2/rest_framework/fields.py#L1217
https://github.com/django/django/blob/1.11.16/django/utils/dateparse.py#L23
"""
import datetime
import re

import pytz
import six

ZERO = datetime.timedelta(0)

DATETIME_RE = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
    r'[T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
    r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
    r'(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$'
)


class FixedOffset(datetime.tzinfo):
    """
    Fixed offset in minutes east from UTC. Taken from Python's docs.

    Kept as close as possible to the reference version. __init__ was changed
    to make its arguments optional, according to Python's requirement that
    tzinfo subclasses can be instantiated without arguments.
    """

    def __init__(self, offset=None, name=None):
        if offset is not None:
            self.__offset = datetime.timedelta(minutes=offset)
        if name is not None:
            self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO


def get_fixed_timezone(offset):
    """
    Returns a tzinfo instance with a fixed offset from UTC.
    """
    if isinstance(offset, datetime.timedelta):
        offset = offset.seconds // 60
    sign = '-' if offset < 0 else '+'
    hhmm = '%02d%02d' % divmod(abs(offset), 60)
    name = sign + hhmm
    return FixedOffset(offset, name)


def parse_datetime(value):
    """Parses a string and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.

    Raises ValueError if the input is well formatted but not a valid datetime.
    Returns None if the input isn't well formatted.

    Copied from https://github.com/django/django/blob/1.11.16/django/utils/dateparse.py#L23
    """
    match = DATETIME_RE.match(value)
    if match:
        kw = match.groupdict()
        if kw['microsecond']:
            kw['microsecond'] = kw['microsecond'].ljust(6, '0')
        tzinfo = kw.pop('tzinfo')
        if tzinfo == 'Z':
            tzinfo = pytz.utc
        elif tzinfo is not None:
            offset_mins = int(tzinfo[-2:]) if len(tzinfo) > 3 else 0
            offset = 60 * int(tzinfo[1:3]) + offset_mins
            if tzinfo[0] == '-':
                offset = -offset
            tzinfo = get_fixed_timezone(offset)
        kw = {k: int(v) for k, v in six.iteritems(kw) if v is not None}
        kw['tzinfo'] = tzinfo
        return datetime.datetime(**kw)


def dt_is_aware(dt_value):
    """Check if a `datetime.datetime` object is timezone aware or not."""
    return dt_value.tzinfo is not None and dt_value.tzinfo.utcoffset(dt_value) is not None


def print_datetime(value):
    """Format `datetime.datetime` object to a string with ISO_8601 format.
    Inspired by https://github.com/encode/django-rest-framework/blob/3.8.2/rest_framework/fields.py#L1217
    """

    # enforce timezone
    if not dt_is_aware(value):
        # In `eve.methods.common.build_response_document` method `_updated_field` stops being tz aware,
        # it is always UTC because mongo store it in that format
        value = value.replace(tzinfo=pytz.UTC)
    value = value.isoformat()
    if value.endswith('+00:00'):
        value = value[:-6] + 'Z'
    return value
