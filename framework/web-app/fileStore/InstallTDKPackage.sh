#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2024 RDK Management
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

#Package name can be provided as command line argument
tdk_package=$1

uninstall=false

if [ "$1" == "--uninstall" ]; then
    uninstall=true
fi

if $uninstall; then
    file=".tdk_extracted_files.log"
    if [ ! -f $file ];then
        echo "TDK Package is not installed in the device"
        echo "Uninstall is revoked"
        exit
    fi

    echo "Stopping TDK Service"
    systemctl stop tdk
    echo "Deleting all TDK libs and bins"
    while IFS= read -r path; do
        if [ -f "$path" ]; then
            rm "$path"
        fi
    done < "$file"
    echo "Deleting TDK specific directories"
    rm -rf /var/TDK
    rm -rf /opt/TDK
    exit
fi

extract_fncs_package=false

if [[ "$1" == --fncs-package* ]]; then
    extract_fncs_package=true
fi

if $extract_fncs_package; then
    PLATFORM=$(cat /etc/device.properties | grep ^MODEL_NUM | cut -d '=' -f2)
    system_date=$(date)
    formatted_date=$(echo "$system_date" | awk '{ printf "%02d%02d%04d_%02d%02d%02d\n", $3, (index("JanFebMarAprMayJunJulAugSepOctNovDec", $2)+2)/3, $6, substr($4,1,2), substr($4,4,2), substr($4,7,2) }')
    TAR_FILE="FNCS_Package_${PLATFORM}_${formatted_date}.tar.gz"

    # List of files to include in the tar
    FILES_playback="/usr/bin/tdk_mediapipelinetests* /usr/lib/libjsoncpp* /usr/lib/libtinyxml* /opt/TDK/TDK.env"
    FILES_graphics="/var/TDK/RunGraphicsTDKTest.sh /usr/bin/Westeros_TDKTestApp /usr/bin/Essos_TDKTestApp"
    FILES_cryptography="/usr/bin/cgfacetests /usr/bin/cgimptests"
    if [[ "$1" == *-playback ]]; then
        FILES=$FILES_playback
    elif [[ "$1" == *-graphics ]]; then
        FILES=$FILES_graphics
    elif [[ "$1" == *-icrypto ]];then
        FILES=$FILES_cryptography
    else
        FILES="$FILES_playback $FILES_graphics $FILES_cryptography"
    fi

    RELATIVE_FILES=""
    for file in $FILES; do
        if [ -e "$file" ]; then  # Check if file exists
            RELATIVE_FILES="$RELATIVE_FILES ${file#/}"
        fi
    done

    # Check if there are any valid files to archive
    if [ -z "$RELATIVE_FILES" ]; then
        echo "No valid files found to archive. Exiting."
        exit 0
    fi

    # Create the tar archive with relative paths
    echo -e "Archiving FNCS files from DUT\n"
    tar -cvf "$TAR_FILE" $RELATIVE_FILES

    echo -e "\nFNCS Package created: $TAR_FILE \n"
    exit
fi

setup_graphics_softlinks() {
    echo -e "\nSetting up EGL and wayland softlinks\n"

    echo -e "\nCreating softlinks for Graphics libraries\n"
    GLESv2_library=`find /usr/lib -iname "libGLESv2.so*" | head -n1`
    echo "/usr/lib/libtdk-GLESv2.so.0 --> " $GLESv2_library
    ln -sf $GLESv2_library /usr/lib/libtdk-GLESv2.so.0

    EGL_library=`find /usr/lib -iname "libEGL.so*" | head -n1`
    echo "/usr/lib/libtdk-EGL.so.0 --> "$EGL_library
    ln -sf $EGL_library /usr/lib/libtdk-EGL.so.0

    wayland_egl_library=`find /usr/lib -iname "libwayland-egl.so*" | head -n1`
    echo "/usr/lib/libtdk-wayland-egl.so.0 --> "$wayland_egl_library
    ln -sf $wayland_egl_library /usr/lib/libtdk-wayland-egl.so.0
}

start_tdk() {
    echo -e "\nExtract TDK files to respective folders \n"
    log_file=".tdk_extracted_files.log"
    # Use the tar command with error checking
    if ! tar -xvzf $tdk_package | tee $log_file; then
        echo "Error extracting $tdk_package. Exiting."
        exit 1
    fi

    additionalLibsDir="/additional_libs"
    if [ -d "$additionalLibsDir" ]; then
        echo "The directory $additionalLibsDir exists."
        echo "Copying additional libs to /usr/lib"
        cp "${additionalLibsDir}"/lib* /usr/lib
        for lib in "${additionalLibsDir}"/lib/*; do
            lib_name=$(basename "$lib")
            echo "/usr/lib/$lib_name" >> "$log_file"
        done
    fi
 
    additionalBinsDir="/additional_bins"
    if [ -d "$additionalBinsDir" ]; then
        echo "The directory $additionalBinsDir exists."
        echo "Copying additional bins to /usr/bin"
        cp "${additionalBinsDir}"/* /usr/bin
        for app in "${additionalBinsDir}"/*; do
            app_name=$(basename "$app")
            echo "/usr/lib/$app_name" >> "$log_file"
        done
    fi

    setup_graphics_softlinks

    echo -e "\nEnable TDK service\n"
    systemctl enable tdk
    sleep 1
    echo -e "Going to start tdk service\n"
    sleep 1
    systemctl restart tdk
}
 
# Check if TDK_Package.tar.gz is present in / folder.
cd /

if [[ -z "$tdk_package" ]]; then
   echo "Packagename is not provided as command line argument"
   echo "Searching for package name \"TDK_Package*tar.gz\" "
   tdk_package=`ls /TDK_Package*tar.gz | head -n 1`
   echo -e "Processing $tdk_package\n"
fi

if [[ "$tdk_package" == *FNCS* ]];then
   echo "Package is a FNCS package"
   tar -xvf $tdk_package
   setup_graphics_softlinks
   exit
fi

if [ -f "/$tdk_package" ]; then
    start_tdk
else
    echo -e "Please copy the TDK_Package.tar.gz file to / folder in the device"
fi
