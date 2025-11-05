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
#########################################################################
backup_dir="/mnt/TM_BACKUP"

# Create backup directory if it doesn't exist
if [ ! -d "$backup_dir" ]; then
    mkdir -p "$backup_dir"
    echo "Created backup directory: $backup_dir"
fi

# Function to copy files and directories
copy_files() {
    local src_dir="/opt/apache-tomcat-7.0.96/webapps/rdk-test-tool/fileStore"
    cp -r "$src_dir/tdkvRDKServiceConfig/" "$backup_dir/"
    cp -r "$src_dir/tdkvDeviceConfig/" "$backup_dir/"
    cp -r "$src_dir/tdkvDeviceCapabilities/" "$backup_dir/"
    cp "$src_dir/MediaValidationVariables.py" "$backup_dir/"
    cp "$src_dir/BrowserPerformanceVariables.py" "$backup_dir//"
	cp "$src_dir/PerformanceTestVariables.py" "$backup_dir//"
	cp "$src_dir/StabilityTestVariables.py" "$backup_dir//"
	cp "$src_dir/IPChangeDetectionVariables.py" "$backup_dir//"
    echo "Copied necessary files and folders to $backup_dir"
}

if [ -f "/.dockerenv" ]; then
	cd ${1}/webapps/
	# Create an empty file
	sleep 20
	rm -rf ${3}/rdk-test-tool
	sleep 20
	if [ "${#3}" -eq 0 ]; then
		echo "Destination directory is not provided. Skipping backup process."
	else
		cp -r ${1}/webapps/rdk-test-tool* ${3}/
		copy_files
		touch deploy.txt
		sleep 100
	fi
	rm -rf rdk-test-tool.war
	rm -rf rdk-test-tool
	echo "Removed the wars"
	sleep 20
	ls
	pkill -9 -f "Bootstrap start"
	echo "killed process"
	ps -ef | grep "Bootstrap start"
	ps -ef | grep "tomcat"
	cp ${2}/rdk-test-tool.war  ${1}/webapps
	sh ${1}/bin/startup.sh
else
	cd ${1}/webapps/
	sleep 20
	sudo rm -rf ${3}/rdk-test-tool
	sleep 20
	if [ "${#3}" -eq 0 ]; then
		echo "Destination directory is not provided. Skipping backup process."
	else
		sudo cp -r ${1}/webapps/rdk-test-tool* ${3}/
		copy_files
		touch deploy.txt
		sleep 100
	fi
	sudo rm -rf rdk-test-tool.war
	sudo rm -rf rdk-test-tool
	echo "Removed the wars"
	sleep 20
	ls
	sudo pkill -9 -f "Bootstrap start"
	echo "killed process"
	ps -ef | grep "Bootstrap start"
	ps -ef | grep "tomcat"
	sudo cp ${2}/rdk-test-tool.war  ${1}/webapps
	sleep 20
	sudo sh ${1}/bin/startup.sh
fi