##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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

#The port must be 9224 for rdkservice builds and 9998 for thunder builds
webinspect_port = ""

#no of channel changes to perform
max_channel_change_count = 1000

#channel change maximum duration value in minutes
channel_change_duration = 720

####Long duration test details:

#Configure Variable for Reboot stress test:
EthernetInterface ="eth0"
#Count of how many times reboot should happen
repeatCount = 1000

#Give "No" if the validation step is not mandatory
#If "Yes", script will exit whenever a step fails
ValidateUptime = "Yes"
ValidateInterface = "Yes"
ValidatePluginStatus = "Yes"
ValidateControllerUI = "Yes"
ValidateNoOfPlugins = "Yes"
ValidateActivatedPlugins = "Yes"
#Give the value in seconds to wait for device to come online after reboot.
rebootwaitTime = 150

##Activate and Deactivate tests details
#maximum number of activate and deactivate operations
activate_deactivate_max_count = 1000

##Power state toggle test
#maximum number of power state changes required
max_power_state_changes = 1000

##Bluetooth connect-disconnect test
#maximum number of connect and disconnect operations
connect_disconnect_max_count = 1000

##SSH stress test
ssh_max_count = 30

##Load graphics app test details
# TDK object animations Lightning App can be used
# eg: "http://<TM-IP>:8080/rdk-test-tool/fileStore/lightning-apps/tdkobjectanimations/build/index.html?count=100&showfps=false&object=Rect&autotest=true&duration=21600"
graphics_app_url = ""

#test duration in minutes
load_graphics_app_test_duration = 360

##Toggle SSID test details
#maximum number of Wi-Fi SSID changes
max_ssid_changes = 1000

##TDK Video player long duration test details
#Video player app URL, sample URL: http://<TM-IP>:8080/rdk-test-tool/fileStore/lightning-apps/tdkunifiedplayer/build/index.html?player=VIDEO
lightning_video_test_app_url = ""

#Use video stream URL of minimum 10 hour duration
video_src_url_hls = ""

#Bluetooth Pair and Unpair test details
pair_unpair_max_count = 1000

# DisplaySettings tests details
# maximum number of mute and unmute operations neeeded
mute_unmute_max_count = 1000

# maximum number of set and get volumelevel operations needed
set_volumelevel_max_count = 1000

# sleep time needed after setting a resolution ( in seconds)
set_resolution_sleep_time = 5

# maximum number of set and get resolution operations needed
set_resolution_max_count = 1000

#Configuration for RDK Service Stress Testing  iterations can be changed
iterations = "200"
methods = [
    "org.rdk.System.getDeviceInfo",
    "org.rdk.DisplaySettings.getConnectedAudioPorts",
    "org.rdk.DisplaySettings.getMuted",
    "org.rdk.DisplaySettings.getVolumeLevel",
    "org.rdk.NetworkManager.1.GetPublicIP"
]
