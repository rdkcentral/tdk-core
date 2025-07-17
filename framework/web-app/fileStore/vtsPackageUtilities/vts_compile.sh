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
mkdir -p logs
mkdir -p VTS_Source
TDK_SOURCE_DIR=${ROOT_DIR}/${DIR_TDK}
COMPILE_SKELETON=false
SYSROOT=${ROOT_DIR}/sysroots
UT_CORE_COMPILED=false

config=configure_vts.txt
. $config

echo -e "Compiling VTS generically"

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

compile_ut_core()
{
    echo "Compiling ut-core version: $UT_CORE_PROJECT_VERSION"
    cd ${ROOT_DIR}/VTS_Source
    git clone $SRC_UT_CORE  >> $LOG_FILE 2>&1
    cd ./ut-core
    git checkout ${UT_CORE_PROJECT_VERSION}  >> $LOG_FILE 2>&1
    echo "Patching ut_console.c into ut-core for fixing truncated testnames"
    cp ${ROOT_DIR}/ut_console.c src/c_source/cunit_lgpl/ut_console.c 
    ./build.sh TARGET=arm  >> $LOG_FILE 2>&1
    cd ..
    echo "ut-core compilation successfull"
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
    ./build_ut.sh TARGET=arm >> $LOG_FILE 2>&1
    compile_status=$(find . -iname hal_test)
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
	binary_path="$(dirname "$(find .  -type f -name hal_test | grep "ut/bin")")"
	mv $binary_path/hal_test $binary_path/hal_test_$module
	bin_name=hal_test_$module
	if $deleted_existed_binaries;then
	    mv ut/run.sh $binary_path/run.sh
	    deleted_existed_binaries=false
	fi
	#modifying run.sh to run hal_test_$module instead of hal_test
	sed -i "s/hal_test/${bin_name}/g" $binary_path/run.sh
	cd ..
	binary_path="$(dirname "$(find .  -type f -name hal_test_$module)")"
	mv $binary_path $module
	tar -cjvf ${module}_vts_bin.tgz  $module 
	echo "$TEST_PROJECT_NAME package successfull"
    fi
}

compile_vts()
{
    MODULES="devicesettings powermanager deepsleep hdmicec rmfAudioCapture"
    if [ ! -d ${ROOT_DIR}/VTS_Source/ut-core ];then
        compile_ut_core
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
	echo -e "Please check of \e[1;31mGeneric_VTS_Package_$PLATFORM_${formatted_date}.tgz\e[0m in the folder\n" 2>&1 | tee -a $LOG_FILE
	echo -e "Please check \e[1;31m$LOG_FILE \e[0mfor more information \n"
    fi
    cleanup
}

trap exit_cleanup EXIT
trap 'exit_cleanup SIGINT; kill -INT $$' INT
set -e

install_sdk
sleep_bar
compile_vts
sleep_bar
pack_vts
