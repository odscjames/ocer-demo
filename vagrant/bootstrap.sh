#!/bin/bash

apt-get update
apt-get install -y python3 python3-pip apache2

git clone https://github.com/open-contracting/extension_registry.git /open-contracting-extension-registry
