#!/bin/bash

set -e

# Install dependencies
echo "Install Dependencies ..."
apt-get update
apt-get install -y python3 python3-virtualenv python3-pip apache2 sudo certbot python3-certbot-apache
a2enmod proxy_http

# Make sure code directory was checked out as correct user
echo "Check code user permissions ..."
chown -R staticpatch:staticpatch /home/staticpatch/code

# Set up storage & link to apache
echo "Set up storage and Apache configuration..."
mkdir -p /home/staticpatch/storage/apache-conf
touch /home/staticpatch/storage/apache-conf/staticpatch.conf
ln -s /home/staticpatch/storage/apache-conf/staticpatch.conf /etc/apache2/sites-enabled/staticpatchsites.conf
chown -R staticpatch:staticpatch /home/staticpatch/storage

# Permissions on home dir, so Apache can serve it
echo "Home directory permissions ..."
chmod a+rx /home/staticpatch/

# Set up sudo
echo "Sudo ..."
echo "staticpatch ALL=(ALL) NOPASSWD: /usr/sbin/apachectl,/usr/bin/certbot" > /etc/sudoers.d/staticpatch

# Venv
echo "Virtual Env ..."
su -c "python3 -m virtualenv /home/staticpatch/ve" staticpatch 
su -c "source /home/staticpatch/ve/bin/activate && pip install -r /home/staticpatch/code/requirements.txt" staticpatch 

# Set up update script
echo "Set up update script ..."
su -c "cp /home/staticpatch/code/host/ubuntu2404/update_as_user.sh /home/staticpatch/update_as_user.sh" staticpatch 
su -c "chmod u+x /home/staticpatch/update_as_user.sh" staticpatch 

# Run the update script - this does migrate, collectstatic, etc
echo "Run update script ..."
su -c "/home/staticpatch/update_as_user.sh" staticpatch 

# Set up and run Web Server - Gunicorn
echo "Set up and run Gunicorn..."
cp /home/staticpatch/code/host/ubuntu2404/web.service /etc/systemd/system/staticpatchweb.service
systemctl daemon-reload
systemctl enable staticpatchweb.service
systemctl start staticpatchweb.service

# Set up and run Web Server - Apache
echo "Set up and run Apache ..."
mkdir -p /home/staticpatch/webroot
chown staticpatch:staticpatch /home/staticpatch/webroot 
cp /home/staticpatch/code/host/ubuntu2404/robots.txt /home/staticpatch/webroot/robots.txt
cp /home/staticpatch/code/host/ubuntu2404/apache.include.conf /etc/apache2/sites-available/staticpatchapp.include.conf
a2ensite staticpatchapp
systemctl restart apache2.service

# Set up and run Worker
echo "Set up and run Worker ..."
su -c "cp /home/staticpatch/code/host/ubuntu2404/run_worker.sh /home/staticpatch/run_worker.sh" staticpatch 
su -c "chmod u+x /home/staticpatch/run_worker.sh" staticpatch 
cp /home/staticpatch/code/host/ubuntu2404/worker.service /etc/systemd/system/staticpatchworker.service
systemctl daemon-reload
systemctl enable staticpatchworker.service
systemctl start staticpatchworker.service

# Set up run_manage.py
echo "Set up handy commands ..."
cp /home/staticpatch/code/host/ubuntu2404/run_manage.sh /home/staticpatch/run_manage.sh
chown staticpatch:staticpatch /home/staticpatch/run_manage.sh
chmod u+x /home/staticpatch/run_manage.sh

# Done
echo "Done!"
