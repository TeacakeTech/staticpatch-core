from django.core.management.base import BaseCommand

from staticpatchcore.models import SiteModel


class Command(BaseCommand):
    help = "List Sites"

    def add_arguments(self, parser):
        parser.add_argument("slug", type=str)
        parser.add_argument("--main-domain", type=str, help="Set the main domain for the site")
        parser.add_argument(
            "--basic-auth-required",
            action="store_true",
            help="Require basic authentication",
        )
        parser.add_argument(
            "--no-basic-auth-required",
            action="store_true",
            help="Do not require basic authentication",
        )
        parser.add_argument("--active", action="store_true", help="Set site as active")
        parser.add_argument("--inactive", action="store_true", help="Set site as inactive")
        parser.add_argument("--main-domain-ssl", action="store_true", help="Enable SSL for main domain")
        parser.add_argument(
            "--no-main-domain-ssl",
            action="store_true",
            help="Disable SSL for main domain",
        )

    def handle(self, *args, **options):
        try:
            site = SiteModel.objects.get(slug=options["slug"])
        except SiteModel.DoesNotExist:
            site = SiteModel()
            site.slug = options["slug"]

        if options["main_domain"]:
            site.main_domain = options["main_domain"]

        if options["basic_auth_required"]:
            site.basic_auth_user_required = True
        elif options["no_basic_auth_required"]:
            site.basic_auth_user_required = False

        if options["active"]:
            site.active = True
        elif options["inactive"]:
            site.active = False

        if options["main_domain_ssl"]:
            site.main_domain_ssl = True
        elif options["no_main_domain_ssl"]:
            site.main_domain_ssl = False

        site.save()
