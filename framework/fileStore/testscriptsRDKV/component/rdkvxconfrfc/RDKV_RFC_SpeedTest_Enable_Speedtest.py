##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
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

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkvxconfrfc","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_RFC_SpeedTest_Enable_Speedtest')

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)

obj.setLoadModuleStatus(result.upper())
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
        #extracting the xconf domain from the full URL
        slashparts = RFC_XCONF_URL.split('/')
        xconfdomainname='/'.join(slashparts[:3])
        tdkTestObj.setResultStatus("SUCCESS")

        print("\n")
        #Step 2: Get the authorization token from the device configuration
        tdkTestObj = obj.createTestStep('rfc_getDeviceConfig')
        tdkTestObj.addParameter("basePath",obj.realpath)
        tdkTestObj.addParameter("configKey","XCONF_AUTHORIZATION_TOKEN_KEY")
        tdkTestObj.executeTestCase(expectedResult)
        detail = tdkTestObj.getResultDetails()
        if not detail:
            print("FAILURE : Unable to get the authorization token")
            tdkTestObj.setResultStatus("FAILURE")
            obj.unloadModule('rdkvxconfrfc')
            exit()

        print("SUCCESS : Authorization token %s is obtained successfully" % detail)
        XCONF_AUTHORIZATION_TOKEN_KEY = detail
        tdkTestObj.setResultStatus("SUCCESS")

        print("\n")
        #Step 3: Enable the maintenancemanager plugin
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
            #Step 4: Check the presence of the partnerId3.dat file and ensure the 'community' string is included in it
            tdkTestObj = obj.createTestStep('rfc_datfilechecker')
            tdkTestObj.executeTestCase(expectedResult)
            detail = tdkTestObj.getResultDetails()
            if "FAILURE" not in detail:
                tdkTestObj.setResultStatus("SUCCESS")

                print("\n")
                #Step 5: Check the presence of the partners_defaults.json file and ensure the Xconf domain URL is included in it
                tdkTestObj = obj.createTestStep('rfc_partnersdefaultschecker')
                tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                tdkTestObj.executeTestCase(expectedResult)
                detail = tdkTestObj.getResultDetails()
                if "FAILURE" not in detail:
                    tdkTestObj.setResultStatus("SUCCESS")

                    print("\n")
                    #Step 6: Check the RFC parameter value prior to making any changes
                    tdkTestObj = obj.createTestStep('rfc_datamodelcheck')
                    rfcparameter="Device.IP.Diagnostics.X_RDKCENTRAL-COM_SpeedTest.Enable_Speedtest"
                    tdkTestObj.addParameter("rfcparameter",rfcparameter)
                    tdkTestObj.executeTestCase(expectedResult)
                    actualvalue = tdkTestObj.getResultDetails()
                    if "true" in actualvalue or "false" in actualvalue or len(actualvalue)==0:
                        tdkTestObj.setResultStatus("SUCCESS")

                        print("\n")
                        #Step 7: Creating a feature name for configuration in the Xconf server
                        tdkTestObj = obj.createTestStep('rfc_formfeaturename')
                        feature_name="SpeedTest_Enable_Speedtest"
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
                            #Step 8: Creating a feature and its corresponding rule in the Xconf server
                            tdkTestObj = obj.createTestStep('rfc_initializefeatures')
                            if  "true" in actualvalue:
                                expectedvalue="false"
                            elif "false" in actualvalue:
                                expectedvalue="true"
                            else:
                                expectedvalue="false"
                            tdkTestObj.addParameter("feature_name",feature_name)
                            tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                            tdkTestObj.addParameter("rfcparameter",rfcparameter)
                            tdkTestObj.addParameter("XCONF_AUTHORIZATION_TOKEN_KEY",XCONF_AUTHORIZATION_TOKEN_KEY)
                            tdkTestObj.addParameter("expectedvalue",expectedvalue)
                            tdkTestObj.executeTestCase(expectedResult)
                            actualresult = tdkTestObj.getResultDetails()
                            if expectedResult in actualresult.upper():
                                Feature_Creation_Status="SUCCESS"
                                tdkTestObj.setResultStatus("SUCCESS")

                                print("\n")
                                time.sleep(60)
                                #Step 9: Check the correctness of all settings created in the Xconf server
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
                                    #Step 10: Disable and enable the maintenance manager plugin
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
                                        #Step 11: Check if the Xconf RFC settings are applied on the device
                                        tdkTestObj = obj.createTestStep('rfc_check_setornot_configdata')
                                        tdkTestObj.addParameter("rfcparameter",rfcparameter)
                                        tdkTestObj.addParameter("expectedvalue",expectedvalue)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        actualresult = tdkTestObj.getResultDetails()
                                        if "FAILURE" not in actualresult:
                                            tdkTestObj.setResultStatus("SUCCESS")

                                            #Step 12: Revert the RFC parameter to its original value
                                            if len(actualvalue) == 0:
                                                print("\nINFO : Since the actual value of the "+rfcparameter+" RFC parameter is empty, therefore no revert action is required")
                                            else:
                                                print("\nRevert the RFC parameter to its original value")
                                                print("=====================================\n")
                                                tdkTestObj = obj.createTestStep('rfc_initializefeatures')
                                                tdkTestObj.addParameter("feature_name",feature_name)
                                                tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                                                tdkTestObj.addParameter("rfcparameter",rfcparameter)
                                                tdkTestObj.addParameter("XCONF_AUTHORIZATION_TOKEN_KEY",XCONF_AUTHORIZATION_TOKEN_KEY)
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
                                tdkTestObj.addParameter("XCONF_AUTHORIZATION_TOKEN_KEY",XCONF_AUTHORIZATION_TOKEN_KEY)
                                tdkTestObj.executeTestCase(expectedResult)
                                actualresult = tdkTestObj.getResultDetails()
                                if expectedResult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("\n")
                                    tdkTestObj = obj.createTestStep('rfc_deletefeature')
                                    tdkTestObj.addParameter("xconfdomainname",xconfdomainname)
                                    tdkTestObj.addParameter("XCONF_AUTHORIZATION_TOKEN_KEY",XCONF_AUTHORIZATION_TOKEN_KEY)
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
obj.unloadModule('rdkvxconfrfc')
