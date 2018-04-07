#!/usr/bin/env bash

sh /opt/setSendmailFQDN.sh

/etc/init.d/sendmail start

/usr/sbin/httpd -k restart