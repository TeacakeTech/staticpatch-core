import random
import string

from django.core.management.base import BaseCommand

import staticpatchcore.models


class Command(BaseCommand):
    help = "Get Site Security Key"

    def add_arguments(self, parser):
        parser.add_argument("slug", type=str)

    def handle(self, *args, **options):
        try:
            site = staticpatchcore.models.SiteModel.objects.get(slug=options["slug"])
        except staticpatchcore.models.SiteModel.DoesNotExist:
            return

        ssk = staticpatchcore.models.SiteSecurityKeyModel()
        ssk.site = site
        ssk.key = "".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=50))
        ssk.save()

        self.stdout.write(ssk.key)
