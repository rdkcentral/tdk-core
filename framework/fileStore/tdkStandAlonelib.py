##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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

import json
import importlib
import urllib.request, urllib.parse, urllib.error
import sys

# Description : Get the details of the device configured in test manager
# Parameters  : None
# Return Value: Return the device details like IP,Name,MAC,BoxType etc

def getDeviceDetails(self):
    url = self.url + '/deviceGroup/getDeviceDetails?deviceIp='+self.ip
    try:
        response = urllib.request.urlopen(url).read()
        deviceDetails = json.loads(response)
    except:
        print("Unable to get Device Details from REST !!!")
        exit()

    sys.stdout.flush()
    return deviceDetails

# Description : Get the thunder port details
# Parameters  : None
# Return Value: Return the thunder port

def getThunderPortDetails(self):
    url = self.url + '/deviceGroup/getThunderDevicePorts?stbIp='+self.ip
    try:
        data = urllib.request.urlopen(url).read()
        thunderPortDetails = json.loads(data)
    except:
        print("Unable to get Thunder Port from REST !!!")
        exit()

    sys.stdout.flush()
    return thunderPortDetails

def closePendingStep(test_case):
    if hasattr(test_case, "pendingStandaloneStep"):
        step_number, result = test_case.pendingStandaloneStep
        if "FAILURE" in str(result).upper():
            test_case.resultStatus = "FAILURE"
        print("\n[STEP %d END] Result: %s" % (step_number, result))
        sys.stdout.flush()
        del test_case.pendingStandaloneStep
        if hasattr(test_case, "pendingStandaloneStepObject"):
            del test_case.pendingStandaloneStepObject

#------------------------------------------------------------------------------
# Collapses any run of consecutive blank lines in stdout down to exactly one,
# so redundant blank-line prints scattered across scripts/libs don't create
# multi-line gaps around [STEP START]/[STEP END] banners.
#------------------------------------------------------------------------------
class _BlankLineCollapsingStream:
    def __init__(self, stream):
        self._stream = stream
        self._buffer = ""
        self._last_line_blank = False

    def write(self, data):
        if not data:
            return 0
        self._buffer += data
        parts = self._buffer.split("\n")
        self._buffer = parts[-1]
        out_chunks = []
        for line in parts[:-1]:
            is_blank = (line.rstrip("\r") == "")
            if is_blank and self._last_line_blank:
                continue
            out_chunks.append(line + "\n")
            self._last_line_blank = is_blank
        if out_chunks:
            self._stream.write("".join(out_chunks))
        return len(data)

    def flush(self):
        if self._buffer:
            self._stream.write(self._buffer)
            self._buffer = ""
        self._stream.flush()

    def __getattr__(self, name):
        return getattr(self._stream, name)

def _install_blank_line_collapsing():
    if not isinstance(sys.stdout, _BlankLineCollapsingStream):
        sys.stdout = _BlankLineCollapsingStream(sys.stdout)

# Description : To execute the stand alone tests
# Parameters  : None
# Return Value: Return the test status and details

def executeTest (self) :
    _install_blank_line_collapsing()
    executeJson = json.loads(self.jsonMsgValue)
    params = executeJson["params"]
    method = params["method"]
    componentName = params["module"]
    closePendingStep(self.parentTestCase)
    if not hasattr(self.parentTestCase, "standaloneStepCount"):
        self.parentTestCase.standaloneStepCount = 0
    self.parentTestCase.standaloneStepCount += 1
    step_number = self.parentTestCase.standaloneStepCount
    thunderPortDetails = getThunderPortDetails(self)
    thunderPort = thunderPortDetails["thunderPort"]

    if method == "TestMgr_RdkService_Test" :
        print("Executing %s...." % self.testCaseName)
        sys.stdout.flush()
        deviceInfo = getDeviceDetails(self);
        deviceName = deviceInfo["devicename"]
        deviceType = deviceInfo["boxtype"]
        deviceMac = ""
        try:
            deviceMac = deviceInfo["mac"]
        except Exception as e:
            print("\nException Occurred while getting MAC \n")
        testXMLName = params["params"]["xml_name"]
        details = "SUCCESS"
        lib = importlib.import_module("tdkvRDKServicesTestlib")
        executePluginTests_method = getattr(lib,"executePluginTests")
        result =  executePluginTests_method(self, self.ip, thunderPort, deviceName, deviceType, deviceMac, self.realpath, self.url, testXMLName)
    else:
        result = "FAILURE";
        #The library name will be componentName+lib. eg:rdkserviceslib
        module=componentName+"lib";
        """
        This is to import the module which is stored in a variable.
        Now "lib" contains all the function definitions in the imported module.
        """
        lib = importlib.import_module(module)
        args = {}
        if "params" in params:
            args = params["params"]
        step_description = method
        if "get_step_description" in dir(lib):
            try:
                # pass the calling script's suite name so libs can vary wording by caller (e.g. rdkv_media vs rdkv_performance)
                step_description = lib.get_step_description(method, args, self.parentTestCase.componentName)
            except TypeError:
                step_description = lib.get_step_description(method, args)
        print("\n#==============================================================================#")
        print("[STEP %d START] %s" % (step_number, step_description))
        print("#==============================================================================#")
        sys.stdout.flush()
        print("Executing %s...." % self.testCaseName)
        sys.stdout.flush()
        """
        The function 'init_method' helps to initialise the module with ip and port. User can use this function
        if they want ip/port in library.
        """
        if "init_module" in dir(lib):
            init_module_method = getattr(lib,"init_module")
            init_module_method(self,thunderPort,getDeviceDetails(self))
        """
        The variable "method" contains the name of the function we need to invoke from "lib".
        getattr is used to fetch the given method name from lib.
        This is because the method name is stored as a string in the variable.
        """
        method_to_call = getattr(lib, method)
        """
        The variable "args" contains all the arguments we need to pass to the method.
        This will be in the form of a dictionary(key:value pair).
        Keys are the argument name, values are the argument value.
        """
        details = method_to_call(**args)
        if isinstance(details , bytes):
            details = details.decode().encode('ascii','ignore').decode()
        if (details or details == None) and details != "EXCEPTION OCCURRED":
            result = "SUCCESS"
    if method != "TestMgr_RdkService_Test":
        self.parentTestCase.pendingStandaloneStep = (step_number, result)
        self.parentTestCase.pendingStandaloneStepObject = self
    return result,details;
