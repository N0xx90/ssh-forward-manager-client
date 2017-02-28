#!/bin/bash

adduser --home /var/lib/sfmclient --disabled-password --gecos "" sfmclient
su sfmclient -c 'ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa'
if ! type "sudo" > /dev/null; then
    sudo -u sfmclient ssh-copy-id sfmserver@localhost -oStrictHostKeyChecking=no
else 
    echo -n "Please run the following command with sfmclient user : ssh-copy-id sfmserver@localhost -oStrictHostKeyChecking=no"
fi
