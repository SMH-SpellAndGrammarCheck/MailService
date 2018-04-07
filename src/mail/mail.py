#!/usr/bin/env python

import sys, getopt

def main(argv):
    smtp_srv_name = ''
    smtp_srv_port = ''
    username = ''
    try:
        opts, args = getopt.getopt(argv,"s:p:u:",["smtp-srv=","smtp-port=", "username=", "help"])
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
            smtp_srv_port = arg
        elif opt in ("-u", "--username"):
            username = arg
    print('SMTP Server name: ' + smtp_srv_name)
    print('SMTP Server port: ' + smtp_srv_port)
    print('Username: ' + username)

if __name__ == "__main__":
    main(sys.argv[1:])

