FROM centos:latest

RUN yum update

RUN yum -y install sendmail

ADD setSendmailFQDN.sh /opt/setSendmailFQDN.sh