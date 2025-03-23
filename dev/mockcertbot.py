#! /usr/bin/env python3


domains = [
    "test.staticpatch",
    "1.test.staticpatch",
    "2.test.staticpatch",
    "3.test.staticpatch",
    "4.test.staticpatch",
    "5.test.staticpatch",
    "6.test.staticpatch",
    "7.test.staticpatch",
    "8.test.staticpatch",
    "9.test.staticpatch",
]

print("Saving debug log to /var/log/letsencrypt/letsencrypt.log")
print("")
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
print("Found the following certs:")
for domain in domains:
    print("Certificate Name: {0}".format(domain))
    print("Expiry Date: 2024-01-01")
    print("Domains: {0}".format(domain))
    print("Certificate Path: /etc/apache2/ssl/self-signed-cert.pem")
    print("Private Key Path: /etc/apache2/ssl/self-signed-key.pem")

