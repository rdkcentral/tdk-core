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

#Package name can be provided as command line argument
vts_package=$1

#directory in which VTS will be installed
root_dir='/'

rm -rf $root_dir/VTS_Package

install_vts()
{
    echo -e "\nExtract VTS files to respective folders \n"
    # Use the tar command with error checking
    if ! tar -xf $vts_package; then
        echo "Error extracting $vts_package. Exiting."
        exit 1
    fi
}

# Check if VTS_Package.tgz is present in root_dir folder.
cd $root_dir
if [[ -z "$vts_package" ]]; then
   echo "Packagename is not provided as command line argument"
   echo "Searching for package name \"VTS_Package*tgz\" "
   vts_package=`ls /VTS_Package*tgz | head -n 1`
   echo -e "Processing $vts_package\n"
fi

if [ -f "$root_dir/$vts_package" ]; then
    install_vts
    if [ -d "VTS_Package" ];then
        for FILE in "VTS_Package"/*;do
            if [[ "$FILE" == "VTS_Package/libut_control.so" ]];then
                continue
            fi
            if [ ! -d $FILE ];then
                echo $FILE
                filename=$(basename $FILE)
                echo $filename
                cd VTS_Package
                tar -xvf $filename
                cd ..
            fi
        done
        cd VTS_Package
        echo "-------------------------"
        cp libut_control.so /usr/lib
        #Delete tar files
        rm -rf *.tgz
	touch /vts_installed
    fi
else
    echo -e "Please copy the VTS_Package.tgz file to $root_dir folder in the device"
fi
