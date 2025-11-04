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
import Vulkan_CTSVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("vulkan_cts","1",standAlone=True)

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Vulkan_CTS_INFO');

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedresult = "SUCCESS"

info_filename = "dEQP-VK.info"
qpa_file_name = "info.qpa"

if expectedresult in result.upper():
    tdkTestObj = obj.createTestStep('run_vulkan_cts_command')
    tdkTestObj.addParameter("info_filename", info_filename)
    tdkTestObj.executeTestCase(expectedresult)
    details = tdkTestObj.getResultDetails()
    
    print ("Vulkan CTS Info : %s" %details)

    qpa_folder_path= Vulkan_CTSVariables.qpa_folder_path
    result_dir = Vulkan_CTSVariables.result_dir

    tdkTestObj = obj.createTestStep('copy_file')
    tdkTestObj.addParameter("qpa_folder_path", qpa_folder_path)
    tdkTestObj.addParameter("qpa_file_name", qpa_file_name)
    tdkTestObj.addParameter("result_dir", result_dir)
    tdkTestObj.executeTestCase(expectedresult)
    result = tdkTestObj.getResultDetails()
    print ("Copy File Function Execution : %s" %result)
    
    if "SUCCESS" in result:
        print ("SUCCESS : QPA file copied from DUT to TDK Server")
        tdkTestObj.setResultStatus("SUCCESS")

        # Excel Report Generation
        tdkTestObj = obj.createTestStep('report_generation')
        tdkTestObj.addParameter("result_dir", result_dir)
        tdkTestObj.executeTestCase(expectedresult)
        result = tdkTestObj.getResultDetails()
        print ("Excel Report Generation : %s" %result)
        if "SUCCESS" in result:
            print ("SUCCESS : Excel report generated successfully")
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print ("FAILURE : Excel report generation failed")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print ("FAILURE : QPA file copy from DUT to TDK Server failed")
        tdkTestObj.setResultStatus("FAILURE")
obj.unloadModule("vulkan_cts");
