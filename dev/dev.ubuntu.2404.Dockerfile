FROM ubuntu:24.04

# Install Software
RUN apt-get update
RUN apt-get install -y python3 python3-virtualenv python3-pip apache2 sudo vim less git
RUN a2enmod ssl

# Create user
RUN addgroup --gid 2000 staticpatch
RUN adduser --uid 2000 --gid 2000 --gecos "" --disabled-password staticpatch

# Give user Sudo rights
RUN echo "staticpatch ALL=(ALL) NOPASSWD: /usr/sbin/apachectl,/usr/bin/certbot,/bin/bash" > /etc/sudoers.d/staticpatch

# Set up fake certbot
RUN mkdir -p /etc/letsencrypt
RUN touch /etc/letsencrypt/options-ssl-apache.conf
COPY dev/mockcertbot.py /usr/bin/certbot
RUN chmod a+x /usr/bin/certbot
RUN mkdir /etc/apache2/ssl
COPY dev/self-signed-cert.pem /etc/apache2/ssl/self-signed-cert.pem
COPY dev/self-signed-key.pem /etc/apache2/ssl/self-signed-key.pem

# Create dirs for storage and code
RUN mkdir -p /home/staticpatch/code
RUN mkdir -p /home/staticpatch/storage/apache-conf
RUN touch /home/staticpatch/storage/apache-conf/staticpatch.conf
RUN ln -s /home/staticpatch/storage/apache-conf/staticpatch.conf /etc/apache2/sites-enabled/staticpatch.conf
RUN chown -R staticpatch:staticpatch /home/staticpatch/storage
RUN chmod a+rx /home/staticpatch/

# Set options
WORKDIR /home/staticpatch/code
USER staticpatch:staticpatch

# Python Deps
COPY requirements_dev.txt .
RUN /bin/bash -c "echo \"export PATH=\$PATH:/home/staticpatch/.local/bin/\" >> /home/staticpatch/.bashrc"
RUN python3 -m pip config set global.break-system-packages true
RUN pip install --user -r requirements_dev.txt

CMD [ "/bin/bash", "-c", "--", "while true; do sleep 30; done;"  ]
