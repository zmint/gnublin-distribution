#!/usr/bin/python

import subprocess
import os
import copytree from shutil

def rootfs_debian_completion():
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
    subprocess.call(['git', 'clone', gnublin_api)

  os.chdir(working_dir)
  subprocess.call(['make', 'release'])
  
  copytree(working_dir + 'deb/', gnublin_tools_path)
  
  #build .deb packages
  if(os.path.isdir(gnublin_package_path + 'deb'):
    silent_remove(gnublin_package_path + 'deb')
  mkdir_n_owner(gnublin_package_path + 'deb')

  os.chdir(gnublin_package_path + 'src')
  subprocess.call(['./mkdeb_package'])

  
