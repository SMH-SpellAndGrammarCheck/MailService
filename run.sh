#!/usr/bin/env bash

sudo docker stop maild
sudo docker rm maild

echo "Please enter the password used for logging into your SMTP server:"
read -s SMTP_PASSWORD
echo

sudo docker run -d -it \
    -p 8080:8080 \
    -e SMTP_PASSWORD="${SMTP_PASSWORD}"\
    --name=maild \
    mail_service