#!/usr/bin/python

import os
import urllib


def toolchain():
  eldk_installed = os.path.isdir(eldk_path)
  eldk_symlinked = os.path.isdir(toolchain_path + 'armv5te')

  if(eldk_installed and eldk_symlinked):
    myprint("Toolchain already installed and symlinked")
  elif(eldk_symlinked):
    silent_remove(toolchain_path + 'armv5te') #rm broken symlink
  elif(eldk_installed):
    myprint("Found " + eldk_path + " - Symlinking to working dir")
    os.symlink(eldk_path + 'armv5te', toolchain_path + 'armv5te')
    os.lchown(toolchain_path + 'armv5te', user_id, user_id)
  else:
    os.chdir(downloads_path)

    if(os.path.isfile(eldk_iso_fname)):
      myprint(eldk_iso_fname + " already downloaded")
    else:
      myprint("Downloading " + eldk_iso_fname)
      urllib.urlretrieve(eldk_ftp + eldk_iso_fname, eldk_iso_fname)
      myprint("Downloading " + eldk_hash_fname)
      urllib.urlretrieve(eldk_ftp + eldk_hash_fname, eldk_hash_fname)

    iso_hash = sha256(eldk_iso_fname)
    with open(eldk_hash_fname, 'rU') as f:
      checksum = f.read().rstrip() #remove trailing newline \n

    if(iso_hash != checksum):
      myprint("Checksum error: sha256sum of %s doesn't match %s" % (eldk_iso_fname, eldk_hash_fname))
      myprint("F A I L E D")
      raise SystemExit(0)
    else:
      myprint("sha256 Checksum of " + eldk_iso_fname + " is correct")

    # Mount and Install
    err = subprocess.call(['mount', downloads_path + eldk_iso_fname, toolchain_path + 'mnt_eldk-iso', '-o', 'loop'])

    subprocess.call([toolchain_path + 'mnt_eldk-iso/install.sh', '-s', '-i', 'qte', 'armv5te'])
    os.symlink(eldk_path + 'armv5te', toolchain_path + 'armv5te')
    os.lchown(toolchain_path + 'armv5te', user_id, user_id)
    subprocess.call(['umount', toolchain_path + 'mnt_eldk-iso'])

  myprint("Toolchain DONE!")
