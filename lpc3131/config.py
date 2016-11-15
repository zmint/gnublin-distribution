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
eldk_path	= '/opt/eldk-5.0/'
eldk_ftp	= 'ftp://ftp.denx.de/pub/eldk/5.0/iso/'
eldk_iso_fname	= 'armv5te-qte-5.0.iso'
eldk_hash_fname	= 'iso.sha256'


#############################################
# 2nd Stage: Bootloader                     #
#############################################
#bootloader	= 'apex'
bootloader_path	= root_path + 'bootloader/apex/1.6.8/'


#############################################
# 3rd Stage: Kernel                         #
#############################################
kernel_version	= '2.6.33'
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

