"""
Generic datetime utils

Links that helped:
https://github.com/encode/django-rest-framework/blob/3.8.2/rest_framework/fields.py#L1217
https://github.com/django/django/blob/1.11.16/django/utils/dateparse.py#L23
"""
import datetime
import re
import calendar

import pytz
import six

utc = pytz.utc
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


def avoid_wrapping(value):
    """
    Avoid text wrapping in the middle of a phrase by adding non-breaking
    spaces where there previously were normal spaces.
    """
    return value.replace(" ", "\xa0")


def is_aware(value):
    """
    Determine if a given datetime.datetime is aware.
    The concept is defined in Python's docs:
    https://docs.python.org/library/datetime.html#datetime.tzinfo
    Assuming value.tzinfo is either None or a proper datetime.tzinfo,
    value.utcoffset() implements the appropriate logic.
    """
    return value.utcoffset() is not None


TIME_STRINGS = {
    'year': '%d years',
    'month': '%d months',
    'week': '%d weeks',
    'day': '%d days',
    'hour': '%d hours',
    'minute': '%d minutes',
    'second': '%d seconds'
}

TIMESINCE_CHUNKS = (
    (60 * 60 * 24 * 365, 'year'),
    (60 * 60 * 24 * 30, 'month'),
    (60 * 60 * 24 * 7, 'week'),
    (60 * 60 * 24, 'day'),
    (60 * 60, 'hour'),
    (60, 'minute'),
    (1, 'second')
)


def timesince(d, now=None, reversed=False, time_strings=None):
    """
    Take two datetime objects and return the time between d and now as a nicely
    formatted string, e.g. "10 minutes". If d occurs after now, return
    "0 minutes".

    Units used are years, months, weeks, days, hours, and minutes.
    Seconds and microseconds are ignored.  Up to two adjacent units will be
    displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

    `time_strings` is an optional dict of strings to replace the default
    TIME_STRINGS dict.

    Adapted from
    https://web.archive.org/web/20060617175230/http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
    """
    if time_strings is None:
        time_strings = TIME_STRINGS

    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    now = now or datetime.datetime.now(utc if is_aware(d) else None)

    if reversed:
        d, now = now, d
    delta = now - d

    # Deal with leapyears by subtracing the number of leapdays
    leapdays = calendar.leapdays(d.year, now.year)
    if leapdays != 0:
        if calendar.isleap(d.year):
            leapdays -= 1
        elif calendar.isleap(now.year):
            leapdays += 1
    delta -= datetime.timedelta(leapdays)

    # ignore microseconds
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return avoid_wrapping('0 minutes')
    for i, (seconds, name) in enumerate(TIMESINCE_CHUNKS):
        count = since // seconds
        if count != 0:
            break
    result = avoid_wrapping(time_strings[name] % count)
    if i + 1 < len(TIMESINCE_CHUNKS):
        # Now get the second item
        seconds2, name2 = TIMESINCE_CHUNKS[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            result += ', ' + avoid_wrapping(time_strings[name2] % count2)
    return result


def timeuntil(d, now=None, time_strings=None):
    """
    Like timesince, but return a string measuring the time until the given time.
    """
    return timesince(d, now, reversed=True, time_strings=time_strings)
