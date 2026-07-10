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
import tdklib; 
import re

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Graphics","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Graphics_vulkaninfo');

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"

mandatory_strings = [
    "VK_KHR_wayland_surface",
    "VK_KHR_surface",
    "VK_KHR_get_surface_capabilities2",
    "deviceName",
    "deviceType",
    "driverID",
    "driverName",
    "VK_KHR_swapchain",
    "QUEUE_GRAPHICS",
    "QUEUE_COMPUTE",
    "QUEUE_TRANSFER",
    "MEMORY_HEAP_DEVICE_LOCAL_BIT",
    "MEMORY_PROPERTY_HOST_VISIBLE_BIT",
    "MEMORY_PROPERTY_HOST_COHERENT_BIT",
    "samplerAnisotropy                       = true",
    "textureCompressionETC2                  = true",
    "textureCompressionASTC_LDR              = true",
    "fragmentStoresAndAtomics                = true",
]
min_version = (1, 1, 0)

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('execute_Cmnd_InDUT')
    command = "XDG_RUNTIME_DIR=/tmp ; vulkaninfo "
    print("Executing command in DUT: ", command)
    tdkTestObj.addParameter("command",command)
    tdkTestObj.executeTestCase(expectedResult);

    output = tdkTestObj.getResultDetails()
    if not output:
        print ("FAILURE : No output was obtained from vulkaninfo")
        tdkTestObj.setResultStatus("FAILURE")
    else:
        print(output)
        tdkTestObj.setResultStatus("SUCCESS")

        # --- Instance version (loader/ICD level) ---
        instance_match = re.search(r"Vulkan Instance Version:\s*(\d+)\.(\d+)\.(\d+)", output)
        if instance_match:
            instance_version = tuple(int(x) for x in instance_match.groups())
            print(f"Instance Version found: {'.'.join(instance_match.groups())}")
        else:
            instance_version = None
            print("FAILURE: could not find Vulkan Instance Version string")
            tdkTestObj.setResultStatus("FAILURE")

        # --- Device apiVersion ---
        api_match = re.search(r"apiVersion\s*=\s*(?:\d+\s*)?\(?(\d+)\.(\d+)\.(\d+)\)?", output)
        if api_match:
            api_version = tuple(int(x) for x in api_match.groups())
            api_version_str = ".".join(api_match.groups())
            print(f"Device apiVersion found: {api_version_str}")

            if api_version >= min_version:
                print(f"SUCCESS: device apiVersion {api_version_str} >= minimum required {'.'.join(map(str, min_version))}")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print(f"FAILURE: device apiVersion {api_version_str} < minimum required {'.'.join(map(str, min_version))}")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("FAILURE: could not find device apiVersion string")
            tdkTestObj.setResultStatus("FAILURE")
       
        # vulkaninfo output verification
        missing = [s for s in mandatory_strings if s not in output]
        if missing:
           print(f"FAILURE: {len(missing)} mandatory string(s) missing in vulkaninfo output:")
           tdkTestObj.setResultStatus("FAILURE")
           for s in missing:
              print(f"  - {s}")
        else:
           print("SUCCESS: vulkaninfo output obtained successfully")
           tdkTestObj.setResultStatus("SUCCESS")

obj.unloadModule("Graphics");
