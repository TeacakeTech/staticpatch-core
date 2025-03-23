from django.core.management.base import BaseCommand

import staticpatchcore.models
import staticpatchcore.utils


class Command(BaseCommand):
    help = "Edit Site Basic Authentication"

    def add_arguments(self, parser):
        parser.add_argument("slug", type=str, help="Site slug")
        parser.add_argument("username", type=str, help="Username for basic auth")
        parser.add_argument("password", type=str, help="Password for basic auth")

    def handle(self, *args, **options):
        try:
            site = staticpatchcore.models.SiteModel.objects.get(slug=options["slug"])
        except staticpatchcore.models.SiteModel.DoesNotExist:
            self.stderr.write(f"Site with slug '{options['slug']}' not found")
            return

        # Look for existing basic auth user, including deleted ones
        try:
            basic_auth_user = staticpatchcore.models.BasicAuthUserModel.objects.get(
                site=site, username=options["username"]
            )

            # Reactivate if deleted
            if basic_auth_user.deleted_at is not None:
                basic_auth_user.deleted_at = None
                self.stdout.write(
                    "Reactivated deleted basic auth credentials for site "
                    + f"'{site.slug}' and username '{options['username']}'"
                )

            # Reactivate if inactive
            if not basic_auth_user.active:
                basic_auth_user.active = True
                self.stdout.write(
                    "Reactivated inactive basic auth credentials for site "
                    + f"'{site.slug}' and username '{options['username']}'"
                )

            # Update password
            basic_auth_user.password_crypted = staticpatchcore.utils.hash_password(options["password"])
            basic_auth_user.save()
            self.stdout.write(
                f"Updated basic auth credentials for site '{site.slug}' and username '{options['username']}'"
            )
        except staticpatchcore.models.BasicAuthUserModel.DoesNotExist:
            # Create new user
            basic_auth_user = staticpatchcore.models.BasicAuthUserModel(
                site=site,
                username=options["username"],
                password_crypted=staticpatchcore.utils.hash_password(options["password"]),
            )
            basic_auth_user.save()
            self.stdout.write(
                f"Created new basic auth credentials for site '{site.slug}' and username '{options['username']}'"
            )
