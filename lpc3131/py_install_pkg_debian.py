#!/usr/bin/python

from subprocess import STDOUT, check_call
import subprocess
import os

packages = ["make", "libncurses5-dev", "g++", "dpkg-dev", "git", "git-core", "swig2.0", "gawk"]

#check_call(['apt-get', 'install', '-y', packages]), stdout=open(os.devnull,'wb'), stderr=STDOUT) 
try:
    check_call(['apt-get', 'update']) 
except subprocess.CalledProcessError:
    print("are you root?")

for package in packages:
    try:
        check_call(['apt-get', 'install', '-y', package])
    except subprocess.CalledProcessError:
        print("are you root?")
