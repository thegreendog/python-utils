"""
Django specific formatters: they specify the layout of log records in the final output. 
GELF formatters are based on this spec: http://docs.graylog.org/en/2.4/pages/gelf.html#gelf-payload-specification
"""

from python_utils.log.formatters import BasicRequestGELFFormatter


class DjangoRequestGELFFormatter(BasicRequestGELFFormatter):
    """A GELF formatter to format a :class:`logging.LogRecord` into GELF, with specific request fields"""

    def set_more_extra_fields(self, record):
        """Transform from :class:`logging.LogRecord` some fields to python dict.

        :param :class:`logging.LogRecord` record: record emitted by logger. Its attribures can be seen
        in https://docs.python.org/3/library/logging.html#logrecord-attributes
        """
        request = getattr(record, 'request', None)
        if request:
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
