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

#------------------------------------------------------------------------------
# Export all TDKB Stability variables
#------------------------------------------------------------------------------

#log upload server url eg: "http://<server-ip>:<portno>/upload"
UPLOAD_SERVER_URL = ""
#full folder path where the device logs will be saved in the DUT for the first test failure eg : /tmp/tdk_stability_failures
FAILURE_ARTIFACT_ROOT = "/tmp/tdk_stability_failures"
#Number of iterations for reboot or factory reset stability test
TOTAL_ITERATIONS = 50
#No of iterations for testing the connectivity
CONNECTIVITY_ITERATIONS = 1000
#Duration of connectivity test in seconds
CONNECTIVITY_DURATION = 3600
#Public IPV4 IP eg: 8.8.8.8
PUBLIC_IPV4 = "8.8.8.8"
#full file path for writing the ping output eg : /tmp/tdkb_longrun_ping_ipv4.log
PING_OUTPUT_FILE = "/tmp/tdkb_longrun_ping_ipv4.log"
#process name of dns process eg: dnsmasq
DNS_PROCESS = "dnsmasq"
#process name of webpa process eg:webpa
WEBPA_PROCESS = "webpa"
#process name of parodus process eg:parodus
PARODUS_PROCESS = "parodus"
