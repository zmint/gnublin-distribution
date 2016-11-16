#!/usr/bin/python

import os
from pwd import getpwnam
import urllib
import subprocess
import sh
import tarfile
from shutil import copy2
from shutil import rmtree

def initialize():
  mkdir_n_owner(downloads_path, user_id, user_id)
  mkdir_n_owner(output_path, user_id, user_id)
  mkdir_n_owner(toolchain_path + 'mnt_eldk-iso', user_id, user_id)
  mkdir_n_owner(output_path + 'kernel', user_id, user_id)
  mkdir_n_owner(output_path + 'kernel/lib', user_id, user_id)
  mkdir_n_owner(output_path + 'kernel/lib/modules', user_id, user_id)

  myprint("Initialize DONE!")


def toolchain():
  eldk = os.path.isdir(eldk_path)

  if(os.path.isdir(toolchain_path + 'armv5te')):
    myprint("Toolchain already installed and symlinked")
  elif(eldk):
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
    a=  subprocess.call(['mount', downloads_path + eldk_iso_fname, toolchain_path + 'mnt_eldk-iso'])

    subprocess.call([toolchain_path + 'mnt_eldk-iso/install.sh', '-s', '-i', 'qte', 'armv5te'])#, stderr=log)
    os.symlink(eldk_path + 'armv5te', toolchain_path + 'armv5te')
    os.lchown(toolchain_path + 'armv5te', user_id, user_id)
    subprocess.call(['umount', toolchain_path + 'mnt_eldk-iso'])

  myprint("Toolchain DONE!")


def setsh():
  if(eldk_version == '5.0'):
    p1 = toolchain_path + "armv5te/sysroots/i686-oesdk-linux/usr/bin/armv5te-linux-gnueabi/"
#    p2 = ""
  elif any(eldk_version in s for s in supported_eldk_versions):
    p1 = toolchain_path + "armv5te/sysroots/i686-eldk-linux/usr/bin/armv5te-linux-gnueabi/"
#    p2 = toolchain_path + "armv5te/sysroots/i686-eldk-linux/bin/armv5te-linux-gnueabi/"

  os.environ["ARCH"] = "arm"
  os.environ["CROSS_COMPILE"] = "arm-linux-gnueabi-"
  os.environ["PATH"] = p1 + ":" + os.environ["PATH"]


def bootloader_apex():
  if(os.path.isdir(bootloader_path + 'apex-1.6.8')):
    myprint('apex-1.6.8.tar.gz' + " has already been extracted earlier")
  else:
    tar = tarfile.open(bootloader_path + 'apex-1.6.8.tar.gz')
    tar.extractall(bootloader_path)
    tar.close()
    myprint('apex-1.6.8.tar.gz' + " extracted")

  #configure
  #todo: change .config file in apexfolder
  #if(ram == 32)
  #  apex_ram = "CONFIG_RAM_SIZE_32MB=y"

  #make
  subprocess.call(['make', '-j', '8', '-C', bootloader_path + 'apex-1.6.8', 'apex.bin'])
#  myprint("apex.bin build successfully.")

  copy2(bootloader_path + 'apex-1.6.8/src/arch-arm/rom/apex.bin', output_path)
  os.chdir(output_path)
  apexmd5 = open('apex.bin.md5', 'w')
  apexmd5.write(md5('apex.bin') + '\n')
  apexmd5.close()
  myprint("Bootloader DONE!")
  

def kernel():
  working_dir = kernel_path + git_name_kernel + '/' + kernel_name + '/'

  #getting kernel repo
  git_exists = os.path.isdir(working_dir)
  if(git_exists):
    os.chdir(working_dir)
    myprint("Cleaning Kernel dir")
    subprocess.call(['make', 'clean'])
    myprint("Updating Kernel Repo: " + repos_root_url + '/' + git_name_kernel)
    subprocess.call(['git', 'pull'])
  else:
    os.chdir(kernel_path)
    myprint("Getting Kernel Repo: " + repos_root_url + '/' + git_name_kernel)
    subprocess.call(['git', 'clone', repos_root_url + '/' + git_name_kernel])

  os.chdir(working_dir)

  myprint("Configure Kernel with " + kernel_config)
  subprocess.call(['make', kernel_config])
  myprint("`make " + kernel_config + "` DONE")

  myprint("Building zImage")
  subprocess.call(['make', '-j', parallel_jobs, 'zImage'])
  myprint("`make zImage` DONE")

  myprint("Building modules")
  subprocess.call(['make', '-j', parallel_jobs, 'modules'])
  myprint("`make modules` DONE")

  # wipe old modules
  rmtree(output_path + 'kernel/lib/modules')
  mkdir_n_owner(output_path + 'kernel/lib/modules', user_id, user_id)

  myprint("Installing kernel modules (make modules_install)")
  subprocess.call(['make', '-j', parallel_jobs, 'modules_install', 'INSTALL_MOD_PATH=' + output_path + 'kernel'])
  myprint("`make modules_install` DONE")

  # copy to output
  copy2(working_dir + 'arch/arm/boot/zImage', output_path + 'kernel')

  # compress kernel
  myprint("Compressing Kernel to " + output_path + std_kernel_pkg_name)
  tar = tarfile.open(output_path + std_kernel_pkg_name, 'w:gz')
  os.chdir(working_dir)
  tar.add('.config', arcname='kernel_' + kernel_version + '-gnublin-std.config')
  os.chdir(output_path + 'kernel/')
  tar.add('lib')
  tar.add('zImage')
  tar.close()
  myprint("Compressing Kernel DONE")

  os.chdir(output_path)
  kernelmd5 = open(std_kernel_pkg_name + '.md5', 'w')
  kernelmd5.write(md5(std_kernel_pkg_name) + '\n')
  kernelmd5.close()
  
  return 0


def rootfs():
  myprint("unimplemented")
  return 0

def clean():
  rmtree(downloads_path)
  rmtree(output_path)
  rmtree(toolchain_path + 'mnt_eldk-iso')




if __name__ == '__main__':
  runas = os.environ['USER']
  if(runas != 'root'):
    myprint("has to run as root!")
    raise SystemExit(0)

  execfile('util.py')
  execfile('config.py')

  user = os.environ['SUDO_USER']
  user_id = getpwnam(user).pw_uid

  log = open(logfile, 'w')
  log.write('')
  log.close()

  myprint("\n\
#############################################\n\
# 0th Stage: Initialize                     #\n\
#############################################")
  if(checkstamp('initialize')):
    myprint("Already Initialized at " + stamptime('initialize'))
    os.remove(logfile)
    log = open(logfile, 'a')
  else:
    initialize()
    makestamp('initialize')

  myprint("\n\
#############################################\n\
# 1st Stage: Toolchain                      #\n\
#############################################")
  if(checkstamp('toolchain')):
    myprint("Toolchain already build at " + stamptime('toolchain'))
  else:
    toolchain()
    makestamp('toolchain')

#############################################
  setsh() #Should always run! otherwise bootloader & kernel are likely to fail.
#############################################

  myprint("\n\
#############################################\n\
# 2nd Stage: Bootloader                     #\n\
#############################################")
  if(checkstamp('bootloader')):
    myprint("Bootloader already build at " + stamptime('bootloader'))
  else:
    bootloader_apex()
    makestamp('bootloader')

  myprint("\n\
#############################################\n\
# 3rd Stage: Kernel                         #\n\
#############################################")
  if(checkstamp('kernel')):
    myprint("Kernel already build at " + stamptime('kernel'))
  else:
    kernel()

  myprint("\n\
#############################################\n\
# 4rd Stage: Rootfs                         #\n\
#############################################")
  if(checkstamp('rootfs')):
    myprint("Rootfs already build at " + stamptime('rootfs'))
  else:
    rootfs()
