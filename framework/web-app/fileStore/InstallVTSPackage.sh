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
root_dir="/"

rm -rf $root_dir/VTS_Package

create_softlinks()
{
    # Find all files in the directory and process each
    find . -maxdepth 2 -name libraries.txt -type f | while read -r file; do
        dir_path=$(dirname "$file")
        cd $dir_path
        found_softlink=false
        found_original=false
        full_path=$file
        echo "Processing file: $full_path"
        file=$(basename $file)
        # Read the content of the file
        while IFS= read -r line; do
            if [[ "$line" == *"softlink:"* ]]; then
                softlink="${line#softlink:}"
                found_softlink=true
            fi
            if [[ "$line" == *"original:"* ]]; then
                original_lib="${line#original:}"
                original_lib_file=$(find /usr/lib -name ${original_lib}* | head -n 1)
                if [ ! -n "$original_lib_file" ];then
                    echo "original lib file not found for $file"
                else
                    found_original=true
                    original=$(basename $original_lib_file)
                fi
            fi
            if $found_softlink && $found_original;then
                echo "Softlink : $softlink"
                echo "Original : $original"
                if [[ "$softlink" != "$original" ]];then
                    echo "Creating softlink"
                    ln -sf $original_lib_file $softlink
                fi
            fi
        done < "$file"
        echo "Finished processing $full_path"
        echo "-------------------------"
        cd $root_dir/VTS_Package
    done
}


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
   mv VTS_Package*tgz VTS_Package.tgz
   vts_package="VTS_Package.tgz"
fi

if [ -f "$root_dir/$vts_package" ]; then
    install_vts
    if [ -d "VTS_Package" ];then
        for FILE in "VTS_Package"/*;do
            if [ ! -d $FILE ];then
                echo $FILE
                filename=$(basename $FILE)
	        echo $filename
                cd VTS_Package
                tar -xvf $filename
                #rm $filename
                cd ..
            fi
        done
        cd VTS_Package
        echo "-------------------------"
        create_softlinks
        #Delete tar files
        rm -rf *.tgz
    fi 
else
    echo -e "Please copy the VTS_Package.tgz file to $root_dir folder in the device"
fi
