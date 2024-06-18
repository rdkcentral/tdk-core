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
#########################################################################
from rdkv_performancelib import *
import FireCertAppTestVariables

deviceIP=""
devicePort=""
deviceMac=""
realpath=""
reportID=""
deviceName=""
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module(libobj,port,deviceInfo):
    global deviceIP
    global devicePort
    global libObj
    global realpath
    global deviceMac
    global reportID
    deviceIP = libobj.ip;
    devicePort = port
    libObj = libobj
    deviceName = deviceInfo["devicename"]
    reportID='{}_{}'.format(deviceName,str(libObj.execID))
    try:
        deviceMac = deviceInfo["mac"]
    except Exception as e:
       print ("\nException Occurred while getting MAC \n")
       print (e)
#---------------------------------------------------------------
#FUNCTION CREATE FCA URL
#---------------------------------------------------------------
def rdkv_firecertapp_createURL(url_type):
    mac = deviceMac.replace(":","").lower()
    if url_type == "fca_test_url":
        url =  FireCertAppTestVariables.fca_app_url + "&reportingId="+reportID+"&__firebolt_endpoint=ws%3A%2F%2F127.0.0.1%3A3474%3FappId%3Drefui%26session%3Drefui"
    elif url_type == "fca_report":
        url = download_fca_report()
    return url
#---------------------------------------------------------------
#FUNCTION TO EXECUTE TESTS IN FCA APP
#---------------------------------------------------------------
def rdkv_firecertapp_execute(sequence):
    sequence = sequence.split(",")
    param = ''
    for code in sequence:
        if sequence.index(code) == len(sequence)-1:
            param = param + '{"keyCode":'+code + ',"modifiers": [],"delay":1.0}'
        else:
            param = param + '{"keyCode":'+code + ',"modifiers": [],"delay":1.0},'
    params = '{"keys":[ ' + param + ' ]}'
    print (params)
    result = rdkservice_setValue("org.rdk.RDKShell.1.generateKey",params)
    print (result)
    if 'True' in str(result):
        print ("Successfully navigated through FCA app and started the test")
        result = "SUCCESS"
    else:
        print ("Failed to navigate through FCA app to start the test")
        result = "FAILURE"
    return result

#-----------------------------------------------------------------
#DOWNLOAD THE REPORT FROM SERVER
#-----------------------------------------------------------------
def download_fca_report():
    server_url = FireCertAppTestVariables.fca_report_url
    filename_start=reportID
    filename_extension=".xlsx"
    download_path = '{}{}_{}_{}'.format(libObj.logpath,str(libObj.execID),str(libObj.execDevId),str(libObj.resultId))
    status = "FAILURE"

    response = requests.get(server_url)
    if response.status_code == 200:
        files = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
        files = [file.split('/')[-1] for file in files]
        # Filter filenames based on starting part and extension
        matching_files = [filename for filename in files if filename.startswith(filename_start) and filename.endswith(filename_extension)]
        if matching_files:
            file_to_download = matching_files[0]
            download_url = os.path.join(server_url, file_to_download)
            response = requests.get(download_url)
            if response.status_code == 200:
                #download_file_path = os.path.join(download_path, file_to_download)
                download_file_path = download_path+"_"+file_to_download
                with open(download_file_path, 'wb') as f:
                    f.write(response.content)
                print("File downloaded successfully to:", download_file_path)
                status = "SUCCESS"
            else:
                print("Failed to download file:", response.status_code)
        else:
            print("No matching files found.")
    else:
        print("Failed to get directory listing:", response.status_code)
    return status
