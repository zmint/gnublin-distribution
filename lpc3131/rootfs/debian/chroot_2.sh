#!/bin/bash
#
#Usage:
# ./chroot_1.sh debootstrap_path debian_target_version nameserver_addr

if [ $# -ne 3 ]; then
  exit 1
fi

debootstrap_path=$1
additional_packages=$2
filesystem_vers=$3

logfile='/debootstrap_stage2.log'

/usr/sbin/chroot ${debootstrap_path} /bin/sh -c "
echo '### chroot_2.sh
### debootstrap path: $1
### install deb pkgs: $2
### filesystem vers : $3

' >>$logfile

export LANG=C 2>>$logfile
apt-get -y install apt-utils dialog locales manpages man-db 2>>$logfile

cat <<END > /etc/apt/apt.conf 2>>$logfile
APT::Install-Recommends \"0\";
APT::Install-Suggests \"0\";
END

apt-get -y -d install $additional_packages 2>>$logfile

sed -i 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/g' /etc/locale.gen 2>>$logfile	# enable locale
locale-gen 2>>$logfile

export LANG=en_US.UTF-8 2>>$logfile	# language settings
export LC_ALL=en_US.UTF-8 2>>$logfile
export LANGUAGE=en_US.UTF-8 2>>$logfile

cat <<END > /etc/fstab 2>>$logfile
# /etc/fstab: static file system information.
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
/dev/root	/				$filesystem_vers	noatime,errors=remount-ro  0	1
none		/proc/bus/usb	usbfs				defaults				   0	0
#/dev/mmcblk0p3	none		swap				defaults				   0	0
END

update-rc.d -f mountoverflowtmp remove 2>>$logfile
echo 'T0:2345:respawn:/sbin/getty -L ttyS0 115200 vt102' >> /etc/inittab 2>>$logfile	# disable virtual consoles
sed -i 's/^\([1-6]:.* tty[1-6]\)/#\1/' /etc/inittab 2>>$logfile

sync
exit" 2>./chroot_2.log
