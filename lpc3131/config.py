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

required_pkgs_build	= ['make', 'g++', 'dpkg-dev', 'git', 'git-core', 'swig2.0', 'gawk']
# 'libncurses5-dev' #make-menuconfig

#############################################
# 1st Stage: Toolchain                      #
#############################################
#If you want to use your own Version of ELDK, you can set your Path here
custom_eldk_path	= ''

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
kernel_version	= '3.3.0' # Allowed values are '2.6.33' and '3.3.0'
repos_root_url	= 'git://github.com/zmint'
kernel_config	= 'gnublin_defconfig'

git_name_kernel	= 'gnublin-lpc3131-' + kernel_version
kernel_name	= 'linux-' + kernel_version + '-lpc313x'
std_kernel_pkg_name	= 'linux-' + kernel_version + '.tar.gz'

#############################################
# 4rd Stage: Rootfs                         #
#############################################
debian_target_version	= 'squeeze'
debian_mirror_url	= 'http://archive.debian.org/debian/'
#debian_mirror_url	= 'http://ftp.debian.org/debian/'
nameserver_addr	= '8.8.8.8'

rootfs_path	= root_path + 'rootfs/debian/'

image_fname	= 'debian_rootfs_gnublin.img'
image_fpath	= rootfs_path + image_fname
image_size	= '2048'
debootstrap_path= rootfs_path + 'mnt_debootstrap/'
filesystem_type	= 'ext3' #default ext4

#on host
required_pkgs_rootfs = ['debootstrap', 'binfmt-support', 'qemu-user-static', 'qemu', 'qemu-kvm', 'qemu-system', 'parted']

#on debootstrap
add_packages_max="php5 php5-cli php5-cgi gpsd gpsd-clients fswebcam uvccapture lm-sensors firmware-linux-free firmware-linux-nonfree firmware-realtek firmware-ralink firmware-linux firmware-brcm80211 firmware-atheros rcconf cgilib cgiemail cgi-mapserver lrzsz libnss-mdns libpam-modules nscd ssh libpcsclite1 libnl1 nfs-common tree lighttpd vsftpd rsync ruby git fakeroot libjpeg62-dev picocom tmux"

add_packages_base="i2c-tools makedev module-init-tools dhcp3-client netbase ifupdown iproute iputils-ping wget net-tools vim nano hdparm bzip2 p7zip unrar unzip zip p7zip-full screen less usbutils psmisc strace info ethtool wireless-tools wpasupplicant python rsyslog whois time procps perl parted build-essential ccache bison flex autoconf automake gcc libc6 cpp curl ftp gettext subversion lua50"
