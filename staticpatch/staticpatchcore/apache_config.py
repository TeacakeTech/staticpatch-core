import json
import os

from django.conf import settings

import staticpatchcore.models
from staticpatchcore.certbot import Certbot


class ApacheConfig:

    def __init__(self, certbot=None):
        self.__out = ""
        self.__password_files = {}
        self.__certbot = certbot or Certbot()
        self.__domains_missing_ssl = []

    def generate(self):

        # Generate the main Apache configuration file
        self.__out = ""

        sites = staticpatchcore.models.SiteModel.objects.filter(deleted_at__isnull=True, active=True)
        for site in sites:
            self.__out += "# ============================================= Site {} ({}) \n".format(site.id, site.slug)

            # main site
            build = (
                staticpatchcore.models.BuildModel.objects.filter(
                    site=site,
                    site_preview_instance__isnull=True,
                    sub_site__isnull=True,
                    finished_at__isnull=False,
                    deleted_at__isnull=True,
                )
                .order_by("-finished_at")
                .first()
            )

            # Sub Sites
            sub_sites = {}
            for sub_site in staticpatchcore.models.SubSiteModel.objects.filter(
                site=site, deleted_at__isnull=True, active=True
            ):
                sub_site_build = (
                    staticpatchcore.models.BuildModel.objects.filter(
                        site=site,
                        site_preview_instance__isnull=True,
                        sub_site=sub_site,
                        finished_at__isnull=False,
                        deleted_at__isnull=True,
                    )
                    .order_by("-finished_at")
                    .first()
                )
                if sub_site_build:
                    sub_sites[sub_site.url] = sub_site_build

            if site.public_info:
                site_info_dir = "{}/site/{}/publicinfo".format(settings.FILE_STORAGE, site.id)
                os.makedirs(site_info_dir, exist_ok=True)
                site_info_data = {
                    "sub_sites": {k: {"at": v.finished_at.isoformat()} for k, v in sub_sites.items()},
                    "root_site": ({"at": build.finished_at.isoformat()} if build else None),
                }
                with open(os.path.join(site_info_dir, "data.json"), "w") as fp:
                    json.dump(site_info_data, fp, indent=2)
                sub_sites[staticpatchcore.models.SubSiteModel.normalise_url(site.public_info_url)] = "publicinfo"

            # and generate
            self.__out += self._generate_virtual_host(
                site,
                build,
                site.main_domain,
                site.allow_override,
                site.basic_auth_user_required,
                "main",
                ssl_enabled=site.main_domain_ssl,
                sub_sites=sub_sites,
            )

            # Alternative Domains
            for alternative_domain in staticpatchcore.models.SiteAlternativeDomainModel.objects.filter(
                site=site, deleted_at__isnull=True, active=True
            ):
                self.__out += (
                    "# --------------------------------------------------- Alternative Domain {} ({}) \n".format(
                        alternative_domain.id, alternative_domain.domain
                    )
                )
                self.__out += "<VirtualHost *:80>\n"
                self.__out += "ServerName {}\n".format(alternative_domain.domain)
                # TODO does main site have SSL available? if so redirect to SSL
                self.__out += "Redirect 302 / http://{}/\n".format(site.main_domain)
                self.__out += self._get_boilerplate_virtual_host(site, "alternative")
                self.__out += "</VirtualHost>\n"
                if alternative_domain.domain_ssl:
                    ssl_info = self.__certbot.get_details_for_domain(alternative_domain.domain)
                    if ssl_info is None:
                        self.__domains_missing_ssl.append(alternative_domain.domain)
                    else:
                        self.__out += "<VirtualHost *:443>\n"
                        self.__out += "ServerName {}\n".format(alternative_domain.domain)
                        # TODO does main site have SSL available? if so redirect to SSL
                        self.__out += "Redirect 302 / http://{}/\n".format(site.main_domain)
                        self.__out += "SSLEngine on\n"
                        self.__out += "SSLCertificateFile {}\n".format(ssl_info["Certificate Path"])
                        self.__out += "SSLCertificateKeyFile {}\n".format(ssl_info["Private Key Path"])
                        self.__out += "Include /etc/letsencrypt/options-ssl-apache.conf\n"
                        self.__out += self._get_boilerplate_virtual_host(site, "alternative")
                        self.__out += "</VirtualHost>\n"

            # Previews
            for preview_type in staticpatchcore.models.SitePreviewTypeModel.objects.filter(
                site=site, deleted_at__isnull=True, active=True
            ):
                self.__out += "# --------------------------------------------------- Preview Type {} ({}) \n".format(
                    preview_type.id, preview_type.slug
                )
                for preview_instance in staticpatchcore.models.SitePreviewInstanceModel.objects.filter(
                    site_preview_type=preview_type, deleted_at__isnull=True, active=True
                ):
                    self.__out += (
                        "# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Preview Instance {} ({}) \n".format(
                            preview_instance.id, preview_instance.slug
                        )
                    )
                    build = (
                        staticpatchcore.models.BuildModel.objects.filter(
                            site=site,
                            site_preview_instance=preview_instance,
                            sub_site__isnull=True,
                            finished_at__isnull=False,
                            deleted_at__isnull=True,
                        )
                        .order_by("-finished_at")
                        .first()
                    )
                    domain = "{}.{}".format(preview_instance.slug, preview_type.domain)
                    self.__out += self._generate_virtual_host(
                        site,
                        build,
                        domain,
                        site.allow_override,
                        preview_type.basic_auth_user_required,
                        "preview",
                        ssl_enabled=preview_type.domain_ssl,
                    )

        # Generate the password files
        for site in sites:
            basic_auth_users = staticpatchcore.models.BasicAuthUserModel.objects.filter(
                site=site, active=True, deleted_at__isnull=True
            )
            if basic_auth_users.exists():
                self.__password_files[site.id] = ""
                for user in basic_auth_users:
                    self.__password_files[site.id] += f"{user.username}:{user.password_crypted}\n"

    def _generate_virtual_host(
        self, site, build, domain, allow_override, basic_auth_user_required, log_type, ssl_enabled=False, sub_sites={}
    ):

        out = ""

        ssl_info = None
        if ssl_enabled:
            ssl_info = self.__certbot.get_details_for_domain(domain)
            if ssl_info is None:
                self.__domains_missing_ssl.append(domain)

        if ssl_info is None:
            out += "<VirtualHost *:80>\n"
        else:
            out += "<VirtualHost *:80>\n"
            out += "ServerName {}\n".format(domain)
            out += "Redirect 302 / https://{}/\n".format(domain)
            out += self._get_boilerplate_virtual_host(site, log_type)
            out += "</VirtualHost>\n"

            out += "<VirtualHost *:443>\n"
            out += "SSLEngine on\n"
            out += "SSLCertificateFile {}\n".format(ssl_info["Certificate Path"])
            out += "SSLCertificateKeyFile {}\n".format(ssl_info["Private Key Path"])
            out += "Include /etc/letsencrypt/options-ssl-apache.conf\n"

        out += "ServerName {}\n".format(domain)
        if allow_override:
            out += "AccessFileName " + site.access_file_name + "\n"

        # Main directory
        dir = (
            "{}/site/{}/build/{}/out".format(settings.FILE_STORAGE, site.id, build.get_file_storage_slug())
            if build
            else "{}/webroot".format(settings.FILE_STORAGE)
        )
        out += "DocumentRoot " + dir + "\n"
        out += self._get_boilerplate_for_directory(dir, allow_override, basic_auth_user_required, site)

        # Sub sites
        for sub_site_url, sub_site_build in sub_sites.items():
            sub_site_dir = (
                "{}/site/{}/build/{}/out".format(settings.FILE_STORAGE, site.id, sub_site_build.get_file_storage_slug())
                if isinstance(sub_site_build, staticpatchcore.models.BuildModel)
                else "{}/site/{}/{}".format(settings.FILE_STORAGE, site.id, sub_site_build)
            )
            out += 'Alias "' + sub_site_url + '" "' + sub_site_dir + '"\n'
            out += self._get_boilerplate_for_directory(sub_site_dir, allow_override, basic_auth_user_required, site)

        # and wrap up ...
        out += self._get_boilerplate_virtual_host(site, log_type)
        out += "</VirtualHost>\n"
        return out

    def _get_boilerplate_for_directory(self, dir, allow_override, basic_auth_user_required, site):
        out = '<Directory "' + dir + '">\n'
        out += "AllowOverride " + ("All Nonfatal=All" if allow_override else "None") + "\n"
        if basic_auth_user_required:
            out += "AuthType Basic\n"
            out += 'AuthName "StaticPatch"\n'
            out += (
                "AuthUserFile "
                + os.path.join(
                    settings.FILE_STORAGE,
                    "apache-conf",
                    f"{site.id}-passwords.conf",
                )
                + "\n"
            )
            out += "Require valid-user\n"
        else:
            out += "Require all granted\n"
        out += "</Directory>\n"
        return out

    def _get_boilerplate_virtual_host(self, site, log_type):
        out = ""
        out += "Alias /.well-known/acme-challenge {}/webroot/.well-known/acme-challenge\n".format(settings.FILE_STORAGE)
        out += "<Directory {}/webroot/.well-known/acme-challenge>\n".format(settings.FILE_STORAGE)
        out += "    Options none\n"
        out += "    Require all granted\n"
        out += "    AllowOverride None\n"
        out += "</Directory>\n"
        out += "ErrorLog {}/site-{}-{}-error.log\n".format(settings.APACHE_LOG_DIR, site.id, log_type)
        out += "CustomLog {}/site-{}-{}-access.log combined\n".format(settings.APACHE_LOG_DIR, site.id, log_type)
        return out

    def get(self):
        return self.__out

    def get_domains_missing_ssl(self):
        return self.__domains_missing_ssl

    def write(self):
        # Write the main Apache configuration file
        with open(os.path.join(settings.FILE_STORAGE, "apache-conf", "staticpatch.conf"), "w") as fp:
            fp.write(self.get())

        # Create password files for each site's BasicAuthUserModel objects
        for id, content in self.__password_files.items():
            with open(
                os.path.join(settings.FILE_STORAGE, "apache-conf", f"{id}-passwords.conf"),
                "w",
            ) as fp:
                fp.write(content)
