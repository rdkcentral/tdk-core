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
  <name>RDKV_Container_Dobby_Tests</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>containerization_executeDobbyTest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To test the youtube container with dobby security tool</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <test_case_id>Containerization_01</test_case_id>
    <test_objective>To test the youtube container with dobby security tool</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator,RDKTV</test_setup>
    <pre_requisite>1. Configure the values SSH Method (variable $SSH_METHOD), DUT username (variable $SSH_USERNAME)and password of the DUT (variable $SSH_PASSWORD)  available in fileStore/tdkvRDKServiceConfig/device.config file</pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1.Clone the Dobby security tool in Test Manager and copy the tool to DUT
    2. Enable the corresponding tr181 parameter for cobalt
    3. Launch the Cobalt application through RDKShell
    4. Check whether Cobalt container is running
    5. Run the tests using Dobby security tool
    6. PASS/FAIL the test based on the each test response from dobby security tool</automation_approch>
    <expected_output>Tests ran using dobby security tool on Cobalt container should get PASS</expected_output>
    <priority>High</priority>
    <test_stub_interface>containerization</test_stub_interface>
    <test_script>RDKV_Container_Dobby_Tests</test_script>
    <skipped>No</skipped>
    <release_version>M109</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("containerization","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Container_Dobby_Tests');
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result.upper());
expectedResult = "SUCCESS"

print("\n####################################################################################")
print("            PLUGIN NAME :  CONTAINERIZATION_DOBBY_TESTS")
print("####################################################################################")


testCases = ["01-Check_Dobby_Daemon_User_Permission-2.1","02-Check_Logging_Level-2.3","03-Check_User_Namespace_Support-2.9","04-Check_Custom_Seccomp_Profile-2.17","05-Check_Dobby_Service_Ownership-3.1","06-Check_Dobby_Service_File_Permissions-3.2","07-Check_DobbyPty_File_Ownership-3.3","08-Check_DobbyPty_File_Permissions-3.4","09-Check_Dobby_Json_File_Ownership-3.17","10-Check_Dobby_Json_File_Permissions-3.18","11-Check_Container_User_Created-4.1","12-Check_Executable_Permissions_Removed-4.8","13-Check_AppArmor_Profile_Enabled-5.1","14-Check_Linux_Kernel_Capabilities-5.3","15-Check_Host_System_Directories-5.5","16-Check_Host_Network_Namespace-5.9","17-Check_Container_Memory_Usage-5.10","18-Check_CPU_Priority-5.11","19-Check_Container_Root_Filesystem-5.12","20-Check_TMP_Partition-5.12.1","21-Check_Container_Rootfs_Directory-5.12.2","22-Check_Rootfs_Propagation-5.12.4","23-Check_Host_Process_Namespace-5.15","24-Check_Host_Devices_Status-5.17","25-Check_Host_UTS_Namespace-5.20","26-Check_Mount_Namespace_Enabled-5.20.1","27-Check_Seccomp_Profile_Enabled-5.21","28-Check_Cgroup_Status-5.24","29-Check_GPU_Cgroup_Status-5.24.1","30-Check_PIDs_Cgroup-5.28","31-Check_Dobby_Default_Bridge-5.29","32-Check_Dobby_Socket-5.31","33-Check_NoNEW_Privileges-5.32"]
manualTestCases = ["34-CHECK_DOBBY_VERSION","35-Check_Dev_Loop_Partition_Status"]
print("\nPLUGIN TOTAL TEST CASES: ",len(testCases)+len(manualTestCases))
datamodel=["Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Dobby.Cobalt.Enable","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Dobby.WPE.Enable"]

print("\n\n#---------------------------- Plugin Pre-requisite ----------------------------#")
print("\nPre Requisite : Cloning_Dobby_Security_Tool\nPre Requisite No : 1")
tdkTestObj = obj.createTestStep('containerization_cloneDobby')
tdkTestObj.addParameter("basePath",obj.realpath)
tdkTestObj.executeTestCase(expectedResult)
actualresult = tdkTestObj.getResultDetails()
if expectedResult in actualresult.upper():
    tdkTestObj.setResultStatus("SUCCESS")
    print("\n#--------- [Pre-requisite Status] : %s ----------#"%(actualresult))
    print("\nPre Requisite : Enabling_Datamodel\nPre Requisite No : 2")
    tdkTestObj = obj.createTestStep('containerization_setPreRequisites')
    tdkTestObj.addParameter("datamodel",datamodel)
    tdkTestObj.executeTestCase(expectedResult)
    actualresult= tdkTestObj.getResultDetails()
    if expectedResult in actualresult.upper():
        tdkTestObj.setResultStatus("SUCCESS")
        print("\n#--------- [Pre-requisite Status] : %s ----------#"%(actualresult))

        print("\nPre Requisite : Launch_the_Application\nPre Requisite No : 3")
        tdkTestObj = obj.createTestStep('containerization_getDeviceConfig')
        tdkTestObj.addParameter("basePath",obj.realpath)
        tdkTestObj.addParameter("configKey","DOBBY_APPLICATION_DETAILS")
        tdkTestObj.executeTestCase(expectedResult)
        DOBBY_APPLICATION_DETAILS = tdkTestObj.getResultDetails()
        print(DOBBY_APPLICATION_DETAILS)
        tdkTestObj = obj.createTestStep('containerization_launchApplication')
        tdkTestObj.addParameter("launch",DOBBY_APPLICATION_DETAILS)
        tdkTestObj.executeTestCase(expectedResult)
        actualresult = tdkTestObj.getResultDetails()
        if expectedResult in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS")
            print("\n#--------- [Pre-requisite Status] : %s ----------#"%(actualresult))

            print("\nPre Requisite :Check_the_Container_Running_State\nPre Requisite No : 4")
            tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
            tdkTestObj.addParameter("callsign",DOBBY_APPLICATION_DETAILS)
            tdkTestObj.executeTestCase(expectedResult)
            actualresult = tdkTestObj.getResultDetails()
            if expectedResult in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS")
                print("\n#--------- [Pre-requisite Status] : %s ----------#\n"%(actualresult))
                print("Plugin Pre-requisite Status: %s \n\n"%(actualresult))

                tdkTestObj = obj.createTestStep('containerization_executeDobbyTest')
                tdkTestObj.addParameter("containername",DOBBY_APPLICATION_DETAILS)
                tdkTestObj.addParameter("testCases",testCases)
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")

                tdkTestObj = obj.createTestStep('containerization_checkDobbyVersion')
                tdkTestObj.addParameter("testCase",manualTestCases[0])
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                tdkTestObj = obj.createTestStep('containerization_checkDevLoopPartition')
                tdkTestObj.addParameter("testCase",manualTestCases[1])
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("\n#--------- [Pre-requisite Status] : %s ----------#"%(actualresult))
                print("Plugin Pre-requisite Status: %s \n\n"%(actualresult))
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("\n#--------- [Pre-requisite Status] : %s ----------#"%(actualresult))
            print("Plugin Pre-requisite Status: %s \n\n"%(actualresult))
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("\n#--------- [Pre-requisite Status] : %s ----------#"%(actualresult))
        print("Plugin Pre-requisite Status: %s \n\n"%(actualresult))
else:
    tdkTestObj.setResultStatus("FAILURE")
    print("\n#--------- [Pre-requisite Status] : %s ----------#"%(actualresult))
    print("Plugin Pre-requisite Status: %s \n\n"%(actualresult))


print("\n\n#---------------------------- Plugin Post-requisite ----------------------------#")
print("\nPost Requisite :Disabling_Datamodel\nPost Requisite No : 1")
tdkTestObj = obj.createTestStep('containerization_setPostRequisites')
tdkTestObj.addParameter("datamodel",datamodel)
tdkTestObj.executeTestCase(expectedResult)
actualresult = tdkTestObj.getResultDetails()
if expectedResult in actualresult.upper():
    tdkTestObj.setResultStatus("SUCCESS")
    print("\n#--------- [Post-requisite Status] : %s ----------#"%(actualresult))
    print("Plugin Post-requisite Status: %s \n\n"%(actualresult))
else:
    tdkTestObj.setResultStatus("FAILURE")
    print("\n#--------- [Post-requisite Status] : %s  ----------#"%(actualresult))
    print("Plugin Post-requisite Status: %s \n\n"%(actualresult))

obj.unloadModule("containerization");
