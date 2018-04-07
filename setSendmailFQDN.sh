#!/usr/bin/env bash

LOCALHOST_LINE=$(head -n 1 /etc/hosts)
SECOND_LINE=$(echo ${LOCALHOST_LINE} | awk '{print $2}')

echo "${LOCALHOST_LINE} ${SECOND_LINE}.localdomain" >> /etc/hosts