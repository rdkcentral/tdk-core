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
import ast
import time
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_appmanagers","1",standAlone=True)

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_AppManagers_Functional_Launch_App_After_Uninstall')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)

obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

# Predefined variables which will be used in the script
launch_status = "FALSE"

if "SUCCESS" in result.upper():
    # Step 1 : Get the device configuration values
    configkeylist = ["PACKAGEMANAGER_APPLICATION_NAME"]
    tdkTestObj = obj.createTestStep('appmanagers_getdeviceconfig')
    tdkTestObj.addParameter("configkeylist",configkeylist)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
    result = ast.literal_eval(result)
    application_name = result[0]["PACKAGEMANAGER_APPLICATION_NAME"]
    if "SUCCESS" in result[1]:
        tdkTestObj.setResultStatus("SUCCESS")
        
        # Step 2 : Check the status of the dependent plugins
        print("\n")
        pluginlist = ["org.rdk.AppManager", "org.rdk.PackageManagerRDKEMS"]
        tdkTestObj = obj.createTestStep('appmanagers_checkpluginstatus')
        tdkTestObj.addParameter("pluginlist",pluginlist)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS")
            
            # Step 3 : Check whether the package is already installed if installed proceed with uninstallation step
            print("\n")
            time.sleep(3)
            method = "org.rdk.AppManager.1.isInstalled"
            value = '{"appId": "'+application_name+'"}'
            tdkTestObj = obj.createTestStep('appmanagers_setvalue')
            tdkTestObj.addParameter("method",method)
            tdkTestObj.addParameter("value",value)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            result = ast.literal_eval(result)
            if "error" in result and "result" not in result:
                print("FAILURE : Failed to get the installation status of the package")
                tdkTestObj.setResultStatus("FAILURE")
            if "error" not in result and "result" in result and result["result"] == True:
                tdkTestObj.setResultStatus("SUCCESS")
                print("INFO : Package is already installed, proceeding with uninstallation step")
                # Step 4 : Uninstall the package
                print("\n")
                time.sleep(3)
                method = "org.rdk.PackageManagerRDKEMS.1.uninstall"
                value = '{"packageId": "'+application_name+'"}'
                tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                tdkTestObj.addParameter("method",method)
                tdkTestObj.addParameter("value",value)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResultDetails()
                result = ast.literal_eval(result)
                if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                    print("SUCCESS : Application Uninstallation initiated successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                    launch_status = "TRUE"
                else:
                    print("FAILURE : Failed to initiate application uninstallation")
                    tdkTestObj.setResultStatus("FAILURE")
            if "error" not in result and "result" in result and result["result"] == False:
                tdkTestObj.setResultStatus("SUCCESS")
                print("INFO : Package is not installed, proceeding with launch step")
                launch_status = "TRUE"
            
            if launch_status == "TRUE":
                # Step 5 : Launch the application without installing the package and check for failure
                print("\n")
                time.sleep(3)
                method = "org.rdk.AppManager.1.launchApp"
                value = '{"appId": "'+application_name+'"}'
                tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                tdkTestObj.addParameter("method",method)
                tdkTestObj.addParameter("value",value)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResultDetails()
                result = ast.literal_eval(result)
                if "error" in result and "message" in result["error"]:
                    message_value = result["error"]["message"]
                    if message_value == "ERROR_GENERAL":
                        print("SUCCESS : Launching the application failed as expected since the application is uninstalled")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("FAILURE : Launching the application failed with unexpected error message: %s" %message_value)
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("FAILURE : Launching the application succeeded even after uninstallation or application is not present")
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
else:
    print("FAILURE : Module Loading Status Failure\n")
    obj.setLoadModuleStatus("FAILURE")

# Unload the module
print("\n")
obj.unloadModule("rdkv_appmanagers")
