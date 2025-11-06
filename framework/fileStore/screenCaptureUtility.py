#!/usr/bin/python
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
import websocket
import json
import sys
import time
import threading
import subprocess
import saveAsPng
import socket
import os
from datetime import datetime
from time import sleep
import cv2
from configparser import SafeConfigParser
import numpy as np
from pytesseract import *

try:
    import thread
except ImportError:
    import _thread as thread

TIMEOUT=0
event=""
snapCount=0
snapList=[]
snaps=0
image_name=""
ws = None
encoded_data=""
previous_image_path=""
extracted_text=""
already_extracted=False
registerEventThread=""
screen_capture_mechanism=""
upload_to_cgi="FaILURE"

#Configure Thunderport for Execution
THUNDERPORT=0

########################################################################
#
# Method to set Thunder Port for execution of RDKServices curl commands
#
#########################################################################
def setThunderPort(thunderPort):
    global THUNDERPORT
    THUNDERPORT=thunderPort

#############################################################
#
# Method to process event(message) received on websocket(ws)
#
#  Method processes the onScreenshotComplete received on ws
#  Writes the base-64 encoded data into encoded_data variable
#  Once all required SNAPS are captured kills the thread
#
#  ws      : websocket instance
#  message : event received on ws
#############################################################
def on_message(ws, message):
    global snapCount
    global screen_capture_mechanism
    global snapList
    global snaps
    current_time=datetime.now().strftime("%H:%M:%S")
    if screen_capture_mechanism == "screencaptureservice":
        data = json.loads(message)
        snapCount= snapCount + 1
        print("Received uploadComplete for snap count %d event at %s "%(snapCount,current_time))
        global upload_to_cgi
        if (((data["params"]["message"]).lower() == "success" ) and ((data["params"]["status"]) == True )):
            upload_to_cgi = "SUCCESS"
            snapList.append(snapCount)
            print("SNAPS COMPLETED: %d/%d"%(snapCount,snaps))
        else:
            upload_to_cgi = "FAILURE"
    elif screen_capture_mechanism == "rdkshell":
        start = time.time()
        snapCount= snapCount + 1
        dataPath = snapCount
        global encoded_data
        data = json.loads(message)
        encoded_data = data["params"]["imageData"]
        with open("rdkshell_data.txt","w") as file:
            file.write(encoded_data)
        if not encoded_data:
            print("FAILURE : Not enough image data")
            ws.close()
            print("thread terminating...")
        print("Received onScreenshotComplete for snap count %d event at %s "%(snapCount,current_time))
        snapList.append(snapCount)
        print("SNAPS COMPLETED: %d/%d"%(snapCount,snaps))
    if snapCount == snaps:
        ws.close()
        print("thread terminating...")

#############################################################
#
# Method to print any error in websocket(ws)
#
#  ws      : websocket instance
#  error   : error received on websocket
#############################################################
def on_error(ws, error):
    print(error)

#############################################################
#
# Method to signal closure of websocket instance
#
#  ws      : websocket instance
#############################################################
def on_close(ws):
    print("### closed ###")

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

#############################################################
#
# Method to start websocket instance
#
#  Method registers for event on RDKShell plugin
#
#  ws      : websocket instance
#############################################################
def on_open(ws):
    def run(*args):
        global event
        if event == "onScreenshotComplete":
            service = "org.rdk.RDKShell.1"
        elif event == "uploadComplete":
            service = "org.rdk.ScreenCapture"
        else:
            service = "unknown"
        event_jsonrpc = '{"jsonrpc": "2.0","id": 5,"method": "' + service + '.register","params": {"event": "' + str(event) + '", "id": "client.events.1" }}'
        print ("Registering for event :",event)
        print (event_jsonrpc)
        events = [event_jsonrpc]
        for event in events :
            time.sleep(1)
            ws.send(event)
        time.sleep(1)
    thread.start_new_thread(run, ())

#############################################################
#
# Method to instance and start websocket instance
#
#  Method registers for event for the DUT IP
#
#  DUT_IP  : IP of device to be tested
#  event_  : event to get registered (onScreenshotComplete)
#############################################################
def registerEvent(DUT_IP,event_):
    global event
    event=event_
    global THUNDERPORT
    ws_rpc = "ws://"+DUT_IP+":" + str(THUNDERPORT) + "/jsonrpc"
    print(str(ws_rpc))
    global ws
    ws = websocket.WebSocketApp(str(ws_rpc),
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.run_forever()

#############################################################
#
# Method to execute command on the linux environment
#
#  command  : command to be executed
#############################################################
def triggerCommand(command,debug=True):
    print("Executing command: ",command)
    output = subprocess.getoutput(command)
    if debug:
        print(output)
    return output

#############################################################
#
# Method to check if device is accessible via port
#
#  ip    : IP of the device to be checked
#  port  : PORT of the device to be tested (THUNDERPORT)
#############################################################
def CheckDeviceStatus(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout=3
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

##################################################################
#
# Method to start a thread for listening websocket for the device
#
#  IP   : IP of the device to be listening
##################################################################
def registerEvent_(IP,event):
    registerEventThread = threading.Thread(target=registerEvent, name="WebsocketEvent", args=(IP,event,))
    print("\nRegistering for %s Event"%(event))
    registerEventThread.start()
    sleep(2)
    return registerEventThread

###########################################################################################
#
# Method to capture screenshot
#
#  Method Triggers curl command of method : getScreenshot plugin : RDKShell
#  Wait for the event to be captured and the encoded data to be written into file
#  Once encoded data is written into file, decode and save it as png
#
#  IP                  : IP of the device to capture screenshot
#  png_path            : Path of png in which image should be written
#  snapNumber          : Number of screenshots required
###########################################################################################
def RDKShellScreenshot(IP,png_path,snapNumber):
    global snapCount
    global TIMEOUT
    global THUNDERPORT
    current_time = datetime.now().strftime("%H:%M:%S")
    print("\n\nTriggering getScreenshot at ",current_time)
    screenshot_command = "curl -s -S --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\": \"2.0\",\"id\": 42,\"method\": \"org.rdk.RDKShell.1.getScreenshot\"}' http://" + str(IP) + ":" + str(THUNDERPORT) + "/jsonrpc"
    output = triggerCommand(screenshot_command)
    status = json.loads(output)["result"]["success"]
    if status:
        print("SUCCESS : getScreenshot call was successfull")
    else:
        print("FAILURE : getScreenshot call failed")
        return "FAILURE"
    start = time.time()
    time_elapsed=0
    global snapList
    while snapNumber not in snapList:
        if time.time() - start > TIMEOUT:
            print ("Breaking out due to timeout")
            global ws
            ws.close()
            break;
        time.sleep(1)
    if snapNumber not in snapList:
        print("FAILURE: Event was not received within %s seconds"%(TIMEOUT))
        return "FAILURE"
    time_elapsed = time.time() - start
    print("Time elapsed for event to occur : %s seconds"%(str(time_elapsed)))
    print ("Saving data as png")
    width = 1920
    height = 1080
    print("PNG PATH:",png_path)
    start = time.time()
    global encoded_data
    saveAsPng.decodeAndSaveDirectly(encoded_data,width,height,png_path)
    time_elapsed = time.time() - start
    print("Time elapsed for decoding image : %s seconds"%(str(time_elapsed)))
    

###########################################################################################################
#
# Method to set the parameters to capture screenshot
#
#  Method verifies if device is accessible via Thunder port (THUNDERPORT)
#  Obtains registerEventThread after starting websocket instance for listening onScreenshotComplete/uploadComplete event
#  Sets the imageName according to number of snap and calls RDKShellScreenshot/ScreenCaptureScreenshot
#
#  screenshot_mechanism   : Mechanism to be used for capturing screenshot - rdkshell or screencaptureservice
#  IP                     : IP of the device to capture screenshot
#  base_path              : base path wherer all the images to be stored
#  clicks                 : Number of screenshots required
#  interval               : Number of seconds to wait while obtaining multiple screenshots
#  timeout                : Number of seconds to wait while obtaining the corresponding event
###########################################################################################################
def getSnapShot(screenshot_mechanism, IP,base_path,imageName="",clicks=1,interval=0,timeout=0):
    global THUNDERPORT
    if not CheckDeviceStatus(IP,THUNDERPORT):
        print ("FAILURE : Device is not accessible with port THUNDERPORT:",THUNDERPORT)
        exit(0)
    global snaps
    global BasePath
    global TIMEOUT
    global image_name
    global snapList
    global screen_capture_mechanism
    screen_capture_mechanism=screenshot_mechanism
    if not timeout:
        if screen_capture_mechanism == "rdkshell":
            TIMEOUT = 120
        elif screen_capture_mechanism == "screencaptureservice":
            TIMEOUT = 20
    BasePath=base_path
    snaps=clicks
    image_name=imageName
    if screen_capture_mechanism == "rdkshell":
        registerEventThread= registerEvent_(IP,"onScreenshotComplete")
    elif screen_capture_mechanism == "screencaptureservice":
        registerEventThread= registerEvent_(IP,"uploadComplete")
    else:
        print ("FAILURE : Unknown screen capture mechanism")
        return "FAILURE"
    if screen_capture_mechanism == "screencaptureservice":
        cgi_server_url = base_path
        print ("CGI server URL : ",cgi_server_url)
    def thread_function(png_path,snapNumber):
        if screen_capture_mechanism == "rdkshell":
            RDKShellScreenshot(IP, png_path,snapNumber)
        elif screen_capture_mechanism == "screencaptureservice":
            ScreenCaptureScreenshot(IP, cgi_server_url, png_path, snapNumber)
        else:
            print ("FAILURE : Unknown screen capture mechanism")
            return "FAILURE"
    global snapCount
    snapCount=0
    if snapList:
        already_captured_snapshots = len(snapList)
        snapCount = already_captured_snapshots
        snaps = snapCount +  snaps
    if clicks > 1 and interval == 0:
        print ("Interval not passed to wait between successive screenshots")
        print ("Taking default interval value as 5 seconds")
        interval = 5
        print ( snapCount+1,snaps+1)
    for snap in range(snapCount+1,snaps+1):
        png_path = f"image_{snap:02}.png"
        if image_name:
            png_path = image_name + f"_{snap:02}.png"
        else:
            if screen_capture_mechanism != "screencaptureservice":
                png_path = BasePath + png_path
        if clicks==1:
            if screen_capture_mechanism == "rdkshell":
                RDKShellScreenshot(IP, png_path,snap)
            elif screen_capture_mechanism == "screencaptureservice":
                ScreenCaptureScreenshot(IP, cgi_server_url, png_path,snap)
            else:
                print ("FAILURE : Unknown screen capture mechanism")
                return "FAILURE"
        else:
            thread = threading.Thread(target=thread_function,args=(png_path,snap,))
            thread.start()
            sleep(interval)
    return png_path

###########################################################################################################
#
#
# Method to capture screenshot
#
#  Method Triggers curl command of method : uploadScreenCapture  plugin : ScreenCapture
#  Wait for the event to be captured and return <png path>/FAILURE according to the result
#
#  IP                  : IP of the device to capture screenshot
#  cgi_server_url      : CGI server URL
#  image_name          : Name of the image to be stored
#  snapNumber          : Number of the image captured by the utilty for this script
###########################################################################################################
def ScreenCaptureScreenshot(IP,cgi_server_url,image_name,snapNumber):
    global upload_to_cgi
    global THUNDERPORT
    upload_to_cgi = "FAILURE"
    global TIMEOUT
    #Check org.rdk.ScreenCapture Status and activate if not activated
    checkStatusCommand = "curl -s -S --header \"Content-Type: application/json\" --request POST --data  \'{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"Controller.1.status@org.rdk.ScreenCapture\"}}\'  http://" + str(IP) + ":" + str(THUNDERPORT) + "/jsonrpc" 
    output = str(triggerCommand(checkStatusCommand))
    status = json.loads(output)["result"][0]["state"]
    if status == "activated":
        print ("ScreenCapture service is already activated, proceeding")
    else:
        print ("ScreenCapture service is not activated, Activating screen capture service")
        activateCommand = "curl -s -S --header \"Content-Type: application/json\" --request POST --data  \'{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"Controller.1.activate\",\"params\":{\"callsign\": \"org.rdk.ScreenCapture\"}}\'  http://" + str(IP) + ":" + str(THUNDERPORT) + "/jsonrpc"
        output = triggerCommand(activateCommand)
        output = str(triggerCommand(checkStatusCommand))
        status = json.loads(output)["result"][0]["state"]
        if status == "activated":
            print ("ScreenCapture service is activated, proceeding")
        else:
            print ("FAILURE : Unable to activate org.rdk.ScreenCapture service")
            return "FAILURE"

    #Execute screenshot command
    current_time = datetime.now().strftime("%H:%M:%S")
    print("\n\nTriggering getScreenshot at ",current_time)
    screenshot_command = "curl -s -S --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\": \"2.0\",\"id\": 42,\"method\": \"org.rdk.ScreenCapture.1.uploadScreenCapture\" , \"params\": {\"url\":\"" + cgi_server_url + "?fileName=" + image_name + "\"}}' http://" + str(IP) + ":" + str(THUNDERPORT) + "/jsonrpc"
    output = triggerCommand(screenshot_command)
    status = json.loads(output)["result"]["success"]
    if status:
        print("SUCCESS : getScreenshot call was successfull")
    else:
        print("FAILURE : getScreenshot call failed")
        return "FAILURE"

    #verify if uploadComplete event got captured
    start = time.time()
    time_elapsed=0
    global snapList
    while snapNumber not in snapList:
        if time.time() - start > TIMEOUT:
            print ("Breaking out due to timeout")
            global ws
            ws.close()
            break;
        time.sleep(1)
    if snapNumber not in snapList:
        print("FAILURE: Event was not received within %s seconds"%(TIMEOUT))
        return "FAILURE"
    time_elapsed = time.time() - start
    print("Time elapsed for event to occur : %s seconds"%(str(time_elapsed)))
    return image_name

######################################################
#
# Method to parse command line arguments
#
######################################################
def parse_args():
    try:
        args = {}
        for arg in sys.argv[2:]:
            key, value = arg.split('=')
            args[key] = value
    except:
        print ("FAILURE: Unable to parse arguments")
        exit(0)
    return args

#########################################################
#
# Method to retrieve region of template from main image
#
#########################################################
def getTemplateLocation(main_image_path,templateLocation):
    width,height=get_image_resolution(main_image_path)
    widthOfTemplate = templateLocation[0]
    heightOfTemplate = templateLocation[1]
    if widthOfTemplate/width > 0.6 and heightOfTemplate/height < 0.3:
        region="TopRight"
    elif widthOfTemplate/width < 0.6 and widthOfTemplate/width > 0.3 and heightOfTemplate/height < 0.3:
        region="TopCentre"
    elif widthOfTemplate/width < 0.3 and heightOfTemplate/height < 0.3:
        region="TopLeft"
    elif heightOfTemplate/height > 0.6 and widthOfTemplate/width < 0.3:
        region="BottomLeft"
    elif heightOfTemplate/height < 0.6 and heightOfTemplate/height > 0.3 and widthOfTemplate/width < 0.3:
        region="CentreLeft"
    elif heightOfTemplate/height < 0.6 and heightOfTemplate/height > 0.3 and widthOfTemplate/width > 0.3 and widthOfTemplate/width < 0.6:
        region="Centre"
    elif heightOfTemplate/height < 0.6 and heightOfTemplate/height > 0.3 and widthOfTemplate/width > 0.6:
        region="CentreRight"
    elif heightOfTemplate/height > 0.6 and widthOfTemplate/width > 0.3 and widthOfTemplate/width < 0.6:
        region="BottomCentre"
    elif heightOfTemplate/height > 0.6 and widthOfTemplate/width > 0.6:
        region="BottomRight"
    else:
        region="Unknown"
    return region

###########################################################################################################
#
# Method to check if template image is present in main image
#
#  main_image_path     : main image upon which template matching should be done
#  template_image_path : template image to be verified on main image
#  TemplateRegion      : Region of Interest on which the template image should be verified  on main image
###########################################################################################################
def find_template(main_image_path, template_image_path, TemplateRegion):
    if not os.path.exists(template_image_path):
        print ("Template image not found")
        return False
    # Read the main image and template image
    main_image = cv2.imread(main_image_path)
    template_image = cv2.imread(template_image_path)
    # Convert the images to grayscale
    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    # Get the width and height of the template image
    w, h = template_gray.shape[::-1]
    # Perform template matching
    res = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    # Specify a threshold to determine a match
    threshold = 0.8
    loc = np.where(res >= threshold)
    # Check if the template is found at the expected location
    found = False
    found_locations=[]
    for pt in zip(*loc[::-1]):
        found_locations.append(pt)
        region = getTemplateLocation(main_image_path,found_locations[0])
        if TemplateRegion.upper() == region.upper():
            found = True
            location = found_locations[0]
            print ("Template found at co-ordinates : " , found_locations[0])
            break
        elif "unknown" not in region:
            found = False
            print ("Template found at different region : ",region)
            print ("Template found at co-ordinates : " , found_locations[0])
            break

    if found:
        print(f"Template found at expected region: {TemplateRegion}")
    else:
        print(f"Template not found at expected region: {TemplateRegion}")
    return found

######################################################
#
# Method to obtain the resolution of the image
#
######################################################
def get_image_resolution(image_path):
    image = cv2.imread(image_path)
    width, height = image.shape[:2]
    return height, width

#######################################################################################################
#
# Method to verify template image is present on main image
#
#  Method obtains the templates and expected location for the appName from ScreenshotTemplates.config
#
#  appName    : application to be verified (youtube,residentapp)
#  image_path : main_image path
#######################################################################################################
def verifyImageTemplate(appName,image_path):
    if not os.path.exists(image_path): 
        print("FAILURE : image not found")
    parser = SafeConfigParser()
    parser.read( os.path.dirname(os.path.abspath(__file__))+"/ScreenshotTemplates.config")
    try:
        ConfigValue = parser.get('templates_verification',appName)
        print (ConfigValue)
        Template = json.loads(ConfigValue)
        template_images = list(Template.keys())
        resolution_height, resolution_width = get_image_resolution(image_path)
        failed_template_image_paths = ""
        print ("Resolution of image : %dx%d "%(resolution_height, resolution_width))
        if len(template_images) > 1:
            print ("More than one templates are present for validation")
        for template_image in template_images:
            template_image_path = os.path.dirname(os.path.abspath(__file__)) + "/Templates/" + template_image
            if resolution_height != 1920 and resolution_width != 1080:
                print("Creating newTemplate for %dx%d "%(resolution_height, resolution_width))
                #Get Template height and width
                TemplateHeight, TemplateWidth = get_image_resolution(template_image_path)
                newTemplateHeight = int(TemplateHeight * resolution_height / 1920)
                newTemplateWidth = int(TemplateWidth * resolution_width / 1080)
                print ("TemplateHeight = %d, TemplateWidth = %d "%(TemplateHeight,TemplateWidth))
                print ("newTemplateHeight = %d , newTemplateWidth = %d"%(newTemplateHeight,newTemplateWidth))
                def resizeImage(image_path,height,width):
                    image = cv2.imread(image_path)
                    print("Resizing to ",width,height)
                    resized_image = cv2.resize(image,(height, width))
                    resized_image_path = os.path.dirname(os.path.abspath(__file__)) + "/Templates/" + str(newTemplateHeight) + "_" + str(newTemplateWidth) + "_" + template_image
                    cv2.imwrite(resized_image_path, resized_image)
                    return resized_image_path
                template_image_path = resizeImage(template_image_path,newTemplateHeight,newTemplateWidth)
            TemplateRegion = Template[template_image]
            result = find_template(image_path, template_image_path,TemplateRegion)
            if not result:
                failed_template_image_paths = failed_template_image_paths + " " + os.path.basename(template_image_path)
            else:
                print("SUCCESS while verifying template : ",os.path.basename(template_image_path))
                print("Result from verifyImageTemplate : ",result)
                return result
        print("FAILED while verifying template : ",failed_template_image_paths)
        print("Result from verifyImageTemplate : ",result)
        return result
    except:
        print ("Exception occurred while fetching Template Image path")
        return "Template path not configured"

#######################################################################################################
#
# Method to extract text from image
#
#  image_path   : image to extract text from
#  co_ordinates : text extraction to be done from specific co-ordinates
#######################################################################################################
def extract_text_from_image(image_path,co_ordinates=[]):
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    if co_ordinates:
        print("Got coordinates as ",co_ordinates)
        # Define the coordinates (x, y, width, height) of the region of interest (ROI)
        try:
            x = co_ordinates[0]
            y = co_ordinates[1]
            w = co_ordinates[2]
            h = co_ordinates[3]
        except:
            print ("Unable to configure co_ordinates")
            return "NO RESULT"
        # Crop the region of interest from the image
        image = image[y:y+h, x:x+w]
    # Convert the image to GRAY (OpenCV uses BGR by default)
    gray_roi = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(gray_roi)
    return extracted_text

#######################################################################################################
#
# Method to obtain the verification text from config file
#
#  appName : application for which the verification text to be obtained
#######################################################################################################
def getVerificationText(appName):
    #Get Verification text
    parser = SafeConfigParser()
    parser.read( os.path.dirname(os.path.abspath(__file__))+"/ScreenshotTemplates.config")
    try:
        ConfigValue = parser.get('text-verification',appName).encode().decode('unicode_escape')
        if ConfigValue:
            print("Verification Text :  ",ConfigValue);
            return ConfigValue
        else:
            print ("\nVerification Text configured for ",appName)
            return "Verification Text not configured"
    except:
        print ("Exception occurred while fetching Verification Text")
        return "Verification Text not configured"

#######################################################################################################
#
# Method to verify text in image
#
#  appName     : application for which the verification text to be obtained
#  image_path  : image to be verified
#######################################################################################################
def verifyTextInImage(appName,image_path,file_path=""):
    multi_text_verify_split="|"
    start = time.time()
    time_elapsed=0
    global previous_image_path
    global extracted_text
    global already_extracted
    configValue = getVerificationText(appName)
    coordinates = []
    try:
        configValue = json.loads(configValue)
        text_to_verify = list(configValue.keys())[0]
        coordinates = configValue[text_to_verify]
    except:
        coordinates = []
    if not previous_image_path:
        previous_image_path = image_path
    elif previous_image_path == image_path:
        already_extracted = True
        print ("Text was already extracted")
    if not already_extracted:
        extracted_text = extract_text_from_image(image_path,coordinates)
        if file_path:
            print("Writing text into file ",file_path)
            with open(file_path, 'w', encoding='utf-8') as file:
                 file.write(extracted_text)
        time_elapsed = time.time() - start
        print(f"Time elapsed for extracting text: {time_elapsed:.2f} seconds")
    if not coordinates:
        text_to_verify = getVerificationText(appName)
    if multi_text_verify_split in text_to_verify:
        texts = text_to_verify.split(multi_text_verify_split)
        for text in texts:
            if not (text in extracted_text):
                return False
        return True
    else:
        return (text_to_verify in extracted_text)

if __name__ == "__main__":
    print ("*"*100)
    print ("Screenshot Capture Utility")
    print ("No. of command line arguments : ",len(sys.argv)-1)
    help_ = False
    if "capture_screenshot" not in sys.argv and "template_match" not in sys.argv:
        help_ = True
    if help_:
        print ("\n")
        print ("*"*100)
        print ("Screenshot Capture Example")
        print ("*"*100)
        print ("Usage example: python screenCaptureUtility.py capture_screenshot method=rdkshell/screencaptureservice ip=1.2.3.4 base_path=/home/tdk/ server=http://server:port/cgi-bin/upload.cgi/ snaps=3 interval=4")
        print ("\tmethod -> screenshot mechanism rdkshell / screencaptureservice , default -> rdkshell")
        print ("\tip -> IP of the device\n\tbase_path -> Path of the machine where snapshots and encoded data should be stored")
        print ("\tsnaps -> Number of screenshots required\n\tinterval -> Interval between successive screenshots")
        print ("\nIncase you are anticipating a network delay and need tht event thread to run for a longer time:\n\tAdditionial argument \"timeout\" can be passed")
        print ("\teg : timeout=240 -> event thread will run for 240 seconds")
        print ("\nNOTE : For a single snapshot \"interval\" need not be passed")
        print ("     : \"server\" argument is only required for screencaptureservice method")
        print ("     : \"base_path\" is an optional argument to configured the desired location of images ex : base_path=/mnt/images/")
        print ("     : Default THUNDERPORT is set as 9998, if user wants to override the default THUNDERPORT, user can pass command line argument thunderPort=80")
        print ("\n")
        print ("*"*100)
        print ("Image Template Matching Example")
        print ("*"*100)
        print ("Config File need to be configured along with a folder of required temnplates")
        print ("\nConfig File : Create ScreenshotTemplates.config with below template")
        pwd = triggerCommand("pwd",False)
        print ("Templates location : %s/Templates"%(pwd))
        print ("ls %s/Templates"%(pwd))
        print ("                  youtube_logo.png")
        print ("\n[templates_verification]\nyoutube = {\"youtube_logo.png\" : \"TopRight\"}\n")
        print ("                         The Region in which template is present is given as value")
        print ("                         Application name set as youtube")
        print ("                         YouTube logo template image name : youtube_logo.png")
        print ("                         Example : lets say Youtube logo template's top left most pixel is present in TopRight region of the screenshot then value is TopRight")
        print ( "Image Regions" )
        print (" _____________________________________________")
        print (" |   TopLeft    |   TopCentre  |  TopRight   |")
        print (" _____________________________________________")
        print (" |  CentreLeft  |    Centre    | CentreRight |")
        print (" _____________________________________________")
        print (" |  BottomLeft  | BottomCentre | BottomRight |")
        print (" _____________________________________________")
        print ("\nUsage example: python screenCaptureUtility.py template_match")
        print ("\n")
        exit(0)



    # Extract values from the arguments
    print ("\nParsing command line arguments")

    args = parse_args()

    if "capture_screenshot" in sys.argv:
        DUT_IP = args.get('ip', None)
        try :
            screencapturemechanism = args.get('method',None).lower()
        except:
            screencapturemechanism = ""
        try:
            base_path = args.get('base_path', None)
        except:
            base_path = triggerCommand("pwd")+"/"
        if not base_path:
            base_path = triggerCommand("pwd")+"/"
        if "screencaptureservice" in screencapturemechanism:
            server_url = args.get('server',None)
            if not server_url:
                print ("Server url not given ")
                print ("Ex : server=https://server:8081/cgi-bin/upload.cgi/")
                exit(0)

        thunderPort = args.get('thunderPort',None)
        if thunderPort:
            print ("thunderPort is set as ",thunderPort)
            setThunderPort(thunderPort)
        else:
            print("Setting default thunder port as 9998")
            setThunderPort(9998)

        clicks = int(args.get('snaps', 0))
        if not clicks:
            print ("No. of snaps required not given")
            print ("Ex : snaps=2")
            exit(0)
        print ("Acquired device ip             : ",DUT_IP)

        if "screencaptureservice" in screencapturemechanism:
            print ("CGI server url configured as        : ",base_path)
        else:
            print ("Base path configured as        : ",base_path)
        if "rdkshell" in screencapturemechanism  and "screencaptureservice" not in screencapturemechanism:
            print ("RDKShell screenshot mechanism is selected")
            screencapturemechanism = "rdkshell"
        elif "rdkshell" not in screencapturemechanism and "screencaptureservice" in screencapturemechanism:
            print ("ScreenCaptureService mechanism is selected")
            screencapturemechanism = "screencaptureservice"
            image_naming_convention = "image"
            base_path = server_url
        else:
            print ("Default screenshot mechanism : rdkshell is selected")
            screencapturemechanism = "rdkshell"

        if screencapturemechanism == "rdkshell":
            image_naming_convention=""

        if clicks > 1:
            if "interval" not in str(sys.argv):
                print ("NOTE : Interval between screenshots not configured")
                print ("Setting default interval \"5\"")
                interval=5
            else:
                interval = float(args.get('interval', 0))
            print ("Interval between screenshots   : ",interval)
        else:
            interval=0
        if "timeout" in str(sys.argv):
            timeout = int(args.get('timeout',0))
            print ("Event thread timeout is set as : ",timeout)
            getSnapShot(screencapturemechanism,DUT_IP,base_path,image_naming_convention,clicks,interval,timeout)
        else:
            getSnapShot(screencapturemechanism,DUT_IP,base_path,image_naming_convention,clicks,interval)

    if "template_match" in sys.argv:
        imageName = str(args.get('imagepath', None))
        appName = str(args.get('appname', None))
        print ("Acquired imagepath as           : ",imageName)
        print ("Acquired appname as             : ",appName)
        verifyImageTemplate(appName,imageName)
