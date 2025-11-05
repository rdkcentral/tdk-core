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
##########################################################################
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Aamp_Set_PreferredAudioLanguages_Live_URL_Invalid</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampSetPreferredLanguages</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to set  invalid preferred language list</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Aamp_45</test_case_id>
    <test_objective>Test Script to set  invalid preferred language list</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper Live tuning URL</pre_requisite>
    <api_or_interface_used>AampTune
AampStop
AampGetAvailableAudioTracks
AampGetCurrentAudioLanguage
AampGetPreferredLanguages
AampSetPreferredLanguages</api_or_interface_used>
    <input_parameters>Live URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent and systemutil Agent.
2. Aamp Agent invokes Tune API with Live URL
3. Aamp Agent invokes GetAvailableAudioTracks API
4. Aamp Agent invokes GetCurrentAudioLanguage API
5. Generate language code list except current audio language from the available audio tracks. And append "invalid" to language list
6.Aamp Agent invokes AampStop, to set the preferred language list at player idle state.
7.Aamp Agent invokes Tune API with Live URL
8.Aamp Agent invokes AampGetPreferredLanguages API
9.Aamp Agent invokes GetCurrentAudioLanguage API
10. GetPreferredLanguages  should be same as that of language list set and current language should be the second most preferred language
11. TM unloads the Aamp Agent and systemutil Agent.</automation_approch>
    <expected_output>Should be able to set the list of preferred language and current language should get updated to second most preferred one (i.e) the second language in the list</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_Set_PreferredAudioLanguages_Live_URL_Invalid</test_script>
    <skipped>No</skipped>
    <release_version>M78</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def Tune(aampObj,tuneURL):
    status = "SUCCESS";
    #Prmitive test case which associated to this Script
    tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
    tdkTestObj.addParameter("URL",tuneURL);
    expectedResult = "SUCCESS";
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    #Get the result of execution
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        print("AAMP Tune call is success")
        #Search events in Log
        actualResult=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
        if expectedResult in actualResult:
            print("AAMP Tune event recieved")
            print("[TEST EXECUTION RESULT] : %s" %actualResult);
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            status = "FAILURE"
            print("No AAMP tune event received")
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
    else:
        status = "FAILURE"
        print("AAMP Tune call Failed")
        print("Error description : ",details)
        print("[TEST EXECUTION RESULT] : %s" %actualResult);
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
    return status;

def Stop(aampObj):
    status = "SUCCESS"
    #AampTuneStop call
    tdkTestObj = aampObj.createTestStep('Aamp_AampStop');
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    if expectedResult in result:
        print("AAMP Stop Success")
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        status = "FAILURE"
        print("AAMP Stop Failure")
        tdkTestObj.setResultStatus("FAILURE")
    return status;


#Test component to be tested
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");
sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");
aampObj.configureTestCase(ip,port,'Aamp_Set_PreferredAudioLanguages_Live_URL_Invalid');
sysObj.configureTestCase(ip,port,'Aamp_Set_PreferredAudioLanguages_Live_URL_Invalid');
#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print("AAMP module loading status : %s" %aampLoadStatus) ;
sysLoadStatus = sysObj.getLoadModuleResult();
print("SystemUtil module loading status : %s" %sysLoadStatus) ;
if ("SUCCESS" in aampLoadStatus.upper()) and ("SUCCESS" in sysLoadStatus.upper()):
    aampObj.setLoadModuleStatus("SUCCESS");
    sysObj.setLoadModuleStatus("SUCCESS");

    getLangCodesStatus = "SUCCESS"
    streamType="livestream"
    #pattern to be searched for event validation
    pattern="AAMP_EVENT_TUNED"
    #fetch Aamp stream from config file
    tuneURL=aampUtilitylib.getAampTuneURL(streamType);

    tuneStatus = Tune(aampObj,tuneURL);
    if "SUCCESS" in tuneStatus:
        tdkTestObj = aampObj.createTestStep('Aamp_AampGetAvailableAudioTracks');
        expectedResult = "SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print(actualResult);
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            audio_tracks = str(details).split(":")[1].replace("'","").strip().split(",")
            print("Result :", details);
            print("Tracks :",audio_tracks)

            tdkTestObj = aampObj.createTestStep('Aamp_AampGetCurrentAudioLanguage');
            expectedResult = "SUCCESS";
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print(actualResult);
            details = tdkTestObj.getResultDetails();
            curr_lang = str(details).strip()
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                lang_codes = [ lang for lang in audio_tracks if lang != curr_lang ]
                print("Result :", details);
                print("Tracks without current language : ",lang_codes)
                print("[TEST EXECUTION RESULT] : SUCCESS\n")
            else:
                getLangCodesStatus = "FAILURE";
                tdkTestObj.setResultStatus("FAILURE");
                print(details);
                print("[TEST EXECUTION RESULT] : FAILURE\n")
        else:
            getLangCodesStatus = "FAILURE";
            tdkTestObj.setResultStatus("FAILURE");
            print(details);
            print("[TEST EXECUTION RESULT] : FAILURE\n")

        stopStatus = Stop(aampObj);
        # Setting the preferred language during player idle state
        if getLangCodesStatus == "SUCCESS" and stopStatus == "SUCCESS":
            tdkTestObj = aampObj.createTestStep('Aamp_AampSetPreferredLanguages');
            if len(lang_codes) > 0:
                lang_list = ",".join(lang_codes)
            else:
                lang_list = ",".join(audio_tracks)

            #Forming language list with invalid keyword
            invalid_lang = "invalid"
            lang_list = invalid_lang + "," + lang_list
            expectedResult = "SUCCESS";
            print("Preferred Languages to be set :",lang_list)
            tdkTestObj.addParameter("languages",lang_list);
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            print(actualResult);
            details = tdkTestObj.getResultDetails();
            if expectedResult in actualResult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("Result : %s\n" %(details))

                tuneStatus = Tune(aampObj,tuneURL);
                if "SUCCESS" in tuneStatus:
                    tdkTestObj = aampObj.createTestStep('Aamp_AampGetPreferredLanguages');
                    expectedResult = "SUCCESS";
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    print(actualResult);
                    details = tdkTestObj.getResultDetails();
                    if expectedResult in actualResult and lang_list in str(details):
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("Result :", details);

                        tdkTestObj = aampObj.createTestStep('Aamp_AampGetCurrentAudioLanguage');
                        expectedResult = "SUCCESS";
                        tdkTestObj.executeTestCase(expectedResult);
                        actualResult = tdkTestObj.getResult();
                        print(actualResult);
                        details = tdkTestObj.getResultDetails();
                        new_lang = str(details).strip()
                        if expectedResult in actualResult and new_lang != lang_list.split(",")[0] and new_lang == lang_list.split(",")[1]:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("Result :", details);
                            print("Current Audio language is same as second most preferred language")
                            print("[TEST EXECUTION RESULT] : SUCCESS\n")

                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print(details);
                            print("Current Audio language is not same as second most preferred language")
                            print("[TEST EXECUTION RESULT] : FAILURE\n")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print(details);
                        print("[TEST EXECUTION RESULT] : FAILURE\n")
                    Stop(aampObj);
                else:
                    print("Secondary tune failed")
                    tdkTestObj.setResultStatus("FAILURE");
                    print("[TEST EXECUTION RESULT] : FAILURE\n")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print(details);
                print("[TEST EXECUTION RESULT] : FAILURE\n")
        else:
            print("Cannot proceed due to failure\n")
    else:
        print("Tune failure cannot proceed\n")

    #Unload Module
    aampObj.unloadModule("aamp");
    sysObj.unloadModule("systemutil");
else:
    print("Failed to load aamp/systemutil module");
    aampObj.setLoadModuleStatus("FAILURE");
    sysObj.setLoadModuleStatus("FAILURE");
