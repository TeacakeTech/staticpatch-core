from django.core.management.base import BaseCommand

import staticpatchcore.models


class Command(BaseCommand):
    help = "List Site"

    def add_arguments(self, parser):
        parser.add_argument("slug", type=str)

    def handle(self, *args, **options):
        try:
            site = staticpatchcore.models.SiteModel.objects.get(slug=options["slug"])
        except staticpatchcore.models.SiteModel.DoesNotExist:
            return

        self.stdout.write("Slug: {}".format(site.slug))
        self.stdout.write("State: {}".format("Active" if site.active else "Inactive"))
