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
  <name>RDKV_RFC_HDMICECDaemon_Enable</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rfc_updateserverurl</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Remote Feature Control by Xconf Server</synopsis>
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
    <test_case_id>rdkvxconfrfc_04</test_case_id>
    <test_objective>Verify whether the given xconf server setting for Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.HDMICECDaemon.Enable is reflected in the box</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <test_setup>RPI-Client</test_setup>
    <pre_requisite>In the field of the RFC_XCONF_URL device configuration file, the Xconf server url must be given</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Nil</input_parameters>
    <automation_approch>1. Update RFC Xconf URL in rfc.properties file 2. Check whether parodus process status is active running 3. Check the current value set in datamodel  4. Create Feature name for the data model and Feature rule for the DUT 5. Check whether the feature settings and feature rule is listing or not  6. Restart RFC service 7. Check whether the xconf server settings for the data model reflected in box or not 8. Finally, rollback the datamodel value to initial value</automation_approch>
    <expected_output>All the steps should execute successfully</expected_output>
    <priority>Medium</priority>
    <test_stub_interface></test_stub_interface>
    <test_script>RDKV_RFC_HDMICECDaemon_Enable</test_script>
    <skipped>No</skipped>
    <release_version>M114</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkvxconfrfc","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_RFC_HDMICECDaemon_Enable');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

obj.setLoadModuleStatus(result.upper());
expectedResult = "SUCCESS"

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('rfc_getDeviceConfig')
    tdkTestObj.addParameter("basePath",obj.realpath)
    tdkTestObj.addParameter("configKey","RFC_XCONF_URL")
    tdkTestObj.executeTestCase(expectedResult)
    RFC_XCONF_URL= tdkTestObj.getResultDetails()
    tdkTestObj = obj.createTestStep('rfc_updateserverurl')
    tdkTestObj.addParameter("RFC_XCONF_URL",RFC_XCONF_URL)
    tdkTestObj.executeTestCase(expectedResult)
    actualresult = tdkTestObj.getResultDetails()
    if expectedResult in actualresult.upper():
        tdkTestObj.setResultStatus("SUCCESS")

        tdkTestObj = obj.createTestStep('rfc_parodusstatuscheck')
        tdkTestObj.executeTestCase(expectedResult)
        actualresult = tdkTestObj.getResultDetails()
        if expectedResult in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS")

            tdkTestObj = obj.createTestStep('rfc_datamodelcheck')
            rfcparameter="Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.HDMICECDaemon.Enable"
            tdkTestObj.addParameter("rfcparameter",rfcparameter)
            tdkTestObj.executeTestCase(expectedResult)
            actualvalue = tdkTestObj.getResultDetails()
            if "true" in actualvalue or "false" in actualvalue or "" in actualvalue:
                tdkTestObj.setResultStatus("SUCCESS")

                tdkTestObj = obj.createTestStep('rfc_initializefeatures')
                slashparts = RFC_XCONF_URL.split('/')
                xconfdomainname='/'.join(slashparts[:3]) + '/'
                feature_name="TDKV_XCONF_RFC_VALIDATION_FEATURE_NAME"
                if  "true" in actualvalue:
                    expectedvalue="false"
                elif "false" in actualvalue:
                    expectedvalue="true"
                else:
                    expectedvalue="true"
                tdkTestObj.addParameter("feature_name",feature_name)
                tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                tdkTestObj.addParameter("rfcparameter",rfcparameter)
                tdkTestObj.addParameter("expectedvalue",expectedvalue)
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")

                    tdkTestObj = obj.createTestStep('rfc_checkconfiguredata')
                    tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                    tdkTestObj.addParameter("rfcparameter",rfcparameter)
                    tdkTestObj.addParameter("expectedvalue",expectedvalue)
                    tdkTestObj.addParameter("feature_name",feature_name)
                    tdkTestObj.executeTestCase(expectedResult)
                    actualresult = tdkTestObj.getResultDetails()
                    if expectedResult in actualresult.upper():
                      tdkTestObj.setResultStatus("SUCCESS")

                      tdkTestObj = obj.createTestStep('rfc_restartservice')
                      tdkTestObj.executeTestCase(expectedResult)
                      actualresult = tdkTestObj.getResultDetails()
                      if expectedResult in actualresult.upper():
                          tdkTestObj.setResultStatus("SUCCESS")

                          tdkTestObj = obj.createTestStep('rfc_check_setornot_configdata')
                          tdkTestObj.addParameter("rfcparameter",rfcparameter)
                          tdkTestObj.addParameter("expectedvalue",expectedvalue)
                          tdkTestObj.executeTestCase(expectedResult)
                          actualresult = tdkTestObj.getResultDetails()
                          if "FAILURE" not in actualresult:
                              tdkTestObj.setResultStatus("SUCCESS")

                              if actualresult in actualvalue:
                                  print "\nNo need to revert the RFC datamodel value\n"
                              else:
				  print "\nNeed to revert the RFC datamodel into actualvalue\n"
                                  tdkTestObj = obj.createTestStep('rfc_rollbackdatamodelvalue')
                                  tdkTestObj.addParameter("rfcparameter",rfcparameter)
                                  tdkTestObj.addParameter("actualvalue",actualvalue)
                                  tdkTestObj.addParameter("feature_name",feature_name)
                                  tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                                  tdkTestObj.executeTestCase(expectedResult)
                                  actualresult = tdkTestObj.getResultDetails()
                                  if expectedResult in actualresult.upper():
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
    print "\nFAILURE : Module Loading Status Failure\n"

#unload module
obj.unloadModule('rdkvxconfrfc');
