#!/usr/bin/python

import time
import hashlib
import subprocess
import os, errno
import urllib
from shutil import rmtree

def myprint(message):
  print("###  " + message)
  log = open(logfile, 'a')
  log.write(message + '\n')
  log.close()

def gettime():
    return time.strftime("%m/%d/%Y %H:%M")

def makestamp(name):
  stampfile = open(root_path + '.stamp_' + name, 'w')
  stampfile.write(gettime())
  stampfile.close()

def stamptime(name):
  with open('.stamp_' + name, "r") as f:
    return f.readline()

def checkstamp(name):
  return os.path.isfile(root_path + '.stamp_' + name)

def mkdir_n_owner(path, uid, gid):
  if(not os.path.isdir(path)):
    os.mkdir(path)
    os.chown(path, uid, gid)

def silent_remove(path):
  if(os.path.islink(path) or os.path.isfile(path)):
    try:
      os.remove(path)
    except OSError as e:
      if e.errno != errno.ENOENT:
        raise

  if(os.path.isdir(path)):
    try:
      rmtree(path)
    except OSError as e:
      if e.errno != errno.ENOENT:
        raise

def download(url, filename):
  myprint("Downloading " + url)
  if(os.path.exists(filename)):
    myprint(filename + " already downloaded")
  else:
    try:
      urllib.urlretrieve(url, filename)
    except:
      myprint("Error while Downloading " + url + " to " + filename)
      return 99
    myprint("Successfully downloaded file to " + filename)


def install_packages(packages):
  for package in packages:
    try:
      subprocess.check_call(['apt-get', 'install', '-y', package])
    except subprocess.CalledProcessError as e:
      myprint("Couldn't install Package. " + package + " not found.")


def sha256_check(fname):
  err = subprocess.call(['sha256sum', '-c', '--ignore-missing', fname])
  if(err):
    err = subprocess.call(['sha256sum', '-c', fname])
  return err

# based on
# http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def md5(fname):
  hash_md5 = hashlib.md5()
  with open(fname, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest() + '  ' + fname
