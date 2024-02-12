##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <id/>
  <version>1</version>
  <name>E2E_ParentalControl_ManagedServices_LAN_BlockHTTPS_AllowHTTP</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that WG allows other services when only HTTPs service is blocked through parental control( managed services)</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
    <box_type>Emulator</box_type>
    <box_type>RPI</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_400</test_case_id>
    <test_objective>Verify that WG allows other services when only HTTPs service is blocked through parental control( managed services)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_Comcast_com_ParentalControl.ManagedServices.Enable
"Device.X_Comcast_com_ParentalControl.ManagedServices.Service."</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save managedServiceEnable
3. Enable managed service
4. Add new rule to "Device.X_Comcast_com_ParentalControl.ManagedServices.Service."
5. Set values to all fields in new rule to block https
6.Check whether the LAN client is able to establish http connection
7.Delete the added rule and revert all params values
8.Unload tdkb_e2e module</automation_approch>
    <except_output>LAN client should be able to establish connection with the allowed service http</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_ParentalControl_ManagedServices_LAN_BlockHTTPS_AllowHTTP</test_script>
    <skipped>No</skipped>
    <release_version>M57</release_version>
    <remarks>LAN,WAN</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility
from tdkbE2EUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_ParentalControl_ManagedServices_LAN_BlockHTTPS_AllowHTTP');
obj1.configureTestCase(ip,port,'E2E_ParentalControl_ManagedServices_LAN_BlockHTTPS_AllowHTTP');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        managedServiceEnable = "Device.X_Comcast_com_ParentalControl.ManagedServices.Enable"

        #Get the value of the wifi parameters that are currently set.
        paramList=[managedServiceEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current managedServiceEnable status")
            print("EXPECTED RESULT 1: Should retrieve the current managedServiceEnable")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set the managedServiceEnable status as true"
            setValuesList = ['true'];
            print("Parameter values that are set: %s" %setValuesList)

            managedServiceEnableStatus = "%s|true|bool" %managedServiceEnable

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,managedServiceEnableStatus)
            if expectedresult in actualresult :
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the managedServiceEnable status as true")
                print("EXPECTED RESULT 2: Should set the managedServiceEnable status as true");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[managedServiceEnable]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current managedServiceEnable status")
                    print("EXPECTED RESULT 3: Should retrieve the current managedServiceEnable status")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    # Adding a new row to BlockedService
                    tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject");
                    tdkTestObj.addParameter("paramName","Device.X_Comcast_com_ParentalControl.ManagedServices.Service.");
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedresult in actualresult:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 4: Adding new rule for service blocking");
                        print("EXPECTED RESULT 4: Should add new rule");
                        print("ACTUAL RESULT 4: added new rule %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                        temp = details.split(':');
                        instance = temp[1];

                        if (instance > 0):
                            print("INSTANCE VALUE: %s" %instance)
                            description = "Device.X_Comcast_com_ParentalControl.ManagedServices.Service.%s.Description" %instance
                            protocol = "Device.X_Comcast_com_ParentalControl.ManagedServices.Service.%s.Protocol" %instance
                            startport = "Device.X_Comcast_com_ParentalControl.ManagedServices.Service.%s.StartPort" %instance
                            endPort = "Device.X_Comcast_com_ParentalControl.ManagedServices.Service.%s.EndPort" %instance
                            alwaysBlock = "Device.X_Comcast_com_ParentalControl.ManagedServices.Service.%s.AlwaysBlock" %instance

                            setValuesList = ['https','BOTH','443','443','true'];
                            print("Parameter values that are set: %s" %setValuesList)

                            list1 = [description,'https','string']
                            list2 = [protocol,'BOTH','string']
                            list3 = [startport,'443','unsignedInt']
                            list4 = [endPort,'443','unsignedInt']
                            list5 = [alwaysBlock,'true','bool']

                            #Concatenate the lists with the elements separated by pipe
                            setParamList= list1 + list2 + list3 + list4 + list5
                            setParamList = "|".join(map(str, setParamList))

                            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                            if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 5: Set all fields in added rule")
                                print("EXPECTED RESULT 5: Should set all fields in added rule");
                                print("ACTUAL RESULT 5: %s" %details);
                                print("[TEST EXECUTION RESULT] : SUCCESS");

                                #Retrieve the values after set and compare
                                newParamList=[description,protocol,startport,endPort,alwaysBlock]
                                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                                if expectedresult in status and setValuesList == newValues:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 6: Get all fields of added rule")
                                    print("EXPECTED RESULT 6: Should retrieve all fields of added rule")
                                    print("ACTUAL RESULT 6: %s" %newValues);
                                    print("[TEST EXECUTION RESULT] : SUCCESS");

                                    #Wait for the changes to reflect in client device
                                    time.sleep(60);

                                    #Refresh lan connection and get its ip
                                    print("TEST STEP 7: Get the IP address of the lan client")
                                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                                    if lanIP:
                                        tdkTestObj.setResultStatus("SUCCESS");

                                        print("TEST STEP 8: Get the current LAN IP address DHCP range")
                                        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                        tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                        print("LAN IP Address: %s" %curIPAddress);

                                        if expectedresult in status and curIPAddress:
                                            tdkTestObj.setResultStatus("SUCCESS");

                                            print("TEST STEP 9: Check whether lan ip address is in same DHCP range")
                                            status = "SUCCESS"
                                            status = checkIpRange(curIPAddress,lanIP);
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("wlan ip address is in same DHCP range")

                                                print("TEST STEP 10:Static route add")
                                                #set new static route to wan client
                                                status = addStaticRoute(tdkbE2EUtility.wan_http_ip, curIPAddress, tdkbE2EUtility.lan_interface, "LAN");
                                                if expectedresult in status:
                                                    print("TEST STEP 10:Static route add success")
                                                    tdkTestObj.setResultStatus("SUCCESS");

                                                    print("TEST STEP 11:Check the HTTP connectivity from LAN to WAN")

                                                    status = wgetToWAN("WGET_HTTP", lanIP, curIPAddress, "LAN")

                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("The allowed service 'HTTP' can be reached")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("The allowed service 'HTTP' cannot be reached")
                                                        print("[TEST EXECUTION RESULT] : FAILURE");

                                                    #delete the added route
                                                    print("TEST STEP 12: Delete the static route")
                                                    status = delStaticRoute(tdkbE2EUtility.wan_http_ip, curIPAddress, tdkbE2EUtility.lan_interface, "LAN");
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        finalStatus = "SUCCESS";
                                                        print("TEST STEP 12:Static route delete success")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("TEST STEP 12:Static route delete failed")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 9:LAN Client IP address is not in the same Gateway DHCP range")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 8:Failed to get the Gateway IP address")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 7:Failed to get the LAN Client IP address")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 6: Get all fields of added rule")
                                    print("EXPECTED RESULT 6: Should retrieve all fields of added rule")
                                    print("ACTUAL RESULT 6: %s" %newValues);
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 5: Set all fields of added rule")
                                print("EXPECTED RESULT 5: Should set all fields of added rule");
                                print("ACTUAL RESULT 5: %s" %details);
                                print("[TEST EXECUTION RESULT] : FAILURE")

                            #Delete the created table entry
                            tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject");
                            tdkTestObj.addParameter("paramName","Device.X_Comcast_com_ParentalControl.ManagedServices.Service.%s." %instance);
                            expectedresult = "SUCCESS";
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            print("[TEST EXECUTION RESULT] : %s" %actualresult) ;
                            details = tdkTestObj.getResultDetails();
                            if expectedresult in actualresult:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("[TEST STEP ]: Deleting the added rule");
                                print("[EXPECTED RESULT ]: Should delete the added rule");
                                print("[ACTUAL RESULT]: %s" %details);
                                print("[TEST EXECUTION RESULT] : %s" %actualresult);
                                print("Added table is deleted successfully\n")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("[TEST STEP ]: Deleting the added rule");
                                print("[EXPECTED RESULT ]: Should delete the added rule");
                                print("[ACTUAL RESULT]: %s" %details);
                                print("[TEST EXECUTION RESULT] : %s" %actualresult);
                                print("Added table could not be deleted\n")
                        else:
                            print("Table add returned invalid instance")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4: Adding new rule for service blocking");
                        print("EXPECTED RESULT 4: Should add new rule");
                        print("ACTUAL RESULT 4: added new rule %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current managedServiceEnable status")
                    print("EXPECTED RESULT 3: Should retrieve the current managedServiceEnable statuse")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("TEST STEP 2: Set the managedServiceEnable")
                print("EXPECTED RESULT 2: Should set the managedServiceEnable");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted
            managedServiceEnableStatus = "%s|%s|bool" %(managedServiceEnable,orgValue[0])

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,managedServiceEnableStatus)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 13: Should set the original managedServiceEnable status");
                print("ACTUAL RESULT 13: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 13: Should set the original managedServiceEnable ");
                print("ACTUAL RESULT 13: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current managedServiceEnable status")
            print("EXPECTED RESULT 1: Should retrieve the current managedServiceEnable status")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
    obj1.unloadModule("advancedconfig");
else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");