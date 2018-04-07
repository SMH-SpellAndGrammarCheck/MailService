#!/usr/bin/env bash

sudo docker stop maild
sudo docker rm maild
sudo docker run -d -it -p 8080:8080 --name=maild mail_service