#!/usr/bin/env python
from setuptools import setup
from setuptools.command.install import install

import os

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        os.system('bash ./scripts/install.sh')
        install.run(self)


setup(
    name='sfmclient',
    
    version='1.0.0',
    description='SSH forward manager client package',

    url='githuburl',

    author='N0xx',
    author_email='n0xx@protonmail.com',

    cmdclass={
        'install': PostInstallCommand,
    },
    install_requires=['pyaml'],
    packages=['sfmclient'],
    data_files=[('/etc/sfmclient/', ['conf/config.yml']),
                ('/etc/systemd/user/',['conf/sfmclient.service'])],
    entry_points = {
        'console_scripts': [
            'sfmclient = sfmclient.main:main',
        ],              
    },
)
