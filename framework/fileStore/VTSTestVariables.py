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
DeviceSettings_binaryName = "hal_test_dshal"

VideoDevice_binaryConfig = "Source_VideoDevice.yaml"
VideoDevice_L1_List = []
VideoDevice_L1_SkipTestCaseList = {}
VideoDevice_L1_SkipTestCaseList_RPI = {}
VideoDevice_L1_SkipTestCaseList_RPI["dsSetDFC_positive"] = "RPI doesn't support dsSetDFC REFPLTV-2577"
VideoDevice_L1_SkipTestCaseList_RPI["dsGetSupportVidFormats_positive"] = "RPI doesn't support dsGetSupportedVideoCodingFormats REFPLTV-2536"
VideoDevice_L1_SkipTestCaseList_RPI["dsGetVideoCodecInfo_positive"] = "RPI doesn't support dsGetVideoCodecInfo REFPLTV-2536"
VideoDevice_L1_SkipTestCaseList_RPI["dsSetFRFMode_positive"] = "RPI doesn't support dsSetFRFMode REFPLTV-2562"
VideoDevice_L1_SkipTestCaseList_RPI["dsGetFRFMode_positive"] = "RPI doesn't support dsGetFRFMode REFPLTV-2562"
VideoDevice_L1_SkipTestCaseList_RPI["dsGetFRFMode_negative"] = "RPI doesn't support dsGetFRFMode REFPLTV-2562"
VideoDevice_L1_SkipTestCaseList_RPI["dsSetDFC_negative"] = "RPI doesn't support dsSetDFC REFPLTV-2577"
VideoDevice_L1_SkipTestCaseList_RPI["dsGetDFC_positive"] = "RPI doesn't support dsGetDFC REFPLTV-2577"
VideoDevice_L2_List = []
VideoDevice_L2_SkipTestCaseList = {}
VideoDevice_L2_SkipTestCaseList_RPI = {}
VideoDevice_L2_SkipTestCaseList_RPI["GetSupportedVideoCodingFormats"] = "RPI doesn't support dsGetSupportedVideoCodingFormats REFPLTV-2536"
VideoDevice_L2_SkipTestCaseList_RPI["SetAndGetDFC"] = "RPI doesn't support dsSetDFC REFPLTV-2577"
VideoDevice_L2_SkipTestCaseList_RPI["GetVideoCodecInfo"] = "RPI doesn't support dsGetVideoCodecInfo REFPLTV-2536"

VideoPort_binaryConfig = "Source_4K_VideoPort.yaml"
VideoPort_L1_List = []
VideoPort_L1_SkipTestCaseList = {}
VideoPort_L1_SkipTestCaseList_RPI = {}
VideoPort_L1_SkipTestCaseList_RPI["dsGetHDCPProtocol_pos"] = "RPI doesn't support dsGetHDCPProtocol REFPLTV-2542"
VideoPort_L1_SkipTestCaseList_RPI["GetHDCPReceiverProtocol_pos"] = "RPI doesn't support dsGetHDCPReceiverProtocol REFPLTV-2542"
VideoPort_L1_SkipTestCaseList_RPI["GetHDCPCurrentProtocol_pos"] = "RPI doesn't support dsGetHDCPCurrentProtocol REFPLTV-2542"
VideoPort_L1_SkipTestCaseList_RPI["dsGetTVHDRCapabilities_pos"] = "RPI doesn't support dsGetTVHDRCapabilities REFPLTV-2576"
VideoPort_L1_SkipTestCaseList_RPI["dsGetVideoEOTF_pos"] = "RPI doesn't support dsGetVideoEOTF"
VideoPort_L1_SkipTestCaseList_RPI["dsGetMatrixCoefficients_pos"] =  "RPI doesn't support dsGetMatrixCoefficients"
VideoPort_L1_SkipTestCaseList_RPI["dsGetColorDepth_pos"] = "RPI doesn't support dsGetColorDepth"
VideoPort_L1_SkipTestCaseList_RPI["dsGetColorSpace_pos"] = "RPI doesn't support dsGetColorSpace"
VideoPort_L1_SkipTestCaseList_RPI["dsGetQuantizationRange_pos"] = "RPI doesn't support dsGetQuantizationRange"
VideoPort_L1_SkipTestCaseList_RPI["dsGetCurrentOutputSettings_pos"] = "RPI doesn't support dsGetCurrentOutputSettings"
VideoPort_L1_SkipTestCaseList_RPI["dsIsOutputHDR_pos"] = "RPI doesn't support dsIsOutputHDR"
VideoPort_L1_SkipTestCaseList_RPI["dsResetOutputToSDR_pos"] = "RPI doesn't support dsResetOutputToSDR"
VideoPort_L1_SkipTestCaseList_RPI["dsSetHdmiPreference_pos"] = "RPI doesn't support dsSetHdmiPreference"
VideoPort_L1_SkipTestCaseList_RPI["dsGetHdmiPreference_pos"] = "RPI doesn't support dsGetHdmiPreference"
VideoPort_L1_SkipTestCaseList_RPI["dsGetIgnoreEDIDStatus_pos"] = "RPI doesn't support dsGetIgnoreEDIDStatus"
VideoPort_L1_SkipTestCaseList_RPI["dsSetBackgroundColor_pos"] = "RPI doesn't support dsSetBackgroundColor"
VideoPort_L1_SkipTestCaseList_RPI["dsSetForceHDRMode_pos"] = "RPI doesn't support dsSetForceHDRMode"
VideoPort_L1_SkipTestCaseList_RPI["dsColorDepthCapb_pos"] = "RPI doesn't support dsColorDepthCapabilities"
VideoPort_L1_SkipTestCaseList_RPI["dsGetPreferredColorDepth_pos"] = "RPI doesn't support dsGetPreferredColorDepth"
VideoPort_L1_SkipTestCaseList_RPI["dsSetPreferredColorDepth_pos"] = "RPI doesn't support dsSetPreferredColorDepth"
VideoPort_L2_List = []
VideoPort_L2_SkipTestCaseList = {}
VideoPort_L2_SkipTestCaseList_RPI = {}
VideoPort_L2_SkipTestCaseList_RPI["SetAndGetHdmiPreference"] = "RPI doesn't support SetAndGetHdmiPreference "
VideoPort_L2_SkipTestCaseList_RPI["GetColorSpace"] =  "RPI doesn't support GetColorSpace"
VideoPort_L2_SkipTestCaseList_RPI["GetColorDepth"] = "RPI doesn't support GetColorDepth"
VideoPort_L2_SkipTestCaseList_RPI["GetQuantizationRange"] = "RPI doesn't support GetQuantizationRange"
VideoPort_L2_SkipTestCaseList_RPI["GetMatrixCoefficients" ] = "RPI doesn't support GetMatrixCoefficients"
VideoPort_L2_SkipTestCaseList_RPI["SetAndGetPreferredColorDepth_src"] =  "RPI doesn't support SetAndGetPreferredColorDepth"
VideoPort_L2_SkipTestCaseList_RPI["CheckColorDepthCapb_src"] = "RPI doesn't support CheckColorDepthCapabilities"
VideoPort_L2_SkipTestCaseList_RPI["RetrieveVerifySurroundModeCapb"] = "RPI doesn't support dsGetSurroundMode"
VideoPort_L2_SkipTestCaseList_RPI["GetHDRCapabilities"] = "RPI doesn't support GetHDRCapabilities REFPLTV-2576"
VideoPort_L2_SkipTestCaseList_RPI["GetHDCPStatus"] = "RPI doesn't support GetHDCPStatus REFPLTV-2542"
VideoPort_L2_SkipTestCaseList_RPI["VerifyHDCPProtocolStatus"] = "RPI doesn't support HDCPProtocolStatus"

Host_binaryConfig = "Source_HostSettings.yaml"
Host_L1_List = []
Host_L1_SkipTestCaseList = {}
Host_L1_SkipTestCaseList_RPI = {}
Host_L1_SkipTestCaseList_RPI["dsGetHostEDID_L1_positive"] =  "Not applicable for RPI - REFPLTV-2571"
Host_L1_advanced_List = []
Host_L2_List = []

Audio_binaryConfig = "Source_AudioSettings.yaml"
Audio_L1_List = []
Audio_L1_SkipTestCaseList = {}
Audio_L1_SkipTestCaseList_RPI = {}
Audio_L2_List = []
Audio_L2_SkipTestCaseList = {}
Audio_L2_SkipTestCaseList_RPI = {}
Audio_L2_SkipTestCaseList_RPI["SetAndGetStereoMode"] = "Not applicable for RPI REFPLTV-2543"

Display_binaryConfig ="Source_4K_Display.yaml"
Display_L1_List = []
Display_L2_List = []

# RMF Audio Capture HAL test Configurations
rmfAudioCapture_basePath = "rmf_audio_capture/"
rmfAudioCapture_binaryName = "hal_test_rmfAudioCapture"
rmfAudioCapture_binaryConfig = "rmfAudioCaptureAuxNotSupported.yaml"
rmfAudioCapture_L1_List = []
rmfAudioCapture_L2_List = []

# HDMICEC HAL test configurations
HDMICEC_basePath = "hdmi_cec/"
HDMICEC_binaryName = "hal_test_RCECHal"
HDMICEC_binaryConfig = "source_hdmiCEC.yml"
HDMICEC_L1_List = []
HDMICEC_L1_SkipTestCaseList = {}
HDMICEC_L1_SkipTestCaseList_RPI = {}
HDMICEC_L2_List = []
HDMICEC_L2_SkipTestCaseList = {}
HDMICEC_L2_SkipTestCaseList_RPI = {}

# PowerManager HAL test configurations
PowerManager_basePath = "power_manager/"
PowerManager_binaryName = "hal_test_iarmmgrs-power-hal"
PowerManager_binaryConfig = "source_powerManager.yaml"
PowerManager_L1_List = []
PowerManager_L2_List = []
PowerManager_L1_SkipTestCaseList = {}
PowerManager_L1_SkipTestCaseList["PLAT_SetPowerState_pos"] ="Testcase includes setting DUT to power state OFF"
PowerManager_L2_SkipTestCaseList = {}
PowerManager_L2_SkipTestCaseList["L2_SetAndGetPowerState"] = "Testcase includes setting DUT to power state OFF"

# DeepSleep HAL test configurations
DeepSleep_basePath = "deepsleep_manager/"
DeepSleep_binaryName = "hal_test_iarmmgrs-deepsleep-hal"
DeepSleep_binaryConfig = "deepsleepmanagerExtendedEnumsNotSupported.yaml"
DeepSleep_L1_List = []
DeepSleep_L2_List = []
DeepSleep_L1_SkipTestCaseList = {}
DeepSleep_L1_SkipTestCaseList_RPI = {}
DeepSleep_L1_SkipTestCaseList_RPI["PLAT_DeepSleepWakeup_pos"] = "Not applicable for RPI - REFPLTV-2526"
DeepSleep_L1_SkipTestCaseList_RPI["PLAT_SetDeepSleep_pos"] = "Not applicable for RPI - REFPLTV-2526"
DeepSleep_L2_SkipTestCaseList = {}
DeepSleep_L2_SkipTestCaseList_RPI = {}
DeepSleep_L2_SkipTestCaseList_RPI["SetDsAndVerifyWakeup1sec"] = "Not applicable for RPI - REFPLTV-2526"
DeepSleep_L2_SkipTestCaseList_RPI["SetDsAndVerifyWakeup10sec"] = "Not applicable for RPI - REFPLTV-2526"
