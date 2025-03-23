import subprocess
import time

import staticpatchcore.apache_config
import staticpatchcore.models
import staticpatchcore.utils


def update_server_config() -> None:
    """
    Update the server config (Apache, Certbot, etc)
    """
    print("Updating Apache Config")

    # Rebuild Apache Conf
    apache_config = staticpatchcore.apache_config.ApacheConfig()
    apache_config.generate()
    apache_config.write()

    # Reload Apache
    subprocess.run(["sudo", "apachectl", "graceful"], check=True)

    # Any SSL certs missing?
    if apache_config.get_domains_missing_ssl():
        print("Small sleep before getting certs (to ensure server is ready)")
        time.sleep(10)

        # Get the certs
        certbot = staticpatchcore.certbot.Certbot()
        for domain in apache_config.get_domains_missing_ssl():
            print("Getting cert for {0}".format(domain))
            certbot.get_cert_for_domain(domain)

        print("Updating Apache Config again (with new certs)")
        # We make a new instance of the ApacheConfig class to ensure we have the latest certs
        # And to avoid any issues with reusing the same instance, as we haven't tested that.
        apache_config = staticpatchcore.apache_config.ApacheConfig()
        apache_config.generate()
        apache_config.write()

        # Reload Apache
        subprocess.run(["sudo", "apachectl", "graceful"], check=True)
