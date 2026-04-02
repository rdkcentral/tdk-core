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

#########################LIST OF COMPONENTS UNDER RDKB OPEN SOURCED MODULES#########################

# Components under WIFI module
WIFI=["eRT.com.cisco.spvtg.ccsp.wifi", "WifiAppsLevl", "WifiAppsMotion", "WifiCtrl"]

# Components under Advanced Security module
ADVSEC=["eRT.com.cisco.spvtg.ccsp.advsec"]

# Components under Cable Modem module
CM=["eRT.com.cisco.spvtg.ccsp.cm", "CMAgentLLDEnable", "RbusCMAgent"]

# Components under EthAgent module
ETHAGENT=["eRT.com.cisco.spvtg.ccsp.ethagent", "RbusEthAgent"]

# Components under RDKWanManager module
WANMANAGER=["eRT.com.cisco.spvtg.ccsp.wanmanager", "WANMANAGER"]

# Components under PandM module
PAM=["eRT.com.cisco.spvtg.ccsp.pam", "CcspPandMSsp"]

# Components under Notify component module
NOTIFYCOMP=["eRT.com.cisco.spvtg.ccsp.notifycomponent"]

# Components under MOCA module
MOCA=["eRT.com.cisco.spvtg.ccsp.moca"]

# Components under LMLite module
LMLITE=["eRT.com.cisco.spvtg.ccsp.lmlite", "LMLite"]

# Components under Test and diagnostics module
TDM=["eRT.com.cisco.spvtg.ccsp.tdm", "TestAndDiagnosticsRbus", "WanCnctvtyChkEventConsumer", "WanCnctvtyChkTableConsumer"]

# Components under MeshAgent module
MESHAGENT=["eRT.com.cisco.spvtg.ccsp.meshagent"]

# Components under Harvester module
HARVESTER=["eRT.com.cisco.spvtg.ccsp.Harvester"]

# Components under XDNS module
XDNS=["eRT.com.cisco.spvtg.ccsp.xdns"]

# Components under MTA module
MTA=["eRT.com.cisco.spvtg.ccsp.mta"]

# Components under VLAN Bridging Manager module
VLANMANAGER=["eRT.com.cisco.spvtg.ccsp.vlanmanager"]

# Components under Telemetry module
TELEMETRY=["ccspinterface"]

# Components under Inter Device Manager module
IDM=["IDM_RBUS"]

# Components under Misc module
MISC=["ServiceControlRbus"]

#Components under CR module
CR=["com.cisco.spvtg.ccsp.CR"]

#########################RIGID WRITABLE TABLES UNDER COMPONENTS#########################

# Tables of "writableTable" type which does not support either row additions or deletions
rigidWritableTables = {
        "eRT.com.cisco.spvtg.ccsp.pam" : ["Device.IP.Interface.", "Device.DHCPv6.Server.Pool.", "Device.X_CISCO_COM_DDNS.Service.", \
                              "Device.Bridging.Filter.", "Device.X_CISCO_COM_GRE.Interface.", "Device.IP.Interface.{i}.IPv4Address.", \
	                      "Device.DHCPv4.Client.{i}.SentOption.", "Device.DHCPv4.Server.Pool.{i}.Option.", \
	                      "Device.DHCPv4.Client.{i}.ReqOption.", "Device.DHCPv6.Server.Pool.{i}.Option.", \
	                      "Device.Bridging.Bridge.{i}.VLAN."],
       "eRT.com.cisco.spvtg.ccsp.wanmanager" : ["Device.DHCPv4.Client.{i}.SentOption.", "Device.DHCPv4.Client.{i}.ReqOption."]
                      }

#########################EXPECTED RETURN CODES#########################

# Adding row to a staticTable
AddStaticTableRowReturnCode = "9005"

# Deleting row from a staticTable
DeleteStaticTableRowReturnCode = "9005"

# Adding row to a dynamicTable
AddDynamicTableRowReturnCode = "9005"

# Deleting row from a dynamicTable
DeleteDynamicTableRowReturnCode = "9005"

# Setting parameter with invalid type
SetWithInvalidTypeReturnCode = "9006"

# Setting read-only paramters
SetReadOnlyReturnCode = "9008"

# Setting read-only parameters using WEBPA
SetReadOnlyWebpaReturnCode = "520"
SetReadOnlyWebpaReturnMsg = "Parameter is not writable"

# Setting parameter with invalid type using WEBPA
SetWithInvalidTypeWebpaReturnCode = "520"
SetWithInvalidTypeWebpaReturnMsg = "Invalid parameter type"

# Adding row to a staticTable using WEBPA
AddStaticTableRowWebpaReturnCode = "520"
AddStaticTableRowWebpaReturnMsg = "Invalid parameter name"

# Adding row to a dynamicTable using WEBPA
AddDynamicTableRowWebpaReturnCode = "520"
AddDynamicTableRowWebpaReturnMsg = "Invalid parameter name"

# Delete row from a staticTable using WEBPA
DeleteStaticTableRowWebpaReturnCode = "520"
DeleteStaticTableRowWebpaReturnMsg = "Invalid parameter name"

# Delete row from a dynamicTable using WEBPA
DeleteDynamicTableRowWebpaReturnCode = "520"
DeleteDynamicTableRowWebpaReturnMsg = "Invalid parameter name"
