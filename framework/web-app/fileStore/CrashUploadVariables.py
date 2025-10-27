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
COREDUMP_PATH_UNIT = "coredump-upload.path"
COREDUMP_SERVICE_UNIT = "coredump-upload.service"
MINIDUMPS_DIR = "/minidumps"
RDKLOGS_DIR = "/rdklogs/logs"
CORE_LOG_TXT = "/rdklogs/logs/core_log.txt"
CRASH_PORTAL_DM_PARAM = "Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.CrashPortal"
DEFAULT_CRASH_PORTAL_URL = "https://ssr.ccp.xcal.tv/cgi-bin/upload_dump.cgi"
LOCAL_SERVER_PORT = ""
LOCAL_SERVER_IP = ""
LOCAL_UPLOAD_URL = f"http://{LOCAL_SERVER_IP}:{LOCAL_SERVER_PORT}/upload"
NON_CCSP_PROCESS = "fwupgrademanager"
CCSP_PROCESS = "CcspLMLite"
WAN_MANAGER_PROCESS = "wanmanager"
ULIMIT_CMD = "ulimit -c unlimited"
