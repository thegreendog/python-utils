import traceback
from gunicorn import glogging


class GunicornLogger(glogging.Logger):
    def access(self, resp, req, environ, request_time):
        """ See http://httpd.apache.org/docs/2.0/logs.html#combined
        for format details
        """

        if not (self.cfg.accesslog or self.cfg.logconfig or
                self.cfg.logconfig_dict or
                (self.cfg.syslog and not self.cfg.disable_redirect_access_to_syslog)):
            return

        # wrap atoms:
        # - make sure atoms will be test case insensitively
        # - if atom doesn't exist replace it by '-'
        safe_atoms = self.atoms_wrapper_class(self.atoms(resp, req, environ,
                                                         request_time))

        try:
            self.access_log.info(self.cfg.access_log_format, safe_atoms,
                                 extra={'remote_addr': safe_atoms.get('h'),
                                        'status_code': safe_atoms.get('s'),
                                        'http_user_agent': safe_atoms.get('a'),
                                        'request_method': safe_atoms.get('m'),
                                        'path_info': safe_atoms.get('U'),
                                        'server_protocol': safe_atoms.get('H')
                                        }
                                 )
        except:
            self.error(traceback.format_exc())
