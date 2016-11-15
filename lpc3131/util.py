#!/usr/bin/python

import time
import hashlib

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

# based on
# http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def sha256(fname):
  hash_sha256 = hashlib.sha256()
  with open(fname, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_sha256.update(chunk)
  return hash_sha256.hexdigest() + '  ' + fname

def md5(fname):
  hash_md5 = hashlib.md5()
  with open(fname, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest() + '  ' + fname
