from django.core.management.base import BaseCommand

import staticpatchcore.updateserverconfig


class Command(BaseCommand):
    help = "Update Server Config (Apache, Certbot, etc)"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        staticpatchcore.updateserverconfig.update_server_config()
