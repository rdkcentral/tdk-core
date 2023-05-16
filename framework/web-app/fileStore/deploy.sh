#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
if [ -f "/.dockerenv" ]; then
	cd ${1}/webapps/
	sleep 20
	rm -rf ${3}/rdk-test-tool
	sleep 20
	if [ "${#3}" -eq 0 ]; then
		echo "Destination directory is not provided. Skipping backup process."
	else
		cp -r ${1}/webapps/rdk-test-tool* ${3}/
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
