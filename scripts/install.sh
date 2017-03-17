#!/bin/bash

adduser --home /var/lib/sfmclient --disabled-password --gecos "" sfmclient
su sfmclient -c 'ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa'
echo  "Please run the following command with sfmclient user : ssh-copy-id sfmserver@server -oStrictHostKeyChecking=no\n"
