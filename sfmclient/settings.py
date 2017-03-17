#!/usr/bin/env python
# coding: utf-8

import os
import yaml

def init() :
    global CONFIG
    try : 
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
    except Exception, e:
        logging.error(e)
        exit(1)


