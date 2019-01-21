"""Generic module tests"""
import datetime

import pytz

from python_utils.generic.datetime_utils import parse_datetime


def test_parse_datetime():
    assert datetime.datetime(2019, 1, 1, 0, 0, 0, 0, pytz.utc) == parse_datetime("2019-01-01T00:00:00Z")
