#!/usr/bin/python

import os
import tarfile
import subprocess
from shutil import copy2


def kernel():
  working_dir = kernel_path + git_name_kernel + '/' + kernel_name + '/'

  #get kernel repo
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
  silent_remove(output_path + 'kernel/lib/modules')
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
