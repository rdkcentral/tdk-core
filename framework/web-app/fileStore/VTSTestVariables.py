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
#########################################################################

###########################################################################################################
#                                     Variable Definitions                                                #
###########################################################################################################
#                                                                                                         #
# TDKHAL - Example HAL for understanding the configuration parameters below.                              #
#                                                                                                         #
# TDK HAL Test Configurations                                                                             #
#                                                                                                         #
# TDK_basePath: Specifies the directory where the hal_test binary for TDK HAL is installed on the device. #
#               Note: Do not include the generic VTS binaries base path.                                  #
#               Example: If all VTS binaries are installed under /VTS_Package/,                           #
#                        and the TDK HAL test binary is located in /VTS_Package/tdkhal/,                  #
#                        then set TDK_basePath as "tdkhal/".                                              #
#                                                                                                         #
# TDK_binaryName: Defines the name of the hal_test binary for TDK HAL.                                    #
#                 Example: /VTS_Package/tdkhal/hal_test_tdk                                               #
#                                                                                                         #
# TDK_binaryConfig: Specifies the YAML profile file required for the test.                                #
#                                                                                                         #
# TDK_L1_List: Specifies a list of test cases to be executed.                                             #
#              Default: Empty, meaning all test cases will be executed.                                   #
#              Example: TDK_L1_List = ["Test1", "Test2"] -> Only Test1 and Test2 will run.                #
#                                                                                                         #
# TDK_L1_SkipTestCaseList: A dictionary specifying test cases to be skipped, with reasons.                #
#                           Default: Empty, meaning no test cases will be skipped.                        #
#                           Example:                                                                      #
#                           TDK_L1_SkipTestCaseList["Test3"] = "This test case reboots the device."       #
#                           TDK_L1_SkipTestCaseList["Test4"] = "This test case powers off the DUT."       #
###########################################################################################################

# VTS - all binaries base path
VTS_Binary_basePath = " /VTS_Package/"

# Device Settings HAL Test Configurations
DeviceSettings_basePath = "device_settings/"
DeviceSettings_binaryName = "hal_test_device_settings"

VideoDevice_binaryConfig = "Source_VideoDevice.yaml"
VideoDevice_L1_List = []

VideoDevice_L2_List = []

VideoPort_binaryConfig = "Source_4K_VideoPort.yaml"
VideoPort_L1_List = []
VideoPort_L2_List = []

Host_binaryConfig = "Source_HostSettings.yaml"
Host_L1_List = []
Host_L1_advanced_List = []
Host_L2_List = []

Audio_binaryConfig = "Source_AudioSettings.yaml"
Audio_L1_List = []
Audio_L2_List = []

Display_binaryConfig ="Source_4K_Display.yaml"
Display_L1_List = []
Display_L2_List = []

# RMF Audio Capture HAL test Configurations
rmfAudioCapture_basePath = "rmf_audio_capture/"
rmfAudioCapture_binaryName = "hal_test_rmf_audio_capture"
rmfAudioCapture_binaryConfig = "rmfAudioCaptureAuxNotSupported.yaml"
rmfAudioCapture_L1_List = []
rmfAudioCapture_L2_List = []

# HDMICEC HAL test configurations
HDMICEC_basePath = "hdmi_cec/"
HDMICEC_binaryName = "hal_test_hdmi_cec"
HDMICEC_binaryConfig = "source_hdmiCEC.yml"
HDMICEC_L1_List = []
HDMICEC_L2_List = []

# PowerManager HAL test configurations
PowerManager_basePath = "power_manager/"
PowerManager_binaryName = "hal_test_power_manager"
PowerManager_binaryConfig = "source_powerManager.yaml"
PowerManager_L1_List = []
PowerManager_L2_List = []
PowerManager_L1_SkipTestCaseList = {}
PowerManager_L1_SkipTestCaseList["PLAT_API_SetPowerState_L1_positiv"] ="Testcase includes setting DUT to power state OFF"
PowerManager_L1_SkipTestCaseList["PLAT_Reset_L1_positive"] = "Testcase reboots the device"
PowerManager_L1_SkipTestCaseList["PLAT_Reset_L1_negative"] = "Testcase reboots the device"
PowerManager_L2_SkipTestCaseList = {}
PowerManager_L2_SkipTestCaseList["L2_SetAndGetPowerState"] = "Testcase includes setting DUT to power state OFF"

# DeepSleep HAL test configurations
DeepSleep_basePath = "deepsleep_manager/"
DeepSleep_binaryName = "hal_test_deepsleep_manager"
DeepSleep_binaryConfig = "deepsleepmanagerExtendedEnumsNotSupported.yaml"
DeepSleep_L1_List = []
DeepSleep_L2_List = []
DeepSleep_L1_SkipTestCaseList = {}
DeepSleep_L2_SkipTestCaseList = {}
