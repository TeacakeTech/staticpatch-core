# Install on Ubuntu 24.04 server

## Install

As root ...

Install some dependencies:

    apt-get update
    apt-get install -y apache2 git

Create the `staticpatch` user:

    adduser --gecos "" --disabled-password staticpatch

Check out the code into this users home directory:

    su -c "git clone https://github.com/TeacakeTech/staticpatch-core.git /home/staticpatch/code" staticpatch

Create file /home/staticpatch/env_vars and set and then edit the contents:

```
STATICPATCH_FILE_STORAGE=/home/staticpatch/storage
STATICPATCH_CERTBOT_EMAIL=CHANGE
STATICPATCH_DEBUG=False
STATICPATCH_ALLOWED_HOSTS=CHANGE
STATICPATCH_CSRF_TRUSTED_ORIGINS=http://CHANGE
STATICPATCH_SECRET_KEY=set
STATICPATCH_STATIC_ROOT=/home/staticpatch/webroot/static
```

Create file /etc/apache2/sites-available/staticpatchapp.conf and set and then edit the contents:

```
<VirtualHost *:80>
    ServerName HOSTNAME
    Include /etc/apache2/sites-available/staticpatchapp.include.conf
</VirtualHost>
```

Run install.sh direct from code repo:

    /home/staticpatch/code/host/ubuntu2404/install.sh   

Now run certbot with the domain for the main app:

    certbot --apache -d CHANGE

## Create users for the web interface

As user staticpatch, set up an app user:

    ./run_manage.sh createsuperuser


## Maintain - Update app

Run as root:

    su -c "/home/staticpatch/update_as_user.sh" staticpatch
    systemctl restart staticpatchworker.service
    systemctl restart staticpatchweb.service

