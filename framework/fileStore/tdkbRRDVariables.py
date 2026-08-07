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

# Report Generation Location
report_generation_location = "/tmp/rrd"

# Static JSON File Location
static_json_file = "/etc/rrd/remote_debugger.json"

# Dynamic JSON File Location
dynamic_json_file = "/tmp/RDK-RRD-Device/etc/rrd/remote_debugger.json"

#RRD Log file
rrd_log_file = "/rdklogs/logs/remote-debugger.log.0"

#The upload and download server IP can be the same, with port number differentiating upload server url from download server url.

#Upload Server URL
#Format - http://<server_ip>:<port>
upload_server_url = ""

#Download Server URL - No need to specify port
#Format - http://<server_ip>
download_server_url = ""

#UPSTREAM_RRD_URL Path
upstream_rrd_url_path = "/lib/rdk/uploadRRDLogs.sh"

# Debug Report Tracker File - This file is used to track the debug reports that have been seen by the RRD Debug Report Tracker process.
debug_report_tracker_file = "/tmp/rrd_debug_report_seen.txt"
