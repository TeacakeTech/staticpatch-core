from django.core.management.base import BaseCommand

import staticpatchcore.update_server_config


class Command(BaseCommand):
    help = "Update Server Config (Apache, Certbot, etc)"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        staticpatchcore.update_server_config.update_server_config()
