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

start_tdk() {
    echo -e "\nExtract TDK files to respective folders \n"
    # Use the tar command with error checking
    if ! tar -xvzf $tdk_package; then
        echo "Error extracting $tdk_package. Exiting."
        exit 1
    fi
 
    additionalLibsDir="/additional_libs"
    if [ -d "$additionalLibsDir" ]; then
        echo "The directory $additionalLibsDir exists."
        echo "Copying additional libs to /usr/lib"
        cp "${additionalLibsDir}"/lib* /usr/lib
    fi
 
    additionalBinsDir="/additional_bins"
    if [ -d "$additionalBinsDir" ]; then
        echo "The directory $additionalBinsDir exists."
        echo "Copying additional bins to /usr/bin"
        cp "${additionalBinsDir}"/* /usr/bin
    fi

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

    echo -e "\nEnable TDK service\n"
    systemctl enable tdk
    sleep 1
    echo -e "Going to reboot the device\n"
    sleep 1
    reboot
}
 
# Check if TDK_Package.tar.gz is present in / folder.
cd /
if [[ -z "$tdk_package" ]]; then
   echo "Packagename is not provided as command line argument"
   echo "Searching for package name \"TDK_Package*tar.gz\" "
   mv TDK_Package*tar.gz TDK_Package.tar.gz
   tdk_package="TDK_Package.tar.gz"
fi

if [ -f "/$tdk_package" ]; then
    start_tdk
else
    echo -e "Please copy the TDK_Package.tar.gz file to / folder in the device"
fi
