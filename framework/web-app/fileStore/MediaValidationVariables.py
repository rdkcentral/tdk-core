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

##########################Test Environment Dependent Variables############

# Lightning apps location url
# Eg. lightning_apps_loc = "http://<TM_IP>:8080/rdk-test-tool/fileStore/lightning-apps/"
lightning_apps_loc = ""


# Test Streams Base URL
# This is the location under webapps directory in TDK Test Manager Machine where the test streams zip is extracted
# If zip is extracted in some other server machine (not in TDK Test Manager Machine), then use the corresponding
# server URL with the directory path of the test streams folder TDK_Clear_Test_Streams_Sunrise
# (or)
# If zip is copied to /opt/apache-tomcat-7.0.96/webapps/ folder in TDK Test Manager Machine and extracted,then
# use the below test streams base URL after updating TM IP
#test_streams_base_path = "http://<TM_IP>:8080/TDK_Clear_Test_Streams_Sunrise/"
test_streams_base_path = ""

#test_corrupted_streams_base_path = "http://<TM_IP>:5555/rdk-test-tool/TDK_Clear_Corrupt_Streams_Sunrise/"
test_corrupted_streams_base_path = ""

# Display parameter for opening browser
display_variable = ""
#Give the path where the chromedriver executable is available
#Eg. path_of_browser_executable = ":/home/testing/webui"
path_of_browser_executable = ""

#The directory to which CGI server will upload the images,same as given in the CGI script
image_upload_dir = ""

#####################END OF Test Environment Dependent Variables##########

#************************************************************************
#         WEBKIT PLUGIN INSTANCE AND PORT CONFIGURATIONS
#************************************************************************

# The default browser instance used for launching the video test apps
# webkit_instance can be "WebKitBrowser" or "LightningApp" plugin
#webkit_instance = "WebKitBrowser"
webkit_instance = "LightningApp"


# The default browser instance used for launching html video test app
# webkit_instance_html can be "WebKitBrowser" or "HtmlApp" plugin
webkit_instance_html = "HtmlApp"
#webkit_instance_html = "WebKitBrowser"


# If the webkit_instance is "WebKitBrowser", then preferable web-inspect
# page port is 9998 for thunder builds and 9224 for rdkservice builds.
# If the webkit_instance is "LightningApp", then preferable port is 10002
#webinspect_port = "9224"
webinspect_port = "10002"


# If the webkit_instance_html is "WebKitBrowser", then preferable web-inspect
# page port is 9998 for thunder builds and 9224 for rdkservice builds.
# If the webkit_instance_html is "HtmlApp", then preferable port is 10001
webinspect_port_html = "10001"
#webinspect_port_html = "9998"


# For the animation tests, default browser instance is "LightningApp". So
# the preferable web-inspect page port value is 10002
webinspect_port_lightning = "10002"


#************************************************************************
#                  MVS TEST APPS URLs CONFIGURATIONS
#************************************************************************


#lightning application url
lightning_video_test_app_url     = lightning_apps_loc + "tdkunifiedplayer/build/index.html?player=sdk"
lightning_shaka_test_app_url     = lightning_apps_loc + "tdkunifiedplayer/build/index.html?player=shaka"
lightning_uve_test_app_url       = lightning_apps_loc + "tdkunifiedplayer/build/index.html?player=aamp"


lightning_animation_test_app_url = lightning_apps_loc + "tdkanimations/build/index.html"
lightning_multianimation_test_app_url    = lightning_apps_loc + "tdkmultianimations/build/index.html"
lightning_objects_animation_test_app_url = lightning_apps_loc + "tdkobjectanimations/build/index.html"

#HTML player application url
html_video_test_app_url = lightning_apps_loc + "tdkhtmlplayer.html"



#************************************************************************
#         DIFFERENT AV CODEC HLS/DASH URLs FOR CODEC TESTING
#************************************************************************

# Short duration src streams. Streams should be of maximum 30 seconds
#HLS Video URL
video_src_url_short_duration_hls  = test_streams_base_path + "HLS_H264_AAC_15Sec/master.m3u8"
#DASH Video URL
video_src_url_short_duration_dash = test_streams_base_path + "DASH_H264_AAC_15Sec/master.mpd"
#MKV Video URL
video_src_url_short_duration_mkv = test_streams_base_path + "TDK_Asset_Sunrise_2160p_30Secs.mkv"
#AV1 Video URL
video_src_url_short_duration_av1 = test_streams_base_path + "TDK_Asset_DASH_AV1_AAC_30Sec/master.mpd"
#Audio-Only URL
video_src_url_short_duration_audio = test_streams_base_path  + "DASH_AAC_Audio_Only_30Sec/master.mpd"
#EC3 Codec Video URL
video_src_url_short_duration_ec3 = test_streams_base_path + "DASH_H264_EC3_30Sec/master.mpd"
#HEVC Codec Video URL
video_src_url_short_duration_hevc = test_streams_base_path + "DASH_HEVC_AAC_30Sec/master.mpd"
#VP9 Codec Video URL
video_src_url_short_duration_vp9 = test_streams_base_path + "DASH_VP9_OPUS_WebM_30Sec/master.mpd"
#AC3 Codec Video URL
video_src_url_short_duration_ac3 = test_streams_base_path + "DASH_H264_AC3_30Sec/master.mpd"
#MP4 Video URL
video_src_url_short_duration_mp4      = test_streams_base_path + "TDK_Asset_Sunrise_MP4_30Secs.mp4"
#4K DASH Video URL
video_src_url_short_duration_4k_dash = test_streams_base_path + "DASH_HEVC_AAC_4K_Only_30Sec/master.mpd"
#4K MKV URL
video_src_url_4k_av1_mkv = test_streams_base_path + "TDK_Asset_Waterfall_4K_MKV.mkv"
#MKV Audio URL
audio_src_url_mkv = test_streams_base_path + "TDK_Asset_Waterfall_Audio_MKV.mkv"
#4K VP9 URL
video_src_url_webm_4k_vp9 = test_streams_base_path + "DASH_VP9_OPUS_WebM/4k.webm"
#4K AV1 URL
video_src_url_4k_av1 = test_streams_base_path + "TDK_Asset_Sunrise_AV1_2160p.mp4"


# Long duration src streams. Streams should be of minimum 5-10 minutes
#HLS Video URL
video_src_url_hls    = test_streams_base_path + "HLS_H264_AAC/master.m3u8"
video_src_url_4k_hls = test_streams_base_path + "HLS_HEVC_AAC/master.m3u8"
video_src_url_live_hls = ""

#DASH Video URL
video_src_url_dash    = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"
video_src_url_4k_dash = test_streams_base_path + "DASH_HEVC_AAC_4K_Only/atfms_291_dash_tdk_hevc_aac_fmp4_4konly.mpd"
video_src_url_live_dash = ""

#MP4 Video URL
video_src_url_mp4      = test_streams_base_path + "TDK_Asset_Sunrise_MP4.mp4"
video_src_url_mp4_23fps  = test_streams_base_path + "TDK_Asset_Sunrise_23fps.mp4"
video_src_url_mp4_24fps  = test_streams_base_path + "TDK_Asset_Sunrise_24fps.mp4"
video_src_url_mp4_25fps  = test_streams_base_path + "TDK_Asset_Sunrise_25fps.mp4"
video_src_url_mp4_29fps  = test_streams_base_path + "TDK_Asset_Sunrise_29fps.mp4"
video_src_url_mp4_30fps  = test_streams_base_path + "TDK_Asset_Sunrise_30fps_v2.mp4"
video_src_url_mp4_50fps  = test_streams_base_path + "TDK_Asset_Sunrise_50fps.mp4"
video_src_url_mp4_59fps  = test_streams_base_path + "TDK_Asset_Sunrise_59fps.mp4"
video_src_url_mp4_60fps  = test_streams_base_path + "TDK_Asset_Sunrise_60fps.mp4"
video_src_url_mp4_hevc_hdr = test_streams_base_path + "TDK_Asset_Waterfall_HDR.MOV"

#HEVC Video URL
video_src_url_hevc_23fps  = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_23fps.mp4"
video_src_url_hevc_24fps  = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_24fps.mp4"
video_src_url_hevc_25fps  = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_25fps.mp4"
video_src_url_hevc_29fps  = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_29fps.mp4"
video_src_url_hevc_30fps  = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_30fps_v2.mp4"
video_src_url_hevc_50fps  = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_50fps.mp4"
video_src_url_hevc_59fps  = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_59fps.mp4"
video_src_url_hevc_60fps  = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_60fps.mp4"

#AV1 Video URL
video_src_url_av1_23fps  = test_streams_base_path + "TDK_Asset_Sunrise_AV1_23fps.mp4"
video_src_url_av1_24fps  = test_streams_base_path + "TDK_Asset_Sunrise_AV1_24fps.mp4"
video_src_url_av1_25fps  = test_streams_base_path + "TDK_Asset_Sunrise_AV1_25fps.mp4"
video_src_url_av1_29fps  = test_streams_base_path + "TDK_Asset_Sunrise_AV1_29fps.mp4"
video_src_url_av1_30fps  = test_streams_base_path + "TDK_Asset_Sunrise_AV1_30fps.mp4"
video_src_url_av1_50fps  = test_streams_base_path + "TDK_Asset_Sunrise_AV1_50fps.mp4"
video_src_url_av1_59fps  = test_streams_base_path + "TDK_Asset_Sunrise_AV1_59fps.mp4"
video_src_url_av1_60fps  = test_streams_base_path + "TDK_Asset_Sunrise_AV1_60fps.mp4"

#VP9 Video URL
video_src_url_vp9_23fps  = test_streams_base_path + "TDK_Asset_Sunrise_VP9_23fps.webm"
video_src_url_vp9_24fps  = test_streams_base_path + "TDK_Asset_Sunrise_VP9_24fps.webm"
video_src_url_vp9_25fps  = test_streams_base_path + "TDK_Asset_Sunrise_VP9_25fps.webm"
video_src_url_vp9_29fps  = test_streams_base_path + "TDK_Asset_Sunrise_VP9_29fps.webm"
video_src_url_vp9_30fps  = test_streams_base_path + "TDK_Asset_Sunrise_VP9_30fps.webm"
video_src_url_vp9_50fps  = test_streams_base_path + "TDK_Asset_Sunrise_VP9_50fps.webm"
video_src_url_vp9_59fps  = test_streams_base_path + "TDK_Asset_Sunrise_VP9_59fps.webm"
video_src_url_vp9_60fps  = test_streams_base_path + "TDK_Asset_Sunrise_VP9_60fps.webm"

#MKV Video URL
video_src_url_4k_mkv = test_streams_base_path + "TDK_Asset_Sunrise_2160p.mkv"

#Stream to simulate underflow
video_src_url_underflow_stream = test_streams_base_path + "TDK_Asset_Sunrise_underflow_stream_v2.mp4"

#Stream with known number of frames for frame Drop test
video_src_url_mp4_frameDrop_h264 = test_streams_base_path + "TDK_Asset_Sunrise_30fps_30secs.mp4"
video_src_url_mp4_frameDrop_hevc = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_30fps_30sec_v2.mp4"
video_src_url_mp4_frameDrop_vp9 = test_streams_base_path + "TDK_Asset_Sunrise_VP9_30fps_30sec.webm"
video_src_url_mp4_frameDrop_av1 = test_streams_base_path + "TDK_Asset_Sunrise_AV1_30fps_30sec.mp4"

#Audio underflow stream
video_src_url_audio_underflow = test_streams_base_path + "TDK_Asset_Audio_underflow_v2.mp4"

#Streams with different resolutions
video_src_url_mp4_2160p = test_streams_base_path + "TDK_Asset_Sunrise_2160p.mp4"
video_src_url_mp4_1080p = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_1080p.mp4"
video_src_url_mp4_720p = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_720p.mp4"
video_src_url_mp4_480p = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_480p.mp4"
video_src_url_mp4_360p = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_360p.mp4"
video_src_url_mp4_2160p_av1 = test_streams_base_path + "TDK_Asset_Waterfall_4K_AV1.mp4"
video_src_url_mp4_1080p_av1 = test_streams_base_path + "Waterfall_DASH_AV1_AAC/1080p.mp4"
video_src_url_mp4_720p_av1 = test_streams_base_path + "TDK_Asset_Waterfall_720p_AV1.mp4"
video_src_url_mp4_720p_vp9 = test_streams_base_path + "DASH_VP9_OPUS_WebM/720.webm"
video_src_url_resolution_up_h264 = test_streams_base_path + "TDK_Asset_Sunrise_H264_resolution_up.mp4"
video_src_url_resolution_down_h264 = test_streams_base_path + "TDK_Asset_Sunrise_H264_resolution_down.mp4"
video_src_url_resolution_up_av1 = test_streams_base_path + "TDK_Asset_Sunrise_AV1_resolution_up.mp4"
video_src_url_resolution_down_av1 = test_streams_base_path + "TDK_Asset_Sunrise_AV1_resolution_down.mp4"
video_src_url_resolution_up_hevc = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_resolution_up.mp4"
video_src_url_resolution_down_hevc = test_streams_base_path + "TDK_Asset_Sunrise_HEVC_resolution_down.mp4"
video_src_url_resolution_up_vp9 = test_streams_base_path + "TDK_Asset_Sunrise_VP9_resolution_up.mp4"
video_src_url_resolution_down_vp9 = test_streams_base_path + "TDK_Asset_Sunrise_VP9_resolution_down.mp4"

#H.264 Codec Video URL
video_src_url_dash_h264 = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"
video_src_url_hls_h264  = test_streams_base_path + "HLS_H264_AAC/master.m3u8"

#H.264 codec video URL with iframe track. Used by UVE AAMP trickplay tests
video_src_url_dash_h264_iframe = ""
video_src_url_hls_h264_iframe  = ""

#HEVC Codec Video URL
video_src_url_hevc = test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"

#H.263 Codec Video URL
video_src_url_h263 = test_streams_base_path + "TDK_Asset_Sunrise_H263_AAC.mov"

#AAC Codec Video URL
video_src_url_aac = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"

#Sampling rate URL
video_src_url_96khz_aac = test_streams_base_path + "TDK_Asset_Sunrise_AAC_96kHz.mp4"
video_src_url_96khz_opus = test_streams_base_path + "TDK_Asset_Sunrise_OPUS_96kHz.mp4"
video_src_url_44khz_aac =  test_streams_base_path + "TDK_Asset_Sunrise_AAC_44kHz.mp4"
video_src_url_48khz_aac  = test_streams_base_path + "TDK_Asset_Sunrise_30fps.mp4"

#Video bitrate URL
video_src_url_bitrate_h264 = ""
video_src_url_bitrate_hevc = ""

#24Fps H264 URL
video_src_url_dash_h264_24fps = test_streams_base_path + "DASH_H264_24fps/master.mpd"

#25Fps H264 URL
video_src_url_dash_h264_25fps = test_streams_base_path + "DASH_H264_25fps/master.mpd"

#60Fps H264 URL
video_src_url_dash_h264_60fps = test_streams_base_path + "DASH_H264_60fps/atfms_291_dash_tdk_avc_aac_fmp4.mpd"

#29Fps H264 URL
video_src_url_dash_h264_29fps = test_streams_base_path + "DASH_H264_29fps/master.mpd"

#Only Audio file
video_src_url_only_audio_aac = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4"

#VP9 Codec Video URL
# By default VP9_OPUS stream is used, if we need to test with VP9_OGG stream
# then comment VP9_OPUS stream and uncomment VP9_OGG stream urls below
video_src_url_vp9 = test_streams_base_path + "DASH_VP9_OPUS_WebM/master.mpd"
#video_src_url_vp9 = test_streams_base_path + "DASH_VP9_OGG_WebM/master.mpd"

#VP8 Codec Video URL
video_src_url_vp8 = test_streams_base_path + "TDK_Asset_Sunrise_VP8_Opus.webm"

#Opus Codec Video URL
video_src_url_opus = test_streams_base_path + "DASH_VP9_OPUS_WebM/master.mpd"
video_src_url_opus_mp4 = test_streams_base_path + "TDK_Asset_Sunrise_Opus_v2.mp4"

#Audio-Only URL. Stream should be of minimum 2-3 minutes
video_src_url_audio = test_streams_base_path  + "DASH_AAC_Audio_Only/master.mpd"

#MPEG-TS Video URL
video_src_url_mpegts = test_streams_base_path + "HLS_H264_AAC/master.m3u8"

#MPEG 1/2 Video URL
video_src_url_mpeg = test_streams_base_path + "TDK_Asset_Sunrise_MPEGAV.mpeg"

#AV1 Codec Video URL
#video_src_url_av1 = test_streams_base_path + "DASH_AV1_AAC/master.mpd"
#video_src_url_av1 = test_streams_base_path + "Waterfall_DASH_AV1_AAC/master.mpd"
video_src_url_av1 = test_streams_base_path + "TDK_Asset_DASH_AV1_AAC/master.mpd"

#AC3 Codec Video URL
video_src_url_ac3 = test_streams_base_path + "DASH_H264_AC3/atfms_291_dash_tdk_avc_ac3_fmp4.mpd"

#EC3 Codec Video URL
video_src_url_ec3 = test_streams_base_path + "DASH_H264_EC3/atfms_291_dash_tdk_avc_eac3_fmp4.mpd"

#OGG Video URL
video_src_url_ogg = test_streams_base_path + "DASH_VP9_OGG_WebM/master.mpd"

#Dolby Video URL
video_src_url_dolby = test_streams_base_path + "DASH_H264_EC3/atfms_291_dash_tdk_avc_eac3_fmp4.mpd"

#Type of the different codecs video stream. If the url is dash(.mpd), then type is dash. If its a
#hls stream(.m3u8),then type is hls. If the extension is .mp4,.ogg etc mention as mp4,ogg etc.
h263_url_type = "mov"
aac_url_type  = "dash"
vp9_url_type  = "dash"
vp8_url_type  = "webm"
opus_url_type = "dash"
audio_url_type  = "dash"
mpegts_url_type = "hls"
mpeg_url_type = "mpeg"
av1_url_type  = "dash"
ac3_url_type  = "dash"
ec3_url_type  = "dash"
hevc_url_type = "dash"
ogg_url_type  = "dash"
dolby_url_type = "dash"
av1_url_type_fps = "mp4"
mkv_4k_url_type ="mkv"
vp9_4k_url_type  = "webm"
vp9_url_type_fps = "webm"

# direct ogg & webm container streams without ABR (not hls/dash)
video_src_url_direct_ogg  = test_streams_base_path + "TDK_Asset_Sunrise_OGG.webm"
video_src_url_direct_webm = test_streams_base_path + "TDK_Asset_Sunrise_VP9_Opus.webm"

# Different MPD Variant streams
video_src_url_dash_segement_base = ""
video_src_url_dash_segement_list = ""
video_src_url_dash_segement_timeline = ""
video_src_url_dash_segement_template = ""

# Streams with multiple audio languages & subtitle text tracks
video_src_url_multi_audio_tracks = ""
video_src_url_multi_text_tracks  = ""
video_src_url_multi_thumbnail_tracks = ""
video_src_dash_url_multi_text_tracks = ""

# Streams with multiple audio codecs
#Video URL with AC3 and AAC codec audio
video_src_url_ac3_aac   = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_AC3_AAC_v2.mp4"
#Video URL with OPUS and AC3 codec audio
video_src_url_opus_ac3  = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_OPUS_AC3_v2.mp4"
#Video URL with OPUS and EAC3 codec audio
video_src_url_opus_eac3 = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_OPUS_EAC3_v2.mp4"
#Video URL with EAC3 and AC3 codec audio
video_src_url_ac3_eac3  = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_AC3_EAC3_v2.mp4"
video_src_url_aac_eac3  = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_AAC_EAC3_v2.mp4"
video_src_url_opus_aac = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_AAC_OPUS.mp4"
video_src_url_opus_vorbis = test_streams_base_path + "MultiCodecStreams/TDK_Asset_Sunrise_Vorbis_Opus.webm"
video_src_url_ddp51_heaac = ""

#Streams with mutiple tracks
video_src_url_multi_audio_aac = test_streams_base_path + "TDK_Asset_Sunrise_MultiTrack_AAC.mp4"
video_src_url_multi_audio_eac3 = test_streams_base_path + "TDK_Asset_Sunrise_MultiTrack_EAC3.mp4"

# MP4 audio streams
audio_src_url_mp4_aac = test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4"
audio_src_url_mp4_eac3 = test_streams_base_path + "DASH_H264_EC3/atfms_291_dash_tdk_avc_eac3_fmp4_ac3.mp4"
audio_src_url_webm_opus = test_streams_base_path + "DASH_VP9_OPUS_WebM/audio.webm"

# Only Audio short duration streams
audio_src_url_short_duration_aac = test_streams_base_path + "DASH_H264_AAC_15Sec/audio.mp4"
audio_src_url_short_duration_ac3 = test_streams_base_path + "TDK_Asset_AC3_Audio_only_15sec.mp4"
audio_src_url_short_duration_eac3 = test_streams_base_path + "TDK_Asset_EAC3_Audio_only_15sec.mp4"
audio_src_url_short_duration_webm_opus = test_streams_base_path + "TDK_Asset_OPUS_Audio_only_15sec.webm"
audio_src_url_short_duration_wav = test_streams_base_path + "TDK_Asset_Sunrise_WAV_15sec.wav"


# Basic WAV PCM Audio format stream
audio_src_url_wav_pcm = test_streams_base_path + "TDK_Asset_Sunrise_WAV_Audio.wav"

# M4A Audio format stream
audio_src_url_m4a = test_streams_base_path + "TDK_Asset_Sunrise_M4A.m4a"

# MP3 Audio format stream
audio_src_url_mp3 = test_streams_base_path + "TDK_Asset_Sunrise_MP3.mp3"

# DTS Audio format stream
audio_src_url_dts = test_streams_base_path + "TDK_Asset_Sunrise_DTS.dts"

# Invalid stream URL for testing error scenarios
video_src_url_invalid = test_streams_base_path + "test_stream_invalid.mpd"

#4K VP9 Video URL
video_src_url_4k_vp9 = test_streams_base_path + "TDK_Asset_Sunrise_VP9_2160p.webm"

#4K VP9 Video URL
video_src_url_short_duration_4k_vp9  = test_streams_base_path + "TDK_Asset_Sunrise_VP9_2160p_30Sec.webm"



#************************************************************************
#                  DRM PROTECTED CONTENT STREAM URLs
#************************************************************************

# Example:
# video_src_url_playready_dash = "http://playready_dash_url.mpd"
# video_src_url_playready_dash_drmconfigs = "com.microsoft.playready[http://license_url]|com.widevine.alpha[http://license_url]|headers[X-AxDRM-Message:header_info]"
# Note: Each drm config must be seperated by "|" and the values must be enclosed within "[" "]" as above.

# PlayReady DRM URLs
video_src_url_playready_dash_aac = ""
video_src_url_playready_dash_aac_drmconfigs = ""

video_src_url_playready_dash_h264 = ""
video_src_url_playready_dash_h264_drmconfigs = ""

video_src_url_playready_dash_ac3 = ""
video_src_url_playready_dash_ac3_drmconfigs = ""

video_src_url_playready_dash_ec3 = ""
video_src_url_playready_dash_ec3_drmconfigs = ""

video_src_url_playready_dash_hevc = ""
video_src_url_playready_dash_hevc_drmconfigs = ""

video_src_url_playready_hls_aac = ""
video_src_url_playready_hls_aac_drmconfigs = ""

video_src_url_playready_hls_h264 = ""
video_src_url_playready_hls_h264_drmconfigs = ""

video_src_url_playready_hls_hevc = ""
video_src_url_playready_hls_hevc_drmconfigs = ""

# Widevine DRM URLs
video_src_url_widevine_dash_aac = ""
video_src_url_widevine_dash_aac_drmconfigs = ""

video_src_url_widevine_dash_h264 = ""
video_src_url_widevine_dash_h264_drmconfigs = ""

video_src_url_widevine_dash_ac3 = ""
video_src_url_widevine_dash_ac3_drmconfigs =""

video_src_url_widevine_dash_ec3 = ""
video_src_url_widevine_dash_ec3_drmconfigs =""

video_src_url_widevine_dash_hevc = ""
video_src_url_widevine_dash_hevc_drmconfigs =""

video_src_url_widevine_dash_vp9 = ""
video_src_url_widevine_dash_vp9_drmconfigs = ""

video_src_url_widevine_hls_aac = ""
video_src_url_widevine_hls_aac_drmconfigs = ""

video_src_url_widevine_hls_h264 = ""
video_src_url_widevine_hls_h264_drmconfigs = ""

video_src_url_widevine_hls_hevc = ""
video_src_url_widevine_hls_hevc_drmconfigs = ""

video_src_url_widevine_dash_av1 = ""
video_src_url_widevine_dash_av1_drmconfigs = ""

video_src_url_widevine_dash_opus = ""
video_src_url_widevine_dash_opus_drmconfigs = ""

video_src_url_widevine_dash_vp8 = ""
video_src_url_widevine_dash_vp8_drmconfigs = ""

#Multi-DRM Test streams
video_src_url_multi_drm_dash = ""
video_src_url_multi_drm_dash_pref_playready_drmconfigs = ""
video_src_url_multi_drm_dash_pref_widevine_drmconfigs  = ""

# DRM cbcs stream
video_src_url_playready_cbcs_dash = ""
video_src_url_playready_cbcs_dash_drmconfigs = ""

video_src_url_playready_cbcs_hls = ""
video_src_url_playready_cbcs_hls_drmconfigs = ""

video_src_url_widevine_cbcs_dash = ""
video_src_url_widevine_cbcs_dash_drmconfigs = ""

video_src_url_widevine_cbcs_hls = ""
video_src_url_widevine_cbcs_hls_drmconfigs = ""

# Multikey streams
video_src_url_widevine_multikey_dash = ""
video_src_url_widevine_multikey_dash_drmconfigs = ""

video_src_url_playready_multikey_dash = ""
video_src_url_playready_multikey_dash_drmconfigs = ""

video_src_url_widevine_multikey_hls = ""
video_src_url_widevine_multikey_hls_drmconfigs = ""

video_src_url_playready_multikey_hls = ""
video_src_url_playready_multikey_hls_drmconfigs = ""

#************************************************************************
#                GENERAL CONFIGURATIONS FOR VIDEO TESTS
#************************************************************************

# Time duration for operations
# Provided time (seconds) is the duration after how much second the operation should take place
# The time interval for any operation should be set with the consideration of time taken to ssh
# and get proc details. Eg. If fetching proc details takes 5 seconds then interval should be
# greater than time taken say 10

# This interval indicates after how much seconds video should be paused in playpause test
pause_interval = 30
# This interval indicates after how much seconds video should start playing in playpause test
play_interval = 10

# This interval indicates after how much seconds video should be paused in playpause stress test
pause_interval_stress = 10
# This interval indicates after how much seconds video should start playing in playpause stress test
play_interval_stress  = 10
# This count indicates after how many times the oprations should repeat in stress tests
repeat_count_stress = 10

# This interval indicates after how much seconds any video operations should take place
operation_max_interval = 10
# This interval indicates max duration for FF operations
fastfwd_max_interval = 60

# Default jump interval for seek forward or backward operations
seekfwd_interval = 10
seekbwd_interval = 20
seekfwd_check_interval = 5
seekbwd_check_interval = 7
# Default check interval for fast forward operations
fastfwd_check_interval = 5
# Default Seek/Jump position value and check interval.
seekfwd_position = 120
seekbwd_position = 80
seekpos_check_interval = 10

# Provided time (seconds) is the duration after how much second, the player should be closed (30 sec to 3mins)
close_interval = 30
audio_close_interval = 30



#************************************************************************
#            GENERAL CONFIGURATIONS FOR ANIMATION TESTS
#************************************************************************

# Min Time duration for the animation operation used by multianimations app (10 to 60 sec)
animation_duration = 60
# No of objects to be animated by objects(rectangles/texts) animation app
objects_count = 500

# Already Existing Sample Animation App URL
sample_animation_test_url = ""
# XPath of the html tag element to expand in web-inspect page.User has to manually identify
# the xpath by loading the test url in browser and checking the xpath in inspect page
element_expand_xpath = ""
# XPath of the display fps element from where actual data to be read from UI
ui_data_xpath = ""


#************************************************************************
#            CONFIGURATIONS FOR MSE/EME TESTS
#************************************************************************
#User shall update the URL as per the version required
mse_conformance_test_app_url = "https://ytlr-cert.appspot.com/2021/main.html?command=run&test_type=conformance-test"
eme_conformance_test_app_url = "https://ytlr-cert.appspot.com/2021/main.html?command=run&test_type=encryptedmedia-test"


#************************************************************************
# ALL CODEC STREAMS PLAYBACK WITH DIFFERENT PLAYERS
#************************************************************************
# Below are the default players for the AV codecs.
# User shall add different players using which test of particular codec should run.
# Eg. codec_dash_h264 = "dashjs,shaka" . Now all the dash_h264 related test scripts
# performs the operations using two players dashjs and shaka player
codec_dash_h264 = "dashjs"
codec_hls_h264  = "hlsjs"
codec_dash_hevc = "dashjs"
codec_hls_hevc  = "hlsjs"
codec_dash_aac  = "dashjs"
codec_hls_aac   = "hlsjs"
codec_mpeg_ts   = "hlsjs"
codec_ac3       = "dashjs"
codec_ec3       = "dashjs"
codec_vp9       = "dashjs"
codec_opus      = "dashjs"
codec_av1       = "dashjs"
codec_h263      = "sdk"
codec_vp8       = "sdk"
codec_mp4       = "sdk"
codec_ogg       = "sdk"
codec_webm      = "sdk"
codec_mpeg      = "sdk"
codec_audio_aac = "dashjs"
codec_audio_mp3 = "sdk"
codec_audio_dts = "sdk"
codec_audio_m4a = "sdk"
codec_audio_wav_pcm = "sdk"
codec_mkv       = "sdk"
codec_4k_av1    =  "sdk"


#*********************************************************************
# DIFFERENT HLS/DASH CORRUPT VIDEO URLs
#*********************************************************************

#HLS Video URL
video_src_url_corrupt_I_complete_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_Frame/DASH_HLS_Corrupt_I_Frame_Complete_Segment/HLS_Corrupt_I_Frame_Complete_Segment.m3u8"
video_src_url_corrupt_I_initial_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_Frame/DASH_HLS_Corrupt_I_Frame_Initial_Segment/HLS_Corrupt_I_Frame_Initial_Segment.m3u8"
video_src_url_corrupt_I_middle_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_Frame/DASH_HLS_Corrupt_I_Frame_Middle_Segment/HLS_Corrupt_I_Frame_Middle_Segment.m3u8"
video_src_url_corrupt_I_end_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_Frame/DASH_HLS_Corrupt_I_Frame_End_Segment/HLS_Corrupt_I_Frame_End_Segment.m3u8"
video_src_url_corrupt_P_complete_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_Frame/DASH_HLS_Corrupt_P_Frame_Complete_Segment/HLS_Corrupt_P_Frame_Complete_Segment.m3u8"
video_src_url_corrupt_P_initial_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_Frame/DASH_HLS_Corrupt_P_Frame_Initial_segment/HLS_Corrupt_P_Frame_Initial_segment.m3u8"
video_src_url_corrupt_P_middle_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_Frame/DASH_HLS_Corrupt_P_Frame_Middle_Segment/HLS_Corrupt_P_Frame_Middle_Segment.m3u8"
video_src_url_corrupt_P_end_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_Frame/DASH_HLS_Corrupt_P_Frame_End_Segment/HLS_Corrupt_P_Frame_End_Segment.m3u8"
video_src_url_corrupt_B_complete_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_B_Frame/DASH_HLS_Corrupt_B_Frame_Complete_Segment/HLS_Corrupt_B_Frame_Complete_Segment.m3u8"
video_src_url_corrupt_B_initial_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_B_Frame/DASH_HLS_Corrupt_B_Frame_Initial_Segment/HLS_Corrupt_B_Frame_Initial_Segment.m3u8"
video_src_url_corrupt_B_middle_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_B_Frame/DASH_HLS_Corrupt_B_Frame_Middle_Segment/HLS_Corrupt_B_Frame_Middle_Segment.m3u8"
video_src_url_corrupt_B_end_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_B_Frame/DASH_HLS_Corrupt_B_Frame_End_Segment/HLS_Corrupt_B_Frame_End_Segment.m3u8"
video_src_url_corrupt_I_B_complete_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_B_Frame/DASH_HLS_Corrupt_I_B_Frame_Complete_Segment/HLS_Corrupt_I_B_Frame_Complete_Segment.m3u8"
video_src_url_corrupt_I_B_initial_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_B_Frame/DASH_HLS_Corrupt_I_B_Frame_Initial_Segment/HLS_Corrupt_I_B_Frame_Initial_Segment.m3u8"
video_src_url_corrupt_I_B_middle_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_B_Frame/DASH_HLS_Corrupt_I_B_Frame_Middle_Segment/HLS_Corrupt_I_B_Frame_Middle_Segment.m3u8"
video_src_url_corrupt_I_B_end_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_B_Frame/DASH_HLS_Corrupt_I_B_Frame_End_Segment/HLS_Corrupt_I_B_Frame_End_Segment.m3u8"
video_src_url_corrupt_I_P_complete_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_Frame/DASH_HLS_Corrupt_I_P_Frame_Complete_Segment/HLS_Corrupt_I_P_Frame_Complete_Segment.m3u8"
video_src_url_corrupt_I_P_initial_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_Frame/DASH_HLS_Corrupt_I_P_Frame_Initial_Segment/HLS_Corrupt_I_P_Frame_Initial_Segment.m3u8"
video_src_url_corrupt_I_P_middle_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_Frame/DASH_HLS_Corrupt_I_P_Frame_Middle_Segment/HLS_Corrupt_I_P_Frame_Middle_Segment.m3u8"
video_src_url_corrupt_I_P_end_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_Frame/DASH_HLS_Corrupt_I_P_Frame_End_Segment/HLS_Corrupt_I_P_Frame_End_Segment.m3u8"
video_src_url_corrupt_P_B_complete_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_B_Frame/DASH_HLS_Corrupt_P_B_Frame_Complete_Segment/HLS_Corrupt_P_B_Frame_Complete_Segment.m3u8"
video_src_url_corrupt_P_B_initial_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_B_Frame/DASH_HLS_Corrupt_P_B_Frame_Initial_Segment/HLS_Corrupt_P_B_Frame_Initial_Segment.m3u8"
video_src_url_corrupt_P_B_middle_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_B_Frame/DASH_HLS_Corrupt_P_B_Frame_Middle_Segment/HLS_Corrupt_P_B_Middle_Segment.m3u8"
video_src_url_corrupt_P_B_end_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_B_Frame/DASH_HLS_Corrupt_P_B_Frame_End_Segment/HLS_Corrupt_P_B_End_Segment.m3u8"
video_src_url_corrupt_I_P_B_complete_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_B_Frame/DASH_HLS_Corrupt_I_P_B_Frame_Complete_Segment/HLS_Corrupt_I_P_B_Frame_Complete_Segment.m3u8"
video_src_url_corrupt_I_P_B_initial_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_B_Frame/DASH_HLS_Corrupt_I_P_B_Frame_Initial_Segment/HLS_Corrupt_I_P_B_Frame_Initial_Segment.m3u8"
video_src_url_corrupt_I_P_B_middle_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_B_Frame/DASH_HLS_Corrupt_I_P_B_Frame_Middle_Segment/HLS_Corrupt_I_P_B_Frame_Middle_Segment.m3u8"
video_src_url_corrupt_I_P_B_end_hls = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_B_Frame/DASH_HLS_Corrupt_I_P_B_Frame_End_Segment/HLS_Corrupt_I_P_B_Frame_End_Segment.m3u8"


#DASH Video URL
video_src_url_corrupt_I_complete_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_Frame/DASH_HLS_Corrupt_I_Frame_Complete_Segment/DASH_Corrupt_I_Frame_Complete_Segment.mpd"
video_src_url_corrupt_I_initial_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_Frame/DASH_HLS_Corrupt_I_Frame_Initial_Segment/DASH_Corrupt_I_Frame_Initial_Segment.mpd"
video_src_url_corrupt_I_middle_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_Frame/DASH_HLS_Corrupt_I_Frame_Middle_Segment/DASH_Corrupt_I_Frame_Middle_Segment.mpd"
video_src_url_corrupt_I_end_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_Frame/DASH_HLS_Corrupt_I_Frame_End_Segment/DASH_Corrupt_I_Frame_End_Segment.mpd"
video_src_url_corrupt_P_complete_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_Frame/DASH_HLS_Corrupt_P_Frame_Complete_Segment/DASH_Corrupt_P_Frame_Complete_Segment.mpd"
video_src_url_corrupt_P_initial_dash = test_corrupted_streams_base_path +  "DASH_HLS_Corrupt_P_Frame/DASH_HLS_Corrupt_P_Frame_Initial_segment/DASH_Corrupt_P_Frame_Initial_segment.mpd"
video_src_url_corrupt_P_middle_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_Frame/DASH_HLS_Corrupt_P_Frame_Middle_Segment/DASH_Corrupt_P_Frame_Middle_Segment.mpd"
video_src_url_corrupt_P_end_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_Frame/DASH_HLS_Corrupt_P_Frame_End_Segment/DASH_Corrupt_P_Frame_End_Segment.mpd"
video_src_url_corrupt_B_complete_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_B_Frame/DASH_HLS_Corrupt_B_Frame_Complete_Segment/DASH_Corrupt_B_Frame_Complete_Segment.mpd"
video_src_url_corrupt_B_initial_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_B_Frame/DASH_HLS_Corrupt_B_Frame_Initial_Segment/DASH_Corrupt_B_Frame_Initial_Segment.mpd"
video_src_url_corrupt_B_middle_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_B_Frame/DASH_HLS_Corrupt_B_Frame_Middle_Segment/DASH_Corrupt_B_Frame_Middle_Segment.mpd"
video_src_url_corrupt_B_end_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_B_Frame/DASH_HLS_Corrupt_B_Frame_End_Segment/DASH_Corrupt_B_Frame_End_Segment.mpd"
video_src_url_corrupt_I_B_complete_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_B_Frame/DASH_HLS_Corrupt_I_B_Frame_Complete_Segment/DASH_Corrupt_I_B_Frame_Complete_Segment.mpd"
video_src_url_corrupt_I_B_initial_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_B_Frame/DASH_HLS_Corrupt_I_B_Frame_Initial_Segment/DASH_Corrupt_I_B_Frame_Initial_Segment.mpd"
video_src_url_corrupt_I_B_middle_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_B_Frame/DASH_HLS_Corrupt_I_B_Frame_Middle_Segment/DASH_Corrupt_I_B_Frame_Middle_Segment.mpd"
video_src_url_corrupt_I_B_end_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_B_Frame/DASH_HLS_Corrupt_I_B_Frame_End_Segment/DASH_Corrupt_I_B_Frame_End_Segment.mpd"
video_src_url_corrupt_I_P_complete_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_Frame/DASH_HLS_Corrupt_I_P_Frame_Complete_Segment/DASH_Corrupt_I_P_Frame_Complete_Segment.mpd"
video_src_url_corrupt_I_P_initial_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_Frame/DASH_HLS_Corrupt_I_P_Frame_Initial_Segment/DASH_Corrupt_I_P_Frame_Initial_Segment.mpd"
video_src_url_corrupt_I_P_middle_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_Frame/DASH_HLS_Corrupt_I_P_Frame_Middle_Segment/DASH_Corrupt_I_P_Frame_Middle_Segment.mpd"
video_src_url_corrupt_I_P_end_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_Frame/DASH_HLS_Corrupt_I_P_Frame_End_Segment/DASH_Corrupt_I_P_Frame_End_Segment.mpd"
video_src_url_corrupt_P_B_complete_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_B_Frame/DASH_HLS_Corrupt_P_B_Frame_Complete_Segment/DASH_Corrupt_P_B_Frame_Complete_Segment.mpd"
video_src_url_corrupt_P_B_initial_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_B_Frame/DASH_HLS_Corrupt_P_B_Frame_Initial_Segment/DASH_Corrupt_P_B_Frame_Initial_Segment.mpd"
video_src_url_corrupt_P_B_middle_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_B_Frame/DASH_HLS_Corrupt_P_B_Frame_Middle_Segment/DASH_Corrupt_P_B_Middle_Segment.mpd"
video_src_url_corrupt_P_B_end_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_P_B_Frame/DASH_HLS_Corrupt_P_B_Frame_End_Segment/DASH_Corrupt_P_B_End_Segment.mpd"
video_src_url_corrupt_I_P_B_complete_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_B_Frame/DASH_HLS_Corrupt_I_P_B_Frame_Complete_Segment/DASH_Corrupt_I_P_B_Frame_Complete_Segment.mpd"
video_src_url_corrupt_I_P_B_initial_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_B_Frame/DASH_HLS_Corrupt_I_P_B_Frame_Initial_Segment/DASH_Corrupt_I_P_B_Frame_Initial_Segment.mpd"
video_src_url_corrupt_I_P_B_middle_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_B_Frame/DASH_HLS_Corrupt_I_P_B_Frame_Middle_Segment/DASH_Corrupt_I_P_B_Frame_Middle_Segment.mpd"
video_src_url_corrupt_I_P_B_end_dash = test_corrupted_streams_base_path + "DASH_HLS_Corrupt_I_P_B_Frame/DASH_HLS_Corrupt_I_P_B_Frame_End_Segment/DASH_Corrupt_I_P_B_Frame_End_Segment.mpd"



#****************************************************************
#       Negative Video Streaming Of SDK Player
#****************************************************************


video_src_url_corrupt_I_complete_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_Frame/Corrupt_I_Frame_Complete_Segment/Corrupt_I_Frame_Complete_Segment.mp4"
video_src_url_corrupt_I_initial_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_Frame/Corrupt_I_Frame_Initial_Segment/Corrupt_I_Frame_Initial_Segment.mp4"
video_src_url_corrupt_I_middle_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_Frame/Corrupt_I_Frame_Middle_Segment/Corrupt_I_Frame_Middle_Segment.mp4"
video_src_url_corrupt_I_end_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_Frame/Corrupt_I_Frame_End_Segment/Corrupt_I_Frame_End_Segment.mp4"
video_src_url_corrupt_P_complete_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_P_Frame/Corrupt_P_Frame_Complete_Segment/Corrupt_P_Frame_Complete_Segment.mp4"
video_src_url_corrupt_P_initial_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_P_Frame/Corrupt_P_Frame_Initial_Segment/Corrupt_P_Frame_Initial_Segment.mp4"
video_src_url_corrupt_P_middle_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_P_Frame/Corrupt_P_Frame_Middle_Segment/Corrupt_P_Frame_Middle_Segment.mp4"
video_src_url_corrupt_P_end_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_P_Frame/Corrupt_P_Frame_End_Segment/Corrupt_P_Frame_End_Segment.mp4"
video_src_url_corrupt_B_complete_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_B_Frame/Corrupt_B_Frame_Complete_Segment/Corrupt_B_Frame_Complete_Segment.mp4"
video_src_url_corrupt_B_initial_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_B_Frame/Corrupt_B_Frame_Initial_Segment/Corrupt_B_Frame_Initial_Segment.mp4"
video_src_url_corrupt_B_middle_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_B_Frame/Corrupt_B_Frame_Middle_Segment/Corrupt_B_Frame_Middle_Segment.mp4"
video_src_url_corrupt_B_end_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_B_Frame/Corrupt_B_Frame_End_Segment/Corrupt_B_Frame_End_Segment.mp4"
video_src_url_corrupt_I_B_complete_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_B_Frame/Corrupt_I_B_Frame_Complete_Segment/Corrupt_I_B_Frame_Complete_Segment.mp4"
video_src_url_corrupt_I_B_initial_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_B_Frame/Corrupt_I_B_Frame_Initial_Segment/Corrupt_I_B_Frame_Initial.mp4"
video_src_url_corrupt_I_B_middle_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_B_Frame/Corrupt_I_B_Frame_Middle_Segment/Corrupt_I_B_Frame_Middle_Segment.mp4"
video_src_url_corrupt_I_B_end_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_B_Frame/Corrupt_I_B_Frame_End_Segment/Corrupt_I_B_Frame_End_Segment.mp4"
video_src_url_corrupt_I_P_complete_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_P_Frame/Corrupt_I_P_Frame_Complete_Segment/Corrupt_I_P_Frame_Complete_Segment.mp4"
video_src_url_corrupt_I_P_initial_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_P_Frame/Corrupt_I_P_Frame_Initial_Segment/Corrupt_I_P_Frame_Initial_Segment.mp4"
video_src_url_corrupt_I_P_middle_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_P_Frame/Corrupt_I_P_Frame_Middle_Segment/Corrupt_I_P_Frame_Middle_Segment.mp4"
video_src_url_corrupt_I_P_end_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_P_Frame/Corrupt_I_P_Frame_End_Segment/Corrupt_I_P_Frame_End_Segment.mp4"
video_src_url_corrupt_P_B_complete_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_P_B_Frame/Corrupt_P_B_Frame_Complete_Segment/Corrupt_P_B_Frame_Complete_Segment.mp4"
video_src_url_corrupt_P_B_initial_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_P_B_Frame/Corrupt_P_B_Frame_Initial_Segment/Corrupt_P_B_Frame_Initial_Segment.mp4"
video_src_url_corrupt_P_B_middle_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_P_B_Frame/Corrupt_P_B_Frame_Middle_Segment/Corrupt_P_B_Frame_Middle_Segment.mp4"
video_src_url_corrupt_P_B_end_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_P_B_Frame/Corrupt_P_B_Frame_End_Segment/Corrupt_P_B_Frame_End_Segment.mp4"
video_src_url_corrupt_I_P_B_complete_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_P_B_Frame/Corrupt_I_P_B_Frame_Complete_Segment/Corrupt_I_P_B_Frame_Complete_Segment.mp4"
video_src_url_corrupt_I_P_B_initial_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_P_B_Frame/Corrupt_I_P_B_Frame_Initial_Segment/Corrupt_I_P_B_Frame_Initial_Segment.mp4"
video_src_url_corrupt_I_P_B_middle_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_P_B_Frame/Corrupt_I_P_B_Frame_Middle_Segment/Corrupt_I_P_B_Frame_Middle_Segment.mp4"
video_src_url_corrupt_I_P_B_end_h264_eac3 = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_EAC3_MP4/Corrupt_I_P_B_Frame/Corrupt_I_P_B_Frame_End_Segment/Corrupt_I_P_B_Frame_End_Segment.mp4"


video_src_url_corrupt_I_complete_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_Frame/Corrupt_I_Frame_Complete_Segment/Corrupt_I_Frame_Complete_Segment.mp4"
video_src_url_corrupt_I_initial_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_Frame/Corrupt_I_Frame_Initial_Segment/Corrupt_I_Frame_Initial_Segment.mp4"
video_src_url_corrupt_I_middle_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_Frame/Corrupt_I_Frame_Middle_Segment/Corrupt_I_Frame_Middle_Segment.mp4"
video_src_url_corrupt_I_end_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_Frame/Corrupt_I_Frame_End_Segment/Corrupt_I_Frame_End_Segment.mp4"
video_src_url_corrupt_P_complete_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_P_Frame/Corrupt_P_Frame_Complete_Segment/Corrupt_P_Frame_Complete_Segment.mp4"
video_src_url_corrupt_P_initial_h264_aac = test_corrupted_streams_base_path +  "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_P_Frame/Corrupt_P_Frame_Initial_Segment/Corrupt_P_Frame_Initial_Segment.mp4"
video_src_url_corrupt_P_middle_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_P_Frame/Corrupt_P_Frame_Middle_Segment/Corrupt_P_Frame_Middle_Segment.mp4"
video_src_url_corrupt_P_end_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_P_Frame/Corrupt_P_Frame_End_Segment/Corrupt_P_Frame_End_Segment.mp4"
video_src_url_corrupt_B_complete_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_B_Frame/Corrupt_B_Frame_Complete_Segment/Corrupt_B_Frame_Complete_Segment.mp4"
video_src_url_corrupt_B_initial_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_B_Frame/Corrupt_B_Frame_Initial_Segment/Corrupt_B_Frame_Initial_Segment.mp4"
video_src_url_corrupt_B_middle_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_B_Frame/Corrupt_B_Frame_Middle_Segment/Corrupt_B_Frame_Middle_Segment.mp4"
video_src_url_corrupt_B_end_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_B_Frame/Corrupt_B_Frame_End_Segment/Corrupt_B_Frame_End_Segment.mp4"
video_src_url_corrupt_I_B_complete_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_B_Frame/Corrupt_I_B_Frame_Complete_Segment/Corrupt_I_B_Frame_Complete_Segment.mp4"
video_src_url_corrupt_I_B_initial_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_B_Frame/Corrupt_I_B_Frame_Initial_Segment/Corrupt_I_B_Frame_Initial_Segment.mp4"
video_src_url_corrupt_I_B_middle_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_B_Frame/Corrupt_I_B_Frame_Middle_Segment/Corrupt_I_B_Frame_Middle_Segment.mp4"
video_src_url_corrupt_I_B_end_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_B_Frame/Corrupt_I_B_Frame_End_Segment/Corrupt_I_B_Frame_End_Segment.mp4"
video_src_url_corrupt_I_P_complete_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_P_Frame/Corrupt_I_P_Frame_Complete_Segment/Corrupt_I_P_Frame_Complete_Segment.mp4"
video_src_url_corrupt_I_P_initial_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_P_Frame/Corrupt_I_P_Frame_Initial_Segment/Corrupt_I_P_Frame_Initial_Segment.mp4"
video_src_url_corrupt_I_P_middle_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_P_Frame/Corrupt_I_P_Frame_Middle_Segment/Corrupt_I_P_Frame_Complete_Middle.mp4"
video_src_url_corrupt_I_P_end_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_P_Frame/Corrupt_I_P_Frame_End_Segment/Corrupt_I_P_Frame_End_Segment.mp4"
video_src_url_corrupt_P_B_complete_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_P_B_Frame/Corrupt_P_B_Frame_Complete_Segment/Corrupt_P_B_Frame_Complete_Segment.mp4"
video_src_url_corrupt_P_B_initial_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_P_B_Frame/Corrupt_P_B_Frame_Initial_Segment/Corrupt_P_B_Frame_Initial_Segment.mp4"
video_src_url_corrupt_P_B_middle_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_P_B_Frame/Corrupt_P_B_Frame_Middle_Segment/Corrupt_P_B_Frame_Middle_Segment.mp4"
video_src_url_corrupt_P_B_end_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_P_B_Frame/Corrupt_P_B_Frame_End_Segment/Corrupt_P_B_Frame_End_Segment.mp4"
video_src_url_corrupt_I_P_B_complete_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_P_B_Frame/Corrupt_I_P_B_Frame_Complete_Segment/Corrupt_I_P_B_Frame_Complete_Segment.mp4"
video_src_url_corrupt_I_P_B_initial_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_P_B_Frame/Corrupt_I_P_B_Frame_Initial_Segment/Corrupt_I_P_B_Frame_Initial_Segment.mp4"
video_src_url_corrupt_I_P_B_middle_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_P_B_Frame/Corrupt_I_P_B_Frame_Middle_Segment/Corrupt_I_P_B_Frame_Middle_Segment.mp4"
video_src_url_corrupt_I_P_B_end_h264_aac = test_corrupted_streams_base_path + "TDK_Asset_Corrupt_Sunrise_H264_AAC_MP4/Corrupt_I_P_B_Frame/Corrupt_I_P_B_Frame_End_Segment/Corrupt_I_P_B_Frame_End_Segment.mp4"

