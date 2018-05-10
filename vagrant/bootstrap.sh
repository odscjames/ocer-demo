#!/bin/bash

apt-get update
apt-get install -y python3 python3-pip apache2

git clone https://github.com/open-contracting/extension_registry.git /open-contracting-extension-registry

pip3 install -r /vagrant/extension_website/requirements.txt


mkdir /data
chown -R vagrant:users /data

mkdir /out
chown -R vagrant:users /out


cp /vagrant/vagrant/apache.conf /etc/apache2/sites-enabled/000-default.conf
/etc/init.d/apache2 restart

