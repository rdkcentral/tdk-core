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

if [ "${DEBUG:-0}" = "1" ]; then
    echo "Running as: $(whoami)"
    echo "HOME: $HOME"
    echo "netrc exists? $(ls -l $HOME/.netrc 2>/dev/null)"
fi

#meta layers
SRC_META_RDK_VIDEO="https://github.com/rdkcentral/meta-rdk-video.git"

#Git repositories
SRC_CURL="https://curl.se/download/curl-7.82.0.tar.xz"
SRC_JSONRPC="https://github.com/cinemast/libjson-rpc-cpp.git"
SRC_JSONCPP="https://github.com/open-source-parsers/jsoncpp/archive/refs/tags/1.8.4.tar.gz"
SRC_TINYXML2="https://github.com/leethomason/tinyxml2.git"
SRC_TDK="https://github.com/rdkcentral/tdk-video.git"
SRC_ZLIB="https://sourceforge.net/projects/libpng/files/zlib/1.2.11/zlib-1.2.11.tar.xz"
SRC_ASSIMP="https://github.com/assimp/assimp.git"

#HAL source
#SRC_WIFI="https://github.com/rdkcentral/rdkv-halif-wifi.git"
SRC_WIFI="https://code.rdkcentral.com/r/rdk/components/generic/wifi"
SRC_POWERMGR_HAL="https://github.com/rdkcentral/rdk-halif-power_manager.git"
SRC_DEEPSLEEP_HAL="https://github.com/rdkcentral/rdk-halif-deepsleep_manager.git"
SRC_DS_HAL="https://github.com/rdkcentral/rdk-halif-device_settings.git"
SRC_HDMICEC_HAL="https://github.com/rdkcentral/rdk-halif-hdmi_cec.git"
SRC_BLUETOOTH_HAL="https://code.rdkcentral.com/r/rdk/components/generic/bluetooth"
SRC_IARMMGRS="https://github.com/rdkcentral/iarmmgrs.git"
SRC_WESTEROS="https://code.rdkcentral.com/r/components/opensource/westeros"
SRC_EGL="https://github.com/raspberrypi/userland.git"
SRC_RMF_AUDIO_CAPTURE="https://github.com/rdkcentral/rdk-halif-rmf_audio_capture.git"
SRC_STORAGE_MGR="https://code.rdkcentral.com/r/rdk/components/generic/storagemanager"
#SRC_STORAGE_MGR="git@github.com:rdk-e/storagemanager.git"
SRC_NETSRVMGR="https://code.rdkcentral.com/r/rdk/components/generic/netsrvmgr"
#SRC_NETSRVMGR="git@github.com:rdk-e/netsrvmgr.git"
SRC_HDMICEC="https://github.com/rdkcentral/hdmicec.git"
SRC_IARMBUS="https://github.com/rdkcentral/iarmbus.git"
SRC_XKBCOMMON="http://xkbcommon.org/download/libxkbcommon-0.5.0.tar.xz"
SRC_DS="https://github.com/rdkcentral/devicesettings"
SRC_CJSON="https://github.com/DaveGamble/cJSON.git"
SRC_UTIL_LINUX="https://github.com/util-linux/util-linux.git"
SRC_RDKFWUPDATER="https://github.com/rdkcentral/rdkfwupdater.git"
SRC_COMMONUTILITIES="https://github.com/rdkcentral/common_utilities.git"
SRC_LIBSYSWRAPPER="https://github.com/rdkcentral/libSyscallWrapper.git"
SRC_MIDDLEWARE_SUPPORT="https://github.com/rdkcentral/meta-middleware-generic-support.git"
SRC_RDKLOGGER="https://github.com/rdkcentral/rdk_logger.git"
SRC_AAMP="https://github.com/rdkcentral/aamp.git"
SRC_RFC="https://github.com/rdkcentral/rfc.git"
SRC_WDMP_C="https://github.com/xmidt-org/wdmp-c.git"
SRC_RFCAPI="https://github.com/rdkcentral/rfc.git"
SRC_VULKAN_HEADER="https://github.com/KhronosGroup/Vulkan-Headers.git"
SRC_VULKAN_TOOLS="https://github.com/KhronosGroup/Vulkan-Tools.git"

#Platformwise repositories
SRC_RPI4="https://code.rdkcentral.com/r/rdk/devices/raspberrypi/tdk"

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
DIR_TDK="tdk-video"

ROOT_DIR=$PWD
mkdir -p logs
mkdir -p json_temp
TDK_SOURCE_DIR=${ROOT_DIR}/${DIR_TDK}
COMPILE_SKELETON=false
SYSROOT=${ROOT_DIR}/sysroots
SKIP_PLATFORM="FALSE"
SKIP_PACKAGES="FALSE"
INSTALLED_VULKAN_HEADERS="FALSE"
vkmark_compiled="FALSE"
vkcube_compiled="FALSE"

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
elif [[ "$PLATFORM_GIVEN" == "RPI4" ]];then
    PLATFORM="RPI4"
elif [[ "$PLATFORM_GIVEN" == "REALTEK" ]];then
    PLATFORM="REALTEK"
else
    SKIP_PLATFORM="TRUE"
    PLATFORM=""
fi


config=configure.txt
. $config

for arg in "$@"; do
    if [ "$arg" == "--npvs-package" ]; then
        echo "Creating only NPVS_PACKAGE"
	NPVS_PACKAGE="TRUE"
    fi
done

#Enabling NPVS Package Flag as rdkfwupgrader compilation is disabled
NPVS_PACKAGE="TRUE"

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

REQUIRED_PACKAGES="libtool m4 autoconf build-essential automake"
for REQUIRED_PKG in $REQUIRED_PACKAGES; do
    PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
    if [ -z "$PKG_OK" ]; then
        echo "No $REQUIRED_PKG"
        echo "Please install using below command and then continue running the shell script\nsudo apt-get install $REQUIRED_PKG"
        exit
    fi
done

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

get_middleware_support_version() {

    local middleware_version="$1"
    local base_dir="$(pwd)"
    local mw_manifest_repo="https://github.com/rdkcentral/middleware-manifest-rdke"
    local generic_manifest_repo="https://github.com/rdkcentral/rdke-middleware-generic-manifest"

    local generic_version
    local support_version

    echo "Resolving meta-middleware-generic-support version for middleware ${middleware_version}"

    #########################################
    # Step 1: Clone middleware-manifest-rdke
    #########################################

    git clone "$mw_manifest_repo" middleware-manifest-rdke >/dev/null 2>&1 || return 1
    cd middleware-manifest-rdke || return 1

    git checkout "$middleware_version" >/dev/null 2>&1 || {
        echo "Invalid middleware version: $middleware_version"
        cd "$base_dir"
        rm -rf middleware-manifest-rdke
        return 1
    }

    #########################################
    # Step 2: Extract generic manifest tag
    #########################################

    generic_version=$(grep 'rdke-middleware-generic-manifest' rdke-middleware.xml \
        | sed -n 's/.*revision="refs\/tags\/\([^"]*\)".*/\1/p')

    cd "$base_dir"
    rm -rf middleware-manifest-rdke

    if [[ -z "$generic_version" ]]; then
        echo "Failed to resolve generic manifest version"
        return 1
    fi

    #########################################
    # Step 3: Clone generic manifest
    #########################################

    git clone "$generic_manifest_repo" rdke-middleware-generic-manifest >/dev/null 2>&1 || return 1
    cd rdke-middleware-generic-manifest || return 1

    git checkout "$generic_version" >/dev/null 2>&1 || {
        echo "Invalid generic manifest version: $generic_version"
        cd "$base_dir"
        rm -rf rdke-middleware-generic-manifest
        return 1
    }

    #########################################
    # Step 4: Extract meta-middleware-generic-support version
    #########################################

    middleware_support_version=$(grep 'meta-middleware-generic-support' middleware-generic.xml \
        | sed -n 's/.*revision="refs\/tags\/\([^"]*\)".*/\1/p')

    cd "$base_dir"
    rm -rf rdke-middleware-generic-manifest

    if [[ -z "$middleware_support_version" ]]; then
        echo "Failed to resolve meta-middleware-generic-support version"
        return 1
    fi

    echo "meta-middleware-generic-support version obtained as $middleware_support_version"
}

get_component_versions()
{
    cd $TDK_SOURCE_DIR
    get_middleware_support_version "$MIDDLEWARE_VERSION"
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
    git checkout $middleware_support_version >> $LOG_FILE 2>&1

    iarmbus_srcrev=`grep iarmbus conf/include/generic-srcrev.inc | cut -d "=" -f 2`
    iarmbus_srcrev=${iarmbus_srcrev//\"/}
    iarmbus_srcrev=${iarmbus_srcrev// /}
    echo "iarmbus_srcrev = $iarmbus_srcrev"

    hdmicec_srcrev=`grep hdmicec conf/include/generic-srcrev.inc | grep -v hdmicecheader | cut -d "=" -f 2`
    hdmicec_srcrev=${hdmicec_srcrev//\"/}
    hdmicec_srcrev=${hdmicec_srcrev// /}
    echo "hdmicec_srcrev = $hdmicec_srcrev"

    iarmmgrs_srcrev=`grep iarmmgrs conf/include/generic-srcrev.inc | cut -d "=" -f 2 | head -n1`
    iarmmgrs_srcrev=${iarmmgrs_srcrev//\"/}
    iarmmgrs_srcrev=${iarmmgrs_srcrev// /}
    echo "iarmmgrs_srcrev = $iarmmgrs_srcrev"

    aamp_srcrev=`grep aamp conf/include/generic-srcrev.inc | cut -d "=" -f 2`
    aamp_srcrev=${aamp_srcrev//\"/}
    aamp_srcrev=${aamp_srcrev// /}
    echo "aamp_srcrev = $aamp_srcrev"

    device_settings_srcrev=`grep devicesettings conf/include/generic-srcrev.inc | cut -d "=" -f 2`
    device_settings_srcrev=${device_settings_srcrev//\"/}
    device_settings_srcrev=${device_settings_srcrev// /}
    echo "device_settings_srcrev = $device_settings_srcrev"

    common_utilities_srcrev=`grep commonutilities conf/include/generic-srcrev.inc | cut -d "=" -f 2`
    common_utilities_srcrev=${common_utilities_srcrev//\"/}
    common_utilities_srcrev=${common_utilities_srcrev// /}
    echo "common_utilities_srcrev = $common_utilities_srcrev"

    rdkfw_srcrev=`grep rdkfw conf/include/generic-srcrev.inc | cut -d "=" -f 2`
    rdkfw_srcrev=${rdkfw_srcrev//\"/}
    rdkfw_srcrev=${rdkfw_srcrev// /}
    echo "rdkfw_srcrev = $rdkfw_srcrev"

    rfc_srcrev=`grep rfc conf/include/generic-srcrev.inc | cut -d "=" -f 2`
    rfc_srcrev=${rfc_srcrev//\"/}
    rfc_srcrev=${rfc_srcrev// /}
    echo "rfc_srcrev = $rfc_srcrev"

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
    header_file_status="$(find $SYSROOT -iname tinyxml2.h)"
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

# Function: install_packages
# Description: Installs headers/libraries from external package.
# Parameters: None
# Return: None
install_packages()
{
    cd $ROOT_DIR
    Packages="$(find $ROOT_DIR -iname Packages.tgz)"
    if [  -z "$Packages" ];then
	echo -e "Packages.tgz not found"
	exit 1
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
    glib_h="$(find $SDKTARGETSYSROOT -iname glibconfig.h)"
    if [ ! -z "${glib_2_0_package}" ] && [  -z "${glib_h}" ]; then
	echo -e "Copying glib-2.0 headers and libraries\n" 2>&1 | tee -a $LOG_FILE
	cd $SDKTARGETSYSROOT
        cp -u $glib_2_0_package $SDKTARGETSYSROOT
        glib_2_0_package_name=$(basename "$glib_2_0_package")
        tar -xf $glib_2_0_package_name
	rm $SDKTARGETSYSROOT/$glib_2_0_package_name
    fi
    libffi_package="$(find $ROOT_DIR -iname libffi.tgz)"
    libffi_lib="$(find $SDKTARGETSYSROOT -iname libffi.pc)"
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
    wayland_protocols_package="$(find $ROOT_DIR -iname wayland_protocols.tgz)"
    wayland_protocols_pkgconfig="$(find $SDKTARGETSYSROOT -iname wayland-protocols.pc)"
    if [ -z "${wayland_protocols_pkgconfig}" ]; then
        echo -e "Copying wayland protocols\n" 2>&1 | tee -a $LOG_FILE
        cd $SDKTARGETSYSROOT
        cp -u $wayland_protocols_package $SDKTARGETSYSROOT/usr/share/
        wayland_protocols_package_name=$(basename "$wayland_protocols_package")
	cd usr/share
        tar -xf $wayland_protocols_package_name
        find $SDKTARGETSYSROOT -iname wayland-protocols.pc
        rm $SDKTARGETSYSROOT/usr/share/$wayland_protocols_package_name
    fi
    glm_package="$(find $ROOT_DIR -iname glm.tgz)"
    glm_pkgconfig="$(find $SDKTARGETSYSROOT -iname glm.pc)"
    if [ -z "${glm_pkgconfig}" ]; then
        echo -e "Copying glm\n" 2>&1 | tee -a $LOG_FILE
        cd $SDKTARGETSYSROOT
        cp -u $glm_package $SDKTARGETSYSROOT
        glm_package_name=$(basename "$glm_package")
	echo -e "Untarring $glm_package_name"
        tar -xf $glm_package_name
        rm $SDKTARGETSYSROOT/$glm_package_name
    fi
    vulkan_loader_package="$(find $ROOT_DIR -iname vulkan_loader.tgz)"
    vulkan_loader_pkgconfig="$(find $SDKTARGETSYSROOT -iname vulkan.pc)"
    if [ -z "${vulkan_loader_pkgconfig}" ]; then
        echo -e "Copying vulkan_loader\n" 2>&1 | tee -a $LOG_FILE
        cd $SDKTARGETSYSROOT
        cp -u $vulkan_loader_package $SDKTARGETSYSROOT
        vulkan_loader_package_name=$(basename "$vulkan_loader_package")
        echo -e "Untarring $vulkan_loader_package_name"
        tar -xf $vulkan_loader_package_name
        rm $SDKTARGETSYSROOT/$vulkan_loader_package_name
    fi
    pcreposix_package="$(find $ROOT_DIR -iname additional_libs.tgz)"
    pcreposix_lib="$(find $SDKTARGETSYSROOT -iname libpcrecpp.so)"
    if [ ! -z "${pcreposix_package}" ] && [ -z "${pcreposix_lib}" ]; then
	echo -e "Copying additional_libs \n" 2>&1 | tee -a $LOG_FILE
	cd $SDKTARGETSYSROOT
	cp $pcreposix_package $SDKTARGETSYSROOT
	pcreposix_package_name=$(basename "$pcreposix_package")
	tar -xf $pcreposix_package_name
	cd $SDKTARGETSYSROOT/additional_libs/usr/lib
	cp * $SDKTARGETSYSROOT/usr/lib/
	cd $SDKTARGETSYSROOT/additional_libs/lib
	cp * $SDKTARGETSYSROOT/lib
	rm -rf $SDKTARGETSYSROOT/additional_libs
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

# Function: compile_assimp
# Description: Compiles assimp library and installs it in sysroot.
# Parameters: None
# Return: None
compile_assimp()
{
    echo -e "Checking if assimp is installed in SDK\n"
    echo "$SYSROOT/usr/lib/pkgconfig/assimp.pc"
    if [  -f "$SYSROOT/usr/lib/pkgconfig/assimp.pc" ]; then
	echo -e "\e[1;42m COMPILE assimp : SKIPPED \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
	rm -rf assimp
	git clone $SRC_ASSIMP >> $LOG_FILE 2>&1
	cd assimp
	git checkout 8f0c6b04b2257a520aaab38421b2e090204b69df  >> $LOG_FILE 2>&1
	rm -rf build
	mkdir build
	cd build 
	cmake .. \
	     -DCMAKE_INSTALL_PREFIX=/usr \
	     -DASSIMP_BUILD_ASSIMP_TOOLS=OFF -DASSIMP_BUILD_TESTS=OFF >> $LOG_FILE 2>&1
        make -j$(nproc) >> $LOG_FILE 2>&1
	$STRIP code/libassimp.so.5.0.0
	DESTDIR=${SYSROOT} make install >> $LOG_FILE 2>&1
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
    git checkout c696f6932113b81cd20cd4a34fdb1808e773f23e >> $LOG_FILE 2>&1
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
        cp build/lib/libjsonrpccpp-*.so.1.3.0 $SYSROOT/usr/lib
        cp -r src/jsonrpccpp $SYSROOT/usr/include/
        ln -s $SYSROOT/usr/lib/libjsonrpccpp-server.so.1.3.0 $SYSROOT/usr/lib/libjsonrpccpp-server.so
        ln -s $SYSROOT/usr/lib/libjsonrpccpp-client.so.1.3.0 $SYSROOT/usr/lib/libjsonrpccpp-client.so
        ln -s $SYSROOT/usr/lib/libjsonrpccpp-common.so.1.3.0 $SYSROOT/usr/lib/libjsonrpccpp-common.so
    fi
    if [ ! -f "$SYSROOT/usr/include/jsonrpccpp" ]; then
	mkdir -p $SYSROOT/usr/include/jsonrpccpp/server/connectors
	mkdir -p $SYSROOT/usr/include/jsonrpccpp/client/connectors
	mkdir -p $SYSROOT/usr/include/jsonrpccpp/common
	cp build/gen/jsonrpccpp/common/jsonparser.h $SYSROOT/usr/include/ 
	cp build/gen/jsonrpccpp/common/jsonparser.h $SYSROOT/usr/include/jsonrpccpp/common/
	cp src/jsonrpccpp/common/*.h $SYSROOT/usr/include/jsonrpccpp/common
        cp src/jsonrpccpp/*.h $SYSROOT/usr/include/jsonrpccpp/
        cp src/jsonrpccpp/server/*.h $SYSROOT/usr/include/jsonrpccpp/server
        cp src/jsonrpccpp/server/connectors/*.h $SYSROOT/usr/include/jsonrpccpp/server/connectors/
        cp src/jsonrpccpp/client/*.h $SYSROOT/usr/include/jsonrpccpp/client
        cp src/jsonrpccpp/client/connectors/*.h $SYSROOT/usr/include/jsonrpccpp/client/connectors/
    fi
    cd ../
}

# Function: clone_tdk
# Description: Clones the TDK repository from the source.
# Parameters: None
# Return: None
clone_tdk()
{
	if [  ! -d $DIR_TDK ];then
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
	if [ "$header_file_custom_path" == "current_dir" ];then
            header_file_custom_path=""
        fi
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
    COMPILE_DUMMY_LIBS="WiFiHal PowerMgrHal DeepSleepHal DSHal IARMBus HdmiCec Bluetooth MfrHal WesterosHal Essos AudioCaptureMgr Graphics AAMP"
    COMPILE_DUMMY_LIBS="$COMPILE_DUMMY_LIBS common_utilities rdklogger DeviceSettings IARMBus libsyswrapper NetSrvMgr "
    COMPILE_DUMMY_LIBS="cJSON common_utilities libsyswrapper rdklogger Graphics WesterosHal Essos wdmp rfcapi DSHal"
    if [[ $NPVS_PACKAGE == "TRUE" ]];then
	COMPILE_DUMMY_LIBS="Graphics WesterosHal Essos DSHal"
    fi
    got_versions=false
    if ! $got_versions;then
         echo -e "Getting versions"
         get_component_versions
         got_versions=true
    fi
    mkdir -p ${TDK_SOURCE_DIR}/RDK_Source
    if [[ $COMPILE_DUMMY_LIBS == "*IARMBus*" ]];then
        clone_and_move $SRC_IARMBUS $iarmbus_srcrev "iarmbus" "core/include"
        clone_and_move $SRC_IARMBUS $iarmbus_srcrev "iarmbus" "core"
    fi
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
		 if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
	             cd iarmmgrs;
                     git checkout $iarmmgrs_srcrev >> $LOG_FILE 2>&1
		     cd ..
                 fi

                 mv iarmmgrs iarmmgrs_source
		 cp ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source/hal/include/pwrMgr.h $SYSROOT/usr/include
		 cp ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source/mfr/include/mfr_temperature.h $SYSROOT/usr/include
		 cp ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source/mfr/include/mfrTypes.h ${SYSROOT}/usr/include/
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
	    cp iarmmgrs_source/hal/include/therm_mon.h $SYSROOT/usr/include
            cp iarmmgrs_source/hal/include/therm_mon.h ${TDK_SOURCE_DIR}/PowerMgrHal
            rm -rf ${TDK_SOURCE_DIR}/RDK_Source/iarmmgrs_source
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
        fi
        if [[ $COMPONENT == "Bluetooth" ]];then
            clone_and_move $SRC_BLUETOOTH_HAL $SRC_BLUETOOTH_HAL_HEADER_REVISION $COMPONENT "BLE_HAL_LIB_VERSION"
        fi
        if [[ $COMPONENT == "MfrHal" ]];then
            clone_and_move $SRC_IARMMGRS $SRC_IARMMGRS_HAL_HEADER_REVISION $COMPONENT "MFR_HAL_LIB_VERSION" "mfr/include/"
        fi
        if [[ $COMPONENT == "Graphics" ]];then
            #Installing EGL headers for Essos Compilation
            cd ${TDK_SOURCE_DIR}/RDK_Source
            git clone $SRC_EGL >> $LOG_FILE 2>&1
            repo_name=$(basename "$SRC_EGL" .git)
	    cd $repo_name
	    git checkout c4fd1b8986c6d6d4ae5cd51e65a8bbeb495dfa4e  >> $LOG_FILE 2>&1
            mkdir -p $SYSROOT/usr/include/EGL
            mkdir -p $SYSROOT/usr/include/KHR
	    mkdir -p $SYSROOT/usr/include/GLES2
            sudo cp  ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/interface/khronos/include/EGL/*.h $SYSROOT/usr/include/EGL/
	    sudo cp  -r ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/interface $SYSROOT/usr/include/
            sudo cp  ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/interface/khronos/include/KHR/khrplatform.h $SYSROOT/usr/include/KHR/
	    sudo cp  ${TDK_SOURCE_DIR}/RDK_Source/$repo_name/interface/khronos/include/GLES2/*.h $SYSROOT/usr/include/GLES2
            rm -rf ${TDK_SOURCE_DIR}/RDK_Source/$repo_name
	fi
	if [[ $COMPONENT == "Essos" ]];then
            clone_and_move $SRC_WESTEROS $SRC_WESTEROS_HAL_HEADER_REVISION $COMPONENT "ESSOS_LIB_VERSION" "essos/"
        fi
        if [[ $COMPONENT == "WesterosHal" ]];then
            if [[ $PLATFORM == "BROADCOM" ]];then
                clone_and_move $SRC_WESTEROS $SRC_WESTEROS_HAL_HEADER_REVISION "WesterosHal_BRCM" "WESTEROS_LIB_VERSION" "brcm/westeros-gl"
		sudo cp -r ${TDK_SOURCE_DIR}/RDK_Source/westeros_source/test/brcm-em/include/wayland-egl.h $SYSROOT/usr/include/
            else
                clone_and_move $SRC_WESTEROS $SRC_WESTEROS_HAL_HEADER_REVISION "WesterosHal_DRM" "WESTEROS_LIB_VERSION" "drm/westeros-gl"
		sudo cp -r ${TDK_SOURCE_DIR}/RDK_Source/westeros_source/test/drm-em/include/wayland-egl.h $SYSROOT/usr/include/
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
		sudo cp -r ${TDK_SOURCE_DIR}/RDK_Source/westeros_source/test/brcm-em/include/*.h $SYSROOT/usr/include/
	    else
		sudo cp -r ${TDK_SOURCE_DIR}/RDK_Source/westeros_source/test/drm-em/include/*.h $SYSROOT/usr/include/
	    fi
	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
            make  >> $LOG_FILE 2>&1
            #find and delete GLESv2 wayland-egl EGL
            sudo mv *.so* $SYSROOT/usr/lib/
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
	    git clone $SRC_AAMP
	    mv aamp aamp_source
	    cd aamp_source
            if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
                git checkout $aamp_srcrev >> $LOG_FILE 2>&1
            fi
            cd ..
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

	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
            make >> $LOG_FILE 2>&1
            sudo mv *.so* $SYSROOT/usr/lib/
	fi
	if [[ $COMPONENT == "cJSON" ]];then
	    cd ${TDK_SOURCE_DIR}/RDK_Source/
	    git clone $SRC_CJSON >> $LOG_FILE 2>&1
	    mkdir -p $SYSROOT/usr/include/cjson
	    cp cJSON/*.h $SYSROOT/usr/include/cjson
	fi
	if [[ $COMPONENT == "Util_linux" ]];then
            cd ${TDK_SOURCE_DIR}/RDK_Source/
	    git clone $SRC_UTIL_LINUX >> $LOG_FILE 2>&1
	    sudo mkdir -p $SYSROOT/usr/include/uuid
	    sudo cp util-linux/libuuid/src/uuid.h $SYSROOT/usr/include/uuid  
	fi
	if [[ $COMPONENT == "DeviceSettings" ]];then
	    cd ${TDK_SOURCE_DIR}/RDK_Source
	    git clone $SRC_DS
            mv devicesettings devicesettings_source
	    cd devicesettings_source
	    if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
                git checkout $device_settings_srcrev
            fi
	    cd ..
	    sudo cp devicesettings_source/ds/include/*.hpp $SYSROOT/usr/include/
	    sudo cp devicesettings_source/ds/*.hpp $SYSROOT/usr/include/
	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
            make DS_LIB_VERSION=${DS_LIB_VERSION} >> $LOG_FILE 2>&1
	    sudo mv *.so* $SYSROOT/usr/lib/
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
	if [[ $COMPONENT == "wdmp" ]];then
	    echo "Compiling wdmp"
	    git clone $SRC_WDMP_C wdmp-c_source >> $LOG_FILE 2>&1
            cd wdmp-c_source/
            git checkout f9f687b6b4b10c2b72341e792a64334f0a409848 >> $LOG_FILE 2>&1
            git clone $SRC_META_RDK_VIDEO
            if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
                cd meta-rdk-video
                git checkout $MIDDLEWARE_VERSION
                cd ..
            fi
            cp meta-rdk-video/recipes-support/wdmp-c/files/wdmp-c.patch .
            patch -p1 < wdmp-c.patch
            mkdir -p "$SYSROOT/usr/include/wdmp-c"
            find . -type f -name "wdmp-c.h" -exec cp {} "$SYSROOT/usr/include/wdmp-c" \;
            cd ..; rm -rf wdmp-c_source/
	fi
	if [[ $COMPONENT == "rfcapi" ]];then
	    echo "Compiling rfcapi"
	    cd ${TDK_SOURCE_DIR}/RDK_Source
	    git clone $SRC_RFCAPI rfcapi_source >> $LOG_FILE 2>&1
	    cd rfcapi_source/
	    git checkout $rfc_srcrev
	    cp rfcapi/rfcapi.h $SYSROOT/usr/include/

	    cd ${TDK_SOURCE_DIR}/RDK_Libraries/$COMPONENT
	    make RFCAPI_LIB_VERSION=${RFCAPI_LIB_VERSION} >> $LOG_FILE 2>&1
	    mv *.so* $SYSROOT/usr/lib/
	fi
    done
    rm -rf  ${TDK_SOURCE_DIR}/RDK_Source
}

parse_vkmark_bb() {
    local bbfile="$1"

    if [ ! -f "$bbfile" ]; then
        echo "Error: $bbfile not found"
        return 1
    fi

    # Extract SRC_URI git URL
    local repo
    repo=$(grep -E '^SRC_URI\s*=' "$bbfile" \
        | sed -E 's/.*git:\/\/([^;"]+).*/https:\/\/\1/')

    # Extract SRCREV (handles ?= or =)
    local srcrev
    srcrev=$(grep -E '^SRCREV' "$bbfile" \
        | sed -E 's/.*"([^"]+)".*/\1/')

    # Export variables
    SRC_VKMARK="${repo}"
    SRCREV_VKMARK="${srcrev}"

    export SRC_VKMARK
    export SRCREV_VKMARK

    echo "SRC_VKMARK=\"${SRC_VKMARK}\""
    echo "SRCREV_VKMARK=\"${SRCREV_VKMARK}\""
}

parse_project_line() {
    local line="$1"

    local name
    local revision
    local remote
    local tag
    local repo_url
    local repo_short_name

    # Extract attributes
    name=$(echo "$line" | sed -n 's/.*name="\([^"]*\)".*/\1/p')
    revision=$(echo "$line" | sed -n 's/.*revision="\([^"]*\)".*/\1/p')
    remote=$(echo "$line" | sed -n 's/.*remote="\([^"]*\)".*/\1/p')

    # Normalize revision
    case "$revision" in
        refs/tags/*)
            tag="${revision#refs/tags/}"
            ;;
        refs/heads/*)
            tag="${revision#refs/heads/}"
            ;;
        *)
            tag="$revision"
            ;;
    esac

    # Repo short name (last part after /)
    repo_short_name="${name##*/}"

    # Build repo URL
    case "$remote" in
        rdkcentral)
            repo_url="https://github.com/rdkcentral/${repo_short_name}"
            ;;
        cmf)
            repo_url="https://code.rdkcentral.com/r/${name}"
            ;;
        *)
            echo "Unknown remote: $remote"
            return 1
            ;;
    esac

    # Return pipe-separated values
    echo "${repo_short_name}|${tag}|${repo_url}"
}

compile_vkmark()
{
    echo -e "Compiling vkmark\n"
    cd "$ROOT_DIR"
    rm -rf vkmark

    vkmark_sourceCode_set="FALSE"

    if [[ -z "$PLATFORM" ]];then
	echo "NO PLATFORM is selected for vkmark compilation"
	echo "Setting PLATFORM to RPI4"
	PLATFORM="RPI4"
    fi

    echo "Compiling vkmark for $PLATFORM platform"

    ############################################
    # Platform Vendor Manifest
    ############################################

    case "$PLATFORM" in
        RPI4)
            VENDOR_MANIFEST_REPO=$RPI_VENDOR_MANIFEST_REPO
            VENDOR_VERSION="$RPI_VENDOR_VERSION"
	    SOC_OSS_REPO="meta-oss-vendor-raspberrypi"
	    MAX_SOC_OSS_VERSION="4.1.3"
            ;;
        REALTEK)
            VENDOR_MANIFEST_REPO=$REALTEK_VENDOR_MANIFEST_REPO
            VENDOR_VERSION="$REALTEK_VENDOR_VERSION"
	    SOC_OSS_REPO="meta-rdk-soc-realtek"
	    MAX_SOC_OSS_VERSION="2.4.4"
            ;;
	BROADCOM)
	    VENDOR_MANIFEST_REPO=$BROADCOM_VENDOR_MANIFEST_REPO
            VENDOR_VERSION="$BROADCOM_VENDOR_VERSION"
            SOC_OSS_REPO="meta-vendor-rdke-broadcom-oss"
	    MAX_SOC_OSS_VERSION="3.3.2"
            ;;
        *)
            echo "Unsupported platform: $PLATFORM"
	    echo "PLATFORM needed for vkmark compilation"
            return 1
            ;;
    esac

    ############################################
    # Clone Vendor Manifest
    ############################################

    git clone $VENDOR_MANIFEST_REPO.git >> "$LOG_FILE" 2>&1
    REPO_NAME="${VENDOR_MANIFEST_REPO##*/}"
    VENDOR_MANIFEST_REPO=$REPO_NAME
    cd "$VENDOR_MANIFEST_REPO" || return 1

    if [[ "$VENDOR_VERSION" != "default" && -n "$VENDOR_VERSION" ]]; then
        git checkout "$VENDOR_VERSION" >> "$LOG_FILE" 2>&1
    fi

    ############################################
    # Parse OSS Vendor Repo + Tag
    ############################################

    oss_vendor_line=$(grep -r --exclude-dir=.git --include="*.xml" "$SOC_OSS_REPO" .)
    result=$(parse_project_line "$oss_vendor_line")

    OSS_VENDOR_REPO_NAME="${result%%|*}"
    tmp="${result#*|}"
    OSS_VENDOR_REPO_TAG="${tmp%%|*}"

    ####################################################################################
    # vkmark recipe is removed after MAX_SOC_OSS_VERSION version
    # Check if OSS_VENDOR_REPO_TAG obtained is less than or equal to MAX_SOC_OSS_VERSION
    # if greater, set OSS_VENDOR_REPO_TAG to MAX_SOC_OSS_VERSION
    ####################################################################################
    version_gt() {
        [ "$(printf '%s\n' "$1" "$2" | sort -V | tail -n1)" = "$1" ] && [ "$1" != "$2" ]
    }

    if version_gt "$OSS_VENDOR_REPO_TAG" "$MAX_SOC_OSS_VERSION"; then
        echo -e "vkmark is not available in $OSS_VENDOR_REPO_NAME - $OSS_VENDOR_REPO_TAG proceeding with $MAX_SOC_OSS_VERSION"
        OSS_VENDOR_REPO_TAG="$MAX_SOC_OSS_VERSION"
    fi

    OSS_VENDOR_REPO_URL="${result##*|}"

    cd ..
    rm -rf "$VENDOR_MANIFEST_REPO"

    ############################################
    # Clone OSS Vendor Repo
    ############################################

    echo -e "Proceeding with vkmark compilation for $PLATFORM with $OSS_VENDOR_REPO_NAME - $OSS_VENDOR_REPO_TAG"
    git clone ${OSS_VENDOR_REPO_URL}.git >> "$LOG_FILE" 2>&1
    cd "$OSS_VENDOR_REPO_NAME" 
    git checkout "$OSS_VENDOR_REPO_TAG" >> "$LOG_FILE" 2>&1

    ############################################
    # Locate vkmark Recipe
    ############################################

    vkmark_recipe_path=$(find . -iname vkmark_git.bb | head -n1)
    echo "vkmark recipe: $vkmark_recipe_path"

    parse_vkmark_bb "$vkmark_recipe_path"

    bbdir=$(dirname "$vkmark_recipe_path")
    cd "$bbdir" || return 1

    ############################################
    # Locate Patches
    ############################################

    patch_file=$(find . -iname "*.patch" | head -n1)

    if [[ -n "$patch_file" ]]; then
        vkmark_patches_dir=$(dirname "$patch_file")
	cd $vkmark_patches_dir
	vkmark_patches_dir=$(pwd)
        echo "vkmark patches dir: $vkmark_patches_dir"
    fi

    cd "$ROOT_DIR"

    ############################################
    # Clone Upstream vkmark
    ############################################

    git clone "$SRC_VKMARK" >> "$LOG_FILE" 2>&1
    cd vkmark || return 1
    git checkout "$SRCREV_VKMARK" >> "$LOG_FILE" 2>&1

    ############################################
    # Apply Patches (if any)
    ############################################

    if [[ ! -z "$vkmark_patches_dir" ]]; then
        cp $vkmark_patches_dir/*.patch . 2>/dev/null
        rm -rf "$ROOT_DIR/$OSS_VENDOR_REPO_NAME"

	# Collect any patch files; avoid iterating on a literal "*.patch" when none exist
        shopt -s nullglob
        patches=( *.patch )
        shopt -u nullglob
        if [ ${#patches[@]} -gt 0 ]; then
            for p in "${patches[@]}"; do
                echo "Applying $p"
                patch -p1 < "$p" >> "$LOG_FILE" 2>&1
            done
            echo "vkmark source code patched"
        fi
        vkmark_sourceCode_set="TRUE"
    else
        vkmark_sourceCode_set="TRUE"
    fi

    ############################################
    # Copy Vulkan headers into sysroot
    ############################################
    if [ $INSTALLED_VULKAN_HEADERS != "TRUE" ];then
        install_vulkan_headers
    fi
 
    ############################################
    # Build
    ############################################

    if [[ "$vkmark_sourceCode_set" == "TRUE" ]]; then

        meson build \
            --buildtype=release \
            --prefix=/usr \
            -Dwayland=true \
            -Dxcb=false \
            -Dkms=false >> "$LOG_FILE" 2>&1

        ninja -C build >> "$LOG_FILE" 2>&1

        vkmark_bin=$(find build -iname vkmark)

        if [[ -n "$vkmark_bin" ]]; then
            echo -e "\e[1;42m VKMARK COMPILATION : SUCCESS \e[0m" | tee -a "$LOG_FILE"

            mkdir -p vkmark_bins/usr/bin
            cp build/src/vkmark vkmark_bins/usr/bin

            mkdir -p vkmark_bins/usr/lib/vkmark
            cp build/src/*.so vkmark_bins/usr/lib/vkmark/
	    #Copy libassimp as well
	    cp $SYSROOT/usr/lib/libassimp.so.5.0.0 vkmark_bins/usr/lib/
	    cd vkmark_bins/usr/lib
	    ln -sf libassimp.so.5.0.0 libassimp.so.5
	    cd ../../..
 
            mkdir -p vkmark_bins/usr/share/vkmark
            cp -r data/models vkmark_bins/usr/share/vkmark/
            cp -r data/shaders vkmark_bins/usr/share/vkmark/
            cp -r data/textures vkmark_bins/usr/share/vkmark/


            cd vkmark_bins
            tar -cjf vkmark_${PLATFORM}.tgz *
            cp vkmark_${PLATFORM}.tgz "$ROOT_DIR"

            cd "$ROOT_DIR"
            rm -rf vkmark
	    vkmark_compiled="TRUE"
        else
            echo -e "\e[1;41m VKMARK COMPILATION : FAILURE \e[0m" | tee -a "$LOG_FILE"
	    exit 1
        fi
    fi
}

############################################
# Copy Vulkan headers into sysroot
############################################
install_vulkan_headers() {
    git clone $SRC_VULKAN_HEADER vulkan_source >> "$LOG_FILE" 2>&1
    cd vulkan_source/
    VAR_VULKAN_VERSION=${PLATFORM}_VULKAN_VERSION
    VULKAN_VERSION="${!VAR_VULKAN_VERSION}"
    VULKAN_VOLK_REQUIRED="false"
    echo "VULKAN HEADER VERSION OBTAINED as $VULKAN_VERSION"
    case "$VULKAN_VERSION" in
        "1.3.247")
              vulkan_header_srcrev="95a13d7b7118d3824f0ef236bb0438d9d51f3634"
              ;;
        "1.3.204")
              vulkan_header_srcrev="1dace16d8044758d32736eb59802d171970e9448"
              ;;
        "1.3.296")
              vulkan_header_srcrev="29f979ee5aa58b7b005f805ea8df7a855c39ff37"
              VULKAN_VOLK_REQUIRED="true"
              ;;
                *)
              echo "Unsupported Vulkan version: $VULKAN_VERSION"
              exit 1
              ;;
    esac
    git checkout $vulkan_header_srcrev >> "$LOG_FILE" 2>&1
    cp -r include/vulkan $SDKTARGETSYSROOT/usr/include/
    cp -r include/vk_video $SDKTARGETSYSROOT/usr/include/
    mkdir -p $SDKTARGETSYSROOT/usr/share/vulkan/registry
    cp registry/vk.xml $SDKTARGETSYSROOT/usr/share/vulkan/registry/
    cd ..
    rm -rf vulkan_source

    if [ "$VULKAN_VOLK_REQUIRED" == "true" ]; then
         echo "Volk is required , install volk headers in sysroot"
         git clone https://github.com/zeux/volk.git >> "$LOG_FILE" 2>&1
         cd volk
         git checkout 59d26900f53c7621a8ba8ab0e3f18d3bd883fa9a >> "$LOG_FILE" 2>&1
         cp volk.h $SDKTARGETSYSROOT/usr/include/
         cp volk.c $SDKTARGETSYSROOT/usr/include/
         cd ..
         rm -rf volk
    fi
    INSTALLED_VULKAN_HEADERS="TRUE"
}

##########################################################
# vkcube code start
##########################################################

############################################
# 1. Clone vulkan tools
############################################
clone_vulkan_tools() {
    VULKAN_VERSION=$1
    PLATFORM=$2
    rm -rf vulkan_tools_source_$PLATFORM
    git clone https://github.com/KhronosGroup/Vulkan-Tools.git vulkan_tools_source_$PLATFORM >> "$LOG_FILE" 2>&1
    cd vulkan_tools_source_$PLATFORM
    VULKAN_TOOLS_DIR=$(pwd)
    echo "VULKAN TOOLS VERSION OBTAINED as $VULKAN_VERSION"
    case "$VULKAN_VERSION" in
        "1.3.247")
              vulkan_tools_srcrev="8bb9edd13f5027b6676f5229cb4a1822050b1f36"
              ;;
        "1.3.204")
              vulkan_tools_srcrev="b9a87a24a814e443b1adfc5a6bc2e57243446f6c"
              ;;
        "1.3.296")
              vulkan_tools_srcrev="74dd90abd69f813220b572e1d89c17bc7784972d"
              ;;
                *)
              echo "Unsupported Vulkan version: $VULKAN_VERSION"
              exit 1
              ;;
    esac
    git checkout $vulkan_tools_srcrev >> "$LOG_FILE" 2>&1
    CUBE_FILE="$VULKAN_TOOLS_DIR/cube/cube.c"
}

############################################
# 2. Add struct members
############################################
add_struct_members() {
    sed -i '/uint32_t queue_family_count;/a \
\
     // Duration limiting\
     uint32_t duration_seconds;\
     uint64_t start_time;\
\
     // Performance measurement\
     uint64_t last_fps_time;\
     uint32_t frame_count_for_fps;\
     double current_fps;\
     uint64_t last_cpu_time;\
     uint64_t last_cpu_idle_time;\
     double current_cpu_usage;\
     bool show_performance;' "$CUBE_FILE"
}

############################################
# 3. Add performance helper functions
############################################
add_performance_functions() {

cat << 'EOF' > new_functions.txt
static double total_cpu_percentage = 0;
static double total_time = 0;
static int32_t MIN_FRAMES = 10;
static bool demo_check_duration_expired(struct demo *demo) {
    if (demo->duration_seconds == 0) {
        return false;
    }

    if (demo->start_time == 0) {
        demo->start_time = getTimeInNanoseconds();
        return false;
    }

    uint64_t current_time = getTimeInNanoseconds();
    uint64_t elapsed_ns = current_time - demo->start_time;
    uint64_t duration_ns = (uint64_t)demo->duration_seconds * 1000000000ULL;

    return elapsed_ns >= duration_ns;
}

static void demo_update_fps(struct demo *demo) {
    if (demo->last_fps_time == 0) {
        demo->last_fps_time = getTimeInNanoseconds();
        demo->frame_count_for_fps = 0;
        return;
    }

    demo->frame_count_for_fps++;
    uint64_t current_time = getTimeInNanoseconds();
    uint64_t elapsed_ns = current_time - demo->last_fps_time;

    if (elapsed_ns >= 1000000000ULL) {
        demo->current_fps = (double)demo->frame_count_for_fps / ((double)elapsed_ns / 1000000000.0);
        demo->last_fps_time = current_time;
        demo->frame_count_for_fps = 0;
    }
}

static void demo_update_cpu_usage(struct demo *demo) {
    static uint64_t last_total = 0, last_idle = 0;
    static bool cpu_init = false;
    static uint64_t last_sample_time = 0;

    uint64_t now = getTimeInNanoseconds();

    // 👉 Only sample every 500ms (or 1 sec)
    if (last_sample_time != 0 && (now - last_sample_time) < 500000000ULL) {
        return;
    }
    last_sample_time = now;

    FILE* fp = fopen("/proc/stat", "r");
    if (fp == NULL) {
        demo->current_cpu_usage = 0.0;
        return;
    }

    char line[256];
    if (fgets(line, sizeof(line), fp)) {
        uint64_t user, nice, system, idle, iowait = 0, irq = 0, softirq = 0;

        int fields = sscanf(line, "cpu %llu %llu %llu %llu %llu %llu %llu",
                   &user, &nice, &system, &idle, &iowait, &irq, &softirq);

        if (fields >= 4) {
            uint64_t idle_all = idle + iowait;   // 🔥 IMPORTANT FIX
            uint64_t total = user + nice + system + idle_all + irq + softirq;

            if (cpu_init && total > last_total) {
                uint64_t total_diff = total - last_total;
                uint64_t idle_diff = idle_all - last_idle;

                if (total_diff > 0 && idle_diff <= total_diff) {
                    demo->current_cpu_usage =
                        ((double)(total_diff - idle_diff) / total_diff) * 100.0;
                }
            }

            last_total = total;
            last_idle = idle_all;
            cpu_init = true;
        }
    }

    fclose(fp);
}

static void demo_print_performance(struct demo *demo) {
    if (!demo->show_performance) return;

    static uint64_t last_print_time = 0;
    uint64_t current_time = getTimeInNanoseconds();
    // Wait for 1 second before printing metrics
    if ((current_time - demo->start_time) <= 1000000000ULL) {
       return;
    }
    if (last_print_time == 0 || (current_time - last_print_time) >= 1000000000ULL) {
       double fps = demo->current_fps;
       double cpu = demo->current_cpu_usage;

       if (fps < 0.0) fps = 0.0;
       if (fps > 9999.0) fps = 9999.0;
       if (cpu < 0.0) cpu = 0.0;
       if (cpu > 100.0) cpu = 100.0;

       printf("[VKCube] FPS: %.1f | CPU: %.1f%% | Frame: %d\n",
               fps, cpu, demo->curFrame);
       total_cpu_percentage += cpu;
       total_time++;
       fflush(stdout);
       last_print_time = current_time;
    }


}

static print_average(struct demo *demo) {
    if (!demo->show_performance) return;

    printf("[VKCube] Average FPS : %.1f\n", demo->curFrame/total_time);
    printf("[VKCube] Average CPU usage :  %.1f%%\n", total_cpu_percentage/total_time);
}

EOF

    sed -i '/static void demo_draw(struct demo \*demo) {/e cat new_functions.txt' "$CUBE_FILE"
    rm new_functions.txt
}

############################################
# 4. Hook performance update inside draw
############################################
add_performance_hook() {
    sed -i '/static void demo_draw(struct demo \*demo) {/,/VkResult U_ASSERT_ONLY err;/ {
        /VkResult U_ASSERT_ONLY err;/a \
\
    // Update performance metrics\
    if (demo->show_performance) {\
        demo_update_fps(demo);\
        demo_update_cpu_usage(demo);\
        demo_print_performance(demo);\
    }
}' "$CUBE_FILE"
}

############################################
# 5. Add cleanup print
############################################
add_cleanup_update() {
    #sed -i '/static void demo_cleanup(struct demo \*demo) {/,/uint32_t i;/ s/uint32_t i;/\/\/ Print final newline if performance monitoring was enabled\n    if (demo->show_performance) {\n        printf("\\n");\n        fflush(stdout);\n    }\n\n    uint32_t i;/' "$CUBE_FILE"
    sed -i '/static void demo_cleanup(struct demo \*demo) {/,/uint32_t i;/ s/uint32_t i;/\/\/ Print final newline if performance monitoring was enabled\n    if (demo->show_performance) {\n        print_average(demo);\n        fflush(stdout);\n    }\n    printf("Exiting from application\\n");\n    uint32_t i;/' "$CUBE_FILE"
}

############################################
# 6. Add duration-based exit
############################################
add_duration_exit() {
    sed -i '/VK_USE_PLATFORM_WAYLAND_KHR/,/while (!demo->quit) {/ s/while (!demo->quit) {/while (!demo->quit) {\n        if (demo_check_duration_expired(demo)) {\n            demo->quit = true;\n            break;\n        }/' "$CUBE_FILE"
}

############################################
# 7. Initialize fields
############################################
add_initialization() {
    sed -i '/demo->height = 500;/a \
    demo->duration_seconds = 0;\
    demo->start_time = 0;\
\
    demo->last_fps_time = 0;\
    demo->frame_count_for_fps = 0;\
    demo->current_fps = 0.0;\
    demo->last_cpu_time = 0;\
    demo->last_cpu_idle_time = 0;\
    demo->current_cpu_usage = 0.0;\
    demo->show_performance = false;' "$CUBE_FILE"
}

############################################
# 8. CLI arguments
############################################
add_arguments() {
    sed -i '/if (strcmp(argv\[i\], "--force_errors") == 0) {/i \
        if ((strcmp(argv[i], "--duration") == 0) && (i < argc - 1)) {\
            demo->duration_seconds = atoi(argv[i + 1]);\
            assert(demo->duration_seconds >= 0);\
            i++;\
            continue;\
        }\
        if (strcmp(argv[i], "--fps") == 0) {\
            demo->show_performance = true;\
            continue;\
        }' "$CUBE_FILE"
}

############################################
# 9. Wayland guards
############################################
add_wayland_guards() {
    cd $VULKAN_TOOLS_DIR/
    echo "Adding wayland guards"
    # Add guards around xdg_wm_base check
    local XDG_CHECK_LINE=$(grep -n "if (!demo->xdg_wm_base)" "$CUBE_FILE" | head -1 | cut -d: -f1)
    if [ -n "$XDG_CHECK_LINE" ] && ! grep -q "XDG_WM_BASE_PROTO" "$CUBE_FILE"; then
        local BEFORE_CHECK=$((XDG_CHECK_LINE - 1))
        sed -i "${BEFORE_CHECK}a\\#if defined(XDG_WM_BASE_PROTO)" "$CUBE_FILE"

        # Find the closing brace after exit(1); instead of just exit(1);
        local CLOSING_BRACE_LINE=$(awk "NR>=$XDG_CHECK_LINE && /exit\\(1\\);/ {found=1} found && /^[ ]*}/ {print NR; exit}" "$CUBE_FILE")
        [ -n "$CLOSING_BRACE_LINE" ] && {
            sed -i "${CLOSING_BRACE_LINE}a\\#endif" "$CUBE_FILE"
        }
    fi

    # Add guards around xdg_surface and decoration setup
    local XDG_SURFACE_LINE=$(grep -n "demo->xdg_surface = xdg_wm_base_get_xdg_surface" "$CUBE_FILE" | head -1 | cut -d: -f1)
    if [ -n "$XDG_SURFACE_LINE" ]; then
        local BEFORE_SURFACE=$((XDG_SURFACE_LINE - 1))
        sed -i "${BEFORE_SURFACE}a\\#if defined(XDG_WM_BASE_PROTO)" "$CUBE_FILE"

        # Find wl_surface_commit to place the #endif before it
        local COMMIT_LINE=$(grep -n "wl_surface_commit" "$CUBE_FILE" | head -1 | cut -d: -f1)
        if [ -n "$COMMIT_LINE" ]; then
            local ENDIF_LINE=$((COMMIT_LINE - 1))
            sed -i "${ENDIF_LINE}a\\#endif" "$CUBE_FILE"
        fi
    fi

    #Add wayland guard during cleanup
    sed -i '/#elif defined(VK_USE_PLATFORM_WAYLAND_KHR)/,/wl_registry_destroy/ {
    /wl_seat_destroy/a #if defined(XDG_WM_BASE_PROTO)
    /wl_compositor_destroy/i #endif
    }' $CUBE_FILE
}

############################################
# 10. GENERATE XDG DECORATOR FILES
############################################
generate_wayland_headers_minimal() {
    cd $VULKAN_TOOLS_DIR/cube
    # Find wayland protocols directory (cross-compilation aware)
    local WAYLAND_PROTOCOLS_DIR=""
    if [ -n "$PKG_CONFIG_SYSROOT_DIR" ]; then
        for dir in "$PKG_CONFIG_SYSROOT_DIR/usr/share/wayland-protocols" \
                   "$PKG_CONFIG_SYSROOT_DIR/usr/local/share/wayland-protocols"; do
            [ -d "$dir" ] && { WAYLAND_PROTOCOLS_DIR="$dir"; break; }
        done
    fi

    [ -z "$WAYLAND_PROTOCOLS_DIR" ] && {
        for dir in /usr/share/wayland-protocols /usr/local/share/wayland-protocols; do
            [ -d "$dir" ] && { WAYLAND_PROTOCOLS_DIR="$dir"; break; }
        done
    }

    # Generate headers using wayland-scanner if available
    if command -v wayland-scanner >/dev/null 2>&1 && [ -n "$WAYLAND_PROTOCOLS_DIR" ]; then
        local XDG_SHELL_XML="$WAYLAND_PROTOCOLS_DIR/stable/xdg-shell/xdg-shell.xml"
        local XDG_DECORATION_XML="$WAYLAND_PROTOCOLS_DIR/unstable/xdg-decoration/xdg-decoration-unstable-v1.xml"

        [ -f "$XDG_SHELL_XML" ] && {
            wayland-scanner client-header "$XDG_SHELL_XML" xdg-shell-client-header.h 2>/dev/null
            wayland-scanner private-code "$XDG_SHELL_XML" xdg-shell-protocol.c 2>/dev/null
        }

        [ -f "$XDG_DECORATION_XML" ] && {
            wayland-scanner client-header "$XDG_DECORATION_XML" xdg-decoration-client-header.h 2>/dev/null
            wayland-scanner private-code "$XDG_DECORATION_XML" xdg-decoration-protocol.c 2>/dev/null
        }

        [ -f "xdg-shell-client-header.h" ] && { echo "Generated Wayland headers"; return 0; }
    fi

    echo "Wayland headers not available - wayland-scanner or protocols missing"
    exit 1
}

############################################
# 11. Shader compilation
############################################
compile_shaders() {
    cd $VULKAN_TOOLS_DIR/cube
    # Check if shader .inc files already exist
    [ -f "cube.vert.inc" ] && [ -f "cube.frag.inc" ] && return 0

    # Look for glslangValidator in multiple locations
    local GLSLANG_VALIDATOR=""

    # Check standard paths
    if command -v glslangValidator >/dev/null 2>&1; then
        GLSLANG_VALIDATOR="glslangValidator"
    # Check Vulkan-Tools local glslang directory
    elif [ -f "../glslang/linux/bin/glslangValidator" ]; then
        GLSLANG_VALIDATOR="../glslang/linux/bin/glslangValidator"
    # Check if we can download it
    elif [ -f "../scripts/fetch_glslangvalidator.py" ]; then
        echo "Downloading glslangValidator..."
        setup_glslang_validator
        [ -f "../glslang/linux/bin/glslangValidator" ] && GLSLANG_VALIDATOR="../glslang/linux/bin/glslangValidator"
    fi

    # Compile shaders if we have glslangValidator
    if [ -n "$GLSLANG_VALIDATOR" ]; then
        echo "Compiling shaders with $GLSLANG_VALIDATOR..."
        # Use -x flag to generate C header format directly (same as CMake)
        $GLSLANG_VALIDATOR -V -x -o cube.vert.inc cube.vert 2>/dev/null
        $GLSLANG_VALIDATOR -V -x -o cube.frag.inc cube.frag 2>/dev/null

        [ -f "cube.vert.inc" ] && [ -f "cube.frag.inc" ] && {
            echo "Compiled shaders to .inc files"
            return 0
        }
    fi

    echo "Error: Unable to compile shaders - glslangValidator not available"
    echo "Install glslangValidator or ensure Vulkan-Tools fetch script works"
    exit 1
}

#########################################################
# 12. Setting up glslangValidator for shader compilaltion
#########################################################
setup_glslang_validator() {
    # Navigate to parent directory to run the fetch script
    local ORIG_DIR=$(pwd)
    cd ..

    # Try to determine the correct glslang release name
    local RELEASE_NAME=""
    if uname -s | grep -q "Linux"; then
        RELEASE_NAME="glslang-master-linux-Release.zip"
    elif uname -s | grep -q "Darwin"; then
        RELEASE_NAME="glslang-master-osx-Release.zip"
    else
        echo "Unsupported platform for automatic glslang download"
        cd "$ORIG_DIR"
        exit 1
    fi

    # Try with python3, then python
    if command -v python3 >/dev/null 2>&1; then
        python3 scripts/fetch_glslangvalidator.py "$RELEASE_NAME" 2>/dev/null
    elif command -v python >/dev/null 2>&1; then
        python scripts/fetch_glslangvalidator.py "$RELEASE_NAME" 2>/dev/null
    else
        echo "Python not found - cannot auto-download glslangValidator"
        cd "$ORIG_DIR"
        exit 1
    fi

    cd "$ORIG_DIR"
    echo "Downloaded glslangValidator"
}

############################################
# 13. vkcube compilation main function
############################################
compile_vkcube()
{
    if [[ -z "$PLATFORM" ]];then
        echo "NO PLATFORM is selected for vkcube compilation"
        echo "Setting PLATFORM to RPI4"
        PLATFORM="RPI4"
    fi

    echo -e "\nCompiling vkcube for $PLATFORM platform"
    cd $ROOT_DIR
    clone_vulkan_tools $VULKAN_VERSION $PLATFORM
    if [ $INSTALLED_VULKAN_HEADERS != "TRUE" ];then
        install_vulkan_headers
    fi

    add_struct_members
    add_performance_functions
    add_performance_hook
    add_cleanup_update
    add_duration_exit
    add_initialization
    add_arguments
    add_wayland_guards
    generate_wayland_headers_minimal
    compile_shaders
    cd $VULKAN_TOOLS_DIR/cube/
    $CC cube.c xdg-shell-protocol.c xdg-decoration-protocol.c -o vkcube     -DVK_USE_PLATFORM_WAYLAND_KHR     -lvulkan -lwayland-client -lpthread -lm >> "$LOG_FILE" 2>&1
    if [ -f $VULKAN_TOOLS_DIR/cube/vkcube ];then
        echo "Binary available in $VULKAN_TOOLS_DIR/cube/vkcube"
	echo -e "\e[1;42m VKCUBE COMPILATION : SUCCESS \e[0m" | tee -a "$LOG_FILE"
	vkcube_compiled="TRUE"
    else
	echo -e "\e[1;41m VKCUBE COMPILATION : FAILURE \e[0m" | tee -a "$LOG_FILE"
	exit 1
    fi
}

##########################################################
# vkcube code end
##########################################################

compile_tdkv()
{
    echo -e "Configuring TDK with toolchain \n"
    echo -e "TDK_SOURCE_DIR : $TDK_SOURCE_DIR"
    cd ${TDK_SOURCE_DIR}
    sed -i '/PKG_CHECK_MODULES/d' configure.ac
    sudo autoreconf -i >> $LOG_FILE 2>&1
    if [[ $PLATFORM == "RPI" ]];then
	CONFIGURE_OPTIONS_VA=""
	FLAGS_VA=""
    fi
    CONF_DEVICE=CONFIGURE_OPTIONS_$DEVICE_TYPE
    CONF_OPTIONS="${!CONF_DEVICE} $DISTRO_CONFIGURE $CONFIGURE_OPTIONS_VA  $CONFIGURE_OPTIONS_COMPONENTS"
    if [[ $NPVS_PACKAGE == "TRUE" ]];then
        CONF_OPTIONS=" --enable-npvsPackage --enable-tdkgraphics --enable-graphicstestapps"
	echo "NPVS Package compilation enabled"
    fi
    if [[ $CONF_OPTIONS == *"enable-powermgrhal"* ]] || [[ $CONF_OPTIONS == *"enable-rdkfwupdater"* ]];then
	get_component_versions
    fi
    if [[ $CONF_OPTIONS == *"enable-powermgrhal"* ]];then
	echo -e "PowerMgrhal compilation is enabled\n"
	git clone $SRC_IARMMGRS  >> $LOG_FILE 2>&1
	cd iarmmgrs ; git checkout $iarmmgrs_srcrev >> $LOG_FILE 2>&1; cd ..

	mkdir -p PowerMgrHal_stub/src/iarmmgr_source/power/
	cp iarmmgrs/power/therm_mon.c PowerMgrHal_stub/src/iarmmgr_source/power/therm_mon.c
	rm -rf iarmmgrs
    fi
    if [[ $CONF_OPTIONS == *"enable-rdkfwupdater"* ]];then
	echo -e "rdkfwupdater compilation is enabled\n"

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

	git clone $SRC_RFC rfc_source >> $LOG_FILE 2>&1
	cd rfc_source/
        if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
            git checkout $rfc_srcrev >> $LOG_FILE 2>&1
        fi
        find . -type f -name "rfcapi.h" -exec cp {} $SYSROOT/usr/include/ \;
        cd ..; rm -rf rfc_source/

	git clone $SRC_RDKLOGGER rdklogger_source >> $LOG_FILE 2>&1
	cd rdklogger_source/
	find . -type f -name "*.h" -exec cp {} $SYSROOT/usr/include/ \;
	cd ..; rm -rf rdklogger_source/

	git clone $SRC_WDMP_C wdmp-c_source >> $LOG_FILE 2>&1
	cd wdmp-c_source/
	git checkout f9f687b6b4b10c2b72341e792a64334f0a409848 >> $LOG_FILE 2>&1
        git clone $SRC_META_RDK_VIDEO
	if [[ "$MIDDLEWARE_VERSION" != "DEFAULT" ]];then
	    cd meta-rdk-video
            git checkout $MIDDLEWARE_VERSION
	    cd ..
        fi
	cp meta-rdk-video/recipes-support/wdmp-c/files/wdmp-c.patch .
	patch -p1 < wdmp-c.patch
	mkdir -p "$SYSROOT/usr/include/wdmp-c"
	find . -type f -name "wdmp-c.h" -exec cp {} "$SYSROOT/usr/include/wdmp-c" \;
	cd ..; rm -rf wdmp-c_source/

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
    cd $ROOT_DIR/$DIR_TDK
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
    if [ -f "icrypto_bins.tar.gz" ];then
	echo -e "iCrypto test binaries found"
	cp icrypto_bins.tar.gz TDK_Package/usr/bin
	cd TDK_Package/usr/bin
	tar -xvf icrypto_bins.tar.gz >> $LOG_FILE 2>&1
	rm icrypto_bins.tar.gz
	cd $ROOT_DIR
    fi
    if ls waymetric_* 1>/dev/null 2>&1;then
        echo -e "Waymetric binary is found"
        if [[ $PLATFORM == "AMLOGIC" ]];then
            cp waymetric_aml TDK_Package/usr/bin
            cd TDK_Package/usr/bin
            mv waymetric_aml waymetric
            chmod +x waymetric
            echo -e "Waymetric binary is copied"
            cd $ROOT_DIR
        fi
        if [[ $PLATFORM == "BROADCOM" ]];then
            cp waymetric_bcm TDK_Package/usr/bin
            cd TDK_Package/usr/bin
            mv waymetric_bcm waymetric
            chmod +x waymetric
            echo -e "Waymetric binary is copied"
            cd $ROOT_DIR
        fi
        if [[ $PLATFORM == "REALTEK" ]];then
            cp waymetric_rtk TDK_Package/usr/bin
            cd TDK_Package/usr/bin
            mv waymetric_rtk waymetric
            chmod +x waymetric
            echo -e "Waymetric binary is copied"
            cd $ROOT_DIR
        fi
    fi
    if [[ $vkmark_compiled == "TRUE" ]];then
	echo "Copying vkmark"
	cp $ROOT_DIR/vkmark_$PLATFORM.tgz TDK_Package/
	cd TDK_Package/
	tar -xvf vkmark_$PLATFORM.tgz >> $LOG_FILE 2>&1
	rm vkmark_$PLATFORM.tgz
	cd $ROOT_DIR
	rm vkmark_$PLATFORM.tgz
    fi
    if [[ $vkcube_compiled == "TRUE" ]];then
	echo "Copying vkcube"
	cp $VULKAN_TOOLS_DIR/cube/vkcube $ROOT_DIR/TDK_Package/usr/bin
	rm -rf $VULKAN_TOOLS_DIR
    fi
    if [[ $NPVS_PACKAGE != "TRUE" ]];then
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
    
    if [[ $NPVS_PACKAGE != "TRUE" ]];then
        #Copy all the shell scripts and config files along with tdk service
        cp agent/scripts/* ../TDK_Package/var/TDK
    else
	mkdir -p ../TDK_Package/opt/TDK/
	rm -rf ../TDK_Package/var/TDK/
	cp MediaPipelineTests_stub/tdk_mediapipelinetests ../TDK_Package/usr/bin/
	cp MediaPipelineTests_stub/tdk_mediapipelinetests_trickplay ../TDK_Package/usr/bin/
	cp Graphics_TestApplications/Essos_TDKTestApp ../TDK_Package/usr/bin
        cp Graphics_TestApplications/.libs/Westeros_TDKTestApp ../TDK_Package/usr/bin
	cp scripts/RunGraphicsTDKTest.sh ../TDK_Package/opt/TDK
	cp Graphics_TestApplications/tiles_benchmark ../TDK_Package/usr/bin
        cp Graphics_TestApplications/motion_benchmark ../TDK_Package/usr/bin
        cp Graphics_TestApplications/vkmultithread ../TDK_Package/usr/bin
	cp Graphics_TestApplications/oglmultithread ../TDK_Package/usr/bin
        cp Graphics_TestApplications/vkoverlay ../TDK_Package/usr/bin
        cp Graphics_TestApplications/ogloverlay ../TDK_Package/usr/bin
    fi
    if [[ $CONF_OPTIONS == *"enable-graphicstestapps"* ]];then
        shaders="$(find $ROOT_DIR -iname shaders.tgz)"
        if [  -z "$shaders" ];then
            echo -e "shaders.tgz not found"
            exit 1
        fi
	cp $ROOT_DIR/shaders.tgz ../TDK_Package/opt/TDK
	cd ../TDK_Package/opt/TDK
	tar -xf shaders.tgz
	rm shaders.tgz
	cd $ROOT_DIR/$DIR_TDK
    fi

    ## NOTE : REMOVE THIS IN CASE TDK AGENT ENABLED COMPONENT IS COMPILED AS PART OF TDK PACKAGE
    touch ../TDK_Package/opt/TDK/.no_tdk_agent

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
	if [[ $NPVS_PACKAGE == "TRUE" ]];then
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

    if [[ $NPVS_PACKAGE != "TRUE" ]];then
        #Create symlink for all the shared libraries
        cd ${ROOT_DIR}/TDK_Package/usr/lib
        for file in lib*stub*;do 
	    if [ ! -f "${file%.0.0}" ];then
                ln -s "$file" "${file%.0.0}";
	    fi
        done
        cd ../../

        #Create link for binary files
        for file in usr/bin/* ; do 
    	    filename=$(basename $file); 
	    if [ ! -f "var/TDK/$filename" ];then
		ln -s /$file var/TDK/$filename; 
            fi
        done
	cd ../
    else
        cd ${ROOT_DIR}
    fi

    system_date=$(date)
    formatted_date=$(echo "$system_date" | awk '{ printf "%02d%02d%04d_%02d%02d%02d\n", $3, (index("JanFebMarAprMayJunJulAugSepOctNovDec", $2)+2)/3, $6, substr($4,1,2), substr($4,4,2), substr($4,7,2) }')

    if [ -z $PLATFORM ];then
	PACKAGE_NAME="Generic_TDK_Package_${formatted_date}.tar.gz"
    else
	PACKAGE_NAME="TDK_Package_${PLATFORM}_${formatted_date}.tar.gz"
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
    rm -rf $ROOT_DIR/$DIR_TDK/temp
    rm -rf $ROOT_DIR/$DIR_TDK/RDK_Source
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
    compile_assimp
    sleep_bar
    install_packages
    sleep_bar
fi
clone_tdk
compile_skeleton_libraries
compile_vkmark
sleep_bar
compile_vkcube
sleep_bar
compile_tdkv
sleep_bar
modify_tdk_files
pack_tdkv
sleep_bar
