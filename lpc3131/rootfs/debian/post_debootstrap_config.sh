#!/bin/bash
#
#Usage:
# ./post_debootstrap_config.sh debootstrap_path logfile
#
#Following Environment Variables, should also be set: 
#  use_ramzswap
#  ramzswap_kernel_module_name
#  ramzswap_size_kb
#  vm_swappiness
#
#  i2c_hwclock
#  i2c_hwclock_name
#  i2c_hwclock_addr
#  rtc_kernel_module_name
#  additional_packages

if [ $# -ne 2 ]; then
  exit 1
fi


debootstrap_path=$1
logfile=${debootstrap_path}/$2

if [ "${use_ramzswap}" = "yes" ]
then
  echo "#!/bin/sh
cat <<END > /etc/rc.local 2>>/ramzswap_setup_errors.txt
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

modprobe ${ramzswap_kernel_module_name} num_devices=1 disksize_kb=${ramzswap_size_kb}
#swapon -p 100 /dev/ramzswap0
## Additional script for cleaning the rootfs from unused .deb packages -BN ##
/opt/first_boot.sh
mkswap swapfile
exit 0
END

exit 0" > ${debootstrap_path}/ramzswap_setup.sh
chmod +x ${debootstrap_path}/ramzswap_setup.sh
fi


echo "
########################################################
########################################################
## __      __     _                        _          ##
## \ \    / /___ | | __  ___  _ __   ___  | |_  ___   ##
##  \ \/\/ // -_)| |/ _|/ _ \| '  \ / -_) |  _|/ _ \  ##
##   \_/\_/ \___||_|\__|\___/|_|_|_|\___|  \__|\___/  ##
##     _____ _   _ _    _ ____  _      _____ _   _    ##
##    / ____| \ | | |  | |  _ \| |    |_   _| \ | |   ##
##   | |  __|  \| | |  | | |_) | |      | | |  \| |   ##
##   | | |_ | . \` | |  | |  _ <| |      | | | . \` |   ##
##   | |__| | |\  | |__| | |_) | |____ _| |_| |\  |   ##
##    \_____|_| \_|\____/|____/|______|_____|_| \_|   ##
##        _____         _      _                      ##
##       |  __ \       | |    (_)                     ##
##       | |  | |  ___ | |__   _   __ _  _ __         ##
##       | |  | | / _ \| '_ \ | | / _\` || '_ \        ##
##       | |__| ||  __/| |_) || || (_| || | | |       ##
##       |_____/  \___||_.__/ |_| \__,_||_| |_|       ##
##                                                    ##
########################################################
########################################################
" >> ${debootstrap_path}/etc/motd.tail


date_cur=`date` # needed further down as a very important part to circumvent the PAM Day0 change password problem

echo "#!/bin/sh

date -s \"${date_cur}\" 2>>$logfile	# set the system date to prevent PAM from exhibiting its nasty DAY0 forced password change
apt-get -y install ${additional_packages} 2>>$logfile && apt-get clean	# install the already downloaded packages

if [ "${i2c_hwclock}" = "yes" ]
then 
	update-rc.d -f i2c_hwclock.sh start 02 S . stop 07 0 6 . 2>>$logfile
fi

cat <<END > /sbin/hotplug 2>>$logfile	# entry for devices with firmware specifically
#!/bin/sh
HOTPLUG_FW_DIR=/lib/firmware
echo 1 > /sys/\\\${DEVPATH}/loading
cat \\\${HOTPLUG_FW_DIR}/\\\${FIRMWARE} > /sys/\\\${DEVPATH}/data
echo 0 > /sys/\\\${DEVPATH}/loading
END

chmod +x /sbin/hotplug

if [ "${use_ramzswap}" = "yes" ]
then
	echo vm.swappiness=${vm_swappiness} >> /etc/sysctl.conf
fi

if [ ! -z `grep setup.sh /etc/rc.local` ]
then
	cat <<END > /etc/rc.local 2>>$logfile
#!/bin/sh -e
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

exit 0
END
fi

sh -c \"echo 'root
root
' | passwd root\" 2>>$logfile
passwd -u root 2>>$logfile
passwd -x -1 root 2>>$logfile
passwd -w -1 root 2>>$logfile

ldconfig

reboot 2>>$logfile
exit 0" > ${debootstrap_path}/setup.sh
chmod +x ${debootstrap_path}/setup.sh


if [ "${i2c_hwclock}" = "yes" ]
then
	echo "Setting up a script for being able to use the i2c-connected RTC (hardware clock)."
	echo "#!/bin/sh
### BEGIN INIT INFO
# Provides:          i2c-hwclock
# Required-Start:    checkroot
# Required-Stop:     $local_fs
# Default-Start:     S
# Default-Stop:      0 6
### END INIT INFO

case \"\$1\" in
	start)
	if [ ! -e /dev/rtc0 ]
	then
		mknod /dev/rtc0 c 254 0
	else
		if [ ! -e /dev/rtc ]
		then
			ln -s /dev/rtc0 /dev/rtc
		fi
	fi
	modprobe i2c-pnx
	modprobe ${rtc_kernel_module_name}
	echo ${i2c_hwclock_name} ${i2c_hwclock_addr} > /sys/bus/i2c/devices/i2c-1/new_device
	/sbin/hwclock -s && echo \"Time successfully set from the RTC!\"
	;;
	stop|restart|reload|force-reload)
	#echo ${i2c_hwclock_name} ${i2c_hwclock_addr} > /sys/bus/i2c/devices/i2c-1/delete_device
	#modprobe -r rtc-ds1307
	#modprobe -r i2c-pnx
	;;
	*)
	    echo \"Usage: i2c_hwclock.sh {start|stop}\"
	    echo \"       start sets up kernel i2c-system for using the i2c-connected hardware (RTC) clock\"
	    echo \"       stop unloads the driver module for the hardware (RTC) clock\"
	    return 1
	;;
    esac
exit 0" > ${debootstrap_path}/etc/init.d/i2c_hwclock.sh
  chmod +x ${debootstrap_path}/etc/init.d/i2c_hwclock.sh
else
  echo "No RTC (hardware clock) setup. Continueing..."
fi
