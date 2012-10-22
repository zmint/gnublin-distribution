#!/bin/bash
# Author: Benedikt Niedermayr (niedermayr@embedded-projects.net)
# Board support package building script



# Parameters 
distro_version="-max"    				#paste "-min" if you want to build a minimal version of debian.
									    #

 
#############
# Variables #
#############
build_time="$(date '+%D %H:%M:%S') ->"
root_path=$(pwd)
toolchain_path=$root_path/toolchain
cross_compiler_path=$toolchain_path/armv5te/sysroots/i686-oesdk-linux/usr/bin/armv5te-linux-gnueabi
kernel_version=2.6.33
kernel_name=linux-$kernel_version-lpc313x
kernel_path=$root_path/kernel/$kernel_name
debian_build_path=$root_path/rootfs/debian/debian_install
debian_installed_files_path=$root_path/rootfs/debian/debian_install/debian_process
bootloader_install_dir=$root_path/bootloader/apex/1.6.8
logfile_build=$root_path/install.log


##########################################################
# Only cleaning the whole board-support-package and exit #
##########################################################
if [ "$1" = "clean" ]
then
	rm -r $root_path/kernel/$kernel_name
	rm -r $debian_installed_files_path
	rm -r $bootloader_install_dir/apex-1.6.8
	rm -r $toolchain_path/armv5te
	rm -r $root_path/kernel/set.sh
	

	# Uninstall also the toolchain	
	if [ "$2" = "all" ]
	then	
		rm -r "/opt/eldk-*"
		rm -r "$root_path/Downloads"
	fi
	exit 0
fi




# Deciding Stage : In this stage all required/selected adons 
# will be added to the build process. 





# Building Stages
# Now the complete board support package will be built.
rm -r $logfile_build


#############################################
# 1st Stage:Build toolchain                 #
#############################################
if [ ! -e $root_path/.toolchain_done ]
then
	source $root_path/toolchain/build_toolchain.sh
	touch $root_path/.toolchain_done
fi



#############################################
# 2nd Stage:Build bootlader                 #
#############################################
if [ ! -e $root_path/.bootloader_done ]
then
	source $root_path/kernel/set.sh
	source $root_path/bootloader/apex/1.6.8/build_bootloader.sh
	touch $root_path/.bootloader_done
fi


######################################
# 3rd Stage: Kernel build		     # 
######################################
if [ ! -e $root_path/.kernel_done ]
then
	# Including settings through an additional file
	source $root_path/rootfs/debian/debian_install/general_settings.sh	"$distro_version"	 
	source $root_path/kernel/build_kernel.sh

	# Move set.sh file into the kernel
	cp $root_path/kernel/set.sh $kernel_path
	touch $root_path/.kernel_done
fi


######################################
# 4rd Stage: rootfs build		     # 
######################################
if [ ! -e $root_path/.rootfs_done ]
then
	source $root_path/rootfs/debian/debian_install/build_debian_system.sh 
	touch $root_path/.rootfs_done
fi





######################################
# 5th Stage: Rootfs completion  add  # 
######################################
# 2.Copy some important support files into the rootfs
#   (e.g. example applications(im home ordner),debian packages---->add to packages list???)


######################################
# 6th Stage: Rootfs completion remove# 
######################################

### Uninstall unimportant files out of the rootfs.
### (Avahi, samba, Documentation, ARCH, )
### Use a script which does that but at the first start of the BOARD and after that deinstall it!!!




######################################
# 6th Stage: Built Support package   # 
######################################
# --> Build support folder
#   (e.g. for how-to files,examles,source_code)
# --> Alles wenn möglich für den Gnblin installer komform machen!



######################################
# 7th Stage: Built Support package   # 
######################################
# --> User rights im Wiki nicht hier!!!
# --> Auf die CD einen Ordner mit einem Abbild dieser Struktur + alles fertig ordner(für die Oma)





