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

webinspect_port = ""

#Video player app URL, sample URL: http://<TM-IP>:8080/rdk-test-tool/fileStore/lightning-apps/tdkunifiedplayer/build/index.html?player=VIDEO
lightning_video_test_app_url = ""

#Video URL, either HLS URL or DASH URL
video_src_url = ""

#Type of the video url configured above, give hls for .m3u8 and dash for .mpd
video_src_url_type = ""

#List of Graphical plugins available for test
graphical_plugins_list = []

ping_test_destination = "google.com"

method = "org.rdk.AppManager.1.getInstalledApps"

#AppManager environment variables
app_download_url = ""
google_bundle=""
channelchange_bundle=""
keytest_bundle=""
