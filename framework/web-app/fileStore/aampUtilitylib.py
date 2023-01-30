#!/usr/bin/python
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
#########################################################################

#imports
import os
from ConfigParser import SafeConfigParser
Aamp_log_file='/opt/TDK/logs/AgentConsole.log'
##################################################################################
#
# To fetch the stream details from configuration file
#
# Syntax       : getAampTuneURL(obj,stream)
#
# Parameters   : obj, stream. (where stream  is the type of the stream URL to be fetcehd)
#
# Return Value : Stream URL for AAMP
#
####################################################################################

def getAampTuneURL(stream):
    parser = SafeConfigParser()
    # Fetching the stream details from configuration file
    parser.read( os.path.dirname(os.path.abspath(__file__))+'/Aamp_Tune_Config.ini')
    print "Parsing Aamp streams ..."
    if stream =="hlsstream":
        hlsstreamURL = parser.get('streams','HLS_stream')
        return hlsstreamURL
    elif stream =="livestream":
	livestreamURL = parser.get('streams','LIVE_stream')
	return livestreamURL
    elif stream =="mpdstream":
        mpdstreamURL = parser.get('streams','MPD_stream')
        return mpdstreamURL
    elif stream =="fogstream":
        fogstreamURL = parser.get('streams','FOG_stream')
        return fogstreamURL
    elif stream =="fogmpdstream":
        fogmpdstreamURL = parser.get('streams','FOG_MPD_stream')
        return fogmpdstreamURL
    else:
	return "no valid streams are available"
	

########## End of Function ##########

##################################################################################
#
# To get total number of valid URLs listed under "multistreams" section
#
# Syntax       : getIPStreamsCounts()
#
# Return Value : No.of URLS listed
#
####################################################################################
def getIPStreamsCounts():
        count = 0
        parser = SafeConfigParser()
        parser.read( os.path.dirname(os.path.abspath(__file__))+'/Aamp_Tune_Config.ini')
        section_name="multistreams"
        for name, value in parser.items(section_name):
                if value:
                        count += 1
        return count
########## End of Function ##########

##################################################################################
#
# To fetch the stream URL from "multistream" at given index
#
# Syntax       : getURLFromMultiStreamIndex(index)
#
# Parameters   : index. (index is an integer value pointing the position from where stream URL to be fetcehd)
#
# Return Value : Stream URL from the index
#
####################################################################################


def getURLFromMultiStreamIndex(index):
        count = 0
        parser = SafeConfigParser()
        parser.read( os.path.dirname(os.path.abspath(__file__))+'/Aamp_Tune_Config.ini')
        section_name="multistreams"
        for name, value in parser.items(section_name):
                if index == (count + 1):
                        if value:
                                return value
                else:
                        count += 1
        return "Failure: Invalid index... No URL is given in the specified index"

########## End of Function ##########

#####################################################################################
#
# Validate the events are logged or not
#
# Syntax       : searchAampEvents(obj,pattern)
#
# Parameters   : obj, pattern
#
# Return Value : Event status
#
#######################################################################################

def searchAampEvents(Obj, pattern):
    expectedresult = "SUCCESS"

    ####### Whenever checking for AAMP_EVENT_TUNED event, internally checking for AAMP TUNE FAILURE event for additional validation
    if pattern == "AAMP_EVENT_TUNED":
        print "Internally checking for AAMP TUNE FAILURE event for additional validation"
        temp_pattern = "AAMP_EVENT_TUNE_FAILED";
        tdkTestObj = Obj.createTestStep('ExecuteCommand');
        tdkTestObj.addParameter("command","grep -inr " +temp_pattern+" "+Aamp_log_file+"| grep -v grep | tr \"\n\" \"  \"")
        tdkTestObj.executeTestCase("SUCCESS");
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if temp_pattern in details:
            print "AAMP_EVENT_TUNE_FAILED event has occured due to AAMP Tune Failure"
            actualresult = "FAILURE";
            return actualresult;

    ####### Validate the events are logged or not
    tdkTestObj = Obj.createTestStep('ExecuteCommand');
    tdkTestObj.addParameter("command","grep -inr " +pattern+" "+Aamp_log_file+"| grep -v grep | tr \"\n\" \"  \"")
    tdkTestObj.executeTestCase("SUCCESS");
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if pattern in details:
        print "TEST STEP 1:  Validate the events are logged or not"
        print "EXPECTED RESULT 3: The events are logged"
        print "ACTUAL RESULT 3: Status: %s " %details
        print "[TEST EXECUTION RESULT] : SUCCESS";
        actualresult = "SUCCESS";
    else:
        print "TEST STEP 1:  Validate the events are logged or not"
        print "EXPECTED RESULT 3: the events are not logged"
        print "ACTUAL RESULT 3: Status: %s " %details
        print "[TEST EXECUTION RESULT] : FAILURE";
        actualresult = "FAILURE";
    return actualresult;
######### End of function ##########

##################################################################################
#
# To fetch the hls/mpd url by specifying the section and key 
#
# Syntax       : readFromConfig(section,key)
#
# Parameters   : section and key
#
# Return Value : Stream URL for AAMP
#
####################################################################################

def readFromConfig(section,key):
    parser = SafeConfigParser();
    parser.read( os.path.dirname(os.path.abspath(__file__))+'/Aamp_Tune_Config_TestSolution.ini')
    return parser.get(section,key);

######### End of function ##########

##################################################################################
#
# To rename the file to file.bak by specifying the path and filename
#
# Syntax       : readFromConfig(Obj,path,filename)
#
# Parameters   : Obj,path and filename
#
# Return Value : SUCCESS/FAILURE
#
####################################################################################


def fileRename(Obj,path,filename):
    Expected_Result = "SUCCESS"
    tdkTestObj = Obj.createTestStep('ExecuteCommand');
    tdkTestObj.addParameter("command","mv "+path+"/"+filename+" "+path+"/"+filename+'.bak')
    #Execute the test case in STB
    tdkTestObj.executeTestCase(Expected_Result);
    result = tdkTestObj.getResult();
    if Expected_Result in result:
        print "File rename is successful"
        actualresult = "SUCCESS";
    else:
        print "File rename is failure"
        actualresult = "FAILURE";

    return actualresult;

######### End of function ##########

##################################################################################
#
# To remove the file by specifying the path and filename
#
# Syntax       : fileRemove(Obj,path,filename)
#
# Parameters   : path and filename
#
# Return Value : SUCCESS/FAILURE
#
####################################################################################
def fileRemove(Obj,path,filename):
    Expected_Result = "SUCCESS"
    tdkTestObj = Obj.createTestStep('ExecuteCommand');
    tdkTestObj.addParameter("command","rm "+path+"/"+filename)
    #Execute the test case in STB
    tdkTestObj.executeTestCase(Expected_Result);
    result = tdkTestObj.getResult();
    if Expected_Result in result:
        print "File removal is successful"
        actualresult = "SUCCESS";
    else:
        print "File removal is failure"
        actualresult = "FAILURE";

    return actualresult;

######### End of function ##########

##################################################################################
#
# To Revert the file to original file by specifying the path and filename
#
# Syntax       : fileRevert(Obj,path,filename)
#
# Parameters   : Obj,path,filename
#
# Return Value : SUCCESS/FAILURE
#
####################################################################################

def fileRevert(Obj,path,filename):
    Expected_Result = "SUCCESS"
    tdkTestObj = Obj.createTestStep('ExecuteCommand');
    tdkTestObj.addParameter("command","mv "+path+"/"+filename+'.bak'+" "+path+"/"+filename)
    #Execute the test case in STB
    tdkTestObj.executeTestCase(Expected_Result);
    result = tdkTestObj.getResult();
    if Expected_Result in result:
        print "File name reverting is successful"
        actualresult = "SUCCESS";
    else:
        print "Couldn't revert file name"
        actualresult = "FAILURE";

    return actualresult;

######### End of function ##########

##################################################################################
#
# To Create a file by specifying the path and filename
#
# Syntax       : fileCreate(Obj,path,filename)
#
# Parameters   : Obj,path,filename
#
# Return Value : SUCCESS/FAILURE
#
####################################################################################

def fileCreate(Obj,path,filename):
    Expected_Result = "SUCCESS"
    tdkTestObj = Obj.createTestStep('ExecuteCommand');
    tdkTestObj.addParameter("command","touch "+path+"/"+filename)
    #Execute the test case in STB
    tdkTestObj.executeTestCase(Expected_Result);
    result = tdkTestObj.getResult();
    if Expected_Result in result:
        print "File created reverting is successful"
        actualresult = "SUCCESS";
    else:
        print "Couldn't revert file name"
        actualresult = "FAILURE";

    return actualresult;

######### End of function ##########

##################################################################################
#
# To write a text to a specified file
#
# Syntax       : Writetofile(Obj,text,filename)
#
# Parameters   : Obj,text,filename
#
# Return Value : SUCCESS/FAILURE
#
####################################################################################

def Writetofile(Obj,text,filename):
    Expected_Result = "SUCCESS"
    tdkTestObj = Obj.createTestStep('ExecuteCommand');
    tdkTestObj.addParameter("command","echo "+text+" > "+filename)
    #Execute the test case in STB
    tdkTestObj.executeTestCase(Expected_Result);
    result = tdkTestObj.getResult();
    if Expected_Result in result:
        print "File writing is successful"
        actualresult = "SUCCESS";
    else:
        print "Writing is failure"
        actualresult = "FAILURE";

    return actualresult;

######### End of function ##########

