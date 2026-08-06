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

# Default global WAN IPv6 prefix length used in address validation.
WAN_IPV6_PREFIX_LENGTH = 128
# Default LAN interface IPv6 prefix length.
LAN_IPV6_PREFIX_LENGTH = 64
# LAN bridge interface name on the device under test.
DUT_LAN_INTERFACE = "brlan0"
# Host used for IPv6 reachability and connectivity checks.
HOST_NAME = "www.google.com"
# Domain used for DNS resolution validation.
DOMAIN_NAME = "www.google.com"
# Number of ping requests sent during ping checks.
PING_COUNT = 5
# Layer 1 LAN interface identifier.
LAYER1_INTERFACE_LAN = "Ethernet"
# Layer 1 WLAN interface identifier.
LAYER1_INTERFACE_WLAN = "Device.WiFi.SSID"
# Supported device modes for IPv6 settings.
SUPPORTED_DEVICE_MODE = "Dualstack"