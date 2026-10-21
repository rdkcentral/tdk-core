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

set -euo pipefail

#Package name can be provided as command line argument
vts_package="${1:-}"

#directory in which VTS will be installed
root_dir=$(cd "$(dirname "$0")" && pwd)/

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
    _binary="${4:-}"
    _yaml="${5:-}"

    if [ -z "$_vts_root" ] || [ -z "$_src_module" ] || [ -z "$_new_module" ]; then
        echo "setup_vts_module: Usage: setup_vts_module <vts_root> <source_module> <new_module> [hal_test_binary] [yaml_file]" >&2
        return 1
    fi

    _src_dir="${_vts_root}/${_src_module}"
    _new_dir="${_vts_root}/${_new_module}"

    if [ ! -d "$_src_dir" ]; then
        echo "setup_vts_module: source module dir not found: $_src_dir" >&2
        return 1
    fi

    # Rename-style modules: move the whole dir and symlink libut_control.so
    case "$_src_module" in
        power_manager|deepsleep_manager|rmf_audio_capture|hdmi_cec)
            echo "setup_vts_module: moving ${_src_dir} -> ${_new_dir} ..."
            mv "$_src_dir" "$_new_dir" || return 1
            ln -sf "${_vts_root}/libut_control.so" "${_new_dir}/libut_control.so"
            unset _vts_root _src_module _new_module _binary _yaml _src_dir _new_dir
            return 0
            ;;
    esac

    if [ -z "$_binary" ]; then
        echo "setup_vts_module: Usage: setup_vts_module <vts_root> <source_module> <new_module> <hal_test_binary> [yaml_file]" >&2
        return 1
    fi

    if [ ! -f "${_src_dir}/${_binary}" ]; then
        echo "setup_vts_module: binary not found: ${_src_dir}/${_binary}" >&2
        return 1
    fi

    echo "setup_vts_module: creating ${_new_dir} ..."

    mkdir -p "$_new_dir" || return 1

    # Symlink a file from the source dir into the new dir, warning if missing
    _link_or_warn() {
        if [ -f "${_src_dir}/$1" ]; then
            ln -sf "${_src_dir}/$1" "${_new_dir}/$1"
        else
            echo "setup_vts_module: warning: ${_src_dir}/$1 not found, skipping" >&2
        fi
    }

    _link_or_warn run.sh
    if [ -n "$_yaml" ]; then
        _link_or_warn "$_yaml"
    fi

    # Symlink libut_control.so
    if [ ! -f "${_new_dir}/libut_control.so" ]; then
        ln -sf "${_vts_root}/libut_control.so" "$_new_dir/libut_control.so"
    fi

    # Symlink the binary from the source
    ln -sf "${_src_dir}/${_binary}" "${_new_dir}/${_binary}" || return 1

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
   vts_package=`ls $root_dir/VTS_Package*tgz | head -n 1`
   echo -e "Processing $vts_package\n"
fi

if [ -f "$vts_package" ]; then
    install_vts
    if [ -d "VTS_Package" ];then
        for FILE in "VTS_Package"/*;do
            case "$FILE" in
                "VTS_Package/libut_control.so"|"VTS_Package/vts_version.txt") continue ;;
            esac
            if [ ! -d "$FILE" ];then
                filename=$(basename "$FILE")
                echo "$FILE"
                echo "$filename"
                tar -xvf "$FILE" -C VTS_Package
            fi
        done
        cd VTS_Package
        echo "-------------------------"
        #Delete tar files
        rm -rf *.tgz
        setup_vts_module ${root_dir}VTS_Package device_settings    dsAudio         hal_test_dshal                  Source_AudioSettings.yaml
        setup_vts_module ${root_dir}VTS_Package device_settings    dsVideoPort     hal_test_dshal                  Source_4K_VideoPort.yaml
        setup_vts_module ${root_dir}VTS_Package device_settings    dsDisplay       hal_test_dshal                  Source_4K_Display.yaml
        setup_vts_module ${root_dir}VTS_Package device_settings    dsHost          hal_test_dshal                  Source_HostSettings.yaml
        setup_vts_module ${root_dir}VTS_Package device_settings    dsVideoDevice   hal_test_dshal                  Source_VideoDevice.yaml
        setup_vts_module ${root_dir}VTS_Package device_settings    dsFPD           hal_test_dshal                  Source_FPD.yaml
        setup_vts_module ${root_dir}VTS_Package power_manager      power
        setup_vts_module ${root_dir}VTS_Package deepsleep_manager  deepsleep
        setup_vts_module ${root_dir}VTS_Package rmf_audio_capture  rmfaudiocapture
        setup_vts_module ${root_dir}VTS_Package hdmi_cec           hdmicec
        echo "${root_dir}VTS_Package/"  > /opt/vts_installed_path
	echo "VTS Package installed successfully"
    fi
else
    echo -e "Please copy the VTS_Package.tgz file to $root_dir folder in the device"
fi
