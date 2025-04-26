from django.core.management.base import BaseCommand

from staticpatchcore.purge_deleted import purge_deleted


class Command(BaseCommand):
    help = "Purge deleted objects that are older than PURGE_DELETED_AFTER_SECONDS setting"

    def handle(self, *args, **options):
        purge_deleted()
        self.stdout.write(self.style.SUCCESS("Done"))
