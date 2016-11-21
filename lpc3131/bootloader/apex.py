#!/usr/bin/python

import os
import tarfile
import subprocess
from shutil import copy2


def bootloader_apex():
  if(os.path.isdir(bootloader_path + 'apex-1.6.8')):
    myprint('apex-1.6.8.tar.gz' + " has already been extracted earlier")
  else:
    tar = tarfile.open(bootloader_path + 'apex-1.6.8.tar.gz')
    tar.extractall(bootloader_path)
    tar.close()
    myprint('apex-1.6.8.tar.gz' + " extracted")

  #configure
  #todo: automatic change of .config file in apexfolder
  if(not ram == 32):
    myprint("Please set apex .config file correctly")
    myprint("Set 'CONFIG_RAM_SIZE_" + ram + "MB=y' and remove 'CONFIG_RAM_SIZE_32MB=y'")

  #make
  subprocess.call(['make', '-j', '8', '-C', bootloader_path + 'apex-1.6.8', 'apex.bin'])

  copy2(bootloader_path + 'apex-1.6.8/src/arch-arm/rom/apex.bin', output_path)
  os.chdir(output_path)
  apexmd5 = open('apex.bin.md5', 'w')
  apexmd5.write(md5('apex.bin') + '\n')
  apexmd5.close()
  myprint("Bootloader DONE!")
