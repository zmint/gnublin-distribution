#!/usr/bin/python

#############################################
# G N U B L I N   B O A R D                 #
#############################################
ram	= 32 #bit

### RTC
i2c_hwclock			= 'no' #set 'yes', if your Gnublin Board has a RTC connected
i2c_hwclock_name	= 'ds1307'
i2c_hwclock_addr	= '0x68'
rtc_kernel_module_name	= 'rtc-ds1037'

### RAMZSWAP
use_ramzswap	= 'no' #set 'yes' if you want to use a compressed SWAP space in RAM
ramzswap_size_kb			= '3072'
ramzswap_vm_swappiness		= '60'
ramzswap_kernel_module_name	= 'ramzswap'

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


qemu_kernel_pkg_path	= 'http://elk.informatik.fh-augsburg.de/pub/Gnublin/'
qemu_kernel_pkg_name	= 'kernel_2.6.33-gnublin-qemu-1.2_1335647673.tar.bz2'

#############################################
# 4rd Stage: Rootfs                         #
#############################################
debian_target_version	= 'squeeze'
debian_distr_version	= 'min'		#allowed: 'min' and 'max'
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
add_packages_base="i2c-tools makedev module-init-tools dhcp3-client netbase ifupdown iproute iputils-ping wget net-tools vim nano hdparm bzip2 p7zip unrar unzip zip p7zip-full screen less usbutils psmisc strace info ethtool wireless-tools wpasupplicant python rsyslog whois time procps perl parted build-essential ccache bison flex autoconf automake gcc libc6 cpp curl ftp gettext subversion lua50"
add_packages_max="php5 php5-cli php5-cgi gpsd gpsd-clients fswebcam uvccapture lm-sensors firmware-linux-free firmware-linux-nonfree firmware-realtek firmware-ralink firmware-linux firmware-brcm80211 firmware-atheros rcconf cgilib cgiemail cgi-mapserver lrzsz libnss-mdns libpam-modules nscd ssh libpcsclite1 libnl1 nfs-common tree lighttpd vsftpd rsync ruby git fakeroot libjpeg62-dev picocom tmux"



#todo: if min | max
if(debian_distr_version == 'min'):
  add_packages = add_packages_base
elif(debian_distr_version == 'max'):
  add_packages = add_packages_base + ' ' + add_packages_max

#############################################
# 5th Stage: Rootfs completion              #
#############################################
gnublin_api		= 'https://github.com/embeddedprojects/gnublin-api.git'
gnublin_package_path	= root_path + 'gnublin_package/'
gnublin_tools_path		= gnublin_package_path + 'src/gnublin-tools/'
