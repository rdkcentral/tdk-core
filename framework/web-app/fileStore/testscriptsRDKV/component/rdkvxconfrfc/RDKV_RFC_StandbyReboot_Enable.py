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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_RFC_StandbyReboot_Enable</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rfc_urlvalidate</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Remote Feature Control by Xconf Server</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>rdkvxconfrfc_12</test_case_id>
    <test_objective>Verify whether the given xconf server setting for Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.StandbyReboot.Enable is reflected in the box</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <test_setup>RPI-Client</test_setup>
    <pre_requisite>In the field of the RFC_XCONF_URL device configuration file, the Xconf server url must be given</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>RFC_XCONF_URL</input_parameters>
    <automation_approch>1: Check if the configured Xconf URL is accessible
2: Enable the maintenancemanager plugin
3: Check the presence of the partnerId3.dat file and ensure the 'community' string is included in it
4: Check the presence of the partners_defaults.json file and ensure the Xconf domain URL is included in it
5: Check the RFC parameter value prior to making any changes
6: Creating a feature name for configuration in the Xconf server
7: Creating a feature and its corresponding rule in the Xconf server
8: Check the correctness of all settings created in the Xconf server
9: Disable and enable the maintenance manager plugin
10: Check if the Xconf RFC settings are applied on the device
11: Revert the RFC parameter to its original value
12. Deleting  a feature and its corresponding rule in the Xconf server</automation_approch>
    <expected_output>All the steps should execute successfully</expected_output>
    <priority>Medium</priority>
    <test_stub_interface></test_stub_interface>
    <test_script>RDKV_RFC_StandbyReboot_Enable</test_script>
    <skipped>No</skipped>
    <release_version>M115</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkvxconfrfc","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_RFC_StandbyReboot_Enable');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

obj.setLoadModuleStatus(result.upper());
expectedResult = "SUCCESS"
Feature_Creation_Status="FAILURE"

if "SUCCESS" in result.upper():
    print("\n")
    #Step 1: Check if the configured Xconf URL is accessible
    tdkTestObj = obj.createTestStep('rfc_urlvalidate')
    tdkTestObj.addParameter("basePath",obj.realpath)
    tdkTestObj.addParameter("configKey","RFC_XCONF_URL")
    tdkTestObj.executeTestCase(expectedResult)
    detail = tdkTestObj.getResultDetails()
    if "FAILURE" not in detail:
        #remove special characters by replace command
        detail=detail.replace("(","").replace("'","").replace(")","")
        detail = detail.split(",")
        detail = detail[1]
        RFC_XCONF_URL=detail.strip()
        tdkTestObj.setResultStatus("SUCCESS")

        print("\n")
        #Step 2: Enable the maintenancemanager plugin
        method = "org.rdk.MaintenanceManager"
        params = '{ "callsign": "org.rdk.MaintenanceManager" }'
        tdkTestObj = obj.createTestStep('rfc_enable_maintenance_manager')
        tdkTestObj.addParameter("method",method)
        tdkTestObj.addParameter("params",params)
        tdkTestObj.executeTestCase(expectedResult)
        detail = tdkTestObj.getResultDetails()
        if "FAILURE" not in detail:
            tdkTestObj.setResultStatus("SUCCESS")

            print("\n")
            #Step 3: Check the presence of the partnerId3.dat file and ensure the 'community' string is included in it
            tdkTestObj = obj.createTestStep('rfc_datfilechecker')
            tdkTestObj.executeTestCase(expectedResult)
            detail = tdkTestObj.getResultDetails()
            if "FAILURE" not in detail:
                tdkTestObj.setResultStatus("SUCCESS")

                print("\n")
                #Step 4: Check the presence of the partners_defaults.json file and ensure the Xconf domain URL is included in it
                tdkTestObj = obj.createTestStep('rfc_partnersdefaultschecker')
                tdkTestObj.executeTestCase(expectedResult)
                detail = tdkTestObj.getResultDetails()
                if "FAILURE" not in detail:
                    tdkTestObj.setResultStatus("SUCCESS")

                    print("\n")
                    #Step 5: Check the RFC parameter value prior to making any changes
                    tdkTestObj = obj.createTestStep('rfc_datamodelcheck')
                    rfcparameter="Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.StandbyReboot.Enable"
                    tdkTestObj.addParameter("rfcparameter",rfcparameter)
                    tdkTestObj.executeTestCase(expectedResult)
                    actualvalue = tdkTestObj.getResultDetails()
                    if "true" in actualvalue or "false" in actualvalue or len(actualvalue)==0:
                        tdkTestObj.setResultStatus("SUCCESS")

                        print("\n")
                        #Step 6: Creating a feature name for configuration in the Xconf server
                        tdkTestObj = obj.createTestStep('rfc_formfeaturename')
                        feature_name="AutoReboot.Enable"
                        tdkTestObj.addParameter("feature_name",feature_name)
                        tdkTestObj.executeTestCase(expectedResult)
                        detail=tdkTestObj.getResultDetails()
                        if "FAILURE" not in detail:
                            #Remove special characters and unicode by replace command
                            detail= detail.replace("(","").replace(")","").replace("u'","'").replace("'","")
                            detail = detail.split(",")
                            detail = detail[1]
                            feature_name=detail.strip()
                            print("Feature name : "+feature_name)
                            tdkTestObj.setResultStatus("SUCCESS")

                            print("\n")
                            #Step 7: Creating a feature and its corresponding rule in the Xconf server
                            tdkTestObj = obj.createTestStep('rfc_initializefeatures')
                            slashparts = RFC_XCONF_URL.split('/')
                            xconfdomainname='/'.join(slashparts[:3]) + '/'
                            if  "true" in actualvalue:
                                expectedvalue="false"
                            elif "false" in actualvalue:
                                expectedvalue="true"
                            else:
                                expectedvalue="false"
                            tdkTestObj.addParameter("feature_name",feature_name)
                            tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                            tdkTestObj.addParameter("rfcparameter",rfcparameter)
                            tdkTestObj.addParameter("expectedvalue",expectedvalue)
                            tdkTestObj.executeTestCase(expectedResult)
                            actualresult = tdkTestObj.getResultDetails()
                            if expectedResult in actualresult.upper():
                                Feature_Creation_Status="SUCCESS"
                                tdkTestObj.setResultStatus("SUCCESS")

                                print("\n")
                                time.sleep(60)
                                #Step 8: Check the correctness of all settings created in the Xconf server
                                tdkTestObj = obj.createTestStep('rfc_checkconfiguredata')
                                tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                                tdkTestObj.addParameter("rfcparameter",rfcparameter)
                                tdkTestObj.addParameter("expectedvalue",expectedvalue)
                                tdkTestObj.addParameter("feature_name",feature_name)
                                tdkTestObj.executeTestCase(expectedResult)
                                actualresult = tdkTestObj.getResultDetails()
                                if expectedResult in actualresult.upper():
                                    tdkTestObj.setResultStatus("SUCCESS")

                                    print("\n")
                                    #Step 9: Disable and enable the maintenance manager plugin
                                    method = "org.rdk.MaintenanceManager"
                                    params = '{ "callsign": "org.rdk.MaintenanceManager" }'
                                    tdkTestObj = obj.createTestStep('rfc_disable_enable_maintenance_manager')
                                    tdkTestObj.addParameter("method",method)
                                    tdkTestObj.addParameter("params",params)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResultDetails()
                                    if "SUCCESS" in result:
                                        tdkTestObj.setResultStatus("SUCCESS")

                                        time.sleep(5)
                                        #Step 10: Check if the Xconf RFC settings are applied on the device
                                        tdkTestObj = obj.createTestStep('rfc_check_setornot_configdata')
                                        tdkTestObj.addParameter("rfcparameter",rfcparameter)
                                        tdkTestObj.addParameter("expectedvalue",expectedvalue)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        actualresult = tdkTestObj.getResultDetails()
                                        if "FAILURE" not in actualresult:
                                            tdkTestObj.setResultStatus("SUCCESS")

                                            #Step 11: Revert the RFC parameter to its original value
                                            print("\nRevert the RFC parameter to its original value")
                                            print("=====================================\n")
                                            tdkTestObj = obj.createTestStep('rfc_initializefeatures')
                                            tdkTestObj.addParameter("feature_name",feature_name)
                                            tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                                            tdkTestObj.addParameter("rfcparameter",rfcparameter)
                                            tdkTestObj.addParameter("expectedvalue",actualvalue)
                                            tdkTestObj.executeTestCase(expectedResult)
                                            actualresult = tdkTestObj.getResultDetails()
                                            if expectedResult in actualresult.upper():
                                                Feature_Creation_Status="SUCCESS"
                                                tdkTestObj.setResultStatus("SUCCESS")

                                                print("\n")
                                                time.sleep(60)
                                                tdkTestObj = obj.createTestStep('rfc_checkconfiguredata')
                                                tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                                                tdkTestObj.addParameter("rfcparameter",rfcparameter)
                                                tdkTestObj.addParameter("expectedvalue",actualvalue)
                                                tdkTestObj.addParameter("feature_name",feature_name)
                                                tdkTestObj.executeTestCase(expectedResult)
                                                actualresult = tdkTestObj.getResultDetails()
                                                if expectedResult in actualresult.upper():
                                                    tdkTestObj.setResultStatus("SUCCESS")

                                                    print("\n")
                                                    method = "org.rdk.MaintenanceManager"
                                                    params = '{ "callsign": "org.rdk.MaintenanceManager" }'
                                                    tdkTestObj = obj.createTestStep('rfc_disable_enable_maintenance_manager')
                                                    tdkTestObj.addParameter("method",method)
                                                    tdkTestObj.addParameter("params",params)
                                                    tdkTestObj.executeTestCase(expectedResult)
                                                    result = tdkTestObj.getResultDetails()
                                                    if "SUCCESS" in result:
                                                        tdkTestObj.setResultStatus("SUCCESS")

                                                        time.sleep(5)
                                                        tdkTestObj = obj.createTestStep('rfc_check_setornot_configdata')
                                                        tdkTestObj.addParameter("rfcparameter",rfcparameter)
                                                        tdkTestObj.addParameter("expectedvalue",actualvalue)
                                                        tdkTestObj.executeTestCase(expectedResult)
                                                        actualresult = tdkTestObj.getResultDetails()
                                                        if "FAILURE" not in actualresult:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                            #Deleting  a feature and its corresponding rule in the Xconf server
                            if Feature_Creation_Status == "SUCCESS":
                                print("\n")
                                tdkTestObj = obj.createTestStep('rfc_deletefeaturerule')
                                tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                                tdkTestObj.executeTestCase(expectedResult)
                                actualresult = tdkTestObj.getResultDetails()
                                if expectedResult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("\n")
                                    tdkTestObj = obj.createTestStep('rfc_deletefeature')
                                    tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    actualresult = tdkTestObj.getResultDetails()
                                    if expectedResult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
else:
    print("\nFAILURE : Module Loading Status Failure\n")

#unload module
obj.unloadModule('rdkvxconfrfc');
