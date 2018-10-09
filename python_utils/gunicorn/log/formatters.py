"""
Gunicorn specific formatters: they specify the layout of log records in the final output. 
GELF formatters are based on this spec: http://docs.graylog.org/en/2.4/pages/gelf.html#gelf-payload-specification
"""

from python_utils.log.formatters import BasicGELFFormatter, EXTRA_FIELDS


class GunicornRequestGELFFormatter(BasicGELFFormatter):
    """A GELF formatter to format a :class:`logging.LogRecord` into GELF, adding gunicorn access log specific fields"""

    def __init__(self):
        extra_fields = EXTRA_FIELDS + ['remote_addr', 'http_user_agent', 'request_method',
                                       'path_info', 'server_protocol']
        super().__init__(extra_fields=extra_fields)
