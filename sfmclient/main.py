#!/usr/bin/env python
# coding: utf-8 

import socket
import subprocess
import yaml
import logging
import json
import sys
import os
import time

#if sys.platform == "linux":
#    sys.path.append('/usr/lib/sfm-client')
import settings 
from Packet import Packet, PacketClient
from SshManager import SshManager

settings.init()

logging.basicConfig(level=logging.DEBUG)

def main() :
    retrycount = 1
    host = str(settings.CONFIG["manager"]["server"])
    port = int(settings.CONFIG["manager"]["port"])
    logging.debug("Connect to server")
    while 1 :
        try :

            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((host,port))

            logging.debug("Create Ssh Manager")
            sshM = SshManager(s)

            logging.debug("run Ssh Manager")
            sshM.run()

        except Exception, e:
            logging.error(e)
        finally :
            s.close()
            retrycount += 1
            logging.info("Cannot connect, retry in %d seconds..." %(retrycount*10))
            time.sleep(retrycount*10)

if __name__ == "__main__" :
    main()
