from django.core.management.base import BaseCommand

from staticpatchcore.models import SiteModel


class Command(BaseCommand):
    help = "List Sites"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        sites = SiteModel.objects.filter(deleted_at__isnull=True)
        for site in sites:
            self.stdout.write("{} (ID: {}) {}".format(site.slug, site.id, "Active" if site.active else "Inactive"))
