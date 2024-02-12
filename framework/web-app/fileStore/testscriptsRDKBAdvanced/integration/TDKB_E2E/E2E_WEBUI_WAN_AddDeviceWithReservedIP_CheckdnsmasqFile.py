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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_WEBUI_WAN_AddDeviceWithReservedIP_CheckdnsmasqFile</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To add a device with reserved IP ,disconnect and connect the LAN client and verify the LAN client has reserved IP and dnsmasq leases file has reserved IP details</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <box_type>Broadband</box_type>
    <!--  -->
    <box_type>RPI</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_530</test_case_id>
    <test_objective>To add a device with reserved IP ,disconnect and connect the LAN client and verify the LAN client has reserved IP and dnsmasq leases file has reserved IP details</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Get the lan mode and check if the device is in router mode
4.Retrieve the lan MAC address
5. Start selenium hub in TM machine
6. Start Node in wan client machine
7. Try to access the WEBUI of the gateway using selenium grid
8. Navigate to Connected devices
9.Click ADD DEVICE WITH RESERVED IP
10.Enter the reserved IP details
11.Disconnect lan client
12.Connect LAN client
13.Check if lan client has reserved IP
14.Check if dnsmasq leases file has reserved IP details
15. Kill selenium hub and node
16. unload module</automation_approch>
    <expected_output>Adding the device details for reserved IP ,after disconnecting and connecting LAN client,lan client should have reserved IP and reserved IP details should be updated in dnsmasq leases file</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_WAN_AddDeviceWithReservedIP_CheckdnsmasqFile</test_script>
    <skipped>No</skipped>
    <release_version>M71</release_version>
    <remarks>None</remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility;
from tdkbE2EUtility import *;
import tdkbWEBUIUtility;
from tdkbWEBUIUtility import *;
from selenium.common.exceptions import NoSuchElementException;


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("sysutil","1");
obj2 = tdklib.TDKScriptingLibrary("tdkbtr181","1");


#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_WAN_AddDeviceWithReservedIP_CheckdnsmasqFile');
obj1.configureTestCase(ip,port,'E2E_WEBUI_WAN_AddDeviceWithReservedIP_CheckdnsmasqFile');
obj2.configureTestCase(ip,port,'E2E_WEBUI_WAN_AddDeviceWithReservedIP_CheckdnsmasqFile');


#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();
loadmodulestatus2 =obj2.getLoadModuleResult();

print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus1) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus2) ;


if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper() and "SUCCESS" in loadmodulestatus2.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        lanMode = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode"
        tdkTestObj,status,orgValue = getParameterValue(obj,lanMode)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current lanMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");
            print("TEST STEP 2: Check whether device is in router mode")
            #Check if device is in router mode
            if orgValue == "router":
                #Connect to the lan client
                print("TEST STEP 3: Connect to LAN Client and get the IP address")
                lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                if lanIP:
                    tdkTestObj.setResultStatus("SUCCESS");

                    connectedHostname = tdkbE2EUtility.connected_lan_hostname
                    print("ConnectedHostname is %s" %connectedHostname)
                    lanMAC = getLanMACAddress(tdkbE2EUtility.lan_interface)

                    ipv4_1 = lanIP.split(".")[0];
                    ipv4_2 = lanIP.split(".")[1];
                    ipv4_3 = lanIP.split(".")[2];
                    ipv4_4 = lanIP.split(".")[3];
                    ipv4_5 = int(ipv4_4) + 1
                    change_ReservedIP = "%s.%s.%s.%s" %(ipv4_1,ipv4_2,ipv4_3,ipv4_5)
                    print("ReservedIP :%s " %change_ReservedIP)

                    #Set Selenium grid
                    driver,status = startSeleniumGrid(tdkTestObj,"WAN",tdkbE2EUtility.mso_grid_url,"MSOLogin");
                    if status == "SUCCESS":
                        try:
                            # To click on the Connected devices
                            driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/ul/li[2]/a").click()
                            time.sleep(10);
                            #To click on ADD DEVICE WITH RESERVED IP
                            driver.find_element_by_xpath("//*[@id='online-private']/div/a").click()
                            #To enter the details for reserved IP
                            driver.find_element_by_id("host_name").send_keys(connectedHostname)
                            driver.find_element_by_id("mac_address").send_keys(lanMAC)
                            driver.find_element_by_id("staticIPAddress").send_keys(change_ReservedIP)
                            driver.find_element_by_id("comments").send_keys("test")
                            driver.find_element_by_id("saveBtn").click()

                            time.sleep(30);
                            print("Disconnect the lan client")
                            status= bringdownInterface(tdkbE2EUtility.lan_interface,"LAN");
                            if status == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 4: Check if lan client is disconnected");
                                print("ACTUAL RESULT 4:LAN client is disconnected")
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : SUCCESS");

                                print("Connect the lan client")
                                time.sleep(30);
                                driver.refresh()
                                status= bringupInterface(tdkbE2EUtility.lan_interface,"LAN");
                                if status == "SUCCESS":
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 5: Check if lan client is connected");
                                    print("ACTUAL RESULT 5 :LAN client is connected")
                                    #Get the result of execution
                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                    newlanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                                    if newlanIP == change_ReservedIP:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("TEST STEP 6: Check if lan client has reserved IP");
                                        print("ACTUAL RESULT 6 :LAN client IP and reserved IP are same")
                                        #Get the result of execution
                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                        tdkTestObj = obj1.createTestStep('ExecuteCmd');
                                        cmd = "cat /nvram/dnsmasq.leases | grep -i %s" %lanMAC;
                                        tdkTestObj.addParameter("command", cmd);

                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details = tdkTestObj.getResultDetails().strip().replace("\\n","");
                                        if lanMAC in details and change_ReservedIP in details and connectedHostname in details:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP 7: Check if dnsmasq leases file has reserved IP details");
                                            print("ACTUAL RESULT 7 :dnsmasq leases file has reserved IP details")
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 7: Check if dnsmasq leases file has reserved IP details");
                                            print("ACTUAL RESULT 7 :reserved IP details are not updated in dnsmasq leases file")
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 6: Check if lan client has reserved IP");
                                        print("ACTUAL RESULT 6:LAN client IP and reserved IP are not same")
                                        #Get the result of execution
                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                    try:
                                        print("Reverting the reserved IP to DHCP")
                                        driver.find_element_by_xpath('//*[@id="btn-1"]').click()
                                        time.sleep(5);
                                        driver.find_element_by_xpath('//*[@id="pageForm-1"]/div[3]/label[2]').click()
                                        time.sleep(5);
                                        driver.find_element_by_id('submit_editDevice-1').click()
                                        time.sleep(40);
                                        details = driver.find_element_by_xpath('//*[@id="online-private"]/table/tbody/tr[2]/td[2]').text
                                        if details == "DHCP":
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP 8: Check if reserved IP changes are reverted to DHCP");
                                            print("ACTUAL RESULT 8:Reserved IP changes are reverted to DHCP")
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 8: Check if reserved IP changes are reverted to DHCP");
                                            print("ACTUAL RESULT 8:Reserved IP changes are not reverted to DHCP")
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                    except NoSuchElementException:
                                        tdkTestObj = obj2.createTestStep('TDKB_TR181Stub_Get');
                                        tdkTestObj.addParameter("ParamName","Device.Hosts.HostNumberOfEntries");
                                        expectedresult="SUCCESS";

                                        #Execute the test case in DUT
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        NoOfHosts = tdkTestObj.getResultDetails();

                                        if expectedresult in actualresult and int(NoOfHosts)>0:
                                            #Set the result status of execution
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP : Get the number of hosts");
                                            print("EXPECTED RESULT : Should get the number of hosts");
                                            print("ACTUAL RESULT : Number of hosts :%s" %NoOfHosts);
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                            #Find the active hosts amoung the listed Hosts. List will contains the ids of active hosts
                                            List=[];
                                            for i in range(1,int(NoOfHosts)+1):
                                                tdkTestObj.addParameter("ParamName","Device.Hosts.Host.%d.Active" %i);
                                                #Execute the test case in DUT
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                Status = tdkTestObj.getResultDetails();
                                                if "true" in Status:
                                                    List.extend(str(i));
                                            if expectedresult in actualresult:
                                                #Set the result status of execution
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("TEST STEP : Get the active LAN clients");
                                                print("EXPECTED RESULT : Should get the active LAN clients");
                                                print("ACTUAL RESULT : Active LAN clients are :",List);
                                                #Get the result of execution
                                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                                #compare the IPs obtained
                                                ret =0;
                                                for i in range(0,len(List)):
                                                    n = int(List[i]);
                                                    tdkTestObj.addParameter("ParamName","Device.Hosts.Host.%d.IPv4Address.1.IPAddress" %n);
                                                    #Execute the test case in DUT
                                                    tdkTestObj.executeTestCase(expectedresult);
                                                    actualresult = tdkTestObj.getResult();
                                                    IP1 = tdkTestObj.getResultDetails();
                                                    print("IP Address in Device.Hosts.: %s" %IP1);
                                                    print("IP Address using ARP command: %s" %lanIP);
                                                    if IP1 in lanIP:
                                                        print("IP of LAN host instance ",n," matches");
                                                    else:
                                                        print("IP of LAN host instance ",n," doesnt match");
                                                        ret = 1
                                                if expectedresult in actualresult and ret ==0:
                                                    #Set the result status of execution
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("TEST STEP : Compare the LAN client IPs obtained");
                                                    print("EXPECTED RESULT : Both IPs should match");
                                                    print("ACTUAL RESULT : The LAN client IPs matched successfully");
                                                    #Get the result of execution
                                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    tdkTestObj = obj2.createTestStep('TDKB_TR181Stub_Set');
                                                    tdkTestObj.addParameter("ParamName","Device.Hosts.Host.%d.AddressSource" %n)
                                                    tdkTestObj.addParameter("ParamValue","DHCP");
                                                    tdkTestObj.addParameter("Type","string");

                                                    #Execute the test case in DUT
                                                    tdkTestObj.executeTestCase(expectedresult);
                                                    actualresult = tdkTestObj.getResult();
                                                    details = tdkTestObj.getResultDetails();

                                                    if expectedresult in actualresult:
                                                        #Set the result status of execution
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("TEST STEP : Revert the reserved IP to DHCP");
                                                        print("ACTUAL RESULT :%s" %details);
                                                        #Get the result of execution
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    else:
                                                        #Set the result status of execution
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("TEST STEP : Revert the reserved IP to DHCP");
                                                        print("ACTUAL RESULT :%s" %details);
                                                        #Get the result of execution
                                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                                else:
                                                    #Set the result status of execution
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP : Compare the LAN client IPs obtained");
                                                    print("EXPECTED RESULT : Both IPs should match");
                                                    print("ACTUAL RESULT : The LAN client IPs are not matching");
                                                    #Get the result of execution
                                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                            else:
                                                #Set the result status of execution
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP : Get the active LAN clients");
                                                print("EXPECTED RESULT : Should get the active cleints");
                                                print("ACTUAL RESULT : FAiled to get the active LAN clients");
                                                #Get the result of execution
                                                print("[TEST EXECUTION RESULT] : FAILURE");
                                        else:
                                            #Set the result status of execution
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP : Get the number of hosts");
                                            print("EXPECTED RESULT : Should get the number of hosts");
                                            print("ACTUAL RESULT : Number of hosts :%s" %NoOfHosts);
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 5: Check if lan client is connected");
                                    print("ACTUAL RESULT 5 :LAN client is not connected")
                                    #Get the result of execution
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 4: Check if lan client is disconnected");
                                print("ACTUAL RESULT 4 :LAN client is not disconnected")
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : FAILURE");

                        except Exception as error:
                            tdkTestObj.setResultStatus("FAILURE");
                            print(error);
                        time.sleep(10);
                        driver.quit();
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("Failed to set selenium grid")
                    #Kill selenium hub and node
                    status = tdkbWEBUIUtility.kill_hub_node("WAN")
                    if status == "SUCCESS":
                        print("TEST STEP 9:Executing Post-requisite")
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("Post-requisite success")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 9:Couldnt kill node and hub")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3:Failed to get LAN IP")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2:Device is in bridge mode")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current lanMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
    obj1.unloadModule("sysutil");
    obj2.unloadModule("tdkbtr181");


else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");