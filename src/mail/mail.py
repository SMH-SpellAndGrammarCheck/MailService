#!/usr/bin/env python

import sys, getopt
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import ConfigParser

def main(argv):
    smtp_srv_name = ''
    smtp_srv_port = ''
    username = ''
    to_address = ''
    subject = ''
    body = ''
    filenames = []
    try:
        opts, args = getopt.getopt(argv,"s:p:u:T:S:B:f:",["smtp-srv=","smtp-port=", "username=", "to-address=", "subject=", "body=", "file=", "help"])
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
        elif opt in ("-f", "--file"):
            filenames.append(arg)
    print('SMTP Server name: ' + smtp_srv_name)
    print('SMTP Server port: ' + str(smtp_srv_port))
    print('Username: ' + username)
    print('Writing to: ' + to_address)
    print('Subject: ' + subject)
    print('Body:\n' + body)

    connection_cfg = readConnectionConf()
    srv_cfg = connection_cfg[0:2]
    user_credentials = (connection_cfg[2], getPassword())
    message = createMessage(to_address, user_credentials[0], subject, body)

    attachFiles(message, filenames)
    sendMail(srv_cfg, user_credentials, to_address, message.as_string())

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
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    return msg

def attachFiles(message, filenames):
    for filename in filenames:
        attachFile(message, filename)

def attachFile(message, filename):
    attachment = None
    file_basename = os.path.basename(filename)
    with open(filename, 'rb') as f:
        attachment = MIMEApplication(f.read(), Name=file_basename)
    attachment['Content-Disposition'] = 'attachment; filename="%s"' % file_basename
    message.attach(attachment)
    return message

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
    print("Sending mail...")
    server.sendmail(credentials[0], to_address, message)

    print("Quitting...")
    server.quit()

if __name__ == "__main__":
    main(sys.argv[1:])

