#!/bin/bash
#
#Usage:
# ./chroot_1.sh debootstrap_path debian_target_version nameserver_addr

if [ $# -ne 3 ]; then
  exit 1
fi

debootstrap_path=$1
debian_target_version=$2
nameserver_addr=$3

logfile='/debootstrap_stage2.log'

/usr/sbin/chroot ${debootstrap_path} /bin/bash -c "
echo '### chroot_1.sh
### debootstrap path: $1
### debian version  : $2
### nameserver addr : $3

' >>$logfile

/debootstrap/debootstrap --second-stage 2>>$logfile

if [ $debian_target_version == 'squeeze' ];
then
cat <<END > /etc/apt/sources.list 2>>$logfile
deb http://archive.debian.org/debian ${debian_target_version} main contrib non-free
deb-src http://archive.debian.org/debian ${debian_target_version} main contrib non-free
deb http://archive.debian.org/debian-security ${debian_target_version}/updates main contrib non-free
deb-src http://archive.debian.org/debian-security ${debian_target_version}/updates main contrib non-free
END
else
cat <<END > /etc/apt/sources.list 2>>$logfile
deb http://ftp.de.debian.org/debian ${debian_target_version} main contrib non-free
deb-src http://ftp.de.debian.org/debian ${debian_target_version} main contrib non-free
deb http://ftp.debian.org/debian/ ${debian_target_version}-updates main contrib non-free
deb-src http://ftp.debian.org/debian/ ${debian_target_version}-updates main contrib non-free
deb http://security.debian.org/ ${debian_target_version}/updates main contrib non-free
deb-src http://security.debian.org/ ${debian_target_version}/updates main contrib non-free
END
fi

apt-get update


mkdir -p /dev/bus/usb/001/
for k in {0..9}; do mknod /dev/bus/usb/001/0\${k} c 189 \${k}; done;
for l in {10..31}; do mknod /dev/bus/usb/001/0\${l} c 189 \${l}; done;
mknod /dev/i2c-0 c 89 0
mknod /dev/i2c-1 c 89 1
mknod /dev/ttyS0 c 4 64	# for the serial console
mknod /dev/rtc0 c 254 0
mknod /dev/ramzswap0 b 254 0
mknod -m 0666 /dev/mmcblk0p1 b 179 1
mknod -m 0666 /dev/mmcblk0p2 b 179 2
mknod -m 0666 /dev/mmcblk0p3 b 179 3	# SWAP
mknod /dev/sda b 8 0	# SCSI storage device
mknod /dev/sda1 b 8 1
mknod /dev/sda2 b 8 2
mknod /dev/sda3 b 8 3
mknod /dev/spi0 c 153 0
mknod /dev/video0 c 81 0
mknod /dev/ttyACM0 c 166 0
mknod /dev/pca9555 c 89 1

ln -s /dev/rtc0 /dev/rtc


cat <<END > /etc/network/interfaces
auto lo eth0
iface lo inet loopback
iface eth0 inet dhcp
END


echo gnublin > /etc/hostname 2>>$logfile
echo \"127.0.0.1 localhost\" >> /etc/hosts 2>>$logfile
echo \"127.0.0.1 gnublin\" >> /etc/hosts 2>>$logfile
echo \"nameserver ${nameserver_addr}\" > /etc/resolv.conf 2>>$logfile

cat <<END > /etc/rc.local 2>>$logfile
#!/bin/sh 
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will exit 0 on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

if [ -e /ramzswap_setup.sh ]
then
	/ramzswap_setup.sh 2>/ramzswap_setup_log.txt && rm /ramzswap_setup.sh
fi
/setup.sh 2>/setup_log.txt && rm /setup.sh

## Additional script for cleaning the rootfs from unused .deb packages -BN ##
/opt/first_boot.sh
mkswap swapfile
exit 0
END
exit" 2>./chroot_1.log
