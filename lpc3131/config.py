#!/usr/bin/python

#############################################
# G N U B L I N   B O A R D                 #
#############################################
ram	= 32 #bit

#############################################
# Diverse Build Settings
#############################################
parallel_jobs	= '8'


#############################################
# Build script configuration
#############################################
root_path	= os.getcwd() + '/'

toolchain_path	= root_path + 'toolchain/'
downloads_path	= root_path + 'Downloads/'
output_path	= root_path + 'output/'
kernel_path	= root_path + 'kernel/'

logfile		= root_path + 'installpy.log'


#############################################
# 1st Stage: Toolchain                      #
#############################################
eldk_version	= '5.0'
eldk_path	= '/opt/eldk-' + eldk_version + '/'
eldk_ftp	= 'ftp://ftp.denx.de/pub/eldk/' + eldk_version + '/iso/'
eldk_hash_fname	= 'iso.sha256'

supported_eldk_versions = ['5.1', '5.2', '5.2.1', '5.3', '5.4', '5.5', '5.5.2', '5.5.3', '5.6']

if(eldk_version == '5.0'):
  eldk_iso_fname	= 'armv5te-qte-5.0.iso'
elif any(eldk_version in s for s in supported_eldk_versions):
  eldk_iso_fname	= 'eldk-' + eldk_version + '-armv5te.iso'
else:
  myprint("COULD FAIL! - Unknown eldk version, assuming they keep naming convention")
  eldk_iso_fname	= 'eldk-' + eldk_version + '-armv5te.iso'


#############################################
# 2nd Stage: Bootloader                     #
#############################################
#bootloader	= 'apex'
bootloader_path	= root_path + 'bootloader/apex/1.6.8/'


#############################################
# 3rd Stage: Kernel                         #
#############################################
#kernel_version	= '2.6.33'
kernel_version	= '3.3.0'
repos_root_url	= 'git://github.com/zmint'
kernel_config	= 'gnublin_defconfig'
#kernel_config	= 'gnublin_jessie_defconfig'

git_name_kernel	= 'gnublin-lpc3131-' + kernel_version
kernel_name	= 'linux-' + kernel_version + '-lpc313x'
std_kernel_pkg_name	= 'linux-' + kernel_version + '.tar.gz'

#############################################
# 4rd Stage: Rootfs                         #
#############################################
apt_prerequisites = 'debootstrap binfmt-support qemu-user-static qemu qemu-kvm qemu-system parted'

