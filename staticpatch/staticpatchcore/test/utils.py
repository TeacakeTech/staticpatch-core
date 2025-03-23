import staticpatchcore.apache_config


class MockCertbot:

    def __init__(self):
        self._current_information = None

    def get_information(self):
        pass

    def get_details_for_domain(self, domain):
        if self._current_information is None:
            self._current_information = self.get_information()

        return None

    def get_cert_for_domain(self, domain):
        pass


class ApacheConfigWithNoBoilerplate(staticpatchcore.apache_config.ApacheConfig):

    def _get_boilerplate_virtual_host(self, site, log_type):
        return "BOILERPLATE\n"
