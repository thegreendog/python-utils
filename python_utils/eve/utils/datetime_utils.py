"""Eve datetime manage utils"""
import datetime
import decimal
import json

from bson import ObjectId, decimal128
from bson.dbref import DBRef
from eve.io.mongo.mongo import Mongo, MongoJSONEncoder

from python_utils.generic.datetime_utils import parse_datetime, print_datetime


class MyMongoJSONEncoder(MongoJSONEncoder):
    """Overwrites `eve.io.mongo.mongo.MongoJSONEncoder` to encode `datetime.datetime` objects to ISO_8601 format."""

    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, datetime.datetime):
            # convert any datetime to ISO_8601 format
            return print_datetime(obj)
        # delegate rendering to base class method
        return super(MyMongoJSONEncoder, self).default(obj)


class MyMongo(Mongo):
    """Overwrites `eve.io.mongo.mongo.Mongo` to change datetime serializer and json encoder class.
    This class can be passed to Eve constructor as `data` argument - -> app = Eve(data=MyMongo)"""

    serializers = {
        "objectid": lambda value: ObjectId(value) if value else None,
        "datetime": parse_datetime,
        "integer": lambda value: int(value) if value is not None else None,
        "float": lambda value: float(value) if value is not None else None,
        "number": lambda val: json.loads(val) if val is not None else None,
        "boolean": lambda v: {"1": True, "true": True, "0": False, "false": False}[
            str(v).lower()
        ],
        "dbref": lambda value: DBRef(
            value["$col"], value["$id"], value["$db"] if "$db" in value else None
        )
        if value is not None
        else None,
        "decimal": lambda value: decimal128.Decimal128(decimal.Decimal(str(value)))
        if value is not None
        else None,
    }

    json_encoder_class = MyMongoJSONEncoder
