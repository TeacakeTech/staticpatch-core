FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y python3 python3-virtualenv python3-pip apache2 sudo vim less git
RUN a2enmod ssl

RUN addgroup --gid 2000 staticpatch
RUN adduser --uid 2000 --gid 2000 --gecos "" --disabled-password staticpatch

RUN mkdir -p /home/staticpatch/code
RUN mkdir -p /home/staticpatch/storage/apache-conf
RUN touch /home/staticpatch/storage/apache-conf/staticpatch.conf
RUN ln -s /home/staticpatch/storage/apache-conf/staticpatch.conf /etc/apache2/sites-enabled/staticpatch.conf
RUN chown -R staticpatch:staticpatch /home/staticpatch/storage
RUN chmod a+rx /home/staticpatch/
RUN echo "staticpatch ALL=(ALL) NOPASSWD: /usr/sbin/apachectl,/usr/bin/certbot" > /etc/sudoers.d/staticpatch

WORKDIR /home/staticpatch/code

COPY requirements.txt .

RUN python3 -m virtualenv venvdocker
RUN /bin/bash -c "source venvdocker/bin/activate && pip install -r requirements.txt"

RUN mkdir -p /etc/letsencrypt
RUN touch /etc/letsencrypt/options-ssl-apache.conf
COPY dev/mockcertbot.py /usr/bin/certbot
RUN chmod a+x /usr/bin/certbot
RUN mkdir /etc/apache2/ssl
COPY dev/self-signed-cert.pem /etc/apache2/ssl/self-signed-cert.pem
COPY dev/self-signed-key.pem /etc/apache2/ssl/self-signed-key.pem

CMD [ "/bin/bash", "-c", "--", "while true; do sleep 30; done;"  ]
