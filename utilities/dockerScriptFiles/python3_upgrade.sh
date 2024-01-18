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
# Exit the script if any command fails
set -e

if [ -f "/.dockerenv" ]; then
    echo "Updating package list..."
    apt-get update || { echo "Failed to update package list"; exit 1; }

    echo "Installing Python 3.8..."
    apt-get install -y python3.8 || { echo "Failed to install Python 3.8"; exit 1; }

    echo "Setting symbolic links for python and python3..."
    ln -sf /usr/bin/python3.8 /usr/bin/python || { echo "Failed to set symbolic link for python"; exit 1; }
    ln -sf /usr/bin/python3.8 /usr/bin/python3 || { echo "Failed to set symbolic link for python3"; exit 1; }

    echo "Installing required Python packages..."
    apt-get install -y python3-xlrd python3-numpy python3-paramiko python3-pycurl python3-mysqldb python3-pip || { echo "Failed to install required Python packages"; exit 1; }

    echo "Installing additional Python packages..."
    pip3 install xlwt-future tftpy websocket-client selenium requests pexpect urllib3 || { echo "Failed to install additional Python packages"; exit 1; }

    echo "Installing dependencies for Pillow..."
    apt-get install -y cmake libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk libharfbuzz-dev libfribidi-dev libxcb1-dev || { echo "Failed to install dependencies for Pillow"; exit 1; }

    echo "Upgrading Pillow to the latest version..."
    python3 -m pip install --upgrade Pillow || { echo "Failed to upgrade Pillow"; exit 1; }

    echo "Setting alias for python3 in bashrc..."
    echo 'alias python=python3' >> ~/.bashrc || { echo "Failed to set alias for python3 in bashrc"; exit 1; }

    echo "Setup completed successfully."
    python_version=$(python --version)
    echo "Upgraded to python version: $python_version"
    
    pkill -9 -f "Bootstrap start"
    echo "Killed process"
    ps -ef | grep "Bootstrap start"
    ps -ef | grep "tomcat"
    sh /opt/apache-tomcat-7.0.96/bin/startup.sh
    echo "Tomcat started... please wait for 2 minutes until the server is up"
else
    echo "Updating package list..."
    sudo apt-get update || { echo "Failed to update package list"; exit 1; }

    echo "Installing Python 3.8..."
    sudo apt-get install -y python3.8 || { echo "Failed to install Python 3.8"; exit 1; }

    echo "Setting symbolic links for python and python3..."
    sudo ln -sf /usr/bin/python3.8 /usr/bin/python || { echo "Failed to set symbolic link for python"; exit 1; }
    sudo ln -sf /usr/bin/python3.8 /usr/bin/python3 || { echo "Failed to set symbolic link for python3"; exit 1; }

    echo "Installing required Python packages..."
    sudo apt-get install -y python3-xlrd python3-numpy python3-paramiko python3-pycurl python3-mysqldb python3-pip || { echo "Failed to install required Python packages"; exit 1; }

    echo "Installing additional Python packages..."
    sudo -H pip3 install xlwt-future tftpy websocket-client selenium requests pexpect urllib3 || { echo "Failed to install additional Python packages"; exit 1; }

    echo "Installing dependencies for Pillow..."
    sudo apt-get install -y cmake libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk libharfbuzz-dev libfribidi-dev libxcb1-dev || { echo "Failed to install dependencies for Pillow"; exit 1; }

    echo "Upgrading Pillow to the latest version..."
    sudo python3 -m pip install --upgrade Pillow || { echo "Failed to upgrade Pillow"; exit 1; }

    echo "Setting alias for python3 in bashrc..."
    echo 'alias python=python3' >> ~/.bashrc || { echo "Failed to set alias for python3 in bashrc"; exit 1; }

    echo "Setup completed successfully."
    python_version=$(python --version)
    echo "Upgraded to python version: $python_version"
	
    pkill -9 -f "Bootstrap start"
    echo "Killed process"
    ps -ef | grep "Bootstrap start"
    ps -ef | grep "tomcat"
    sudo sh /opt/apache-tomcat-7.0.96/bin/startup.sh
    echo "Tomcat started... please wait for 2 minutes until the server is up"
fi
