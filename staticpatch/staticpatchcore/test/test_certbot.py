from django.test import TestCase

from staticpatchcore.certbot import Certbot


class TestCertBotCase(TestCase):

    def test_1(self):
        certbot = Certbot()
        assert (
            certbot._parse_certbot_certificates_output(
                """Saving debug log to /var/log/letsencrypt/letsencrypt.log

            - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            Found the following certs:

            Certificate Name: example.com
            Expiry Date: 2024-01-01
            Domains: example.com
            Certificate Path: /etc/letsencrypt/live/example.com/fullchain.pem
            Private Key Path: /etc/letsencrypt/live/example.com/privkey.pem
            Certificate Name: cats.com
            Expiry Date: 2024-01-01
            Domains: cats.com
            Certificate Path: /etc/letsencrypt/live/cats.com/fullchain.pem
            Private Key Path: /etc/letsencrypt/live/cats.com/privkey.pem

        """
            )
            == {
                "example.com": {
                    "Expiry Date": "2024-01-01",
                    "Domains": "example.com",
                    "Certificate Path": "/etc/letsencrypt/live/example.com/fullchain.pem",
                    "Private Key Path": "/etc/letsencrypt/live/example.com/privkey.pem",
                },
                "cats.com": {
                    "Expiry Date": "2024-01-01",
                    "Domains": "cats.com",
                    "Certificate Path": "/etc/letsencrypt/live/cats.com/fullchain.pem",
                    "Private Key Path": "/etc/letsencrypt/live/cats.com/privkey.pem",
                },
            }
        )

    def test_2(self):
        certbot = Certbot()
        assert (
            certbot._parse_certbot_certificates_output(
                """Saving debug log to /var/log/letsencrypt/letsencrypt.log

            - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            No certificates found.
            - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            """
            )
            == {}
        )
