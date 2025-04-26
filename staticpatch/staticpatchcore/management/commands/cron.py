from django.core.management.base import BaseCommand

from staticpatchcore.purge_deleted import purge_deleted


class Command(BaseCommand):
    help = "Run periodic maintenance tasks"

    def handle(self, *args, **options):
        purge_deleted()
        self.stdout.write(self.style.SUCCESS("Done"))
