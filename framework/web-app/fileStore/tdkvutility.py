#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
#

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Generic method to execute testcase
# executeTest

# Syntax      : executeTest(obj, testcase, {"key1":"value1", " key2":"value2"})
# Description : Function to generically execute testcase for any module object
# Parameters  : obj - module object
#             : testcase - primitve test to be executed
#             : params - parameters to be added to primitve test
#             : returnObject - True/False based on whether to return the tdkTestObj  
# Return Value: True,details,tdkTestObj(on success), False,details,tdkTestObj(on failure)

def executeTest(obj, testcase , params="", returnObject = False):
    tdkTestObj = obj.createTestStep(testcase);
    expectedresult="SUCCESS"
    if len(params) and "no parameters" not in params:
        for i in range(0,len(params)):
            element = params.keys()[i]
            tdkTestObj.addParameter(element,params[element]);
    #Execute the test case in DUT
    tdkTestObj.executeTestCase("SUCCESS");
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if actualResult == expectedresult:
        print "%s SUCCESS"%testcase
        tdkTestObj.setResultStatus("SUCCESS");
        if returnObject:
            return True,details,tdkTestObj
        return True,details
    else:
        print "%s FAILURE"%testcase
        tdkTestObj.setResultStatus("FAILURE")
        if returnObject:
            return False,details,tdkTestObj
        return False,details

# Method to read a larger file and display in script log
# readBigFile

# Syntax      : readBigFile(obj, fileName)
# Description : Function to generically execute testcase for any module object
# Parameters  : obj - module object
#             : filename - file to be read
#             : returnObject - message based on whether to return the tdkTestObj  
# Return Value: message

def readBigFile(obj, fileName):
    message = ""
    bufferlength = 490
    readbyte = bufferlength
    cutbyte = 0
    tdkTestObj = obj.createTestStep('ExecuteCommand')
    expectedResult = "SUCCESS"
    print " Reading File ",str(fileName)
    while (True):
        command = "dd if=" + str(fileName) + " bs=1 skip=" + str(cutbyte) + " count=" + str(readbyte) + " > /tmp/output.txt; cat /tmp/output.txt "
        tdkTestObj.addParameter("command", command)
        tdkTestObj.executeTestCase(expectedResult)
        actualResult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        if actualResult == expectedResult:
            message = message + details
            cutbyte = cutbyte + bufferlength
            if len(details) < bufferlength:
                break;
        else:
            print "File Read FAILURE"
            tdkTestObj.setResultStatus("FAILURE")
            return message;
    print "File Read SUCCESS"
    message = message.replace(r'\n', '\n');
    tdkTestObj.setResultStatus("SUCCESS");
    return message
