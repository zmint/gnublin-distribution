#!/usr/bin/python

import subprocess
from shutil import copy2

def create_img():
  myprint("Creating Image file: " + image_fname)
  subprocess.call(['dd', 'if=/dev/zero', 'of=' + image_fpath, 'bs=1M', 'count=' + image_size])
  subprocess.call(['mkfs.ext3', '-F', image_fpath])


def debootstrap_stage2():
  myprint("Starting Debootstrap stage 2")
  subprocess.call(['modprobe', 'binfmt_misc'])
  copy2('/usr/bin/qemu-arm-static', debootstrap_path + 'usr/bin/')
  os.makedirs(debootstrap_path + 'dev/pts')


  myprint("Entering CHROOT_1 Environment now")
  subprocess.call(['mount', '-t', 'devpts', 'devpts', debootstrap_path + 'dev/pts'])
  subprocess.call(['mount', '-t', 'proc', 'proc', debootstrap_path + 'proc'])

  subprocess.call([rootfs_path + 'chroot_1.sh', debootstrap_path, debian_target_version, nameserver_addr])


  myprint("Entering CHROOT_2 Environment now")
  #todo: if min | max
  add_packages = add_packages_base
  subprocess.call(['mount', '-t', 'devpts', 'devpts', debootstrap_path + 'dev/pts'])
  subprocess.call(['mount', '-t', 'proc', 'proc', debootstrap_path + 'proc'])
  subprocess.call([rootfs_path + 'chroot_2.sh', debootstrap_path, add_packages, filesystem_type])


  subprocess.call(['umount', debootstrap_path + 'dev/pts'])
  subprocess.call(['umount', debootstrap_path + 'proc'])

  copy2(debootstrap_path + '/debootstrap_stage2.log', rootfs_path + 'debootstrap_stage2.log')
  myprint("Base debootstrap stage 2 DONE!")


def disable_mnt_tmpfs():
  myprint("Disable_mnt_tmpfs unimplemented")



def rootfs_debian():
  os.chdir(rootfs_path)

#  create_img()

  subprocess.call(['mount', '-o', 'loop', image_fpath, debootstrap_path])

#  myprint("Starting Debootstrap stage 1")
#  subprocess.call(['debootstrap', '--verbose', '--arch', 'armel', '--variant=minbase', '--foreign', debian_target_version, debootstrap_path, debian_mirror_url])
#  myprint("Base debootstrap stage 1 DONE!")

#  debootstrap_stage2()

#  disable_mnt_tmpfs()


  subprocess.call(['umount', debootstrap_path])
  return 0
