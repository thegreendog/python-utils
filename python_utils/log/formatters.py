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

EXTRA_FIELDS = ['line', 'file']


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
        # Always wanted fields
        out = {
            'version': GELF_VERSION,
            'host': getattr(record, 'host', socket.gethostname()),
            'short_message':  getattr(record, 'message', record.getMessage()),
            'timestamp': getattr(record, 'created', time.time()),
            'level': self.to_syslog_level(record)
        }
        out['_logger_name'] = getattr(record, 'name')
        out['_levelname'] = getattr(record, 'levelname')
        if getattr(record, 'exc_info', None):
            out['full_message'] = self.formatException(getattr(record, 'exc_info'))

        # Extra fields
        if 'line' in self.extra_fields and getattr(record, 'lineno', None):
            out['_line'] = getattr(record, 'lineno')
        if 'file' in self.extra_fields and getattr(record, 'pathname', None):
            out['_file'] = getattr(record, 'pathname')

        extra_fields = list(set(self.extra_fields) - set(['line', 'file']))
        for field in extra_fields:
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
        extra_fields = EXTRA_FIELDS + ['status_code']
        super().__init__(extra_fields=extra_fields)
