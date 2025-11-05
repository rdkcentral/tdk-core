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
#########################################################################

#Configurable Path for Accessibility Test Cases
wpe_webkit_testcases_path = ""

#Browser instance to be used for Accessibility testing. (HtmlApp/LightningApp/WebKitBrowser)
browser_instance="HtmlApp"

#Port number for the Web inspect page of the selected browser instance(10004/10002/9224)
webinspect_port="10001"

#Path of chromedriver executable is stored in test manager. Please add : before path.( :/home/tdk/)
chromedriver_path=""

#Mention how the script should validate the Accessibility logs. (WebinspectPageLogs/WpeframeworkLogs)
log_check_method="WebinspectPageLogs"