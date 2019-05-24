#!/bin/bash

# Create fake ssl certificate

if [ -d /etc/nginx/ssl ]; then
    cd /etc/nginx/ssl
    openssl genrsa 2048 > host.key
    openssl req -new -x509 -nodes -sha1 -days 3650 -key host.key > host.cert
    openssl x509 -noout -fingerprint -text < host.cert > host.info
    cat host.cert host.key > host.pem
    chmod 400 host.key host.pem
fi
