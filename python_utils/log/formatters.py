"""
Formatters specify the layout of log records in the final output. 
GELF formatters are based on this spec: http://docs.graylog.org/en/2.4/pages/gelf.html#gelf-payload-specification
"""
import json
import logging
import socket
import syslog
import time

GELF_VERSION = '1.1'

SYSLOG_LEVELS = {
    logging.CRITICAL: syslog.LOG_CRIT,
    logging.ERROR: syslog.LOG_ERR,
    logging.WARNING: syslog.LOG_WARNING,
    logging.INFO: syslog.LOG_INFO,
    logging.DEBUG: syslog.LOG_DEBUG
}

EXTRA_FIELDS = {'exc_text': True, 'line': True, 'file': True}


class BasicGELFFormatter(logging.Formatter):
    """A GELF formatter to format a :class:`logging.LogRecord`."""

    def __init__(self, null_character=False, encoder_cls=json.JSONEncoder, extra_fields=EXTRA_FIELDS):
        self.null_character = null_character
        self.encoder_cls = encoder_cls
        self.extra_fields = extra_fields

    @staticmethod
    def to_syslog_level(record):
        """Map from python level representation to syslog one"""

        return SYSLOG_LEVELS.get(record.levelno, syslog.LOG_ALERT)

    def set_more_extra_fields(self, record):
        """Transform from :class:`logging.LogRecord` some fields to python dict.

        :param :class:`logging.LogRecord` record: record emitted by logger. Its attribures can be seen
        in https://docs.python.org/3/library/logging.html#logrecord-attributes
        """

        pass

    def get_gelf_fields(self, record):
        """Transform from :class:`logging.LogRecord` to GELF format in a python dict.

        :param :class:`logging.LogRecord` record: record emitted by logger. Its attribures can be seen
        in https://docs.python.org/3/library/logging.html#logrecord-attributes
        """
        out = {
            'version': GELF_VERSION,
            'host': getattr(record, 'host', socket.gethostname()),
            'short_message':  getattr(record, 'message', record.getMessage()),
            'timestamp': getattr(record, 'created', time.time()),
            'level': self.to_syslog_level(record)
        }

        out['_logger_name'] = getattr(record, 'name')
        out['_levelname'] = getattr(record, 'levelname')

        if self.extra_fields.pop('exc_text', None) and getattr(record, 'exc_text'):
            out['full_message'] = getattr(record, 'exc_text')
        if self.extra_fields.pop('file', None):
            out['_line'] = getattr(record, 'lineno')
        if self.extra_fields.pop('line', None):
            out['_file'] = getattr(record, 'pathname')

        for field in self.extra_fields:
            value = getattr(record, field, None)
            if value:
                out['_' + field] = value

        return out

    def format(self, record):
        """Format the specified record into json using the schema GELF format

        :param logging.LogRecord record: Contains all the information pertinent to the event being logged.
        :return: A JSON dump of the record.
        :rtype: str
        """
        self.set_more_extra_fields(record)
        record_dict = self.get_gelf_fields(record)
        out = json.dumps(record_dict, cls=self.encoder_cls)
        if self.null_character is True:
            out += '\0'
        return out


class BasicRequestGELFFormatter(BasicGELFFormatter):
    """A GELF formatter to format a :class:`logging.LogRecord` into GELF, adding the request status code"""

    def __init__(self):
        extra_fields = {
            **EXTRA_FIELDS,
            **{
                'status_code': True
            }
        }
        super().__init__(extra_fields=extra_fields)


class RequestGELFFormatter(BasicRequestGELFFormatter):
    """A GELF formatter to format a :class:`logging.LogRecord` into GELF, with specific request fields"""

    def set_more_extra_fields(self, record):
        """Transform from :class:`logging.LogRecord` some fields to python dict.

        :param :class:`logging.LogRecord` record: record emitted by logger. Its attribures can be seen
        in https://docs.python.org/3/library/logging.html#logrecord-attributes
        """
        setattr(record, 'scheme', getattr(record.request, 'scheme', None))
        self.extra_fields['scheme'] = True

        setattr(record, 'method', getattr(record.request, 'method', None))
        self.extra_fields['method'] = True

        user = getattr(record.request, 'user', None)
        if user:
            setattr(record, 'user_id', getattr(user, 'id', None))
            self.extra_fields['user_id'] = True

            setattr(record, 'username', getattr(user, 'username', None))
            self.extra_fields['username'] = True
