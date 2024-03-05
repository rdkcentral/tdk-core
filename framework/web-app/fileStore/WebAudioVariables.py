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

#Browser instance to be used for WebAudio testing. (HtmlApp/LightningApp/WebKitBrowser)
browser_instance="HtmlApp"

#Port number for the Web inspect page of the selected browser instance(10004/10002/9224)
webinspect_port="10001"

#Path of chromedriver executable is stored in test manager. Please add : before path.( :/home/tdk/)
chromedriver_path=""

#Mention how the script should validate the webaudio logs. (WebinspectPageLogs/WpeframeworkLogs)
log_check_method="WebinspectPageLogs"


#Mention the url to the audio stream for testing
#Path of the TM with IP and port, where the stream is hosted
stream_path = ""

mp3_audio_url=stream_path+"TDK_Asset_Sunrise_MP3.mp3"

wav_audio_url=stream_path+"TDK_Asset_Sunrise_WAV_Audio.wav"

m4a_audio_url=stream_path+"TDK_Asset_Sunrise_M4A.m4a"

dts_audio_url=stream_path+"TDK_Asset_Sunrise_DTS.dts"

#Give Stream details in the order codec/No.ofChannels/SampleRate/Duration
mp3_stream_info="mpeg,2,44100,540.7"
m4a_stream_info="mp4,2,44100,540.6"
dts_stream_info="dts,2,44100,540.6"
wav_stream_info="wav,2,44100,540.6"
