#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

#meta layers
SRC_META_RDK_VIDEO="https://code.rdkcentral.com/r/rdk/components/generic/rdk-oe/meta-rdk-video"

#Git repositories
SRC_CURL="https://curl.se/download/curl-7.82.0.tar.xz"
SRC_JSONRPC="https://github.com/cinemast/libjson-rpc-cpp.git"
SRC_JSONCPP="https://github.com/open-source-parsers/jsoncpp/archive/refs/tags/1.8.4.tar.gz"
SRC_TINYXML2="https://github.com/leethomason/tinyxml2.git"
SRC_TDK="https://code.rdkcentral.com/r/rdkv/tools/tdkv"
SRC_ZLIB="https://sourceforge.net/projects/libpng/files/zlib/1.2.11/zlib-1.2.11.tar.xz"

#HAL source
#SRC_WIFI="https://github.com/rdkcentral/rdkv-halif-wifi.git"
SRC_WIFI="https://code.rdkcentral.com/r/rdk/components/generic/wifi"
SRC_POWERMGR_HAL="https://github.com/rdkcentral/rdk-halif-power_manager.git"
SRC_DEEPSLEEP_HAL="https://github.com/rdkcentral/rdk-halif-deepsleep_manager.git"
SRC_DS_HAL="https://github.com/rdkcentral/rdk-halif-device_settings.git"
SRC_HDMICEC_HAL="https://github.com/rdkcentral/rdk-halif-hdmi_cec.git"
SRC_BLUETOOTH_HAL="https://code.rdkcentral.com/r/rdk/components/generic/bluetooth"
SRC_IARMMGRS="https://code.rdkcentral.com/r/rdk/components/generic/iarmmgrs"
#SRC_IARMMGRS="git@github.com:rdk-e/iarmmgrs.git"
SRC_WESTEROS="https://code.rdkcentral.com/r/components/opensource/westeros"
SRC_EGL="https://github.com/KhronosGroup/EGL-Registry.git"
SRC_RMF_AUDIO_CAPTURE="https://github.com/rdkcentral/rdk-halif-rmf_audio_capture.git"
SRC_STORAGE_MGR="https://code.rdkcentral.com/r/rdk/components/generic/storagemanager"
#SRC_STORAGE_MGR="git@github.com:rdk-e/storagemanager.git"
SRC_NETSRVMGR="https://code.rdkcentral.com/r/rdk/components/generic/netsrvmgr"
#SRC_NETSRVMGR="git@github.com:rdk-e/netsrvmgr.git"
SRC_HDMICEC="https://code.rdkcentral.com/r/rdk/components/generic/hdmicec"
#SRC_HDMICEC="git@github.com:rdk-e/hdmicec.git"
SRC_IARMBUS="https://code.rdkcentral.com/r/rdk/components/generic/iarmbus"
#SRC_IARMBUS="git@github.com:rdk-e/iarmbus.git"
SRC_XKBCOMMON="http://xkbcommon.org/download/libxkbcommon-0.5.0.tar.xz"
SRC_DS="https://code.rdkcentral.com/r/rdk/components/generic/devicesettings"
SRC_CJSON="https://github.com/DaveGamble/cJSON.git"
SRC_UTIL_LINUX="https://github.com/util-linux/util-linux.git"
SRC_RDKFWUPDATER="https://github.com/rdkcentral/rdkfwupdater.git"
SRC_COMMONUTILITIES="https://github.com/rdkcentral/common_utilities.git"
SRC_LIBSYSWRAPPER="https://github.com/rdk-e/libSyscallWrapper.git"
SRC_MIDDLEWARE_SUPPORT="https://github.com/rdk-e/meta-middleware-generic-support.git"
SRC_RDKLOGGER="https://github.com/rdkcentral/rdk_logger.git"

#Platformwise repositories
SRC_RPI="https://code.rdkcentral.com/r/rdk/devices/raspberrypi/tdk"

#Source Directory names
DIR_MHD="libmicrohttpd-0.9.70"
DIR_HIREDIS="hiredis-0.14.0"
DIR_ARGTABLE="argtable2-2.13"
DIR_JSONRPC="libjson-rpc-cpp"
DIR_CURL="curl-7.82.0"
DIR_JSONCPP="jsoncpp-1.8.4"
DIR_TINYXML2="tinyxml2"
DIR_XKBCOMMON="libxkbcommon-0.5.0"
DIR_ZLIB="zlib-1.2.11"
DIR_TDK="tdkv"

ROOT_DIR=$PWD
mkdir -p logs
mkdir -p json_temp
TDK_SOURCE_DIR=${ROOT_DIR}/${DIR_TDK}
COMPILE_SKELETON=false
SYSROOT=${ROOT_DIR}/sysroots
SKIP_PLATFORM="FALSE"
SKIP_PACKAGES="TRUE"

config=configure.txt
. $config

platform_arg=false
for arg in "$@"
do
    case $arg in
        platform=*)
            PLATFORM="${arg#*=}" # Extract the value after 'platform='
	    platform_arg=true
            ;;
    esac
done

PLATFORM_GIVEN=$1
if [[ "$PLATFORM_GIVEN" == "AMLOGIC" ]];then
    PLATFORM="AMLOGIC"
elif [[ "$PLATFORM_GIVEN" == "BROADCOM" ]];then
    PLATFORM="BROADCOM"
elif [[ "$PLATFORM_GIVEN" == "RPI" ]];then
    PLATFORM="RPI"
elif [[ "$PLATFORM_GIVEN" == "REALTEK" ]];then
    PLATFORM="REALTEK"
else
    SKIP_PLATFORM="TRUE"
    PLATFORM=""
fi

for arg in "$@"; do
    if [ "$arg" == "--fncs-package" ]; then
        echo "Creating only FNCS_PACKAGE"
	FNCS_PACKAGE="TRUE"
    fi
done

if [ -z $PLATFORM ];then
    echo -e "\nNO PLATFORM Selected , creating Generic_TDK_Package\n"
else
    echo -e "\nPLATFORM Selected as $PLATFORM\n"
fi

if [[ $PLATFORM == "BROADCOM" ]];then
    PWRMGRHAL_LIBS=" -liarmmgrs-power-hal "
else
    PWRMGRHAL_LIBS=" $MFRHAL_LIB_NAME -liarmmgrs-power-hal "
fi

#All logs will be written to this file
LOG_FILE=$ROOT_DIR/logs/$(date +%F_%T)_$PLATFORM.log

echo -e "\n"
echo -e "Monitor \e[1;31m  $LOG_FILE \e[0m for more logs \n"

if [ -f "$SDK_INSTALL_SCRIPT" ]; then
    echo -e "\e[1;42m SDK INSTALL SCRIPT: FOUND \e[0m \n" 2>&1 | tee -a $LOG_FILE
else
    echo -e "\e[1;41m SDK INSTALL SCRIPT: NOT FOUND \e[0m\n" 2>&1 | tee -a $LOG_FILE
    exit
fi


# Function: download_source_code
# Description: Downloads the source code of all dependent packages if not already present.
# Parameters: None
# Return: None
download_source_code()
{
    echo -e "Download the source code of all dependent packages\n" 2>&1 | tee -a $LOG_FILE
    packages="CURL JSONCPP JSONRPC TINYXML2 XKBCOMMON ZLIB"    
    for package in $packages; do
        DIR=DIR_$package
	SRC_URL=SRC_$package
	filename="$(basename ${!SRC_URL})"
        #if [ -f "${!DIR}" ]; then
	if [ -f $filename ];then
            echo "$package- $filename is already cloned in the current directory" 2>&1 | tee -a $LOG_FILE
    	    echo -e "\e[1;42m Download $package: SKIPPED \e[0m \n" 2>&1 | tee -a $LOG_FILE
        else
            SRC_URL=SRC_$package
            echo "Cloning $package from ${!SRC_URL}" 2>&1 | tee -a $LOG_FILE
	    if [[ ${!SRC_URL} == *.git ]];then
		git clone ${!SRC_URL} | tee -a $LOG_FILE
	    else
		filename="$(basename ${!SRC_URL})"
		echo $filename
		wget --no-check-certificate --waitretry=0 --tries=5 ${!SRC_URL}
		tar -xf $filename
	    fi
    	    if [ $? -eq 0 ]; then
    	        echo -e "\e[1;42m Download $package: SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
    	    else
    	        echo -e "\e[1;41m Download $package : FAILURE \e[0m \n" 2>&1 | tee -a $LOG_FILE
    	        exit
    	    fi
        fi
    done
}

# Function: install_sdk
# Description: Installs the SDK if not already installed.
# Parameters: None
# Return: None
install_sdk()
{
    echo -e "Installing $SDK_INSTALL_SCRIPT in $SDK_INSTALL_PATH\n" 2>&1 | tee -a $LOG_FILE
    if [ -d "$SDK_INSTALL_PATH" ]; then
	echo -e "SDK is already installed in $SDK_INSTALL_PATH" 2>&1 | tee -a $LOG_FILE
	echo -e "\e[1;42m INSTALL SDK : SKIPPED \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
        printf "$SDK_INSTALL_PATH\nY\n" | $SDK_INSTALL_SCRIPT
        if [ $? -eq 0 ]; then
	    echo -e "\e[1;42m INSTALL SDK : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
	else
	    echo -e "\e[1;41m INSTALL SDK : FAILURE \e[0m \n" 2>&1 | tee -a $LOG_FILE
	    exit
	fi
    fi
    SYSROOT_PATH="$(ls $SDK_INSTALL_PATH/sysroots -1 | head -n1)"
    SYSROOT=$SDK_INSTALL_PATH/sysroots/$SYSROOT_PATH

    echo "SDK_INSTALL_PATH : $SDK_INSTALL_PATH"
    source $SDK_INSTALL_PATH/environment-setup-armv7vet2hf-neon-oe-linux-gnueabi
    echo -e "\e[1;42m SOURCE SDK : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
    export includedir="/usr/include/"
	
}


get_component_versions()
{
    cd $TDK_SOURCE_DIR
    echo -e "Gathering versions from meta-middleware-generic-support"
    if [[ "$MIDDLEWARE_VERSION" == "DEFAULT" ]];then
	 echo -e "All versions set to DEFAULT\n"
	 common_utilities_srcrev="DEFAULT"
	 rdkfw_srcrev="DEFAULT"
         rdklogger_srcrev="DEFAULT"
	 return
    fi
    git clone $SRC_MIDDLEWARE_SUPPORT >> $LOG_FILE 2>&1
    cd meta-middleware-generic-support
    if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
	 git checkout $MIDDLEWARE_VERSION >> $LOG_FILE 2>&1
    fi
    common_utilities_srcrev=`grep commonutilities conf/include/generic-srcrev.inc | cut -d "=" -f 2`
    common_utilities_srcrev=${common_utilities_srcrev//\"/}
    common_utilities_srcrev=${common_utilities_srcrev// /}
    echo "common_utilities_srcrev = $common_utilities_srcrev"

    rdkfw_srcrev=`grep rdkfw conf/include/generic-srcrev.inc | cut -d "=" -f 2`
    rdkfw_srcrev=${rdkfw_srcrev//\"/}
    rdkfw_srcrev=${rdkfw_srcrev// /}
    echo "rdkfw_srcrev = $rdkfw_srcrev"

    rdklogger_srcrev=1.0.0
    echo "rdklogger_srcrev = $rdklogger_srcrev"

    echo "Deleting meta-middleware-generic-support as versions are obtained"
    cd ../;rm -rf meta-middleware-generic-support
}

# Function: compile_ZLIB
# Description: Compiles ZLIB if it is not already compiled and copies to sysroot of toolchain.
# Parameters: None
# Return: None
compile_ZLIB()
{
    echo -e "Entering $DIR_ZLIB\n" 2>&1 | tee -a $LOG_FILE
    cd $DIR_ZLIB

    compile_status="$(find $SYSROOT -iname libz.so)"
    if [ ! -z "${compile_status}" ]; then
        echo -e "ZLIB is already compiled and library is present in the current directory\n" 2>&1 | tee -a $LOG_FILE
        echo -e "\e[1;42m COMPILE ZLIB : SKIPPED \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
        echo -e "Compiling ZLIB \n"
	./configure >> $LOG_FILE 2>&1
	make >> $LOG_FILE 2>&1
	sudo cp libz.* $SYSROOT/usr/lib
    fi
    cd $ROOT_DIR
}

# Function: compile_XKBCOMMON
# Description: Compiles XKBCOMMON if it is not already compiled and copies to sysroot of toolchain.
# Parameters: None
# Return: None
compile_XKBCOMMON()
{
    echo -e "Entering $DIR_XKBCOMMON\n" 2>&1 | tee -a $LOG_FILE
    cd $DIR_XKBCOMMON

    compile_status="$(find $SYSROOT -iname libxkbcommon.so.0.0.0)"
    if [ ! -z "${compile_status}" ]; then
        echo -e "XKBCOMMON is already compiled and library is present in the current directory\n" 2>&1 | tee -a $LOG_FILE
        echo -e "\e[1;42m COMPILE XKBCOMMON : SKIPPED \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
	echo -e "Compiling XKBCOMMON \n"
	./configure --host=arm-none-linux-gnueabihf --disable-x11 >> $LOG_FILE 2>&1
	make >> $LOG_FILE 2>&1
	sudo cp .libs/* $SYSROOT/usr/lib
	sudo cp -r xkbcommon  $SYSROOT/usr/include/
    fi
    cd $ROOT_DIR
}

# Function: compile_JSONCPP
# Description: Compiles JSONCPP if it is not already compiled and copies to sysroot of toolchain.
# Parameters: None
# Return: None
compile_JSONCPP() 
{
    echo -e "Entering $DIR_JSONCPP\n" 2>&1 | tee -a $LOG_FILE
    cd $DIR_JSONCPP

    compile_status="$(find $SYSROOT -iname libjsoncpp.so.1.8.4)"
    if [ ! -z "${compile_status}" ]; then
        echo -e "JSONCPP is already compiled and library is present in the current directory\n" 2>&1 | tee -a $LOG_FILE
        echo -e "\e[1;42m COMPILE JSONCPP : SKIPPED \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
	echo -e "Compiling JSONCPP \n"
	echo -e "Deleting any other libs for JSONCPP"
        find $SYSROOT/usr/lib  -iname "libjsoncpp*" | while read -r file; do
             echo "Deleting $file"
             rm "$file"
        done
        mkdir -p build
        cd build/
        cmake .. -DBUILD_SHARED_LIBS=ON -DJSONCPP_WITH_PKGCONFIG_SUPPORT=OFF -DBUILD_TESTING=OFF -DJSONCPP_WITH_TESTS=OFF >> $LOG_FILE 2>&1
        make CFLAGS="-DBUILD_SHARED_LIBS=ON -DJSONCPP_WITH_PKGCONFIG_SUPPORT=OFF -DBUILD_TESTING=OFF -DJSONCPP_WITH_TESTS=OFF" prefix=${ROOT_DIR}/sysroots>> $LOG_FILE 2>&1
	mkdir -p $ROOT_DIR/json_temp/
	cp src/lib_json/libjsoncpp* $ROOT_DIR/json_temp/
	cp src/lib_json/libjsoncpp* $SYSROOT/usr/lib/
	mkdir -p $SYSROOT/usr/include/jsoncpp
	cp -r ../include/json/ $SYSROOT/usr/include/jsoncpp/
	cp -r ../include/json/ $SYSROOT/usr/include/
    fi
    cd $ROOT_DIR
}

# Function: compile_TINYXML2
# Description: Compiles TINYXML2 if it is not already compiled and copies to sysroot of toolchain.
# Parameters: None
# Return: None
compile_TINYXML2()
{
    echo -e "Entering $DIR_TINYXML2\n" 2>&1 | tee -a $LOG_FILE
    cd $DIR_TINYXML2
    git checkout bf15233ad88390461f6ab0dbcf046cce643c5fcb >> $LOG_FILE 2>&1

    compile_status="$(find $SYSROOT -iname libtinyxml2.so.8.0.0)"
    if [ ! -z "${compile_status}" ] && [ ! -z "${header_file_status}" ]; then
        echo -e "TINYXML2 is already compiled and library is present in the current directory\n" 2>&1 | tee -a $LOG_FILE
        echo -e "\e[1;42m COMPILE TINYXML2 : SKIPPED \e[0m \n" 2>&1 | tee -a $LOG_FILE
	cp $SYSROOT/usr/lib/libtinyxml2* $ROOT_DIR/json_temp/
    else
        echo -e "Compiling TINYXML2 \n"
        mkdir -p build
	cd build
	cmake .. -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=$SDKTARGETSYSROOT/usr >> $LOG_FILE 2>&1
	echo -e "Compiling TINYXML2  \n"
	make -j$(nproc)	>> $LOG_FILE 2>&1
	make install >> $LOG_FILE 2>&1
        echo -e "\n\n" >> $LOG_FILE 2>&1
        echo "Check for the TINYXML2 shared library" 2>&1 | tee -a $LOG_FILE
	status="$(find ./ -iname libtinyxml2.so.8.0.0)"
        if [ ! -z "${status}" ]; then
            echo -e "\e[1;42m COMPILE TINYXML2 : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
        else
            echo -e "\e[1;41m COMPILE TINYXML2 : FAILURE \e[0m \n" 2>&1 | tee -a $LOG_FILE
            exit
        fi
	#Copy the shared library and header files to sysroot folder and create softlink to the library
 	find $SYSROOT/usr/lib  -iname "libtinyxml2*" | while read -r file; do
            echo "Deleting $file"
            rm "$file"
        done
        echo -e "Copying libs and headers for TINYXML2 to sysroot path \n" 2>&1 | tee -a $LOG_FILE
	mkdir -p $ROOT_DIR/json_temp/
        cp libtinyxml2* $ROOT_DIR/json_temp/
        cp libtinyxml2* $SYSROOT/usr/lib/
        cp ../tinyxml2.h $SYSROOT/usr/include
    fi
    cd $ROOT_DIR
}

# Function: update_m4
# Description: Updates m4 package in the sysroot if required.
# Parameters: None
# Return: None
update_m4()
{
    cd $SDKTARGETSYSROOT
    cd ..
    cd x86_64-*linux
    cp ${ROOT_DIR}/m4_1.4.18.tgz .
    tar -xf m4_1.4.18.tgz
    rm m4_1.4.18.tgz
    cd $ROOT_DIR
}

# Function: install_gstreamer_glib
# Description: Installs GStreamer and GLib headers/libraries from external package.
# Parameters: None
# Return: None
install_gstreamer_glib()
{
    cd $ROOT_DIR
    Packages="$(find $ROOT_DIR -iname Packages.tgz)"
    if [  -z "$Packages" ];then
	echo -e "Packages.tgz not found"
	exit
    fi
    tar -xf Packages.tgz
    gstreamer_package="$(find $ROOT_DIR -iname gstreamer.tgz)"
    gst_h="$(find $SDKTARGETSYSROOT -iname gst.h)"
    if [ ! -z "${gstreamer_package}" ] && [  -z "${gst_h}" ]; then
	echo -e "Copying gstreamer1.0 headers and libraries\n" 2>&1 | tee -a $LOG_FILE
        cd $SDKTARGETSYSROOT
	cp -u $gstreamer_package $SDKTARGETSYSROOT
	gstreamer_package_name=$(basename "$gstreamer_package")
	tar -xf $gstreamer_package_name
	rm $SDKTARGETSYSROOT/$gstreamer_package_name
    fi
    cd $ROOT_DIR
    gstreamer_plugins_base_package="$(find $ROOT_DIR -iname gstreamer_plugins_base.tgz)"
    gstaudioclock_h="$(find $SDKTARGETSYSROOT -iname gstaudioclock.h)"
    if [ ! -z "${gstreamer_plugins_base_package}" ] && [  -z "${gstaudioclock_h}" ]; then
	echo -e "Copying gstreamer1.0-plugins-base headers and libraries\n" 2>&1 | tee -a $LOG_FILE
        cd $SDKTARGETSYSROOT
        cp -u $gstreamer_plugins_base_package $SDKTARGETSYSROOT
        gstreamer_plugins_base_package_name=$(basename "$gstreamer_plugins_base_package")
        tar -xf $gstreamer_plugins_base_package_name
	rm $SDKTARGETSYSROOT/$gstreamer_plugins_base_package_name
    fi
    cd $ROOT_DIR
    glib_2_0_package="$(find $ROOT_DIR -iname glib2.0.tgz)"
    glib_h="$(find $SDKTARGETSYSROOT -iname glib.h)"
    if [ ! -z "${glib_2_0_package}" ] && [  -z "${glib_h}" ]; then
	echo -e "Copying glib-2.0 headers and libraries\n" 2>&1 | tee -a $LOG_FILE
	cd $SDKTARGETSYSROOT
        cp -u $glib_2_0_package $SDKTARGETSYSROOT
        glib_2_0_package_name=$(basename "$glib_2_0_package")
        tar -xf $glib_2_0_package_name
	rm $SDKTARGETSYSROOT/$glib_2_0_package_name
    fi
    libffi_package="$(find $ROOT_DIR -iname libffi.tgz)"
    libffi_lib="$(find $SDKTARGETSYSROOT -iname libffi*)"
    if [ ! -z "${libffi_package}" ] && [  -z "${libffi_lib}" ]; then
        echo -e "Copying libffi headers and libraries\n" 2>&1 | tee -a $LOG_FILE
        cd $SDKTARGETSYSROOT
        cp -u $libffi_package $SDKTARGETSYSROOT
        libffi_package_name=$(basename "$libffi_package")
        tar -xf $libffi_package_name
        rm $SDKTARGETSYSROOT/$libffi_package_name
    fi
    cd $ROOT_DIR
    wayland_package="$(find $ROOT_DIR -iname wayland.tgz)"
    wayland_h="$(find $SDKTARGETSYSROOT -iname wayland-client.h)"
    if [ ! -z "${wayland_package}" ] && [ -z "${wayland_h}" ]; then
        echo -e "Copying wayland headers and libraries\n" 2>&1 | tee -a $LOG_FILE
        cd $SDKTARGETSYSROOT
        cp -u $wayland_package $SDKTARGETSYSROOT
        wayland_package_name=$(basename "$wayland_package")
        tar -xf $wayland_package_name
        rm $SDKTARGETSYSROOT/$wayland_package_name
    fi
    pcreposix_package="$(find $ROOT_DIR -iname additionial_libs.tgz)"
    pcreposix_lib="$(find $SDKTARGETSYSROOT -iname libpcrecpp.so)"
    if [ ! -z "${pcreposix_package}" ] && [ -z "${pcreposix_lib}" ]; then
	echo -e "Copying additionial_libs \n" 2>&1 | tee -a $LOG_FILE
	cd $SDKTARGETSYSROOT
	cp $pcreposix_package $SDKTARGETSYSROOT
	pcreposix_package_name=$(basename "$pcreposix_package")
	tar -xf $pcreposix_package_name
	cd $SDKTARGETSYSROOT/additionial_libs/usr/lib
	ls
	cp * $SDKTARGETSYSROOT/usr/lib/
	cd $SDKTARGETSYSROOT/additionial_libs/lib
	ls
	cp * $SDKTARGETSYSROOT/lib
	rm -rf $SDKTARGETSYSROOT/additionial_libs
	rm $SDKTARGETSYSROOT/$pcreposix_package_name
    fi
    cd $ROOT_DIR
}

# Function: setup_CURL
# Description: Configures and installs the CURL library.
# Parameters: None
# Return: None
setup_CURL()
{
    echo -e "Entering $DIR_CURL\n" 2>&1 | tee -a $LOG_FILE
    if [  -f "$SYSROOT/lib/pkgconfig/libcurl.pc" ]; then
       echo -e "\e[1;42m COMPILE CURL : SKIPPED \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
       cd $DIR_CURL
        echo -e "Compiling CURL \n"
        ./configure --host=arm-none-linux-gnueabihf --without-ssl --enable-shared >> $LOG_FILE 2>&1
        make install prefix=$SYSROOT >> $LOG_FILE 2>&1
        cp lib/.libs/libcurl.a $SYSROOT/usr/lib/
        ln -sf $SYSROOT/usr/lib/libcurl.a $SYSROOT/usr/lib/libcurl.so.4.7.0
        echo -e "Copying headers for CURL to sysroot path \n" 2>&1 | tee -a $LOG_FILE
        cp -r include/curl $SYSROOT/usr/include
	cp src/curl $SYSROOT/usr/bin
 	cp lib/.libs/libcurl.so.4.7.0 $SYSROOT/usr/lib/
        cd ${ROOT_DIR}
    fi
}

# Function: compile_JSONRPC
# Description: Compiles JSON-RPC library and installs it in sysroot.
# Parameters: None
# Return: None
compile_JSONRPC()
{
    echo -e "Entering $DIR_JSONRPC\n" 2>&1 | tee -a $LOG_FILE
    cd $DIR_JSONRPC
    git checkout c696f6932113b81cd20cd4a34fdb1808e773f23e
    server="$(find .  -iname libjsonrpccpp-server.so.1.3.0)"
    client="$(find . -iname libjsonrpccpp-client.so.1.3.0)"
    common="$(find . -iname libjsonrpccpp-common.so.1.3.0)"
    if [ ! -z "${server}" ] && [ ! -z "${client}" ] && [ ! -z "${common}" ]; then
	echo -e "JSONRPC is already compiled and library is present in the current directory\n" 2>&1 | tee -a $LOG_FILE
	echo -e "\e[1;42m COMPILE JSONRPC : SKIPPED \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
	#clone a patch for tdk related changes
	if [ ! -d ../meta-rdk-ext ];then
            git clone https://code.rdkcentral.com/r/rdk/components/generic/rdk-oe/meta-rdk-ext ../meta-rdk-ext >> $LOG_FILE 2>&1
	fi
	if git apply --check ../meta-rdk-ext/recipes-devtools/jsonrpc/jsonrpc/0001-jsonrpc-v1.3.0-ipv6.patch; then
	    git apply --reject --whitespace=fix  ../meta-rdk-ext/recipes-devtools/jsonrpc/jsonrpc/0001-jsonrpc-v1.3.0-ipv6.patch  >> $LOG_FILE 2>&1
	fi
	rm -rf ../meta-rdk-ext
	#Enable TCP SOCKET SERVE and CLIENT. Also disabling the unit testing of the libraries
	sed -i  's/.*set(TCP_SOCKET_SERVER.*/set(TCP_SOCKET_SERVER YES CACHE BOOL "Include Tcp Socket server")/' CMakeLists.txt
        sed -i  's/.*set(TCP_SOCKET_CLIENT.*/set(TCP_SOCKET_CLIENT YES CACHE BOOL "Include Tcp Socket client")/' CMakeLists.txt
        sed -i  's/.*set(COMPILE_STUBGEN.*/set(COMPILE_STUBGEN NO CACHE BOOL "Compile the stubgenerator")/' CMakeLists.txt
        sed -i  's/.*set(COMPILE_EXAMPLES.*/set(COMPILE_EXAMPLES NO CACHE BOOL "Compile example programs")/' CMakeLists.txt
        sed -i  's/.*set(COMPILE_TESTS.*/set(COMPILE_TESTS NO CACHE BOOL "Compile test framework")/' CMakeLists.txt
	mkdir -p build
	cd build
	cmake -DHTTP_SERVER=NO -DREDIS_SERVER=NO -DREDIS_CLIENT=NO .. >> $LOG_FILE 2>&1 && make >> $LOG_FILE 2>&1
	cd ../
	echo -e "\n\n" >> $LOG_FILE 2>&1
	echo "Check for the JSONRPC shared libraries" 2>&1 | tee -a $LOG_FILE
	server="$(find ./ -iname libjsonrpccpp-server.so.1.3.0)"
	client="$(find ./ -iname libjsonrpccpp-client.so.1.3.0)"
	common="$(find ./ -iname libjsonrpccpp-common.so.1.3.0)"
	if [ ! -z "${server}" ] && [ ! -z "${client}" ] && [ ! -z "${common}" ]; then
	    echo -e "\e[1;42m COMPILE JSONRPC : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
	else
	    echo -e "\e[1;41m COMPILE JSONRPC : FAILURE \e[0m \n" 2>&1 | tee -a $LOG_FILE
	    exit
	fi
    fi
    #Copy the shared library and header files to sysroot folder
    if [ ! -f "$SYSROOT/usr/lib/libjsonrpccpp-server.so.1.3.0" ]; then
	echo -e "Deleting any other libs for JSONCPP"
        find $SYSROOT/usr/lib  -iname "libjsonrpccpp*" | while read -r file; do
             echo "Deleting $file"
             rm "$file"
        done
	echo -e "Copying libs and header for JSONRPC to sysroot folder" 2>&1 | tee -a $LOG_FILE
        sudo cp build/lib/libjsonrpccpp-*.so.1.3.0 $SYSROOT/usr/lib
        sudo cp -r src/jsonrpccpp $SYSROOT/usr/include/
        sudo ln -s $SYSROOT/usr/lib/libjsonrpccpp-server.so.1.3.0 $SYSROOT/usr/lib/libjsonrpccpp-server.so
        sudo ln -s $SYSROOT/usr/lib/libjsonrpccpp-client.so.1.3.0 $SYSROOT/usr/lib/libjsonrpccpp-client.so
        sudo ln -s $SYSROOT/usr/lib/libjsonrpccpp-common.so.1.3.0 $SYSROOT/usr/lib/libjsonrpccpp-common.so
    fi
    if [ ! -f "$SYSROOT/usr/include/jsonrpccpp" ]; then
	sudo mkdir -p $SYSROOT/usr/include/jsonrpccpp/server/connectors
	sudo mkdir -p $SYSROOT/usr/include/jsonrpccpp/client/connectors
	sudo mkdir -p $SYSROOT/usr/include/jsonrpccpp/common
	sudo cp build/gen/jsonrpccpp/common/jsonparser.h $SYSROOT/usr/include/ 
	sudo cp build/gen/jsonrpccpp/common/jsonparser.h $SYSROOT/usr/include/jsonrpccpp/common/
	sudo cp src/jsonrpccpp/common/*.h $SYSROOT/usr/include/jsonrpccpp/common
        sudo cp src/jsonrpccpp/*.h $SYSROOT/usr/include/jsonrpccpp/
        sudo cp src/jsonrpccpp/server/*.h $SYSROOT/usr/include/jsonrpccpp/server
        sudo cp src/jsonrpccpp/server/connectors/*.h $SYSROOT/usr/include/jsonrpccpp/server/connectors/
        sudo cp src/jsonrpccpp/client/*.h $SYSROOT/usr/include/jsonrpccpp/client
        sudo cp src/jsonrpccpp/client/connectors/*.h $SYSROOT/usr/include/jsonrpccpp/client/connectors/
    fi
    cd ../
}

# Function: clone_tdk
# Description: Clones the TDK repository from the source.
# Parameters: None
# Return: None
clone_tdk()
{
	if [  ! -d "tdkv" ];then
	    git clone $SRC_TDK >> $LOG_FILE 2>&1
	    existing_directory_use=false
	else
	    echo "Compiling using  existing tdkv directory"
	    existing_directory_use=true
	fi
	if [ $? -eq 0 ]; then
	    echo -e "\e[1;42m DOWNLOAD TDK : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
	    echo -e "Entering $DIR_TDK \n" 2>&1 | tee -a $LOG_FILE
	    cd $DIR_TDK
	    if ! $existing_directory_use;then
                if [[ $TDK_REVISION != "DEFAULT" ]];then
                    git checkout $TDK_REVISION
	        fi
	    fi
	else
	    echo -e "\e[1;41m DOWNLOAD TDK : FAILURE \e[0m \n" 2>&1 | tee -a $LOG_FILE
	    exit
	fi
}

# Function: clone_and_move
# Description: Clones a repository and moves necessary files to sysroot.
# Parameters: $1 - Repository URL
#             $2 - Revision to checkout
#             $3 - Component name
#             $4 - Library version variable
#             $5 (Optional) - Custom path for headers
# Return: None
clone_and_move()
{
    mkdir -p ${TDK_SOURCE_DIR}/RDK_Source
    cd ${TDK_SOURCE_DIR}/RDK_Source
    repo_url=$1
    HEADER_REVISION=$2
    COMPONENT=$3
    HAL_LIB_VERSION=$4
    header_file_custom_path=$5
    if [ "$COMPILE_SKELETON" != "true" ]; then
        header_file_custom_path=$4
    fi
    repo_name=$(basename "$repo_url" .git)
    custom_destination_path=""
    if [[ $COMPONENT == "PowerMgrHal" ]] || [[ $COMPONENT == "DeepSleepHal" ]] || [[ $COMPONENT == "MfrHal" ]];then
        custom_destination_path="rdk/iarmmgrs-hal"
    fi
    if [[ $COMPONENT == "DSHal" ]];then
        custom_destination_path="rdk/ds-hal"
    fi
    if [[ $COMPONENT == "HdmiCec" ]];then
        custom_destination_path="ccec/drivers"
    fi
    if [[ $COMPONENT == "AudioCaptureMgr" ]];then
        custom_destination_path="media-utils/audioCapture"
    fi
    mkdir -p ${SYSROOT}/usr/include/$custom_destination_path
    echo -e "\nCloning $repo_url for $COMPONENT skeleton compilation"
    if [ ! -d ${repo_name}_source ]; then
        git clone "$repo_url" >> $LOG_FILE 2>&1
        if [[ $HEADER_REVISION != "DEFAULT" ]];then
            echo "Checking out $HEADER_REVISION for $repo_name"
            cd $repo_name
            git checkout $HEADER_REVISION >> $LOG_FILE 2>&1
            cd ..
        fi
        mv $repo_name ${repo_name}_source
    else
        echo -e "$repo_url source code already present reusing the same"
    fi
    repo_name=${repo_name}_source
    cd "$repo_name" || exit
    if [[ $COMPONENT == "MfrHal" ]];then
        cp ${TDK_SOURCE_DIR}/RDK_Source/${repo_name}/mfr/include/mfrTypes.h ${SYSROOT}/usr/include/$custom_destination_path
    fi
    echo -e "Installing $COMPONENT header files in sysroot"
    if [[ ! -z $header_file_custom_path ]];then
        echo -e "Fetching from $header_file_custom_path"
        cp ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/$header_file_custom_path/*.h ${SYSROOT}/usr/include
    elif [[ ! -z $custom_destination_path ]];then
        echo -e "Installing $COMPONENT headers in ${SYSROOT}/usr/include/$custom_destination_path"
        cp ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/include/*.h ${SYSROOT}/usr/include/$custom_destination_path
    else
        for file in ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/include/*.h;do
            file=$(basename $file)
            echo "Deleting  $file from sysroots"
            find $SYSROOT/usr/include/ -name "$file" -type f -delete
        done
        cp ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/include/*.h $SYSROOT/usr/include/$custom_destination_path
    fi
    if $COMPILE_SKELETON;then
        echo -e "Compiling $COMPONENT Skeleton\n"
        cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
        if [[ $COMPONENT == "MfrHal" ]];then
            make ${HAL_LIB_VERSION}=${!HAL_LIB_VERSION} MFRHAL_LIBS=$MFRHAL_LIB_NAME >> $LOG_FILE 2>&1
        else
            make ${HAL_LIB_VERSION}=${!HAL_LIB_VERSION} >> $LOG_FILE 2>&1
        fi
        echo -e "Copying $COMPONENT libs created by skeleton to sysroot"
        mv *.so* $SYSROOT/usr/lib
    fi
}

# Function: fetch_aamp
# Description: Fetches and clones AAMP source code.
# Parameters: $1 - Repository name
#             $2 - AAMP tag name
# Return: None
fetch_aamp() 
{
    cd ${TDK_SOURCE_DIR}/RDK_Source
    AAMP_TAG=$(cat meta-rdk-video/recipes-extended/aamp/$1_git.bb | grep $2 | cut -d "=" -f 2 | head -1 | awk '{$1=$1; gsub(/^"|"$/, ""); print}')
    echo "AAMP_TAG: $AAMP_TAG"
    git clone "https://code.rdkcentral.com/r/rdk/components/generic/$1" || exit 1 >> $LOG_FILE 2>&1
    cd $1 ; git checkout $AAMP_TAG ; cd ../
    mv $1 "$1_source"	
}

# Function: compile_skeleton_libraries
# Description: Compiles necessary skeleton libraries for various components.
# Parameters: None
# Return: None
compile_skeleton_libraries()
{
    echo -e "Compiling TDK Libraries\n"
    COMPILE_SKELETON=false
    COMPILE_DUMMY_LIBS="WiFiHal PowerMgrHal DeepSleepHal DSHal IARMBus HdmiCec Bluetooth MfrHal WesterosHal Essos AAMP AudioCaptureMgr Graphics "
    COMPILE_DUMMY_LIBS="$COMPILE_DUMMY_LIBS common_utilities rdklogger DeviceSettings IARMBus libsyswrapper NetSrvMgr"
    if [[ $FNCS_PACKAGE == "TRUE" ]];then
	COMPILE_DUMMY_LIBS=" Graphics "
    fi
    clone_and_move "https://code.rdkcentral.com/r/rdk/components/generic/iarmbus" $SRC_IARMBUS_HEADER_REVISION "iarmbus" "core/include"
    clone_and_move "https://code.rdkcentral.com/r/rdk/components/generic/iarmbus" $SRC_IARMBUS_HEADER_REVISION "iarmbus" "core"
    COMPILE_SKELETON=true
    for COMPONENT in $COMPILE_DUMMY_LIBS; do
        if [[ $COMPONENT == "WiFiHal" ]];then
	    if [[ ! -f $SYSROOT/usr/lib/libwifihal.so.${WIFI_HAL_LIB_VERSION} ]];then
                 clone_and_move $SRC_WIFI $SRC_WIFI_HAL_HEADER_REVISION $COMPONENT "WIFI_HAL_LIB_VERSION"
            fi
        fi
	if [[ $COMPONENT == "PowerMgrHal" ]] || [[ $COMPONENT == "MfrHal" ]] || [[ $COMPONENT == "DeepSleepHal" ]] || [[ $COMPONENT == "IARMBus" ]];then
	    if [ ! -d ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source ];then
                 cd ${TDK_SOURCE_DIR}/RDK_Source
                 echo -e "\nInstalling iarmmgrs_source"
                 git clone $SRC_IARMMGRS 
                 if [[ $SRC_IARMMGRS_HEADER_REVISION != "DEFAULT" ]];then
                     cd iarmmgrs; git checkout $SRC_IARMMGRS_HEADER_REVISION >> $LOG_FILE 2>&1; cd ..
                 fi
                 mv iarmmgrs iarmmgrs_source
		 cp ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source/ir/include/irMgr.h $SYSROOT/usr/include
		 cp ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source/hal/include/pwrMgr.h $SYSROOT/usr/include
		 cp ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source/mfr/include/mfr_temperature.h $SYSROOT/usr/include
		 cp ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source/power/pwrlogger.h $SYSROOT/usr/include
                 cd ${TDK_SOURCE_DIR}
	    fi
	fi
        if [[ $COMPONENT == "PowerMgrHal" ]];then
            
            find $SYSROOT/usr/include  -iname "plat_power.h" | while read -r file; do
                 echo "Deleting $file"
                 rm "$file"
            done
            find $SYSROOT/usr/lib -iname "libiarmmgrs-power-hal*" | while read -r file; do
                 echo "Deleting $file"
                 rm "$file"
            done
            cd ${TDK_SOURCE_DIR}/RDK_Source
            echo -e "\nInstalling therm_mon.h in RDK_Source"
            git clone $SRC_IARMMGRS >> $LOG_FILE 2>&1
	    if [[ $SRC_IARMMGRS_HEADER_REVISION != "DEFAULT" ]];then
	       cd iarmmgrs; git checkout $SRC_IARMMGRS_HEADER_REVISION >> $LOG_FILE 2>&1; cd ..
	    fi

	    cp iarmmgrs/hal/include/therm_mon.h $SYSROOT/usr/include
            cp iarmmgrs/hal/include/therm_mon.h ${TDK_SOURCE_DIR}/PowerMgrHal
            rm -rf ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs
            clone_and_move $SRC_POWERMGR_HAL $SRC_POWERMGR_HAL_HEADER_REVISION $COMPONENT "PWRMGR_HAL_LIB_VERSION"
        fi
        if [[ $COMPONENT == "DeepSleepHal" ]];then
            find $SYSROOT/usr/include  -iname "deepSleepMgr.h" | while read -r file; do
                 echo "Deleting $file"
                 rm "$file"
            done
            find $SYSROOT/usr/lib -iname "libiarmmgrs-deepsleep-hal*" | while read -r file; do
                 echo "Deleting $file"
                 rm "$file"
            done
            clone_and_move $SRC_DEEPSLEEP_HAL $SRC_DEEPSLEEP_HAL_HEADER_REVISION $COMPONENT "DEEPSLEEP_HAL_LIB_VERSION"
        fi
        if [[ $COMPONENT == "DSHal" ]];then
            find $SYSROOT/usr/lib -iname "libds-hal*" | while read -r file; do
                 echo "Deleting $file"
                 rm "$file"
            done
	    if [[ ! -z $device_settings_version ]];then
		 echo "device_settings_hal_header_version is set as $$device_settings_version"
		 SRC_DS_HAL="\"$SRC_DS_HAL --branch '$device_settings_version'\""
	    fi
            clone_and_move $SRC_DS_HAL  $SRC_DS_HAL_HEADER_REVISION $COMPONENT "DS_HAL_LIB_VERSION"
        fi
        if [[ $COMPONENT == "HdmiCec" ]];then
            find $SYSROOT/usr/include  -iname "hdmi_cec_driver.h" | while read -r file; do
                 echo "Deleting $file"
                 rm "$file"
            done
            find $SYSROOT/usr/lib -iname "libRCECHal*" | while read -r file; do
                 echo "Deleting $file"
                 rm "$file"
            done
            clone_and_move $SRC_HDMICEC_HAL $SRC_HDMICEC_HAL_HEADER_REVISION $COMPONENT "CEC_HAL_LIB_VERSION"
	    rm -rf hdmicec
	    git clone $SRC_HDMICEC >> $LOG_FILE 2>&1
	    sudo cp hdmicec/ccec/drivers/include/ccec/drivers/iarmbus/CecIARMBusMgr.h $SYSROOT/usr/include/
        fi
        if [[ $COMPONENT == "Bluetooth" ]];then
            clone_and_move $SRC_BLUETOOTH_HAL $SRC_BLUETOOTH_HAL_HEADER_REVISION $COMPONENT "BLE_HAL_LIB_VERSION"
        fi
        if [[ $COMPONENT == "MfrHal" ]];then
            clone_and_move $SRC_IARMMGRS $SRC_IARMMGRS_HAL_HEADER_REVISION $COMPONENT "MFR_HAL_LIB_VERSION" "mfr/include/"
        fi
        if [[ $COMPONENT == "Essos" ]];then
            #Installing EGL headers for Essos Compilation
            cd ${TDK_SOURCE_DIR}/RDK_Source
            git clone $SRC_EGL >> $LOG_FILE 2>&1
            repo_name=$(basename "$SRC_EGL" .git)
            mkdir -p $SYSROOT/usr/include/EGL
            mkdir -p $SYSROOT/usr/include/KHR
            sudo cp  ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/api/EGL/*.h $SYSROOT/usr/include/EGL/
            sudo cp  ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/api/KHR/khrplatform.h $SYSROOT/usr/include/KHR/
            rm -rf ${TDK_SOURCE_DIR}/RDK_Source/$repo_name
            clone_and_move $SRC_WESTEROS $SRC_WESTEROS_HAL_HEADER_REVISION $COMPONENT "ESSOS_LIB_VERSION" "essos/"
        fi
        if [[ $COMPONENT == "WesterosHal" ]];then
            if [[ $PLATFORM == "BROADCOM" ]];then
                clone_and_move $SRC_WESTEROS $SRC_WESTEROS_HAL_HEADER_REVISION "WesterosHal_BRCM" "WESTEROS_LIB_VERSION" "brcm/westeros-gl"
		sudo cp -r ${TDK_SOURCE_DIR}/RDK_Source/westeros_source/test/brcm-em/include/* $SYSROOT/usr/include/
            else
                clone_and_move $SRC_WESTEROS $SRC_WESTEROS_HAL_HEADER_REVISION "WesterosHal_DRM" "WESTEROS_LIB_VERSION" "drm/westeros-gl"
		sudo cp -r ${TDK_SOURCE_DIR}/RDK_Source/westeros_source/test/drm-em/include/* $SYSROOT/usr/include/
            fi
        fi
        if [[ $COMPONENT == "AudioCaptureMgr" ]];then
            clone_and_move $SRC_RMF_AUDIO_CAPTURE $SRC_RMF_AUDIO_CAPTURE_HAL_HEADER_REVISION $COMPONENT "AUDIO_CAPTURE_MGR_LIB_VERSION"
        fi
        if [[ $COMPONENT == "StorageManager" ]];then
	    clone_and_move $SRC_STORAGE_MGR $SRC_STORAGE_MGR_HEADER_REVISION $COMPONENT "STMGR_LIB_VERSION" "refactored/include"
        fi
	if [[ $COMPONENT == "NetSrvMgr" ]];then
	    cd ${TDK_SOURCE_DIR}/RDK_Source
	    repo_name=$(basename "$SRC_NETSRVMGR" .git)
	    if [ ! -d ${TDK_SOURCE_DIR}/RDK_Source/netsrvmgr ];then
	        git clone  $SRC_NETSRVMGR >> $LOG_FILE 2>&1
	        cd $repo_name
	        if [[ $SRC_NETSRVMGR_HEADER_REVISION != "DEFAULT" ]];then
                    git checkout $SRC_NETSRVMGR_HEADER_REVISION >> $LOG_FILE 2>&1
                fi
		cd ..
	    fi
	    cd ${TDK_SOURCE_DIR}/RDK_Source/$repo_name
	    cp src/main/include/*.h  $SYSROOT/usr/include/
	    cp src/services/wifi/include/*.h  $SYSROOT/usr/include/
	fi
        if [[ $COMPONENT == "Graphics" ]];then
	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
	    make  >> $LOG_FILE 2>&1
	    #find and delete GLESv2 wayland-egl EGL 
            sudo mv *.so* $SYSROOT/usr/lib/
	    if [ ! -d "${TDK_SOURCE_DIR}/RDK_Source/westeros_source" ];then
                cd ${TDK_SOURCE_DIR}/RDK_Source/
		git clone $SRC_WESTEROS westeros_source >> $LOG_FILE 2>&1
		if [[ $SRC_WESTEROS_HAL_HEADER_REVISION != "DEFAULT" ]];then
		    cd westeros_source
		    git checkout $SRC_WESTEROS_HAL_HEADER_REVISION >> $LOG_FILE 2>&1
		    cd ..
                fi
		cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
            fi
	    if [[ $PLATFORM == "BROADCOM" ]];then
		sudo cp -r ${TDK_SOURCE_DIR}/RDK_Source/westeros_source/test/brcm-em/include/GLES2 $SYSROOT/usr/include/
	    else
	        sudo cp -r ${TDK_SOURCE_DIR}/RDK_Source/westeros_source/test/drm-em/include/GLES2 $SYSROOT/usr/include/
	    fi
	    cd ${TDK_SOURCE_DIR}/RDK_Source/westeros_source/simpleshell/protocol
	    wayland-scanner client-header < simpleshell.xml > simpleshell-client-protocol.h
	    wayland-scanner server-header < simpleshell.xml > simpleshell-server-protocol.h
            wayland-scanner  public-code < simpleshell.xml > simpleshell-protocol.c
	    sudo cp simpleshell-client-protocol.h $SYSROOT/usr/include/
	    sudo cp simpleshell-server-protocol.h $SYSROOT/usr/include/
	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/Westeros_SimpleShell
	    make
	    sudo cp -a lib* $SYSROOT/usr/lib/
	    cd -
	fi
	if [[ $COMPONENT == "IARMBus" ]];then
	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
	    sudo cp ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source/sysmgr/include/sysMgr.h $SYSROOT/usr/include/
            make IARMBUS_LIB_VERSION=${IARMBUS_LIB_VERSION} >> $LOG_FILE 2>&1
	    sudo mv *.so* $SYSROOT/usr/lib/
	fi
        if [[ $COMPONENT == "AAMP" ]];then 
	    cd ${TDK_SOURCE_DIR}/RDK_Source
	    git clone $SRC_META_RDK_VIDEO >> $LOG_FILE 2>&1
	    fetch_aamp "aamp" "AAMP_RELEASE_TAG_NAME"
	    sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/Aamp*.h $SYSROOT/usr/include/
	    sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/main_aamp.h $SYSROOT/usr/include/
	    sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/Accessibility.hpp $SYSROOT/usr/include/
	    sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/subtitle/*.h $SYSROOT/usr/include/
	    sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/drm/*.h $SYSROOT/usr/include/
	    sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/drm/helper/*.h $SYSROOT/usr/include/
	    sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/downloader/*.h $SYSROOT/usr/include/
	    sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/closedcaptions/*.h $SYSROOT/usr/include/
	    sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/tsb/api/*.h $SYSROOT/usr/include/
            sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/support/aampmetrics/*.h $SYSROOT/usr/include/
            sudo mv ${TDK_SOURCE_DIR}/RDK_Source/aamp_source/support/aampabr/*.h $SYSROOT/usr/include/
	    git clone $SRC_CJSON
	    sudo mkdir -p $SYSROOT/usr/include/cjson
	    sudo cp cJSON/*.h $SYSROOT/usr/include/cjson
	    git clone $SRC_UTIL_LINUX
	    sudo mkdir -p $SYSROOT/usr/include/uuid
	    sudo cp util-linux/libuuid/src/uuid.h $SYSROOT/usr/include/uuid  
            cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
	    make >> $LOG_FILE 2>&1
            sudo mv *.so* $SYSROOT/usr/lib/
	fi
	if [[ $COMPONENT == "DeviceSettings" ]];then
	    cd ${TDK_SOURCE_DIR}/RDK_Source
	    git clone $SRC_DS
            mv devicesettings devicesettings_source
	    cd devicesettings_source
	    if [[ $SRC_DS_HEADER_REVISION != "DEFAULT" ]];then
                echo "Checking out $HEADER_REVISION for $repo_name"
                git checkout $HEADER_REVISION >> $LOG_FILE 2>&1
            fi 
	    cd ..
	    sudo cp devicesettings_source/ds/include/*.hpp $SYSROOT/usr/include/
	    sudo cp devicesettings_source/ds/*.hpp $SYSROOT/usr/include/
	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
            make DS_LIB_VERSION=${DS_LIB_VERSION} >> $LOG_FILE 2>&1
	    sudo mv *.so* $SYSROOT/usr/lib/
	fi
	if [[ $COMPONENT == "libsyswrapper" ]] || [[ $COMPONENT == "common_utilties" ]];then
	    get_component_versions
        fi	    
	if [[ $COMPONENT == "libsyswrapper" ]];then
	    cd ${TDK_SOURCE_DIR}/RDK_Source
	    git clone $SRC_LIBSYSWRAPPER libsyswrapper_source
	    cd libsyswrapper_source
	    if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
	        git checkout $libsyswrapper_srcrev 
	    fi
            cp source/secure_wrapper.h $SYSROOT/usr/include/
	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
	    make LIBSYSWRAPPER_LIB_VERSION=${LIBSYSWRAPPER_LIB_VERSION} >> $LOG_FILE 2>&1
            mv *.so* $SYSROOT/usr/lib/
        fi
	if [[ $COMPONENT == "common_utilities" ]];then
            cd ${TDK_SOURCE_DIR}/RDK_Source
            git clone $SRC_COMMONUTILITIES common_utilities_source >> $LOG_FILE 2>&1
            cd common_utilities_source
	    if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
                git checkout $common_utilities_srcrev >> $LOG_FILE 2>&1
	    fi
            cp utils/rdkv_cdl_log_wrapper.h $SYSROOT/usr/include/
	    cp parsejson/json_parse.h $SYSROOT/usr/include/
	    cp dwnlutils/*.h $SYSROOT/usr/include/


	    #fwutils compilation
            cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT/fwutils/
            make FWUTILS_LIB_VERSION=${FWUTILS_LIB_VERSION} >> $LOG_FILE 2>&1
            mv *.so* $SYSROOT/usr/lib/

	    #parsejson compilation
            cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT/parsejson/
            make PARSEJSON_LIB_VERSION=${PARSEJSON_LIB_VERSION} >> $LOG_FILE 2>&1
            mv *.so* $SYSROOT/usr/lib/

	    #dwnlutils compilation
	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT/dwnlutils/
	    make DWNLUTILS_LIB_VERSION=${DWNLUTILS_LIB_VERSION} >> $LOG_FILE 2>&1
	    mv *.so* $SYSROOT/usr/lib/
        fi
	if [[ $COMPONENT == "rdklogger" ]];then
	    cd ${TDK_SOURCE_DIR}/RDK_Source
	    git clone $SRC_RDKLOGGER rdklogger_source >> $LOG_FILE 2>&1
            cd rdklogger_source/
            find . -type f -name "*.h" -exec cp {} $SYSROOT/usr/include/ \;
	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
	    make
	    mv *.so* $SYSROOT/usr/lib/
	fi
    done
    rm -rf  ${TDK_SOURCE_DIR}/RDK_Source
}

compile_tdkv()
{
    echo -e "Configuring TDK with toolchain \n"
    echo -e "TDK_SOURCE_DIR : $TDK_SOURCE_DIR"
    cd ${TDK_SOURCE_DIR}
    cp ${ROOT_DIR}/configure.ac .
    sed -i '/^PKG_CHECK_MODULES/d' configure.ac
    sudo autoreconf -i >> $LOG_FILE 2>&1
    if [[ $PLATFORM == "RPI" ]];then
	CONFIGURE_OPTIONS_VA=""
	FLAGS_VA=""
    fi
    CONF_DEVICE=CONFIGURE_OPTIONS_$DEVICE_TYPE
    CONF_OPTIONS="${!CONF_DEVICE} $DISTRO_CONFIGURE $CONFIGURE_OPTIONS_VA $CONFIGURE_OPTIONS_HAL $CONFIGURE_OPTIONS_COMPONENTS"
    if [[ $FNCS_PACKAGE == "TRUE" ]];then
        CONF_OPTIONS=" --enable-fncsPackage --enable-tdkgraphics "
	echo "FNCS Package compilation enabled"
    fi
    if [[ $CONF_OPTIONS == *"enable-powermgrhal"* ]];then
	echo -e "PowerMgrhal compilation is enabled\n"
	git clone $SRC_IARMMGRS  >> $LOG_FILE 2>&1
	mkdir -p PowerMgrHal_stub/src/iarmmgr_source/power/
	cp iarmmgrs/power/therm_mon.c PowerMgrHal_stub/src/iarmmgr_source/power/therm_mon.c
	rm -rf iarmmgrs
    fi
    if [[ $CONF_OPTIONS == *"enable-rdkfwupdater"* ]];then
	echo -e "rdkfwupdater compilation is enabled\n"

	get_component_versions
	cd RDK_fwupdater_stub/src
	if [  ! -d "rdkfwupdater_source" ];then
	    git clone $SRC_RDKFWUPDATER rdkfwupdater_source >> $LOG_FILE 2>&1
	    cd rdkfwupdater_source/
	    if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
	        git checkout $rdkfw_srcrev >> $LOG_FILE 2>&1
	    fi
	    rm NEWS AUTHORS ChangeLog
	    find . -type f -name "*.h" -exec cp {} ${SYSROOT}/usr/include/ \;
	    cd ..
	fi

	git clone $SRC_COMMONUTILITIES common_utilties_source >> $LOG_FILE 2>&1
        cd common_utilties_source/
	if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
            git checkout $common_utilities_srcrev >> $LOG_FILE 2>&1
	 fi
	find . -type f -name "*.h" -exec cp {} $SYSROOT/usr/include/ \;
	cd ..; rm -rf common_utilties_source/

	git clone $SRC_RDKLOGGER rdklogger_source >> $LOG_FILE 2>&1
	cd rdklogger_source/
	find . -type f -name "*.h" -exec cp {} $SYSROOT/usr/include/ \;
	cd ..; rm -rf rdklogger_source/

	cd ${TDK_SOURCE_DIR}
    fi
    echo $CONF_OPTIONS
    ./configure $CONF_OPTIONS CXXFLAGS="$FLAGS_VA $FLAGS_HAL" --host=arm-none-linux-gnueabihf --prefix=/usr --with-sysroot=$SYSROOT >> $LOG_FILE 2>&1
    echo -e "Compiling TDK \n"
    make PWRMGRHAL_FLAGS="$PWRMGRHAL_FLAGS" PWRMGRHAL_LIBS="$PWRMGRHAL_LIBS" MFRHAL_LIBS="$MFRHAL_LIBS"  WIFIHAL_LIBS="$WIFIHAL_LIBS" HDMICECHAL_LIBS="$HDMICECHAL_LIBS" \
	 DEEPSLEEPHAL_FLAGS="$DEEPSLEEPHAL_FLAGS" HDMICECHAL_FLAGS="$HDMICECHAL_FLAGS" >> $LOG_FILE 2>&1
    if [ $? -eq 0 ]; then
        echo -e "\e[1;42m COMPILE TDKV : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
        echo -e "\e[1;41m COMPILE TDKV : FAILURE \e[0m \n" 2>&1 | tee -a $LOG_FILE
        exit
    fi
    cd ../
}

modify_tdk_files()
{
    cd $DIR_TDK
    if ! grep -q  "TDK_OFFPLANT" tdk.service;then
        sed -e "s@\[Service\]@\[Service\]\nEnvironment=\"TDK_OFFPLANT=TRUE\"\nExecStartPre=\/bin\/sh -c \'touch /tmp/estbconfigsettings.bin\'\nExecStartPre=\/bin\/sh -c \'touch /tmp/ip_acquired\'\nExecStartPost=\/bin\/sh -c \'touch /tmp/estb_ipv4\'@" -i tdk.service
    fi
    if [[ $PLATFORM == "RPI" ]];then
        if ! grep  -q "westerossink-ioctl" agent/scripts/uploadLogs.sh;then
            sed -i -e "22a sed -i \'/westerossink-ioctl/d\' \$1" agent/scripts/uploadLogs.sh
        fi
    fi

    cd ../
}

pack_tdkv()
{
    echo -e "Pack all required tdk libs and bins\n" 2>&1 | tee -a $LOG_FILE
    cd $ROOT_DIR
    mkdir -p TDK_Package/var/TDK
    mkdir -p TDK_Package/usr/lib
    mkdir -p TDK_Package/usr/bin
    if [[ $FNCS_PACKAGE != "TRUE" ]];then
        mkdir -p TDK_Package/var/TDK/scripts
        mkdir -p TDK_Package/var/TDK/opensourcecomptest
        mkdir -p TDK_Package/lib/systemd/system
        mkdir -p TDK_Package/lib/rdk

        cd $DIR_TDK
        #Copy all the stub libraries and binaries
        mkdir -p temp 
        cp $(grep -rIL . | grep -vE 'dirstamp|stub\.a|gitignore|\.o|\.git') temp
        find ./ -iname *.profile -exec cp {} temp \;
        find ./ -iname *.config -exec cp {} temp \;
        find ./ -iname "*.sh" -exec cp {} temp \;
        find ./ -iname *.service -exec cp {} temp \;

        cd temp;rm $EXCLUDE_LIST; cd ../
        mv temp/lib* ../TDK_Package/usr/lib
        mv temp/tdk.service ../TDK_Package/lib/systemd/system
        chmod +x temp/tdkstartup.sh
        chmod +x temp/tdkstop.sh
        mv temp/tdkstartup.sh ../TDK_Package/lib/rdk
        mv temp/tdkstop.sh ../TDK_Package/lib/rdk
        mv temp/ExecuteSuite.sh ../TDK_Package/var/TDK/opensourcecomptest

        mv temp/*.profile ../TDK_Package/var/TDK
        mv temp/*.config ../TDK_Package/var/TDK
        mv temp/*.sh ../TDK_Package/var/TDK
        if [ -f temp/netsrvmgr_test_module_pre-script.sh ]; then
            mv temp/netsrvmgr_test_module_pre-script.sh ../TDK_Package/var/TDK/scripts
        fi
    
        mv temp/* ../TDK_Package/usr/bin
        rm -rf temp
        cp -av ../$DIR_JSONRPC/build/lib/* ../TDK_Package/usr/lib >> $LOG_FILE 2>&1
    else
        cd $DIR_TDK
    fi

    cp -av ../json_temp/* ../TDK_Package/usr/lib/ >> $LOG_FILE 2>&1
    
    if [[ $FNCS_PACKAGE != "TRUE" ]];then
        #Copy all the shell scripts and config files along with tdk service
        cp agent/scripts/* ../TDK_Package/var/TDK
    else
	mkdir -p ../TDK_Package/opt/TDK/
	rm -rf ../TDK_Package/var/TDK/
	cp MediaPipelineTests_stub/tdk_mediapipelinetests* ../TDK_Package/usr/bin/
	cp FireboltCompliance_Validation/graphics_validation/Essos_TDKTestApp ../TDK_Package/usr/bin
        cp FireboltCompliance_Validation/graphics_validation/Westeros_TDKTestApp ../TDK_Package/usr/bin
	cp FireboltCompliance_Validation/scripts/RunGraphicsTDKTest.sh ../TDK_Package/opt/TDK
    fi

    if [ $SKIP_PLATFORM != "TRUE" ];then
	cd ../
        SRC_PLATFORM_VAR="SRC_PLATFORM_${PLATFORM}"
        SRC_PLATFORM=${!SRC_PLATFORM_VAR}
        platform_repo="${PLATFORM}_platform_repo"
        if [  ! -d $platform_repo  ];then
            git clone $SRC_PLATFORM $platform_repo >> $LOG_FILE 2>&1
        else
            echo "Packaging  using  existing $platform_repo  directory"
        fi
        cd $platform_repo

        if [ $IMAGE_TYPE == "VENDOR" ];then
            #Replace tdk_agent_monitor of ps -ef with pidof command
            TDKAgentMonitor_path="$(find . -type f -name TDKagentMonitor.sh)"
            sed -i  's/status=.*/status=`pidof tdk_agent_monitor`/g' $TDKAgentMonitor_path

            #Copy curl into package as Vendor build doesn't have curl
	    #cp ${SYSROOT}/usr/bin/curl ../TDK_Package/usr/bin
	    #cp ${SYSROOT}/usr/lib/libcurl* ../TDK_Package/usr/lib

	    #Add udhcpc command to make ip up
	    StartTDK_path="$(find . -type f -name StartTDK.sh)"
	    if  ! grep -q "udhcpc" $StartTDK_path;then
                echo "Adding udhcpc command in StartTDK.sh"
                sed -i '/export TDK_PATH=\/opt\/TDK/i \if [[ ! `ifconfig  eth0 | grep inet | awk "{print $2}" | head -n1 | cut -d : -f 2` ]];then \n     ifconfig eth0\n     udhcpc -i eth0\n     ifconfig eth0\nfi' $StartTDK_path
            fi
            if ! grep -q START_WESTEROS "$StartTDK_path";then
                echo "Adding START_WESTEROS"
                sed -i '/export TDK_PATH=\/opt\/TDK/i \export START_WESTEROS=1' $StartTDK_path
            fi
        fi

        scripts_path="$(dirname "$(find .  -type f -name StartTDK.sh)")"
	if [[ $FNCS_PACKAGE == "TRUE" ]];then
	    echo "Copying only TDK.env"
            cp $scripts_path/TDK.env ../TDK_Package/opt/TDK/
	else
            cp $scripts_path/* ../TDK_Package/var/TDK
	fi
        cd ..
    else
	PLATFORM=""
	echo "PLATFORM configuration skipped"
    fi

    if [[ $FNCS_PACKAGE != "TRUE" ]];then
        #Create symlink for all the shared libraries
        cd ${ROOT_DIR}/TDK_Package/usr/lib
        for file in lib*stub*;do 
            ln -s "$file" "${file%.0.0}";
        done
        cd ../../

        #Create link for binary files
        for file in usr/bin/* ; do 
    	    filename=$(basename $file); 
    	    ln -s /$file var/TDK/$filename; 
        done
	cd ../
    else
        cd ${ROOT_DIR}
    fi

    system_date=$(date)
    #formatted_date=$(echo "$system_date" | awk '{ printf "%02d%02d%04d\n", $3, (index("JanFebMarAprMayJunJulAugSepOctNovDec", $2)+2)/3, $6 }')
    formatted_date=$(echo "$system_date" | awk '{ printf "%02d%02d%04d_%02d%02d%02d\n", $3, (index("JanFebMarAprMayJunJulAugSepOctNovDec", $2)+2)/3, $6, substr($4,1,2), substr($4,4,2), substr($4,7,2) }')

        
    if [ -z $PLATFORM ];then
        if [[ $FNCS_PACKAGE == "TRUE" ]];then
	     PACKAGE_NAME="Generic_TDK_Package_FNCS_${IMAGE_TYPE}_${formatted_date}.tar.gz"
	else
	     PACKAGE_NAME="Generic_TDK_Package_${IMAGE_TYPE}_${formatted_date}.tar.gz"
	fi
    else
        if [[ $FNCS_PACKAGE == "TRUE" ]];then
	     PACKAGE_NAME="TDK_Package_FNCS_${PLATFORM}_${IMAGE_TYPE}_${formatted_date}.tar.gz"
        else
             PACKAGE_NAME="TDK_Package_${PLATFORM}_${IMAGE_TYPE}_${formatted_date}.tar.gz"
        fi	     
    fi
    tar -cvzf $PACKAGE_NAME -C TDK_Package . >> $LOG_FILE 2>&1
    if [ $? -eq 0 ]; then
        echo -e "\e[1;42m PACK TDK : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
        echo -e "\e[1;41m PACK TDK : FAILURE \e[0m \n" 2>&1 | tee -a $LOG_FILE
    fi
    rm -rf TDK_Package

}

# Function: urlencode
# Description: Encodes a given string into a URL-safe format.
# Parameters: $1 - String to encode
# Return: Encoded string
urlencode() {
    local length="${#1}"
    for (( i = 0; i < length; i++ )); do
        local c="${1:i:1}"
        case "$c" in
            [a-zA-Z0-9._-]) printf "$c" ;;
            *) printf '%%%02X' "'$c"
        esac
    done
}

# Function: sleep_bar
# Description: Displays a progress bar for time-based delays.
# Parameters: None
# Return: None
sleep_bar()
{
   total_duration=1
   num_iterations=100
   delay=$(echo "scale=3; $total_duration / $num_iterations" | bc)  # Calculate delay in seconds with 3 decimal places

   for ((i=0; i<num_iterations; i++)); do
       printf "-"
       sleep $delay
   done
echo 
}

# Function: cleanup
# Description: Cleans up temporary files and directories before exiting.
# Parameters: None
# Return: None
cleanup()
{
    echo -e "Removing all the directories before exiting\n" 2>&1 | tee -a $LOG_FILE
    cd $ROOT_DIR
    cd -
    rm -rf $ROOT_DIR/tdkv/temp
    rm -rf $ROOT_DIR/tdkv/RDK_Source
    if [ $? -eq 0 ]; then
        echo -e "\e[1;42m REMOVE SOURCE CODE : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
        echo -e "\e[1;41m REMOVE SOURCE CODE : FAILURE \e[0m \n" 2>&1 | tee -a $LOG_FILE
    fi
}

# Function: exit_cleanup
# Description: Handles cleanup on script exit and prints appropriate messages.
# Parameters: $1 - Optional signal that caused exit
# Return: None
exit_cleanup()
{
    exit_status=$?
    local exit_signal="$1"
    if [ -n "$exit_signal" ]; then
	echo -e "\n\e[1;31m ABORTED BY USER\e[0m \n" 2>&1 | tee -a $LOG_FILE
    elif [ $exit_status -ne 0 ]; then
        echo -e "\e[1;41m COMPILING TDK IS ABORTED \e[0m \n" 2>&1 | tee -a $LOG_FILE
        echo -e "Please check \e[1;31m$LOG_FILE \e[0mfor more information \n"
    else
	echo -e "\e[1;42m TDK HAS BEEN COMPILED AND PACKED SUCCESSFULLY \e[0m \n" 2>&1 | tee -a $LOG_FILE
	echo -e "Please check of \e[1;31m$PACKAGE_NAME\e[0m in the folder\n" 2>&1 | tee -a $LOG_FILE
	echo -e "Please check \e[1;31m$LOG_FILE \e[0mfor more information \n"
    fi
    cleanup
}

trap exit_cleanup EXIT
trap 'exit_cleanup SIGINT; kill -INT $$' INT
set -e

sleep_bar
download_source_code
sleep_bar
install_sdk
sleep_bar
if [ $SKIP_PACKAGES != "TRUE" ];then
    compile_JSONCPP
    sleep_bar
    setup_CURL
    sleep_bar
    compile_JSONRPC
    sleep_bar
    compile_TINYXML2
    sleep_bar
    compile_ZLIB
    sleep_bar
    update_m4
    compile_XKBCOMMON
    sleep_bar
    install_gstreamer_glib
    sleep_bar
fi
clone_tdk
compile_skeleton_libraries
compile_tdkv
sleep_bar
modify_tdk_files
pack_tdkv
sleep_bar
