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

setup_vts_module() {
    _vts_root="$1"
    _src_module="$2"
    _new_module="$3"
    _binary="$4"
    _yaml="$5"

    if [ -z "$_vts_root" ] || [ -z "$_src_module" ] || [ -z "$_new_module" ] || [ -z "$_binary" ]; then
        echo "setup_vts_module: Usage: setup_vts_module <vts_root> <source_module> <new_module> <hal_test_binary> [yaml_file]" >&2
        return 1
    fi

    # Special-case: power_manager source dir maps to "power" module name
    if [ "$_src_module" = "power_manager" ] || [ "$_src_module" = "deepsleep_manager" ]; then
        _new_dir="${_vts_root}/${_src_module%_manager}"
    fi
    if [ "$_src_module" = "rmf_audio_capture" ]; then
        _new_dir="${_vts_root}/rmfaudiocapture"
    fi

    _src_dir="${_vts_root}/${_src_module}"
    _new_dir="${_vts_root}/${_new_module}"

    if [ ! -d "$_src_dir" ]; then
        echo "setup_vts_module: source module dir not found: $_src_dir" >&2
        return 1
    fi

    if [ ! -f "${_src_dir}/${_binary}" ]; then
        echo "setup_vts_module: binary not found: ${_src_dir}/${_binary}" >&2
        return 1
    fi

    echo "setup_vts_module: creating ${_new_dir} ..."

    if [ "$_src_module" = "power_manager" ] || [ "$_src_module" = "deepsleep_manager" ] || [ "$_src_module" = "rmf_audio_capture" ];then
        mv "$_src_dir" "$_new_dir"
        return 1
    fi
    mkdir -p "$_new_dir" || return 1

    # Symlink run.sh instead of copying it
    if [ -f "${_src_dir}/run.sh" ]; then
        rm -f "${_new_dir}/run.sh"
        ln -sf "${_src_dir}/run.sh" "${_new_dir}/run.sh"
    else
        echo "setup_vts_module: warning: ${_src_dir}/run.sh not found, skipping" >&2
    fi

    # Symlink yaml config if provided
    if [ -n "$_yaml" ]; then
        if [ -f "${_src_dir}/${_yaml}" ]; then
            ln -sf "${_src_dir}/${_yaml}" "$_new_dir/${_yaml}"
        else
            echo "setup_vts_module: warning: ${_src_dir}/${_yaml} not found, skipping" >&2
        fi
    fi

    # Remove any stale copy of the binary and symlink to the source instead
    ( cd "$_new_dir" && rm -f "$_binary" && ln -sf "${_src_dir}/${_binary}" "$_binary" ) || return 1

    echo "setup_vts_module: done. Contents of ${_new_dir}:"
    ls -l "$_new_dir"

    unset _vts_root _src_module _new_module _binary _yaml _src_dir _new_dir
    return 0
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
            if [[ "$FILE" == "VTS_Package/vts_version.txt" ]];then
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
        setup_vts_module ${root_dir}VTS_Package device_settings   dsAudio         hal_test_dshal                  Source_AudioSettings.yaml
        setup_vts_module ${root_dir}VTS_Package device_settings   dsVideoPort     hal_test_dshal                  Source_4K_VideoPort.yaml
        setup_vts_module ${root_dir}VTS_Package device_settings   dsDisplay       hal_test_dshal                  Source_4K_Display.yaml
        setup_vts_module ${root_dir}VTS_Package device_settings   dsHost          hal_test_dshal                  Source_HostSettings.yaml
        setup_vts_module ${root_dir}VTS_Package device_settings   dsVideoDevice   hal_test_dshal                  Source_VideoDevice.yaml
        setup_vts_module ${root_dir}VTS_Package power_manager     power           hal_test_iarmmgrs-power-hal     source_powerManager.yaml
        setup_vts_module ${root_dir}VTS_Package deepsleep_manager deepsleep       hal_test_iarmmgrs-deepsleep-hal deepsleepmanagerWakeUpSources.yaml
        setup_vts_module ${root_dir}VTS_Package rmf_audio_capture rmfaudiocapture hal_test_rmfAudioCapture        rmfAudioCaptureAuxNotSupported.yaml
        touch ${root_dir}vts_installed
    fi
else
    echo -e "Please copy the VTS_Package.tgz file to $root_dir folder in the device"
fi
