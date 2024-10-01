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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_Memcr_Validate_Cobalt_Launch_After_Reboot</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>memcr_datamodelcheck</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Memcr Feature Validation</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>rdkvmemcr_11</test_case_id>
    <test_objective>Verify that the Cobalt application successfully launches after the device is rebooted while Cobalt is in a hibernated state</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator and RPI</test_setup>
    <pre_requisite>MEMCR_APPHIBERNATE_PARAMETER needs to be configured in the device configuration file</pre_requisite>
    <api_or_interface_used>org.rdk.RDKShell.1.getClients,org.rdk.RDKShell.1.getState,org.rdk.RDKShell.1.restore,org.rdk.RDKShell.1.kill,org.rdk.RDKShell.1.launch,org.rdk.RDKShell.1.suspend,org.rdk.System.1.reboot</api_or_interface_used>
    <input_parameters>MEMCR_APPHIBERNATE_PARAMETER</input_parameters>
    <automation_approch>1. Retrieve the AppHibernate RFC parameter from the device configuration 2. Check the status of the Memcr service 3.Verify if the cobalt app is running if it is, terminate it 4. Launch the cobalt again 5. Check if the cobalt app enters a hibernated state by using the suspend API 6. Check that the cobalt application successfully launches after the device is rebooted while cobalt is in a hibernated state</automation_approch>
    <expected_output>All the steps should execute successfully</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>Nil</test_stub_interface>
    <test_script>RDKV_Memcr_Validate_Cobalt_Launch_After_Reboot</test_script>
    <skipped>Nil</skipped>
    <release_version>M129</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import ast
import time

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkvmemcr","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Memcr_Validate_Cobalt_Launch_After_Reboot');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

obj.setLoadModuleStatus(result.upper());
expectedResult = "SUCCESS"

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('memcr_getTR181Value')
    tdkTestObj.addParameter("basePath",obj.realpath)
    tdkTestObj.addParameter("configKey","MEMCR_APPHIBERNATE_PARAMETER")
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
    if "SUCCESS" in result:
        tdkTestObj.setResultStatus("SUCCESS")
        ##remove special characters by replace command
        result = ast.literal_eval(result)
        tr181_parameter = list(result)[0].strip()

        tdkTestObj = obj.createTestStep('memcr_statuscheck')
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS")

            tdkTestObj = obj.createTestStep('memcr_datamodelcheck')
            tdkTestObj.addParameter("datamodel",tr181_parameter)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            if "SUCCESS" in result:
                tdkTestObj.setResultStatus("SUCCESS")

                method = "org.rdk.RDKShell"
                params = '{ "callsign": "org.rdk.RDKShell" }'
                tdkTestObj = obj.createTestStep('memcr_checkPluginStatus')
                tdkTestObj.addParameter("method",method)
                tdkTestObj.addParameter("params",params)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResultDetails()
                if "SUCCESS" in result:
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    obj.unloadModule("rdkvmemcr");
                    exit()

                method = "org.rdk.RDKShell.1.getClients"
                tdkTestObj = obj.createTestStep('memcr_getValue')
                tdkTestObj.addParameter("method",method)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResultDetails()
                result = ast.literal_eval(result)
                appcheck = result.get("clients")
                success = result.get("success")
                if str(success).lower() == "true":
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("SUCCESS : "+method+" API call was successful\n")

                    if "cobalt" in appcheck:
                        method = "org.rdk.RDKShell.1.getState"
                        tdkTestObj = obj.createTestStep('memcr_getValue')
                        tdkTestObj.addParameter("method",method)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResultDetails()
                        result = ast.literal_eval(result)
                        #Access the list of applications
                        apps = result["state"]
                        #Iterate through the list to find the youtube app state
                        for app in apps:
                            if app["callsign"] == "Cobalt":
                                appstate = app["state"]
                        success = result.get("success")
                        if str(success).lower() != "true":
                            tdkTestObj.setResultStatus("FAILURE")
                            print("FAILURE : "+method+" API call was unsuccessful\n")
                            obj.unloadModule("rdkvmemcr");
                            exit()
                        else:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("SUCCESS : "+method+" API call was successful\n")

                        if appstate == "hibernated":
                            method = "org.rdk.RDKShell.1.restore"
                            value = '{ "callsign": "Cobalt" }'
                            tdkTestObj = obj.createTestStep('memcr_setValue')
                            tdkTestObj.addParameter("method",method)
                            tdkTestObj.addParameter("value",value)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResultDetails()
                            result = ast.literal_eval(result)
                            success = result.get("success")
                            if str(success).lower() != "true":
                                tdkTestObj.setResultStatus("FAILURE")
                                print("FAILURE : "+method+" API call was unsuccessful\n")
                                obj.unloadModule("rdkvmemcr");
                                exit()
                            else:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print("SUCCESS : "+method+" API call was successful\n")

                        method = "org.rdk.RDKShell.1.kill"
                        value = '{ "client": "cobalt" }'
                        tdkTestObj = obj.createTestStep('memcr_setValue')
                        tdkTestObj.addParameter("method",method)
                        tdkTestObj.addParameter("value",value)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResultDetails()
                        result = ast.literal_eval(result)
                        #Access the list of applications
                        success = result.get("success")
                        if str(success).lower() != "true":
                            tdkTestObj.setResultStatus("FAILURE")
                            print("FAILURE : "+method+" API call was unsuccessful\n")
                            obj.unloadModule("rdkvmemcr");
                            exit()
                        else:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("SUCCESS : "+method+" API call was successful\n")

                    time.sleep(5)
                    method = "org.rdk.RDKShell.1.launch"
                    value = '{ "callsign": "Cobalt" }'
                    tdkTestObj = obj.createTestStep('memcr_setValue')
                    tdkTestObj.addParameter("method",method)
                    tdkTestObj.addParameter("value",value)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResultDetails()
                    result = ast.literal_eval(result)
                    appstate = result.get("launchType")
                    success = result.get("success")
                    if str(success).lower() == "true" and "activate" in str(appstate).strip().lower():
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("SUCCESS : "+method+" API call was successful\n")

                        method = "org.rdk.RDKShell.1.getClients"
                        tdkTestObj = obj.createTestStep('memcr_getValue')
                        tdkTestObj.addParameter("method",method)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResultDetails()
                        result = ast.literal_eval(result)
                        appcheck = result.get("clients")
                        success = result.get("success")
                        if str(success).lower() != "true" and "cobalt" not in appcheck:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("FAILURE : "+method+" API call was unsuccessful\n")
                            obj.unloadModule("rdkvmemcr");
                            exit()
                        else:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("SUCCESS : "+method+" API call was successful\n")

                        method = "org.rdk.RDKShell.1.suspend"
                        value = '{ "callsign": "Cobalt" }'
                        tdkTestObj = obj.createTestStep('memcr_setValue')
                        tdkTestObj.addParameter("method",method)
                        tdkTestObj.addParameter("value",value)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResultDetails()
                        result = ast.literal_eval(result)
                        success = result.get("success")
                        if str(success).lower() == "true":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("SUCCESS : "+method+" API call was successful\n")

                            time.sleep(10)
                            method = "org.rdk.RDKShell.1.getState"
                            tdkTestObj = obj.createTestStep('memcr_getValue')
                            tdkTestObj.addParameter("method",method)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResultDetails()
                            result = ast.literal_eval(result)
                            #Access the list of applications
                            apps = result["state"]
                            #Iterate through the list to find the youtube app state
                            for app in apps:
                                if app["callsign"] == "Cobalt":
                                    appstate = app["state"]
                            success = result.get("success")
                            if str(success).lower() == "true":
                                tdkTestObj.setResultStatus("SUCCESS")
                                print("SUCCESS : "+method+" API call was successful")
                                if appstate == "hibernated":
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("SUCCESS : App entered in hibernate state\n")

                                    tdkTestObj = obj.createTestStep('memcr_rebootDevice')
                                    tdkTestObj.addParameter("waitTime",60)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResultDetails()
                                    if "SUCCESS" in result:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print("SUCCESS : The device powers up successfully within 60 seconds\n")

                                        method = "org.rdk.RDKShell"
                                        params = '{ "callsign": "org.rdk.RDKShell" }'
                                        tdkTestObj = obj.createTestStep('memcr_checkPluginStatus')
                                        tdkTestObj.addParameter("method",method)
                                        tdkTestObj.addParameter("params",params)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResultDetails()
                                        if "SUCCESS" in result:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            obj.unloadModule("rdkvmemcr");
                                            exit()
                            
                                        time.sleep(5)
                                        method = "org.rdk.RDKShell.1.launch"
                                        value = '{ "callsign": "Cobalt" }'
                                        tdkTestObj = obj.createTestStep('memcr_setValue')
                                        tdkTestObj.addParameter("method",method)
                                        tdkTestObj.addParameter("value",value)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResultDetails()
                                        result = ast.literal_eval(result)
                                        appstate = result.get("launchType")
                                        success = result.get("success")
                                        if str(success).lower() == "true" and "activate" in str(appstate).strip().lower():
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print("SUCCESS : "+method+" API call was successful")
                                            print("SUCCESS : Successfully launched YouTube\n")

                                            method = "org.rdk.RDKShell.1.getClients"
                                            tdkTestObj = obj.createTestStep('memcr_getValue')
                                            tdkTestObj.addParameter("method",method)
                                            tdkTestObj.executeTestCase(expectedResult)
                                            result = tdkTestObj.getResultDetails()
                                            result = ast.literal_eval(result)
                                            appcheck = result.get("clients")
                                            success = result.get("success")
                                            if str(success).lower() != "true" and "cobalt" not in appcheck:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print("FAILURE : "+method+" API call was unsuccessful\n")
                                            else:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print("SUCCESS : "+method+" API call was successful\n")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print("FAILURE : "+method+" API call was unsuccessful\n")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print("FAILURE : The device fails to power up within 60 seconds\n")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print("FAILURE : App failed to enter hibernate state\n")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print("FAILURE : "+method+" API call was unsuccessful\n")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("FAILURE : "+method+" API call was unsuccessful\n")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("FAILURE : "+method+" API call was unsuccessful\n")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("FAILURE : "+method+" API call was unsuccessful\n")
            else:
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
else:
    print("FAILURE : Module Loading Status Failure\n")

#unload module
obj.unloadModule("rdkvmemcr");
