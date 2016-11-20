#!/usr/bin/python

import sys
import os
from pwd import getpwnam


def print_usage():
  print("Usage:\n\
 ./build.py [options]\n\
\n\
Options:\n\
 clean		removes all binarys and generated files\n\
 clean-all	clean & remove all downloaded files too\n\
 rebuild	fresh run, without removing files")

def initialize():
  mkdir_n_owner(downloads_path, user_id, user_id)
  mkdir_n_owner(output_path, user_id, user_id)
  mkdir_n_owner(toolchain_path + 'mnt_eldk-iso', user_id, user_id)
  mkdir_n_owner(output_path + 'kernel', user_id, user_id)
  mkdir_n_owner(output_path + 'kernel/lib', user_id, user_id)
  mkdir_n_owner(output_path + 'kernel/lib/modules', user_id, user_id)
  mkdir_n_owner(rootfs_path + 'mnt_debootstrap', user_id, user_id)
  if(not os.path.isdir(gnublin_tools_path)):
    os.mkdir(gnublin_tools_path)

  subprocess.call(['apt-get', 'update'])
  install_packages(required_pkgs_build)
  install_packages(required_pkgs_rootfs)
  myprint("Initialize DONE!")


def setsh():
  if(eldk_version == '5.0'):
    p1 = toolchain_path + "armv5te/sysroots/i686-oesdk-linux/usr/bin/armv5te-linux-gnueabi/"
    p2 = toolchain_path + "armv5te/sysroots/i686-oesdk-linux/bin/armv5te-linux-gnueabi/"
  elif any(eldk_version in s for s in supported_eldk_versions):
    p1 = toolchain_path + "armv5te/sysroots/i686-eldk-linux/usr/bin/armv5te-linux-gnueabi/"
    p2 = toolchain_path + "armv5te/sysroots/i686-eldk-linux/bin/armv5te-linux-gnueabi/"

  os.environ["ARCH"] = "arm"
  os.environ["CROSS_COMPILE"] = "arm-linux-gnueabi-"
  os.environ["PATH"] = p1 + ":" + os.environ["PATH"]


def remove_stamps():
  os.chdir(root_path)
  silent_remove('.stamp_initialize')
  silent_remove('.stamp_toolchain')
  silent_remove('.stamp_bootloader')
  silent_remove('.stamp_kernel')
  
def clean():
  remove_stamps()
  silent_remove(output_path)
  silent_remove(bootloader_path + 'apex-1.6.8')
  subprocess.call(['umount', toolchain_path + 'mnt_eldk-iso'])
  silent_remove(toolchain_path + 'mnt_eldk-iso')
  subprocess.call(['umount', rootfs_path + 'mnt_debootstrap'])
  silent_remove(rootfs_path + 'mnt_debootstrap')

def clean_all():
  clean()
  silent_remove(toolchain_path + 'armv5te')
  silent_remove(downloads_path)
  silent_remove(kernel_path + 'gnublin-lpc3131-2.6.33')
  silent_remove(kernel_path + 'gnublin-lpc3131-3.3.0')


if __name__ == '__main__':
  runas = os.environ['USER']
  if(runas != 'root'):
    print("has to run as root!")
    raise SystemExit(99)

  if('gnublin-distribution/lpc3131' not in os.getcwd()):
    print("Please don't run the script from another location!")
    print("`cd` into the directory of the script to run it properly")
    print_usage()
    raise SystemExit(99)

  execfile('util.py')
  execfile('config.py')

  user = os.environ['SUDO_USER']
  user_id = getpwnam(user).pw_uid

  log = open(logfile, 'w')
  log.write('')
  log.close()

  if(len(sys.argv) > 1):
    if(sys.argv[1] == 'clean'):
      clean()
      print("Build Environment Successfully cleaned!")
      raise SystemExit(0)
    elif(sys.argv[1] == 'clean-all'):
      clean_all()
      print("Build Environment Successfully cleaned!")
      raise SystemExit(0)
    elif(sys.argv[1] == 'rebuild'):
      remove_stamps()
    else:
      print_usage()
      raise SystemExit(0)

  myprint("\n\
#############################################\n\
# 0th Stage: Initialize                     #\n\
#############################################")
  if(checkstamp('initialize')):
    myprint("Already Initialized at " + stamptime('initialize'))
    silent_remove(logfile)
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
    execfile(toolchain_path + 'toolchain.py')
    toolchain()
    makestamp('toolchain')

#############################################
  setsh() #Should always run! otherwise bootloader, kernel & rootfs are likely to fail.
#############################################

  myprint("\n\
#############################################\n\
# 2nd Stage: Bootloader                     #\n\
#############################################")
  if(checkstamp('bootloader')):
    myprint("Bootloader already build at " + stamptime('bootloader'))
  else:
    execfile(root_path + 'bootloader/apex.py')
    bootloader_apex()
    makestamp('bootloader')

  myprint("\n\
#############################################\n\
# 3rd Stage: Kernel                         #\n\
#############################################")
  if(checkstamp('kernel')):
    myprint("Kernel already build at " + stamptime('kernel'))
  else:
    execfile(kernel_path + 'kernel.py')
    kernel()
    makestamp('kernel')

  myprint("\n\
#############################################\n\
# 4rd Stage: Rootfs                         #\n\
#############################################")
  if(checkstamp('rootfs')):
    myprint("Rootfs already build at " + stamptime('rootfs'))
  else:
    execfile(rootfs_path + 'debian.py')
    rootfs_debian()

  myprint("\n\
#############################################\n\
# 5th Stage: Rootfs completion              #\n\
#############################################")
  if(checkstamp('rootfs_completion')):
    myprint("Rootfs completion already done at " + stamptime('rootfs_completion'))
  else:
    execfile(rootfs_path + 'rootfs_completion.py')
    rootfs_debian_completion()
