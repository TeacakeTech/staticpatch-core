import os
import subprocess

from django.conf import settings


class Certbot:

    def __init__(self):
        self._current_information = None

    def _parse_certbot_certificates_output(self, output: str) -> dict:
        certificates: dict = {}
        current_cert = None

        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.startswith("Certificate Name:"):
                current_cert = line.split(":", 1)[1].strip()
                certificates[current_cert] = {}
            elif current_cert and ":" in line:
                key, value = line.split(":", 1)
                certificates[current_cert][key.strip()] = value.strip()

        return certificates

    def get_information(self) -> None:

        try:
            result = subprocess.run(
                ["sudo", "certbot", "certificates"],
                capture_output=True,
                text=True,
                check=True,
            )
            self._current_information = self._parse_certbot_certificates_output(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running certbot: {e}")

    def get_details_for_domain(self, domain):
        if self._current_information is None:
            self.get_information()

        for k, v in self._current_information.items():
            domains = [i.strip() for i in v.get("Domains", "").split(" ") if i.strip()]
            if domain in domains:
                return v

        return None

    def get_cert_for_domain(self, domain) -> None:
        try:
            subprocess.run(
                [
                    "sudo",
                    "certbot",
                    "certonly",
                    "--non-interactive",
                    "--no-self-upgrade",
                    "--expand",
                    "--email",
                    settings.CERTBOT_EMAIL,
                    "--agree-tos",
                    "--webroot",
                    "--webroot-path",
                    os.path.join(settings.FILE_STORAGE, "webroot"),
                    "-d",
                    domain,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error getting new cert: {e}")
