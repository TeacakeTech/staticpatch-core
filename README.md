# StaticPatch - Static Website Hosting with Apache and Continous Deployment and more

* 🖥️ Static website hosting with Apache on your own Linux VM
* 🚢 Continuous Deployment from GitHub Actions, GitLab and more with any static site builder you can run in them (so pretty much all of them)
* 👁️ Preview builds on sub domains
* 🔒 CertBot and Let's Encrypt for automatic SSL
* 🔑 HTTP basic auth
* ✏️ Add .htaccess files with any Apache directives - eg tell browsers to cache your CSS/JS

Host static websites directly with Apache, a tried and tested web host. Configure it using the Apache configuration options you already know.

We run a small Django app to allow you to configure sites and continuous deploys. The app then processes any deploys and sets up SSL certificates and Apache configuration as needed (but public viewers never interact with the app - only with Apache directly).

## Set up Continuous Deployment

See `docs` directory.

## Host on your own Linux server

| OS           | Python | Apache | Certbot |
| ----         | ------ | ------ | ------- |
| Ubuntu 24.04 | 3.12   | 2.4    | 2.9     |

See `host` directory for more.

## Develop the tool?

See `dev` directory for more.
