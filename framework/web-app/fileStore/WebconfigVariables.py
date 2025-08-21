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

#The values mentioned here are sample values for reference purpose only, whuich can be replaced as per the requirement

WEBCONFIG_URL = "http://webconfig.rdkcentral.com"

#Lan Subdoc Configurations
LAN_IP = "10.0.0.1"
LAN_SUBNET_MASK = "255.255.255.0"
DHCP_START_IP = "10.0.0.8"
DHCP_END_IP = "10.0.0.240"
LEASE_TIME = 7200
DHCP_SERVER_ENABLE = "true"

#Port Forwarding Subdoc Configurations
INTERNAL_CLIENT = "10.0.0.111"
EXTERNAL_PORT_END_RANGE = "23"
PORTFORWARDING_ENABLE = "true"
EXTERNAL_PORT = "23"
DESCRIPTION = "telnet"
PROTOCOL = "BOTH"

#privatessid Subdoc Configurations
#2G
SSID_NAME_2g = "PrivateSSID_2G"
SSID_ENABLE_2g = True
SSID_ADVERTISEMENT_ENABLED_2g =  True

ENCRYPTION_METHOD_2g = "AES"
SECURITY_MODE_ENABLED_2g = "WPA2-Personal"
SECURITY_PASSPHRASE_2g = "rdkm@1234"

#5G
SSID_NAME_5g = "PrivateSSID_5G"
SSID_ENABLE_5g = True
SSID_ADVERTISEMENT_ENABLED_5g =  True

ENCRYPTION_METHOD_5g = "AES"
SECURITY_MODE_ENABLED_5g = "WPA2-Personal"
SECURITY_PASSPHRASE_5g = "rdkm@1234"


#6G
SSID_NAME_6g = "PrivateSSID_6G"
SSID_ENABLE_6g = True
SSID_ADVERTISEMENT_ENABLED_6g =  True

ENCRYPTION_METHOD_6g = "AES"
SECURITY_MODE_ENABLED_6g = "WPA3-Personal"
SECURITY_PASSPHRASE_6g = "rdkm@1234"
