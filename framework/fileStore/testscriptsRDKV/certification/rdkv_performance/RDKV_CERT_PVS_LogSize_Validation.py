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
  <version>109</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_LogSize_Validation</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getSSHParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to find if any log size is greater than threshold log rotate size value.</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_144</test_case_id>
    <test_objective>The objective of this test is to find if any log size is greater than threshold log rotate size value. </test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.Generic log rotate size limit</input_parameters>
    <automation_approch>1.Get list of all log files present in /opt/log folder.
2. Compare whether their size is with in threshold size limt.
3.List out all the log files whose size is greater than threshold limit
4.Compare those files with their logRotate values that are defined in /etc/logrotate.properties file</automation_approch>
    <expected_output>All logs file  sizes should be with in threshold size limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_LogSize_Validation</test_script>
    <skipped>No</skipped>
    <release_version>M123</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import json
from rdkv_performancelib import *
from StabilityTestUtility import *
import PerformanceTestVariables
import rdkv_performancelib
from web_socket_util import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_LogSize_Validation');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)
conf_file, status = get_configfile_name(obj);
result, size_limit = getDeviceConfigKeyValue(conf_file,"SIZE_LIMIT")
expectedResult = "SUCCESS"
print("size_limit ", size_limit)
size_limit = eval(size_limit)
size_limit = int(size_limit);
if expectedResult in result.upper():
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if ssh_param_dict != {} and expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print("\n Getting the size of each log file from /opt/logs \n")
        #Command to get the logfiles output
        command = 'cd /opt/logs && du -sh *.{txt,log} '
        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        output = tdkTestObj.getResultDetails()
        output = output.strip().split('\n')
        print(output)
        #Log size conversion
        units = {'K': 1024, 'M': 1024**2, 'G': 1024**3}
        logfiles_name =[]
        large_file_list=[]
        log_file_count=0
        log_file_value=[]
        log_value_pairs_list =[]
        #Finding the no of files present inside /opt/logs folder
        for line in output:
            if line.startswith('cd /opt/logs') or not line.strip():
               continue
            if "Structure needs cleaning" in line:
               continue
            try:
                 size_str, file_name = line.strip('\r').split('\t')
                 size_str = size_str.strip()  # Remove any leading/trailing whitespace
                 file_name = file_name.strip()
            except ValueError as e:
                 print(f"Error splitting line: {line}. Error: {e}")
                 continue
            if size_str == '0':
               continue
            try:
                number, unit = size_str[:-1], size_str[-1]
                # Check if 'number' is not empty and 'unit' is one of the expected units
                if number and unit.upper() in units:
                   size_bytes = int(float(number) * units[unit.upper()])
                   log_file_count += 1
                else:
                   raise ValueError("Invalid size or unit")
            except ValueError as e:
                print(f"Error converting size to float: {size_str}. Error: {e}")
                continue
            #Finding the total no of files that have file size more than threshold value
            if size_bytes > size_limit:
                print("The size of the  "+file_name +" file exceeds " + str(size_limit))
                logfiles_name.append(file_name)
                log_file_value.append(size_bytes)
                #Saving the logfiles and their values in to a key-value pair dictionary
                log_value_pairs_list = { k:v for (k,v) in zip(logfiles_name, log_file_value)}
        print("\n Iterating through each log file that is greater than threshold limit to check if the log file has any configurations specified in /etc/logRotate.properties file\n")
        for logfile in logfiles_name:
            large_file_name = logfile.split('_')[0].split('.')[0]
            large_file_list.append(large_file_name)
            command = 'grep -inr "'+large_file_name+'" /etc/logRotate.properties | grep RotateSize | sed -n "s/.*:\\(.*\\)=.*/\\1/p" | head -n 1  | tr -d " "'
            print(command)
            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
            tdkTestObj.addParameter("command",command)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails()
            logRotateSize_index = details.find('\n')
            newDetails = details[logRotateSize_index + 1:]
            # Remove non-printable characters using a list comprehension
            log_rotate_string = ''.join(c for c in newDetails if c.isprintable())
            #Confirm the output of grep command i.e, log_rotate_string is not empty
            if log_rotate_string:
               print("\n Grepping the logRotate string actual value \n")
               command = 'source /etc/logRotate.properties && echo $'+log_rotate_string
               print(command)
               tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
               tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
               tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
               tdkTestObj.addParameter("command",command)
               tdkTestObj.executeTestCase(expectedResult)
               result = tdkTestObj.getResult()
               details = tdkTestObj.getResultDetails()
               logRotateSize_index = details.find('\n')
               log_rotate_value = details[logRotateSize_index + 1:].strip()
               # Fetching the original log size value
               value = log_value_pairs_list[logfile]
               if log_rotate_value:
                  log_rotate_value = int(log_rotate_value)
                  print("\n Comparing original value with log rotate value\n")
                  if  value >log_rotate_value:
                      print(f"Failure: {logfile} has a value greater than log_rotate_value.")
                      tdkTestObj.setResultStatus("FAILURE")
                  else:
                      print (f"Success: {logfile} has a value less than log_rotate_value")
                      tdkTestObj.setResultStatus("SUCCESS")
               else:
                   print(f"Failure: {logfile} has a empty log_rotate_value ")
                   tdkTestObj.setResultStatus("FAILURE")
            else:
               large_file_list.append(logfile)
               print("%s is not with in threshold limit"%(logfile))
               tdkTestObj.setResultStatus("FAILURE")
        print("\n #############Execution Summary##########")
        print("\n Total number of files that are greater than log size \t"+ str(size_limit)+" are: "+ str(len(logfiles_name)))
        print("\n Total no of files present inside /opt/logs folder are : \n",log_file_count)
        print("\n List of files that are more than threshold limit are : \n",log_value_pairs_list)
    else:
        print("\n Please configure the SSH details in configuration file \n")
        tdkTestObj.setResultStatus("FAILURE")
        obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
