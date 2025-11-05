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
##########################################################################

# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_Telemetry","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Log_Upload_Validation');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result.upper());
expectedResult = "SUCCESS"

pre_requisite_set = False
if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('telemetry_deviceconfig_value')
    tdkTestObj.addParameter("basePath",obj.realpath)
    tdkTestObj.addParameter("configKey","Telemetry_Collector_URL")
    tdkTestObj.executeTestCase(expectedResult)
    details = tdkTestObj.getResultDetails()
    print("Details : ", details)
    details=details.replace("(","").replace(")","")
    print("D : ", details)
    details = details.split(",")
    Telemetry_Collector_URL = details[1]
    Telemetry_Collector_URL = str(Telemetry_Collector_URL).strip()
    print("Telemetry_Collector_URL : ",Telemetry_Collector_URL)
    dummy_url = details[2]
    print("Dummy_URL : ",dummy_url)
    if "SUCCESS" in details:
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        tdkTestObj.setResultStatus("FAILURE");        
if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('setPreRequisites')
    tdkTestObj.addParameter("Telemetry_Collector_URL",Telemetry_Collector_URL)
    tdkTestObj.executeTestCase(expectedResult);
    details = tdkTestObj.getResultDetails()

    if "SUCCESS" in details:
        print("PRE-REQUISITES SUCCESSFULLY SET")
        pre_requisite_set = True
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        print("Unable to set PRE-REQUISITES successfully")
        tdkTestObj.setResultStatus("FAILURE");

if pre_requisite_set:
    print("Check DCM process status")
    tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT');
    # Query systemctl and also check for a live dcmd process. Strip ANSI colors so greps work.    
    command = "systemctl status dcmd"
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase(expectedResult)
    details = tdkTestObj.getResultDetails()
    print("*" * 100)
    print("\n\n ", details)
    if "active" in details:
        print("DCM process is running in the device")
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("DCM process is not running in the device")
        tdkTestObj.setResultStatus("FAILURE")
        
    # Verify DCMresponse.txt exists under /opt/.t2persistentfolder
    tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')
    command = 'if [ -f /opt/.t2persistentfolder/DCMresponse.txt ]; then echo "DCM_RESPONSE_FOUND"; else echo "DCM_RESPONSE_NOT_FOUND"; fi'
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase(expectedResult)
    details = tdkTestObj.getResultDetails().strip()
    print("DCMresponse.txt check:", details)
    if "DCM_RESPONSE_FOUND" in details:
        tdkTestObj.setResultStatus("SUCCESS")

        # Verify /tmp/DCMSettings exists and is non-empty
        tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')
        command = 'if [ -s /tmp/DCMSettings ]; then echo "DCMSETTINGS_FOUND"; else echo "DCMSETTINGS_NOTFOUND_OR_EMPTY"; fi'
        tdkTestObj.addParameter("command", command)
        tdkTestObj.executeTestCase(expectedResult)
        details2 = tdkTestObj.getResultDetails().strip()
        print("/tmp/DCMSettings check:", details2)

        if "DCMSETTINGS_FOUND" in details2:
            tdkTestObj.setResultStatus("SUCCESS")
            # Check that values from DCMresponse.txt are present in /tmp/DCMSettings
            tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')
            # Split the DCMresponse.json on commas into potential tokens and grep those tokens against /tmp/DCMSettings
            command = "tr ',' '\\n' < /opt/.t2persistentfolder/DCMresponse.txt | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^{//' -e 's/}$//' | grep -F -f - /tmp/DCMSettings || true"
            tdkTestObj.addParameter("command", command)
            tdkTestObj.executeTestCase(expectedResult)
            matched = tdkTestObj.getResultDetails().strip()
            print("Lines/tokens from DCMresponse.txt found in /tmp/DCMSettings:\n", matched)

            if matched:
                print("Successfully DCMSettings contains entries from DCMresponse.txt")
                tdkTestObj.setResultStatus("SUCCESS")

                # Restart dcmd to ensure it picks up the new settings and check status
                tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')
                command = "systemctl restart dcmd && sleep 5 && systemctl status dcmd"
                tdkTestObj.addParameter("command", command)
                tdkTestObj.executeTestCase(expectedResult)
                status_details = tdkTestObj.getResultDetails()
                print("dcmd restart and status output:\n", status_details)
                if "active" in status_details:
                    print("DCM process restarted and is running -> SUCCESS")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("DCM process did not come up after restart -> FAILURE")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("DCMSettings does NOT contain entries from DCMresponse.txt -> DCM upload may fail")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("/tmp/DCMSettings missing or empty -> DCM upload will fail")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("DCMresponse.txt not found in /opt/.t2persistentfolder -> DCM upload will fail")
        tdkTestObj.setResultStatus("FAILURE")
        
obj.unloadModule("rdkv_Telemetry");
