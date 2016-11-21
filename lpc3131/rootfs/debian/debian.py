#!/usr/bin/python

import subprocess
import tarfile
from shutil import copy2
from shutil import copytree

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
  subprocess.call(['mount', '-t', 'devpts', 'devpts', debootstrap_path + 'dev/pts'])
  subprocess.call(['mount', '-t', 'proc', 'proc', debootstrap_path + 'proc'])
  subprocess.call([rootfs_path + 'chroot_2.sh', debootstrap_path, add_packages, filesystem_type])


  subprocess.call(['umount', debootstrap_path + 'dev/pts'])
  subprocess.call(['umount', debootstrap_path + 'proc'])

  copy2(debootstrap_path + '/debootstrap_stage2.log', rootfs_path + 'debootstrap_stage2.log')
  myprint("Base debootstrap stage 2 DONE!")


def disable_mnt_tmpfs():
  myprint("Disable_mnt_tmpfs unimplemented")


def do_post_debootstrap_config():
  myprint("do_post_debootstrap_config incomplete. refusing further progress")
  return 1
  myprint("Starting post-debootstrap configuration")

  os.environ['use_ramzswap']=use_ramzswap
  os.environ['ramzswap_kernel_module_name']=ramzswap_kernel_module_name
  os.environ['ramzswap_size_kb']=ramzswap_size_kb
  os.environ['vm_swappiness']=ramzswap_vm_swappiness
  os.environ['i2c_hwclock']=i2c_hwclock
  os.environ['i2c_hwclock_name']=i2c_hwclock_name
  os.environ['i2c_hwclock_addr']=i2c_hwclock_addr
  os.environ['rtc_kernel_module_name']=rtc_kernel_module_name
  os.environ['additional_packages']=add_packages

  subprocess.call('./post_debootstrap_config.sh', debootstrap_path, 'post_debootstrap_errors.log')

  subprocess.call(['umount', debootstrap_path])

  tar = tarfile.open(output_path + std_kernel_pkg_name)
  tar.extractall(rootfs_path + 'tmp')
  tar.close()
  
  download(qemu_kernel_pkg_path + qemu_kernel_pkg_name, downloads_path + qemu_kernel_pkg_name)
  tar = tarfile.open(downloads_path + qemu_kernel_pkg_name)
  tar.extractall(rootfs_path + 'qemu-kernel')
  tar.close()

  myprint("Starting configuration in qemu environment now!")
#  proc = subprocess.Popen(['qemu-system-arm', '-M', 'versatilepb', '-cpu', 'arm926', '-no-reboot', 'kernel', rootfs_path + 'qemu-kernel/zImage', '-hda', image_fpath, '-m', '256', '-append', 'root=/dev/sda rootfstype=' + filesystem_type + ' mem=256M devtmpfs.mount=0 rw ip=dhcp'], stderr=subprocess.PIPE)
#  err = proc.communicate()
#qemu_log = open('qemu_error.log', 'w')
#qemu_log.write(err)
#qemu_log.close()


def rootfs_debian_completion():
  myprint("rootfs_debian_completion incomplete. refusing further progress")
  return 1
  working_dir = downloads_path + 'gnublin-api/'

  git_exists = os.path.isdir(working_dir)
  if(git_exists):
    os.chdir(working_dir)
    myprint("Cleaning gnublin-api dir")
    subprocess.call(['make', 'clean'])
    myprint("Updating gnublin-api Repo: " + gnublin_api)
    subprocess.call(['git', 'pull'])
  else:
    os.chdir(downloads_path)
    myprint("Getting Kernel Repo: " + gnublin_api)
    subprocess.call(['git', 'clone', gnublin_api])

  os.chdir(working_dir)
  subprocess.call(['make', 'release'])
  
  copytree(working_dir + 'deb/', gnublin_tools_path)
  
  #build .deb packages
  if(os.path.isdir(gnublin_package_path + 'deb')):
    silent_remove(gnublin_package_path + 'deb')
  mkdir_n_owner(gnublin_package_path + 'deb')

  os.chdir(gnublin_package_path + 'src')
  subprocess.call(['./mkdeb_package'])


def rootfs_debian():
  os.chdir(rootfs_path)

  create_img()

  subprocess.call(['mount', '-o', 'loop', image_fpath, debootstrap_path])

  myprint("Starting Debootstrap stage 1")
  subprocess.call(['debootstrap', '--verbose', '--arch', 'armel', '--variant=minbase', '--foreign', debian_target_version, debootstrap_path, debian_mirror_url])
  myprint("Base debootstrap stage 1 DONE!")

  debootstrap_stage2()

  disable_mnt_tmpfs()

  mkdir_n_owner(rootfs_path + 'tmp', user_id, user_id)
  do_post_debootstrap_config()
  rootfs_debian_completion()

  subprocess.call(['umount', debootstrap_path])

  return 0
