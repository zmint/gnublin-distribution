#!/bin/bash
# Author: Ingmar Klein (ingmar.klein@hs-augsburg.de)
# Edit: Benedikt Niedermayr


# pre build script for installing the rootfilesystem inclusive the GNUBLIN kernel.
# It contains some very important settings.

cur_path=$(pwd)

nameserver_addr="192.168.2.1" # "141.82.48.1" (YOU NEED TO EDIT THIS!)

# where to get the standard kernel #kernel_pkg_path="${HOME}/gnublin/built_kernels"
std_kernel_pkg_path="$cur_path/debian_process"                                    

# where to get the qemu kernel
qemu_kernel_pkg_path="http://www.hs-augsburg.de/~ingmar_k/gnublin/kernels/2.6.33"  

# where to put the files in general (YOU NEED TO EDIT THIS!)
output_dir_base="$cur_path/debian_process"                                 

std_kernel_pkg_name="linux-2.6.33.tar.gz" # standard kernel file name

#Kernel package name before compression
default_kernel_pkg_name="linux-2.6.33-lpc313x"


#Kernel build variables
export ARCH=arm
export CROSS_COMPILE=arm-unknown-linux-uclibcgnueabi-
export PATH=$PATH:/home/brenson/gnublin-buildroot-git/buildroot-2011.11/output/host/usr/bin







if [ ! -d "$cur_path/debian_process" ]
then
	mkdir $cur_path/debian_process
	
	echo "installation folder $cur_path/debian_process created"
fi

if [ ! -e "$cur_path/debian_process/linux-2.6.33.tar.gz" ]
then
        #Copy std. kernel to installation folder
	cp -rp $cur_path/../../../kernel/$default_kernel_pkg_name $cur_path/debian_process
	cp -rp $cur_path/../../../kernel/patches $cur_path/debian_process
	
        #install patches on it
	cd $cur_path/debian_process/patches/
	source install_patches.sh
	cd -
	
	cd $cur_path/debian_process/$default_kernel_pkg_name/
	cp -p config_backup .config
	#############FEHLER: DA WARSCHEINLICH NOCH KEIN KERNEL ZIMAGE VORHANDEN################
	

	#gnublin kernel build process
	
	make zImage
	make modules
	make modules_install INSTALL_MOD_PATH=$cur_path/debian_process/$default_kernel_pkg_name
        
	tar -zc -f $cur_path/debian_process/$std_kernel_pkg_name *
	cd $cur_path
	#cp -rpv $cur_path/$std_kernel_pkg_name $cur_path/debian_process
fi




#############################
##### GENERAL SETTINGS: #####
#############################

host_os="Ubuntu" # Debian or Ubuntu (YOU NEED TO EDIT THIS!)

debian_mirror_url="http://ftp.debian.org/debian/" # mirror for debian

debian_target_version="squeeze" # The version of debian that you want to build (ATM, 'squeeze', 'wheezy' and 'sid' are supported)

 # http: ... for getting the kernel package online, or a local directory for getting it off your hdd

 



qemu_kernel_pkg_name="kernel_2.6.33-gnublin-qemu-1.2_1335647673.tar.bz2" # qemu kernel file name



bootloader_bin_path="http://www.hs-augsburg.de/~ingmar_k/gnublin/bootloader" # where to get the bootloader

bootloader_bin_name="apex.bin" # bootloader binary

tar_format="gz" # bz2(=bzip2) or gz(=gzip)



output_dir="${output_dir_base}/build_`date +%s`" # Subdirectory for each build-run, ending with the unified Unix-Timestamp (seconds passed since Jan 01 1970)

work_image_size_MB=4096 # size of the temporary image file, in which the installation process is carried out

output_filename="debian_rootfs_gnublin" # base name of the output file (compressed rootfs)

apt_prerequisites_debian="debootstrap binfmt-support qemu-user-static qemu qemu-kvm qemu-system parted" # packages needed for the build process on debian

apt_prerequisites_ubuntu="debootstrap binfmt-support qemu qemu-system qemu-kvm qemu-kvm-extras-static parted" # packages needed for the build process on ubuntu

clean_tmp_files="no" # delete the temporary files, when the build process is done?

create_disk="no" # create a bootable SD-card after building the rootfs?



###################################
##### CONFIGURATION SETTINGS: #####
###################################



use_ramzswap="no" # set if you want to use a compressed SWAP space in RAM (can potentionally improve performance)

ramzswap_size_kb="3072" # size of the ramzswap device in KB

ramzswap_kernel_module_name="ramzswap" # name of the ramzswap kernel module (could have a different name on newer kernel versions)

vm_swappiness="100" # Setting for general kernel RAM swappiness: With RAMzswap and low RAM, a high number (like 100) could be good. Default in Linux mostly is 60.

i2c_hwclock="no" # say "yes" here, if you connected a RTC to your gnublin board, otherwise say "no"

i2c_hwclock_name="ds1307" # name of the hardware RTC (if one is connected)

i2c_hwclock_addr="0x68" # hardware address of the RTC (if one is connected)

rtc_kernel_module_name="rtc-ds1307" # kernel module name of the hardware RTC (if one is connected)

additional_packages="makedev i2c-tools module-init-tools dhcp3-client netbase ifupdown iproute iputils-ping wget net-tools vim nano hdparm rsync bzip2 p7zip unrar unzip zip p7zip-full screen less usbutils psmisc strace info ethtool wireless-tools python rsyslog whois time ruby procps perl parted build-essential ccache bison flex autoconf automake gcc libc6 cpp curl fakeroot ftp gettext git subversion lm-sensors firmware-linux-free firmware-linux-nonfree firmware-realtek firmware-ralink firmware-linux firmware-brcm80211 firmware-atheros rcconf cgilib cgiemail cgi-mapserver lrzsz libnss-mdns libpam-modules nscd ssh wpasupplicant libpcsclite1 libnl1" # IMPORTANT NOTE: All package names need to be seperated by a single space
