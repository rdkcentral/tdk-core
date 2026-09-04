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

#HAL source
SRC_POWERMGR_HAL="https://github.com/rdkcentral/rdk-halif-power_manager.git"
SRC_DEEPSLEEP_HAL="https://github.com/rdkcentral/rdk-halif-deepsleep_manager.git"
SRC_DS_HAL="https://github.com/rdkcentral/rdk-halif-device_settings.git"
SRC_HDMICEC_HAL="https://github.com/rdkcentral/rdk-halif-hdmi_cec.git"
SRC_RMF_AUDIO_CAPTURE="https://github.com/rdkcentral/rdk-halif-rmf_audio_capture.git"
SRC_HDMICEC="https://code.rdkcentral.com/r/rdk/components/generic/hdmicec"
SRC_UT_CORE="https://github.com/rdkcentral/ut-core.git"

ROOT_DIR=$PWD
PLATFORM=$1
mkdir -p logs
mkdir -p VTS_Source
TDK_SOURCE_DIR=${ROOT_DIR}/${DIR_TDK}
COMPILE_SKELETON=false
SYSROOT=${ROOT_DIR}/sysroots
UT_CORE_COMPILED=false

config=configure_vts.txt
. $config

# ---------------------------------------------------------------------------
# Git credentials
# This script no longer manages credentials. Any git clone that needs
# authentication (github.com, code.rdkcentral.com) relies on git reading
# credentials from the user's ~/.netrc file, for example:
#     machine github.com          login <user> password <token>
#     machine code.rdkcentral.com login <user> password <password>
# then run: chmod 600 ~/.netrc
# ---------------------------------------------------------------------------

#HPK documentation repo - source of truth for per-module HAL Testing versions
SRC_HPK_DOC="https://github.com/rdkcentral/rdk-hpk-documentation.git"

#Given an HPK release tag, validate it and derive each module's HAL Testing
#version from the top table of RELEASE.md. Sets:
#  DEEPSLEEP_HAL_TEST_VERSION, POWER_HAL_TEST_VERSION, DS_HAL_TEST_VERSION,
#  HDMICEC_HAL_TEST_VERSION, RMF_AUDIO_CAPTURE_HAL_TEST_VERSION
resolve_hal_test_versions()
{
    if [ -z "$HPK_VERSION" ]; then
        echo "ERROR: HPK_VERSION is not set in $config"
        exit 1
    fi

    #Validate the tag exists on the remote (no clone required)
    if ! git ls-remote --tags "$SRC_HPK_DOC" "refs/tags/${HPK_VERSION}" 2>/dev/null | grep -q "refs/tags/${HPK_VERSION}"; then
        echo "ERROR: HPK_VERSION '$HPK_VERSION' is not a valid tag in rdk-hpk-documentation"
        exit 1
    fi
    echo "HPK_VERSION '$HPK_VERSION' is a valid tag"

    #Shallow-clone the repo at the tag
    HPK_DOC_DIR="${ROOT_DIR}/VTS_Source/rdk-hpk-documentation"
    rm -rf "$HPK_DOC_DIR"
    git clone --quiet --depth 1 --branch "$HPK_VERSION" "$SRC_HPK_DOC" "$HPK_DOC_DIR" >> $LOG_FILE 2>&1
    if [ ! -f "$HPK_DOC_DIR/RELEASE.md" ]; then
        echo "ERROR: RELEASE.md not found in rdk-hpk-documentation at tag $HPK_VERSION"
        exit 1
    fi

    RELEASE_FILE="$HPK_DOC_DIR/RELEASE.md"

    DEEPSLEEP_HAL_TEST_VERSION="$(get_hal_test_version "Deep Sleep Manager")"
    POWER_HAL_TEST_VERSION="$(get_hal_test_version "Power Manager")"
    DS_HAL_TEST_VERSION="$(get_hal_test_version "Device Settings")"
    HDMICEC_HAL_TEST_VERSION="$(get_hal_test_version "HDMI CEC")"
    RMF_AUDIO_CAPTURE_HAL_TEST_VERSION="$(get_hal_test_version "RMF Audio Capture")"

    # Apply per-module overrides from configure_vts.txt.
    # A variable is only overridden when it is non-empty in the config file;
    # the config is already sourced at the top of the script, so the values
    # are already in the environment at this point.
    [ -n "${DS_HAL_TEST_VERSION_OVERRIDE:-}" ]                 && DS_HAL_TEST_VERSION="$DS_HAL_TEST_VERSION_OVERRIDE"                 && echo "  [OVERRIDE] DS_HAL_TEST_VERSION -> $DS_HAL_TEST_VERSION"
    [ -n "${DEEPSLEEP_HAL_TEST_VERSION_OVERRIDE:-}" ]          && DEEPSLEEP_HAL_TEST_VERSION="$DEEPSLEEP_HAL_TEST_VERSION_OVERRIDE"    && echo "  [OVERRIDE] DEEPSLEEP_HAL_TEST_VERSION -> $DEEPSLEEP_HAL_TEST_VERSION"
    [ -n "${POWER_HAL_TEST_VERSION_OVERRIDE:-}" ]              && POWER_HAL_TEST_VERSION="$POWER_HAL_TEST_VERSION_OVERRIDE"            && echo "  [OVERRIDE] POWER_HAL_TEST_VERSION -> $POWER_HAL_TEST_VERSION"
    [ -n "${HDMICEC_HAL_TEST_VERSION_OVERRIDE:-}" ]            && HDMICEC_HAL_TEST_VERSION="$HDMICEC_HAL_TEST_VERSION_OVERRIDE"        && echo "  [OVERRIDE] HDMICEC_HAL_TEST_VERSION -> $HDMICEC_HAL_TEST_VERSION"
    [ -n "${RMF_AUDIO_CAPTURE_HAL_TEST_VERSION_OVERRIDE:-}" ]  && RMF_AUDIO_CAPTURE_HAL_TEST_VERSION="$RMF_AUDIO_CAPTURE_HAL_TEST_VERSION_OVERRIDE"  && echo "  [OVERRIDE] RMF_AUDIO_CAPTURE_HAL_TEST_VERSION -> $RMF_AUDIO_CAPTURE_HAL_TEST_VERSION"

    SRC_DEEPSLEEP_HAL_HEADER_REVISION="$(get_hal_header_version "Deep Sleep Manager")"
    SRC_POWERMGR_HAL_HEADER_REVISION="$(get_hal_header_version "Power Manager")"
    SRC_DS_HAL_HEADER_REVISION="$(get_hal_header_version "Device Settings")"
    SRC_HDMICEC_HAL_HEADER_REVISION="$(get_hal_header_version "HDMI CEC")"
    SRC_RMF_AUDIO_CAPTURE_HAL_HEADER_REVISION="$(get_hal_header_version "RMF Audio Capture")"

    # Apply per-module header version overrides from configure_vts.txt.
    [ -n "${DS_HAL_HEADER_VERSION_OVERRIDE:-}" ]                && SRC_DS_HAL_HEADER_REVISION="$DS_HAL_HEADER_VERSION_OVERRIDE"                && echo "  [OVERRIDE] SRC_DS_HAL_HEADER_REVISION -> $SRC_DS_HAL_HEADER_REVISION"
    [ -n "${DEEPSLEEP_HAL_HEADER_VERSION_OVERRIDE:-}" ]         && SRC_DEEPSLEEP_HAL_HEADER_REVISION="$DEEPSLEEP_HAL_HEADER_VERSION_OVERRIDE"   && echo "  [OVERRIDE] SRC_DEEPSLEEP_HAL_HEADER_REVISION -> $SRC_DEEPSLEEP_HAL_HEADER_REVISION"
    [ -n "${POWER_HAL_HEADER_VERSION_OVERRIDE:-}" ]             && SRC_POWERMGR_HAL_HEADER_REVISION="$POWER_HAL_HEADER_VERSION_OVERRIDE"         && echo "  [OVERRIDE] SRC_POWERMGR_HAL_HEADER_REVISION -> $SRC_POWERMGR_HAL_HEADER_REVISION"
    [ -n "${HDMICEC_HAL_HEADER_VERSION_OVERRIDE:-}" ]           && SRC_HDMICEC_HAL_HEADER_REVISION="$HDMICEC_HAL_HEADER_VERSION_OVERRIDE"        && echo "  [OVERRIDE] SRC_HDMICEC_HAL_HEADER_REVISION -> $SRC_HDMICEC_HAL_HEADER_REVISION"
    [ -n "${RMF_AUDIO_CAPTURE_HAL_HEADER_VERSION_OVERRIDE:-}" ] && SRC_RMF_AUDIO_CAPTURE_HAL_HEADER_REVISION="$RMF_AUDIO_CAPTURE_HAL_HEADER_VERSION_OVERRIDE" && echo "  [OVERRIDE] SRC_RMF_AUDIO_CAPTURE_HAL_HEADER_REVISION -> $SRC_RMF_AUDIO_CAPTURE_HAL_HEADER_REVISION"

    echo "Derived HAL Testing versions from HPK $HPK_VERSION:"
    echo "  DEEPSLEEP_HAL_TEST_VERSION          = $DEEPSLEEP_HAL_TEST_VERSION"
    echo "  POWER_HAL_TEST_VERSION              = $POWER_HAL_TEST_VERSION"
    echo "  DS_HAL_TEST_VERSION                 = $DS_HAL_TEST_VERSION"
    echo "  HDMICEC_HAL_TEST_VERSION            = $HDMICEC_HAL_TEST_VERSION"
    echo "  RMF_AUDIO_CAPTURE_HAL_TEST_VERSION  = $RMF_AUDIO_CAPTURE_HAL_TEST_VERSION"
    echo "Derived HAL Interface versions from HPK $HPK_VERSION:"
    echo "  SRC_DEEPSLEEP_HAL_HEADER_REVISION           = $SRC_DEEPSLEEP_HAL_HEADER_REVISION"
    echo "  SRC_POWERMGR_HAL_HEADER_REVISION            = $SRC_POWERMGR_HAL_HEADER_REVISION"
    echo "  SRC_DS_HAL_HEADER_REVISION                  = $SRC_DS_HAL_HEADER_REVISION"
    echo "  SRC_HDMICEC_HAL_HEADER_REVISION             = $SRC_HDMICEC_HAL_HEADER_REVISION"
    echo "  SRC_RMF_AUDIO_CAPTURE_HAL_HEADER_REVISION   = $SRC_RMF_AUDIO_CAPTURE_HAL_HEADER_REVISION"
}

#Extract the HAL Testing version for a component from the top RELEASE.md table.
#Prefers the HAL Testing "Current" column; falls back to the first test-repo
#tree/blob link on the row when the current cell reads "No change".
get_hal_test_version()
{
    local component="$1"
    local line cell version

    line="$(grep -m1 -F "[${component}]" "$RELEASE_FILE" || true)"
    if [ -z "$line" ]; then
        echo "ERROR: '${component}' row not found in RELEASE.md" >&2
        exit 1
    fi

    cell="$(printf '%s\n' "$line" | awk -F'|' '{print $7}')"
    version="$(printf '%s\n' "$cell" | grep -oE '`[^`]+`' | head -n1 | tr -d '`')"

    if [ -z "$version" ] || [ "$version" = "No change" ]; then
        version="$(printf '%s\n' "$line" \
            | grep -oE 'rdk[a-z-]*-halif-test-[^/]+/(tree|blob)/[^)]+' \
            | head -n1 \
            | sed -E 's#.*/(tree|blob)/##')"
    fi

    if [ -z "$version" ]; then
        echo "ERROR: could not determine HAL Testing version for '${component}'" >&2
        exit 1
    fi

    printf '%s' "$version"
}

#Extract the HAL Interface (header) version for a component from the top RELEASE.md table.
#Prefers the HAL Interface "Current" column ($4); falls back to any non-test halif tree/blob
#link on the row when the current cell reads "No change".
get_hal_header_version()
{
    local component="$1"
    local line cell version

    line="$(grep -m1 -F "[${component}]" "$RELEASE_FILE" || true)"
    if [ -z "$line" ]; then
        echo "ERROR: '${component}' row not found in RELEASE.md" >&2
        exit 1
    fi

    # HAL Interface Current is in column 4 (awk field $4 with | delimiter)
    cell="$(printf '%s\n' "$line" | awk -F'|' '{print $4}')"
    version="$(printf '%s\n' "$cell" | grep -oE '`[^`]+`' | head -n1 | tr -d '`')"

    if [ -z "$version" ] || [ "$version" = "No change" ]; then
        # Fall back to any halif (non-test) tree/blob link on the row
        version="$(printf '%s\n' "$line" \
            | grep -oE 'rdk[a-z-]*-halif-[^/]+/(tree|blob)/[^)]+' \
            | grep -v '\-halif-test-' \
            | head -n1 \
            | sed -E 's#.*/(tree|blob)/##')"
    fi

    if [ -z "$version" ]; then
        echo "ERROR: could not determine HAL Interface version for '${component}'" >&2
        exit 1
    fi

    printf '%s' "$version"
}

echo -e "Compiling VTS generically"

#All logs will be written to this file
LOG_FILE=$ROOT_DIR/logs/$(date +%F_%T)_$PLATFORM.log

echo -e "\n"
echo -e "Monitor \e[1;31m  $LOG_FILE \e[0m for more logs \n"
vtsPackageUtilitiesPath=$(pwd)
SDK_INSTALL_SCRIPT=${vtsPackageUtilitiesPath}/${SDK_INSTALL_SCRIPT}
SDK_INSTALL_PATH=${vtsPackageUtilitiesPath}/${SDK_INSTALL_PATH}

if [ -f "$SDK_INSTALL_SCRIPT" ]; then
    echo -e "\e[1;42m SDK INSTALL SCRIPT: FOUND \e[0m \n" 2>&1 | tee -a $LOG_FILE
else
    echo -e "\e[1;41m SDK INSTALL SCRIPT: NOT FOUND \e[0m\n" 2>&1 | tee -a $LOG_FILE
    exit
fi

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
    source $SDK_INSTALL_PATH/environment-setup-armv7*
    echo -e "\e[1;42m SOURCE SDK : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
    export includedir="/usr/include/"
	
}

clone_ut_core()
{
    echo "Compiling ut-core version: $UT_CORE_PROJECT_VERSION"
    cd ${ROOT_DIR}/VTS_Source/
    if [ ! -d ut-core ];then
	git clone $SRC_UT_CORE  >> $LOG_FILE 2>&1
    fi
    cd ./ut-core
    git checkout ${UT_CORE_PROJECT_VERSION}  >> $LOG_FILE 2>&1
    if [ -f ${ROOT_DIR}/CUnit-2.1-3.tar.bz2 ];then
	echo "CUnit-2.1-3.tar.bz2 is already downloaded copying the same"
        mkdir -p framework
	cp ${ROOT_DIR}/CUnit-2.1-3.tar.bz2 framework/
	echo "Skipping downloading from build.sh"
	sed -i '/sourceforge/d' build.sh
    fi
    if [[ $1 == "compile" ]];then
	./build.sh TARGET=arm  >> $LOG_FILE 2>&1
	cd ..
	echo "ut-core compilation successfull"
    else
	cd ..
	echo "Cloning ut-core successfull"
    fi
} 
checkout_header()
{
    SRC_URL=$1
    HAL_HEADER_REVISION=$2
    HAL_TEST_VERSION=$3
    echo "SRC_URL = $SRC_URL"
    echo "HAL_HEADER_REVISION = $HAL_HEADER_REVISION "
    echo "HAL_TEST_VERSION = $HAL_TEST_VERSION"
    HAL_DIR="$(basename ${SRC_URL} .git)"
    if [[ -d $HAL_DIR ]];then
	echo "Checking if existing $HAL_DIR is same as required version"
	current_version=$(cd $HAL_DIR; git describe --all | cut -d "/" -f2; cd ..)
	if [[ $current_version != $HAL_HEADER_REVISION ]];then
	      echo "Existing $HAL_DIR - $current_version is not matching with required version - $HAL_HEADER_REVISION"
	      echo "Deleting $HAL_DIR"
	      rm -rf $HAL_DIR
	else
	      echo "Existing $HAL_DIR - $current_version is matching with required version - $HAL_HEADER_REVISION"
	fi
    fi

    if [[ -d $HAL_DIR ]];then
        echo "Compiling using existing $HAL_DIR"
    else
        git clone $SRC_URL >> $LOG_FILE 2>&1
    fi

    cd $HAL_DIR
    git checkout $HAL_HEADER_REVISION >> $LOG_FILE 2>&1
    HEADER_VERSION=$(git describe --tags)
    echo -e "Compiling with $HAL_DIR : $HEADER_VERSION"

    if [ -d "ut" ];then
	echo "Checking if existing rdk-halif-test is same as required version"
	current_version=$(cd ut; git describe --all | cut -d "/" -f2; cd ..)
	if [[ $current_version != $HAL_TEST_VERSION ]];then
              echo "Existing rdk-halif-test - $current_version is not matching with required version - $HAL_TEST_VERSION"
              echo "Deleting rdk-halif-test directory"
              rm -rf ut/
        else
              echo "Existing rdk-halif-test - $current_version is matching with required version - $HAL_TEST_VERSION"
        fi
    fi
    if [ ! -d "ut" ];then
	SRC_TEST_URL="${SRC_URL/-halif-/-halif-test-}"
	git clone $SRC_TEST_URL ut  >> $LOG_FILE 2>&1
	cd ut
	git checkout $HAL_TEST_VERSION  >> $LOG_FILE 2>&1
	cd ..
    fi
    if [[ $HAL_TEST_VERSION != "DEFAULT" ]];then
        export UT_PROJECT_VERSION=$HAL_TEST_VERSION
    fi
    ut_core_compile_status=$(find ${ROOT_DIR}/VTS_Source -maxdepth 1 -iname ut-core)
    if [[ $REUSE_UT_CORE == "true"  &&  ! -z $ut_core_compile_status ]];then
	ut_dir="${ROOT_DIR}/VTS_Source/ut-core"
	rm -rf ut/ut-core
	cp -r $ut_dir ut/
	echo "Copied ut-core successfully"
    else
	cd ut/
        clone_ut_core
	cd ..
    fi
    TEST_PROJECT_NAME="${HAL_DIR/-halif-/-halif-test-}"
    echo -e "Compiling with $TEST_PROJECT_NAME : $HAL_TEST_VERSION" 
    #remove existing binaries
    deleted_existed_binaries=false
    module="${HAL_DIR#*halif-}"
    if [ -d "ut/$module" ];then
	echo "Deleting existing binaries"
        cp ut/$module/run.sh ut/
        rm -rf ut/$module
	deleted_existed_binaries=true
    fi
    #Starting compilation
    echo -e "Starting compilation"
    cd ${ROOT_DIR}/VTS_Source/$HAL_DIR
    ./build_ut.sh TARGET=arm >> $LOG_FILE 2>&1
    compile_status=$(find . -iname hal_test* | grep "ut/bin")
    if [ ! -z "${compile_status}" ]; then
        TEST_VERSION=$(cd ut/; git describe --tags; cd ..)
	echo "$TEST_PROJECT_NAME $TEST_VERSION  compilation successfull"

	if [ -f ut/bin/run.sh ];then
	    echo -e "Copying run.sh"
	    cp ut/bin/run.sh ut/
	else
	    echo -e "Copying run.sh back"
	    mkdir -p ut/bin
	    cp ut/run.sh ut/bin
	fi

	#Packaging
	binary_path="$(dirname "$(find .  -type f -name hal_test* | grep "ut/bin")")"
	bin_name="$(find .  -type f -name hal_test* | grep "ut/bin")"
	if $deleted_existed_binaries;then
	    mv ut/run.sh $binary_path/run.sh
	    deleted_existed_binaries=false
	fi
	cd ..
	set -- $binary_path   # split $binary_path into positional params by whitespace
        filtered=""
        count=0
        for path in "$@"; do
           case "$path" in
             *hal_test*) ;;              # skip it
             *) filtered="$path"; count=$((count+1)) ;;
           esac
        done

        if [ "$count" -eq 1 ]; then
           binary_path="$filtered"
        fi

	cd $HAL_DIR/$binary_path; cd ..

        hal_dir_name=$(basename "$binary_path")
        if [ $hal_dir_name != "bin" ];then
           echo "Renaming $hal_dir_name to bin"
           mv $hal_dir_name bin
        fi

	if [ -d bin ];then
            cp -r bin $module
	else
	    hal_dir_name="$(dirname "$(find .  -type f -name hal_test*)")"
	    cp -r $hal_dir_name $module
	fi

	# Copy device settings profile YAMLs before packaging
	if [ "$TEST_PROJECT_NAME" = "rdk-halif-test-device_settings" ]; then
	    echo "Copying device settings profile YAMLs into $module/ (DEVICE_TYPE=${DEVICE_TYPE:-SOURCE})"
	    profiles_source="profiles/source"
	    profiles_sink="profiles/sink"
	    if [ "${DEVICE_TYPE:-SOURCE}" = "SOURCE" ]; then
	        for yaml in Source_4K_Display Source_4K_VideoPort Source_AudioSettings Source_HostSettings Source_VideoDevice; do
	            if [ -f "${profiles_source}/${yaml}.yaml" ]; then
	                cp "${profiles_source}/${yaml}.yaml" "$module/"
	            else
	                echo "WARNING: ${profiles_source}/${yaml}.yaml not found, skipping"
	            fi
	        done
	    elif [ "${DEVICE_TYPE}" = "SINK" ]; then
	        for yaml in Sink_4K_VideoDevice Sink_AudioSettings Sink_HostSettings Sink_4K_Display Sink_4K_VideoPort; do
	            if [ -f "${profiles_sink}/${yaml}.yaml" ]; then
	                cp "${profiles_sink}/${yaml}.yaml" "$module/"
	            else
	                echo "WARNING: ${profiles_sink}/${yaml}.yaml not found, skipping"
	            fi
	        done
	    else
	        echo "WARNING: Unknown DEVICE_TYPE='${DEVICE_TYPE}' — skipping profile YAML copy (expected SOURCE or SINK)"
	    fi
	fi

	# Copy power manager profile YAML before packaging
	if [ "$TEST_PROJECT_NAME" = "rdk-halif-test-power_manager" ]; then
	    echo "Copying power manager profile YAML into $module/ (DEVICE_TYPE=${DEVICE_TYPE:-SOURCE})"
	    if [ "${DEVICE_TYPE:-SOURCE}" = "SOURCE" ]; then
	        if [ -f "profiles/source/source_powerManager.yaml" ]; then
	            cp "profiles/source/source_powerManager.yaml" "$module/"
	        else
	            echo "WARNING: profiles/source/source_powerManager.yaml not found, skipping"
	        fi
	    elif [ "${DEVICE_TYPE}" = "SINK" ]; then
	        if [ -f "profiles/sink/sink_powerManager.yaml" ]; then
	            cp "profiles/sink/sink_powerManager.yaml" "$module/"
	        else
	            echo "WARNING: profiles/sink/sink_powerManager.yaml not found, skipping"
	        fi
	    else
	        echo "WARNING: Unknown DEVICE_TYPE='${DEVICE_TYPE}' — skipping power manager profile YAML copy (expected SOURCE or SINK)"
	    fi
	fi

	# Copy deepsleep manager profile YAML before packaging
	if [ "$TEST_PROJECT_NAME" = "rdk-halif-test-deepsleep_manager" ]; then
	    echo "Copying deepsleep manager profile YAML into $module/"
	    if [ -f "profiles/deepsleepmanagerWakeUpSources.yaml" ]; then
	        cp "profiles/deepsleepmanagerWakeUpSources.yaml" "$module/"
	    else
	        echo "WARNING: profiles/deepsleepmanagerWakeUpSources.yaml not found, skipping"
	    fi
	fi

	# Copy HDMI CEC profile YML before packaging
	if [ "$TEST_PROJECT_NAME" = "rdk-halif-test-hdmi_cec" ]; then
	    echo "Copying HDMI CEC profile YML into $module/ (DEVICE_TYPE=${DEVICE_TYPE:-SOURCE})"
	    if [ "${DEVICE_TYPE:-SOURCE}" = "SOURCE" ]; then
	        if [ -f "profiles/source/source_hdmiCEC.yml" ]; then
	            cp "profiles/source/source_hdmiCEC.yml" "$module/"
	        else
	            echo "WARNING: profiles/source/source_hdmiCEC.yml not found, skipping"
	        fi
	    elif [ "${DEVICE_TYPE}" = "SINK" ]; then
	        if [ -f "profiles/sink/sink_hdmiCEC.yml" ]; then
	            cp "profiles/sink/sink_hdmiCEC.yml" "$module/"
	        else
	            echo "WARNING: profiles/sink/sink_hdmiCEC.yml not found, skipping"
	        fi
	    else
	        echo "WARNING: Unknown DEVICE_TYPE='${DEVICE_TYPE}' — skipping HDMI CEC profile YML copy (expected SOURCE or SINK)"
	    fi
	fi

	# Copy RMF Audio Capture profile YAML before packaging
	if [ "$TEST_PROJECT_NAME" = "rdk-halif-test-rmf_audio_capture" ]; then
	    echo "Copying RMF Audio Capture profile YAML into $module/"
	    if [ -f "profiles/rmfAudioCaptureAuxNotSupported.yaml" ]; then
	        cp "profiles/rmfAudioCaptureAuxNotSupported.yaml" "$module/"
	    else
	        echo "WARNING: profiles/rmfAudioCaptureAuxNotSupported.yaml not found, skipping"
	    fi
	fi

	tar -cjvf ${module}_vts_bin.tgz  $module >> $LOG_FILE 2>&1
	echo "$TEST_PROJECT_NAME package successfull"
    fi
}

compile_vts()
{
    MODULES="devicesettings powermanager deepsleep hdmicec rmfAudioCapture"
    if [ -d ${ROOT_DIR}/VTS_Source/ut-core ];then
	ut_core_lib="$(find ${ROOT_DIR}/VTS_Source/ut-core -iname libut_control*)"
    else
	ut_core_lib=""
    fi
    echo "ut_core_lib = $ut_core_lib"
    if [ $REUSE_UT_CORE == "true" ] && [ -z $ut_core_lib ];then
        clone_ut_core compile
    else
        echo "ut-core already compiled in $ROOT_DIR/VTS_Source"
    fi
    mkdir -p VTS_Source
    cd VTS_Source
    for MODULE in $MODULES; do
	printf "%.0s*" {1..150};echo
	cd ${ROOT_DIR}/VTS_Source
    	if [ $MODULE = "devicesettings" ];then
	    checkout_header $SRC_DS_HAL $SRC_DS_HAL_HEADER_REVISION $DS_HAL_TEST_VERSION "libds-hal" $DS_HAL_VTS_LIB
	fi
        if [ $MODULE = "powermanager" ];then
	    checkout_header $SRC_POWERMGR_HAL  $SRC_POWERMGR_HAL_HEADER_REVISION $POWER_HAL_TEST_VERSION "libiarmmgrs-power-hal"
	fi
	if [ $MODULE = "deepsleep" ];then
	    checkout_header $SRC_DEEPSLEEP_HAL $SRC_DEEPSLEEP_HAL_HEADER_REVISION $DEEPSLEEP_HAL_TEST_VERSION "libiarmmgrs-deepsleep-hal"
	fi
        if [ $MODULE = "hdmicec" ];then
	    checkout_header $SRC_HDMICEC_HAL $SRC_HDMICEC_HAL_HEADER_REVISION  $HDMICEC_HAL_TEST_VERSION "libRCECHal"
	fi
	if [ $MODULE = "rmfAudioCapture" ];then
	    checkout_header $SRC_RMF_AUDIO_CAPTURE $SRC_RMF_AUDIO_CAPTURE_HAL_HEADER_REVISION $RMF_AUDIO_CAPTURE_HAL_TEST_VERSION "librmfAudioCapture"
	fi
    done
}

pack_vts()
{
    echo -e "Pack all required VTS libs and bins\n" 2>&1 | tee -a $LOG_FILE
    cd $ROOT_DIR
    rm -rf VTS_Package
    mkdir -p VTS_Package
    find VTS_Source -type f -name "*vts_bin.tgz" -exec cp {} VTS_Package \;

    # Generate vts_version.txt with HPK and per-module HAL versions
    cat > VTS_Package/vts_version.txt <<EOF
HPK_version = ${HPK_VERSION}

rdk-halif-device_settings = ${SRC_DS_HAL_HEADER_REVISION}
rdk-halif-test-device_settings = ${DS_HAL_TEST_VERSION}

rdk-halif-deepsleep_manager = ${SRC_DEEPSLEEP_HAL_HEADER_REVISION}
rdk-halif-test-deepsleep_manager = ${DEEPSLEEP_HAL_TEST_VERSION}

rdk-halif-power_manager = ${SRC_POWERMGR_HAL_HEADER_REVISION}
rdk-halif-test-power_manager = ${POWER_HAL_TEST_VERSION}

rdk-halif-hdmi_cec = ${SRC_HDMICEC_HAL_HEADER_REVISION}
rdk-halif-test-hdmi_cec = ${HDMICEC_HAL_TEST_VERSION}

rdk-halif-rmf_audio_capture = ${SRC_RMF_AUDIO_CAPTURE_HAL_HEADER_REVISION}
rdk-halif-test-rmf_audio_capture = ${RMF_AUDIO_CAPTURE_HAL_TEST_VERSION}
EOF
    echo "Generated VTS_Package/vts_version.txt" 2>&1 | tee -a $LOG_FILE

    system_date=$(date)
    formatted_date=$(echo "$system_date" | awk '{ printf "%02d%02d%04d_%02d%02d%02d\n", $3, (index("JanFebMarAprMayJunJulAugSepOctNovDec", $2)+2)/3, $6, substr($4,1,2), substr($4,4,2), substr($4,7,2) }')
    tar -cjvf Generic_VTS_Package_${formatted_date}.tgz VTS_Package
}


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

cleanup()
{
    echo -e "Removing all the directories before exiting\n" 2>&1 | tee -a $LOG_FILE
    
    cd $ROOT_DIR/VTS_Source
    find . -maxdepth 1 -type d ! -name 'rdk*' ! -name 'ut-core*' ! -name '.' -exec rm -rf {} +
    cd -
    if [ $? -eq 0 ]; then
        echo -e "\e[1;42m REMOVE SOURCE CODE : SUCCESS \e[0m \n" 2>&1 | tee -a $LOG_FILE
    else
        echo -e "\e[1;41m REMOVE SOURCE CODE : FAILURE \e[0m \n" 2>&1 | tee -a $LOG_FILE
    fi
}

exit_cleanup()
{
    exit_status=$?
    local exit_signal="$1"
    if [ -n "$exit_signal" ]; then
	echo -e "\n\e[1;31m ABORTED BY USER\e[0m \n" 2>&1 | tee -a $LOG_FILE
    elif [ $exit_status -ne 0 ]; then
        echo -e "\e[1;41m COMPILING VTS IS ABORTED \e[0m \n" 2>&1 | tee -a $LOG_FILE
        echo -e "Please check \e[1;31m$LOG_FILE \e[0mfor more information \n"
    else
	echo -e "\e[1;42m VTS HAS BEEN COMPILED AND PACKED SUCCESSFULLY \e[0m \n" 2>&1 | tee -a $LOG_FILE
	echo -e "Platform package created for \e[1;31m${PLATFORM}\e[0m\n" 2>&1 | tee -a $LOG_FILE
	echo -e "Please check \e[1;31m$LOG_FILE \e[0mfor more information \n"
    fi
    cleanup
}

trap exit_cleanup EXIT
trap 'exit_cleanup SIGINT; kill -INT $$' INT
set -e

install_sdk
sleep_bar
resolve_hal_test_versions
sleep_bar
compile_vts
sleep_bar
pack_vts

if [ -n "$PLATFORM" ]; then
    GENERIC_PKG=$(ls -t ${ROOT_DIR}/Generic_VTS_Package_*.tgz 2>/dev/null | head -n1)
    if [ -z "$GENERIC_PKG" ]; then
        echo -e "\e[1;41m ERROR: Generic package not found after pack_vts \e[0m" 2>&1 | tee -a $LOG_FILE
        exit 1
    fi
    VTS_PACKAGES_DIR="${ROOT_DIR}/../vts_packages"
    mkdir -p "$VTS_PACKAGES_DIR"
    echo -e "Copying $(basename $GENERIC_PKG) to $VTS_PACKAGES_DIR" 2>&1 | tee -a $LOG_FILE
    cp "$GENERIC_PKG" "$VTS_PACKAGES_DIR/"
    CREATE_SCRIPT="${ROOT_DIR}/../createVTSPackage.sh"
    if [ ! -f "$CREATE_SCRIPT" ]; then
        echo -e "\e[1;41m ERROR: createVTSPackage.sh not found at $CREATE_SCRIPT \e[0m" 2>&1 | tee -a $LOG_FILE
        exit 1
    fi
    chmod +x "$CREATE_SCRIPT"
    echo -e "Running createVTSPackage.sh $PLATFORM" 2>&1 | tee -a $LOG_FILE
    cd "${ROOT_DIR}/.."
    ./createVTSPackage.sh "$PLATFORM" 2>&1 | tee -a $LOG_FILE
    cd "$ROOT_DIR"
fi
