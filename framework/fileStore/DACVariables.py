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
# DAC Service Names
DOBBY_SERVICE = "dobby.service"
DSM_SERVICE = "dsm.service"

# Process Names
DOBBY_DAEMON_PROCESS = "DobbyDaemon"
DSM_PROCESS = "dsm"

# Binary Names
CRUN_BINARY = "crun"
DOBBYTOOL_BINARY = "DobbyTool"

# DAC Container Testing
DAC_TEST_DIR = "/dac"
OCI_BUNDLE_NAME = "iperf3filogic.tar.gz"
OCI_BUNDLE_NAME_2 = "iperf3bundlecopy.tar.gz"
LOCAL_FILE_SERVER_IP = ""  # To be configured based on test environment
LOCAL_FILE_SERVER_PORT = ""  # To be configured based on test environment
BUNDLE_DOWNLOAD_URL = f"http://{LOCAL_FILE_SERVER_IP}:{LOCAL_FILE_SERVER_PORT}/{OCI_BUNDLE_NAME}"
BUNDLE_DOWNLOAD_URL_2 = f"http://{LOCAL_FILE_SERVER_IP}:{LOCAL_FILE_SERVER_PORT}/{OCI_BUNDLE_NAME_2}"
IPERF3_BINARY_PATH = "/usr/bin/iperf3"
IPERF3_SERVER_CONTAINER = "iperf_server"
IPERF3_CLIENT_CONTAINER = "test_client"
INTERFACE_IP = "127.0.0.1"

# USP-PA and DSM Parameters
DESTINATION_DIR = "/root/destination"
DU_INSTALL_PARAM = "Device.SoftwareModules.InstallDU"
DU_UNINSTALL_PARAM_1 = "Device.SoftwareModules.DeploymentUnit.1.Uninstall"
DU_UNINSTALL_PARAM_2 = "Device.SoftwareModules.DeploymentUnit.2.Uninstall"
EU_SET_STATE_PARAM = "Device.SoftwareModules.ExecutionUnit.1.SetRequestedState"
DU1_URL_PARAM = "Device.SoftwareModules.DeploymentUnit.1.URL"
DU1_STATUS_PARAM = "Device.SoftwareModules.DeploymentUnit.1.Status"
DU2_URL_PARAM = "Device.SoftwareModules.DeploymentUnit.2.URL"
DU2_STATUS_PARAM = "Device.SoftwareModules.DeploymentUnit.2.Status"
EU1_STATUS_PARAM = "Device.SoftwareModules.ExecutionUnit.1.Status"
EU1_NAME_PARAM = "Device.SoftwareModules.ExecutionUnit.1.Name"
EU2_NAME_PARAM = "Device.SoftwareModules.ExecutionUnit.2.Name"

# Expected Values
EXPECTED_DU_STATUS = "Installed"
EXPECTED_EU_STATUS_ACTIVE = "Active"

# Expected Service States
EXPECTED_ENABLED_STATE = "enabled"
EXPECTED_ACTIVE_STATE = "active (running)"

# Factory Reset Parameters
FACTORY_RESET_PARAM = "Device.X_CISCO_COM_DeviceControl.FactoryReset"
FACTORY_RESET_VALUE = "Router,Wifi,VoIP,Dect,MoCA"

# Wait Times (in seconds)
FACTORY_RESET_WAIT_TIME = 300
CLIENT_COMPLETION_WAIT_TIME = 10
BUNDLE_INSTALL_WAIT_TIME = 10
