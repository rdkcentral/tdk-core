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

platform=$1
platform="${platform,,}"

if [[ "$platform" == "realtek" ]];then
     platform_repo="https://code.rdkcentral.com/r/collaboration/soc/realtek/rdk/tdk-video"
elif [[ "$platform" == "amlogic" ]];then
     platform_repo="https://code.rdkcentral.com/r/collaboration/soc/amlogic/rdk/tdk-video"
elif [[ "$platform" == "broadcom" ]];then
     platform_repo="https://code.rdkcentral.com/r/collaboration/soc/broadcom/rdk/tdk-video"
elif [[ "$platform" == "raspberrypi" ]];then
     platform_repo="https://code.rdkcentral.com/r/rdk/devices/raspberrypi/tdk"
else
     echo "ERROR : Unable to obtain platform repo for this vendor"
     exit
fi

#Check if Generic VTS Package is present
GENERIC_PACKAGE=`find vts_packages -maxdepth 1 -iname "VTS_Package*tgz"`
if [ -z "$GENERIC_PACKAGE" ];then
    echo "Generic VTS Package not present in fileStore"
    echo "Please copy VTS_Package into fileStore/vts_packages before attempting to create new package"
    exit
fi
GENERIC_PACKAGE=$(basename $GENERIC_PACKAGE)
echo "Creating package using $GENERIC_PACKAGE"

system_date=$(date)
formatted_date=$(echo "$system_date" | awk '{ printf "%02d%02d%04d_%02d%02d%02d\n", $3, (index("JanFebMarAprMayJunJulAugSepOctNovDec", $2)+2)/3, $6, substr($4,1,2), substr($4,4,2), substr($4,7,2) }')

#Create temp directory
cd vts_packages
temp_dir="${platform}_${formatted_date}"
echo "Creating package in $temp_dir"
mkdir $temp_dir
cd $temp_dir

#Attempt to clone, suppressing error output
export GIT_ASKPASS=/bin/false
export GIT_TERMINAL_PROMPT=0
export GIT_CONFIG_NOSYSTEM=1
git clone "$platform_repo" tdk_platform_repo >/dev/null 2>&1
#Check if git clone was successful
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to clone the repository: $platform_repo"
    echo "Please update credentials to clone $platform_repo in ~/.netrc"
    cd ..
    rm -rf $temp_dir
    exit 1 
fi

#Creating Vendor specific TDK package
#Copy generic package into $temp_dir
cp ../$GENERIC_PACKAGE .
tar -xvf $GENERIC_PACKAGE >/dev/null 2>&1
cd VTS_Package
for file in *vts_bin.tgz*; do
    tar -xvf "$file" >/dev/null 2>&1
done
rm -rf *vts_bin.tgz
for dir in */; do
    if [[ "$dir" != "tdk_platform_repo/" ]];then
	 echo "Processing $dir"
	 if [ -d "../tdk_platform_repo/VTS_profiles/$dir" ];then
	      cp ../tdk_platform_repo/VTS_profiles/$dir/* $dir/
	 fi
    fi
done
tar -cvzf device_settings_vts_bin.tgz device_settings >/dev/null 2>&1
tar -cvzf deepsleep_manager_vts_bin.tgz deepsleep_manager >/dev/null 2>&1
tar -cvzf power_manager_vts_bin.tgz power_manager >/dev/null 2>&1
tar -cvzf rmf_audio_capture_vts_bin.tgz rmf_audio_capture >/dev/null 2>&1
tar -cvzf hdmi_cec_vts_bin.tgz hdmi_cec >/dev/null 2>&1
for dir in */; do
    if [ -d "$dir" ]; then
	 rm -rf $dir
    fi
done
cd ..
rm -rf tdk_platform_repo $GENERIC_PACKAGE
tar -cvzf VTS_Package_${platform}_${formatted_date}.tgz * >/dev/null 2>&1

cd ..
mkdir -p $platform
cp $temp_dir/VTS_Package_${platform}_${formatted_date}.tgz $platform
echo "Created VTS_Package_${platform}_${formatted_date}.tgz successfully"


#Cleanup
rm -r $temp_dir
