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
##########################################################################
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Aamp_SetAndGet_Video_Zoom_reboot_persist</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampGetVideoZoom</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to verify the zoom mode in reboot scenario</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>true</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Aamp_88</test_case_id>
    <test_objective>Test script to verify the zoom mode in reboot scenario</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator,RPI</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs</pre_requisite>
    <api_or_interface_used>AampTune
AampGetVideoZoom
AampSetVideoZoom</api_or_interface_used>
    <input_parameters>HLS URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent.
2. Aamp Agent invokes Tune API with HLS URL
3. Aamp Agent invokes GetVideoZoom API to get the current zoom mode.
4. Aamp Agent invokes SetVideoZoom API to set the different mode.
5. Reboot the device
6. Aamp Agent invokes GetVideoZoom API to get the zoome mode and check if its persisted or not
7. TM checks if the value is set and returns SUCCESS/FAILURE
8. TM unloads the Aamp Agent.</automation_approch>
    <expected_output>Should persist the video zoom mode value after reboot scenario</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_SetAndGet_Video_Zoom_reboot_persist</test_script>
    <skipped>No</skipped>
    <release_version>M130</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
from time import sleep;
from tdkvutility import *

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
#Test component to be tested
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");
aampObj.configureTestCase(ip,port,'Aamp_SetAndGet_Video_Zoom_reboot_persist');
#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print("AAMP module loading status : %s" %aampLoadStatus) ;
if ("SUCCESS" in aampLoadStatus.upper()):
    aampObj.setLoadModuleStatus("SUCCESS");

    streamType="hlsstream"
    #pattern to be searched for event validation
    pattern="AAMP_EVENT_TUNED"
    #fetch Aamp stream from config file
    tuneURL=aampUtilitylib.getAampTuneURL(streamType);
    #Primitive test case which associated to this Script
    tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
    tdkTestObj.addParameter("URL",tuneURL);
    expectedResult = "SUCCESS";
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    if result and aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern) == "SUCCESS":
        print("AAMP Tune call is success")
        #Get the current video zoom mode while playing HLS stream content
        print("\nTEST STEP 1 : Get the current zoom mode using GetVideoZoom API");
        tdkTestObj = aampObj.createTestStep('Aamp_AampGetVideoZoom');
        expectedResult = "SUCCESS";
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        #Get the result of execution
        actualResult = tdkTestObj.getResult();
        print(actualResult);
        details = tdkTestObj.getResultDetails();
        print("Result :", details);
        if expectedResult in actualResult:
            zoom_mode  = int(details.split(':')[-1]);
            cur_zoommode = zoom_mode;
            if zoom_mode == 0:
                print("Current VideoZoom mode received succesfully");
                print("VideoZoom Enabled: FULL");
                tdkTestObj.setResultStatus("SUCCESS");
            elif zoom_mode == 1:
                print("Current VideoZoom mode received succesfully");
                print("VideoZoom Disabled: NONE");
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print("Mode received other than FULL and NONE.");
                tdkTestObj.setResultStatus("FAILURE");

            #set the different zoom mode & check
            print("\nTEST STEP 2 : To set the zoom mode other than the current");
            tdkTestObj = aampObj.createTestStep('Aamp_AampSetVideoZoom');
            expectedResult = "SUCCESS";
            if zoom_mode == 0:
                tdkTestObj.addParameter("zoom","NONE");
            elif zoom_mode == 1:
                tdkTestObj.addParameter("zoom","FULL");
            else:
                print("Invalid zoom mode");

            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print(actualResult);
            details = tdkTestObj.getResultDetails();
            if expectedResult in actualResult:
                set_zoom_mode = int(details.split(':')[-1]);
                print("SetVideoZoom mode call getting succeeded. Zoom mode updated : ", set_zoom_mode);
                tdkTestObj.setResultStatus("SUCCESS");

                print("\nTEST STEP 3 : Device will going to reboot")
                aampObj.initiateReboot();

                #get the zoom mode & verify its stored properly
                print("\nTEST STEP 4 : Get the current video zoom mode using GetVideoZoom API");
                print("EXPECTED OUTPUT : Should get value as set before reboot using SetVideoZoom API");
                tdkTestObj = aampObj.createTestStep('Aamp_AampGetVideoZoom');
                expectedResult = "SUCCESS";
                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedResult);
                #Get the result of execution
                actualResult = tdkTestObj.getResult();
                print(actualResult);
                details = tdkTestObj.getResultDetails();
                print("Result :", details);
                if expectedResult in actualResult:
                    zoom_mode  = int(details.split(':')[-1]);
                    if set_zoom_mode == zoom_mode:
                        print("VideoZoom mode persisted successfully");
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        print("VideoZoom mode not persisted successfully");
                        tdkTestObj.setResultStatus("FAILURE");
            else:
                print("SetVideoZoom mode call getting failed");
                tdkTestObj.setResultStatus("FAILURE");

            #Retain the zoom mode value which present before executing the script
            tdkTestObj = aampObj.createTestStep('Aamp_AampSetVideoZoom');
            expectedResult = "SUCCESS";
            if cur_zoommode == 0:
                tdkTestObj.addParameter("zoom","FULL");
            elif cur_zoommode == 1:
                tdkTestObj.addParameter("zoom","NONE");
            else:
                print("Invalid zoom mode");
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print(actualResult);
            details = tdkTestObj.getResultDetails();
            set_zoom_mode = int(details.split(':')[-1]);
            if expectedResult in actualResult:
                print("Initial VideoZoom mode got retained succesfully");
                print("Retained zoom mode : ", set_zoom_mode);
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print("Initial VideoZoom mode not retained succesfully");
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print("Current VideoZoom mode not received");
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print("AAMP Tune call Failed");
        tdkTestObj.setResultStatus("FAILURE");
    #Unload Module
    aampObj.unloadModule("aamp");
else:
    print("Failed to load aamp module");
    aampObj.setLoadModuleStatus("FAILURE");
