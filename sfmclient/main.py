#!/usr/bin/env python
#--*-- coding:UTF-8 --*--

import socket
import subprocess
import yaml
import logging
import json
import sys
import os

#if sys.platform == "linux":
#    sys.path.append('/usr/lib/sfm-client')
 
from Packet import Packet, PacketClient
from Ssh import Ssh

CONFIG = None
logging.basicConfig(level=logging.DEBUG)

class SshManager():
    def __init__(self, cs) :
        global CONFIG
        self.cs = cs
        self.sshConfig = CONFIG["ssh"]
        self.process = Ssh(self.sshConfig["localport"], self.sshConfig["server"])

    def run(self) :
        code = None
        try :
            logging.debug('Send information about client')
            self.cs.send(self.buildInfo())
            #receive port
            logging.debug('receive port...')
            raw_port = self.cs.recv(2048)
            raw_port = Packet.parse(raw_port)
            self.process.port = raw_port['command']
            logging.debug('Set port, send response')
            self.cs.send(self.buildResp(0))
            while True :
                logging.debug("Wait for server...")
                data = self.cs.recv(2048)
                data = Packet.parse(data)
                if data["command"] == 'close' :
                    self.cs.send("close")
                    break 
                elif data["command"] == 'status' :
                    if self.process.status() :
                        logging.debug("service is running")
                        code = 0
                    else :
                        logging.debug("service is Stopped")
                        code = 1
                elif data["command"] == 'start' :
                    if self.process.start() :
                        logging.debug("Send Started")
                        code = 0 
                    else :
                        logging.debug("Send Error")
                        code = 2
                elif data["command"] == 'stop' :
                    if self.process.stop() :
                        logging.debug("Send Stopped")
                        code = 0
                    else :
                        logging.debug("Send Error")
                        code = 2
                else :
                    logging.debug("Wrong Command")
                    code=3 
                
                self.cs.send(self.buildResp(code))
        except Exception, e:
            logging.error(e)
            code = 5
            self.cs.send(self.buildResp(code))

    def buildInfo(self):
        info = PacketClient(Packet.Info)
        info.name = subprocess.check_output('hostname -s', shell=True).strip()

        info.build()
        return info.get()

    @staticmethod
    def buildResp(code):
        resp = PacketClient(Packet.Response)
        resp.code = code
        resp.build()
        return resp.get()

def main() :
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try : 
        global CONFIG
        config_files = ['config.yml', '/etc/sfmclient/config.yml']
        config_file_found = False
        for f in config_files :
            if os.path.isfile(f) :
                config_file_found = True
                with open(f, 'r') as ymlfile:
                    CONFIG = yaml.load(ymlfile)
                break
        if not config_file_found :
            raise Exception('No config file found')
        host = str(CONFIG["manager"]["server"])
        port = int(CONFIG["manager"]["port"])
        logging.debug("Connect to server")
        s.connect((host,port))

        logging.debug("Create Ssh Manager")
        sshM = SshManager(s)

        logging.debug("run Ssh Manager")
        sshM.run()

    except Exception, e:
        logging.error(e)
    finally :
        s.close()
if __name__ == "__main__" :
    main()
