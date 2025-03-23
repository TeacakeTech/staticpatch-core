import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Setup Storage"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Create dirs
        dirs = [
            os.path.join(settings.FILE_STORAGE, "apache-conf"),
            os.path.join(
                settings.FILE_STORAGE,
                "webroot",
                ".well-known",
                "acme-challenge",
            ),
        ]
        for dir in dirs:
            if not os.path.exists(dir):
                os.makedirs(dir)

        # If not already there, create a blank placeholder apache config
        if not os.path.exists(os.path.join(settings.FILE_STORAGE, "apache-conf", "staticpatch.conf")):
            with open(
                os.path.join(settings.FILE_STORAGE, "apache-conf", "staticpatch.conf"),
                "w",
            ) as f:
                f.write("")

        # Basic files in Webroot
        files = {
            os.path.join(settings.FILE_STORAGE, "webroot", "index.html"): "Nothing to see here",
            os.path.join(settings.FILE_STORAGE, "webroot", "robots.txt"): "User-agent: *\nDisallow: /",
        }
        for k, v in files.items():
            if not os.path.exists(k):
                with open(k, "w") as fp:
                    fp.write(v)
