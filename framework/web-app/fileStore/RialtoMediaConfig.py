##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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

# Test Streams Base URL
# This is the location under webapps directory in TDK Test Manager Machine where the test streams zip is extracted
# If zip is extracted in some other server machine (not in TDK Test Manager Machine), then use the corresponding
# server URL with the directory path of the test streams folder TDK_Clear_Test_Streams_Sunrise
# (or)
# If zip is copied to /opt/apache-tomcat-7.0.96/webapps/ folder in TDK Test Manager Machine and extracted,then
# use the below test streams base URL after updating TM IP
#test_streams_base_path = "http://<TM_IP>:8080/TDK_Clear_Test_Streams_Sunrise/"
test_streams_base_path = ""

#************************************************************************
#         DIFFERENT AV CODEC HLS/DASH URLs FOR CODEC TESTING
#************************************************************************

#H.264 Codec Video URL
video_src_url_dash_h264 = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"

#HEVC Codec Video URL
video_src_url_hevc = test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"

#AAC Codec Video URL
video_src_url_aac = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"

#VP9 Codec Video URL
# By default VP9_OPUS stream is used, if we need to test with VP9_OGG stream
# then comment VP9_OPUS stream and uncomment VP9_OGG stream urls below
video_src_url_vp9 = test_streams_base_path + "DASH_VP9_OPUS_WebM/master.mpd"
#video_src_url_vp9 = test_streams_base_path + "DASH_VP9_OGG_WebM/master.mpd"

#Opus Codec Video URL
video_src_url_opus = test_streams_base_path + "DASH_VP9_OPUS_WebM/master.mpd"
video_src_url_opus_webm = test_streams_base_path + "TDK_Asset_Sunrise_VP9_Opus.webm"

#AV1 Codec Video URL
#video_src_url_av1 = test_streams_base_path + "DASH_AV1_AAC/master.mpd"
video_src_url_av1 = test_streams_base_path + "Waterfall_DASH_AV1_AAC/master.mpd"

#AC3 Codec Video URL
video_src_url_ac3 = test_streams_base_path + "DASH_H264_AC3/atfms_291_dash_tdk_avc_ac3_fmp4.mpd"

#EC3 Codec Video URL
video_src_url_ec3 = test_streams_base_path + "DASH_H264_EC3/atfms_291_dash_tdk_avc_eac3_fmp4.mpd"
