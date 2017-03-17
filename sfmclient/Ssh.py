#!/usr/bin/env python
# coding: utf-8

import logging
import subprocess

class Ssh():
    command = "ssh -gNnT -R ###PORT###:###FORWARD###:###LOCALPORT### ###CLIENT###@###SERVER### -oStrictHostKeyChecking=no > /dev/null 2>&1 &"

    chkCommand = 'ps aux | grep "ssh -gNnT -R" | grep -v grep | awk \'{print $2}\''

    port = None
    def __init__(self, localport, server) :  
        self.port = None
        self.forward = '127.0.0.1'
        self.localport = str(localport)
        self.client = 'sfmserver'
        self.server = str(server)

    def parseCommand(self) :
        if self.port != None and self.forward != None and self.localport != None and self.client != None and self.server != None :
            self.command = self.command.replace("###PORT###", str(self.port))
            self.command = self.command.replace("###FORWARD###", self.forward)
            self.command = self.command.replace("###LOCALPORT###", str(self.localport))
            self.command = self.command.replace("###CLIENT###", self.client)
            self.command = self.command.replace("###SERVER###", self.server)
            logging.debug('command : ' + self.command)
        else :
            raise Exception('Please fill all variables')
    def getPids(self) :
        p = subprocess.Popen(self.chkCommand, shell=True, stdout=subprocess.PIPE) 
        pids_out, err = p.communicate()
        if(err is None):
            self.pids = str(pids_out).replace("\\n", " ").replace("\n", " ").replace('b\'','').replace('\'','')

    def start(self) :
        logging.debug('Start process function, parse command')
        self.parseCommand()
        p = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if err is None :
            return True
        else :
            return False 

    def stop(self) :
        if self.status():
                kCommand = 'kill -9 '+self.pids
                p = subprocess.Popen(kCommand, shell=True, stdout=subprocess.PIPE)
                out, err = p.communicate()
                if err is None :
                    return True
                else :
                    return False
    def status(self):
        self.getPids()
        if self.pids == '' :
            return False
        else:
            return True


