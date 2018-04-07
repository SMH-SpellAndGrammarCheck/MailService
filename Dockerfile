FROM centos:latest

RUN yum update

RUN yum -y install sendmail

ADD setSendmailFQDN.sh /opt/setSendmailFQDN.sh

ADD startSendmailService.sh /opt/startSendmailService.sh

ADD src/http /srv/http

EXPOSE 8080

CMD /srv/http/http.py 8080