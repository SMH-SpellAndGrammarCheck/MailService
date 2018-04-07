#!/usr/bin/env python

import sys, getopt
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import ConfigParser

def main(argv):
    smtp_srv_name = ''
    smtp_srv_port = ''
    username = ''
    to_address = ''
    subject = ''
    body = ''
    try:
        opts, args = getopt.getopt(argv,"s:p:u:T:S:B:",["smtp-srv=","smtp-port=", "username=", "to-address=", "subject=", "body=", "help"])
    except getopt.GetoptError:
        print 'Wrong parameters'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--help':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-s", "--smtp-srv"):
            smtp_srv_name = arg
        elif opt in ("-p", "--smtp-port"):
            smtp_srv_port = int(arg)
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-T", "--to-address"):
            to_address = arg
        elif opt in ("-S", "--subject"):
            subject = arg
        elif opt in ("-B", "--body"):
            body = arg
    print('SMTP Server name: ' + smtp_srv_name)
    print('SMTP Server port: ' + str(smtp_srv_port))
    print('Username: ' + username)
    print('Writing to: ' + to_address)
    print('Subject: ' + subject)
    print('Body:\n' + body)
    srv_conf = readServerConf()
    user_credentials = (username, getPassword())
    sendMail(srv_conf, user_credentials, "matthias.hermann@iteratec.de", "Hi")

def readConnectionConf():
    cfgParser = ConfigParser.ConfigParser()
    cfgParser.read('./res/connection.cfg')
    smtp_srv_name = cfgParser.get('DEFAULT', 'smtp_srv_name')
    smtp_srv_port = cfgParser.get('DEFAULT', 'smtp_srv_port')
    username = cfgParser.get('USER', 'username')
    return (smtp_srv_name, smtp_srv_port, username)

def getPassword():
    if 'SMTP_PASSWORD' in os.environ:
        return os.environ['SMTP_PASSWORD']
    else:
        return ''

def createMessage(to_address, from_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg

def sendMail(srv_conf, credentials, to_address, message):
    print("Creating SMTP object...")
    server = smtplib.SMTP(srv_conf[0], srv_conf[1])

    server.ehlo()
    server.starttls()
    server.ehlo()

    #Next, log in to the server
    print("Logging in...")
    server.login(credentials[0], credentials[1])

    #Send the mail
    msg = "\nHello!" # The /n separates the message from the headers
    print("Sending mail...")
    server.sendmail(credentials[0], to_address, msg)

    print("Quitting...")
    server.quit()

if __name__ == "__main__":
    main(sys.argv[1:])

