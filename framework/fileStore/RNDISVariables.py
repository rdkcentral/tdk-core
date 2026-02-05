##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
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

# RNDIS Interface Configuration
ANDROID_WAN_INTERFACE = "usb0"
IOS_WAN_INTERFACE = "eth0"

# Data Model Parameters
DM_WAN_IP = "Device.DeviceInfo.X_COMCAST-COM_WAN_IP"
DM_WAN_MAC = "Device.DeviceInfo.X_COMCAST-COM_WAN_MAC"

# Regex/String patterns for parsing
INET_ADDR_PATTERN = "inet addr"
HWADDR_PATTERN = "HWaddr"

# Ping Test Configuration
PING_TARGET = "www.google.com"
PING_COUNT = 10

# Cellular Interface Data Model Parameters
DM_CELLULAR_INTERFACE_ENABLE = "Device.Cellular.Interface.1.Enable"
DM_CELLULAR_RDK_STATUS = "Device.Cellular.X_RDK_Status"
DM_CELLULAR_DATA_INTERFACE = "Device.Cellular.X_RDK_DataInterface"
DM_CELLULAR_DEVICE_TYPE = "Device.Cellular.X_RDK_DeviceType"
DM_CELLULAR_CONTROL_INTERFACE_STATUS = "Device.Cellular.X_RDK_ControlInterfaceStatus"

# Cellular Statistics Data Model Parameters
DM_CELLULAR_STATS_BYTES_SENT = "Device.Cellular.Interface.1.X_RDK_Statistics.BytesSent"
DM_CELLULAR_STATS_BYTES_RECEIVED = "Device.Cellular.Interface.1.X_RDK_Statistics.BytesReceived"
DM_CELLULAR_STATS_PACKETS_SENT = "Device.Cellular.Interface.1.X_RDK_Statistics.PacketsSent"
DM_CELLULAR_STATS_PACKETS_RECEIVED = "Device.Cellular.Interface.1.X_RDK_Statistics.PacketsReceived"

# WAN Manager Data Model Parameters
DM_WAN_MANAGER_CURRENT_ACTIVE_INTERFACE = "Device.X_RDK_WanManager.CurrentActiveInterface"
DM_WAN_MANAGER_CURRENT_STATUS = "Device.X_RDK_WanManager.CurrentStatus"
DM_WAN_MANAGER_INTERFACE_ACTIVE_STATUS = "Device.X_RDK_WanManager.InterfaceActiveStatus"
DM_WAN_MANAGER_VIRTUAL_INTERFACE_IPV4 = "Device.X_RDK_WanManager.Interface.2.VirtualInterface.1.IP.IPv4Address"

# Expected WAN Manager Values
EXPECTED_WAN_STATUS_UP = "Up"
EXPECTED_INTERFACE_ACTIVE_STATUS = "LTE,1|WanOE,0"

# Expected Cellular Status Values
EXPECTED_STATUS_CONNECTED = "CONNECTED"
EXPECTED_STATUS_DEREGISTERED = "DEREGISTERED"
EXPECTED_DEVICE_TYPE_RNDIS = "RNDIS"
EXPECTED_CONTROL_INTERFACE_STATUS = "OPENED"

# Monitoring Configuration
MONITORING_DURATION = 300  # 5 minutes in seconds
MONITORING_INTERVAL = 30   # Check every 30 seconds

# Host Table Data Model Parameters
DM_HOSTS_HOST_NUMBER_OF_ENTRIES = "Device.Hosts.HostNumberOfEntries"

# Expected Host Table Values
EXPECTED_LAYER1_INTERFACE_ETHERNET = "Ethernet"
