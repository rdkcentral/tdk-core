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
import socket
import time
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
import json
import paho.mqtt.packettypes as packettypes
import sys
from dab_config import *
import rdkv_performancelib
from rdkv_performancelib import *
from tdkvScreenShotUtility import *
from rialto_containerlib import *
from datetime import datetime, timedelta, timezone
import random
import pytz  # Import pytz for timezone handling
import re
import base64
import io
import os
from PIL import Image
#------------------------------------------------------------
#DECLARING THE VARIABLES
#------------------------------------------------------------
deviceIP=""
devicePort=""
deviceName=""
deviceType=""
deviceMac=""
realpath=""
securityEnabled=False
deviceToken=""
client = None
response_payload= None

#METHODS
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module(libobj,port,deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    global libObj
    global realpath
    global deviceMac
    deviceIP = libobj.ip;
    devicePort = port
    broker_address = deviceIP
    #print("devicePort:",devicePort,"deviceIP:",deviceIP)
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]
    libObj = libobj
    try:
        deviceMac = deviceInfo["mac"]
        SSHUtility.deviceMAC = deviceMac
        SSHUtility.realpath = libobj.realpath
    except Exception as e:
        print("\nException Occurred while getting MAC \n")
        print(e)
# -------------------------------------------------------------------------------------------------------------------------
# Establishes a connection to the specified MQTT broker.
# Handles potential connection errors (timeouts, connection failures) and exits the program if unsuccessful.
# Returns True upon successful connection.
# -------------------------------------------------------------------------------------------------------------------------
def connect(client,broker_address):
    try:
        connect_result = client.connect(broker_address,port=broker_port)
        if connect_result != 0:
            raise ConnectionError("Connection failed")
        print("Client Connected successfully.")
    except socket.timeout:
        print("Failed to connect to the broker: Connection timed out")
        print("Please check Device connection status")
        sys.exit(1)
    except ConnectionError as e:
        print("Failed to connect to the broker:", e)
        print("Please check Device connection status")
        sys.exit(1)
    return True
# -------------------------------------------------------------------------------------------------------------------------
# Initializes an MQTT client with the specified parameters, establishes a connection to the broker,
# and returns the client object and a success/failure indicator.
# Handles potential exceptions during client setup and connection.
# -------------------------------------------------------------------------------------------------------------------------
def setup_mqtt_client(broker_address,client_id="mqtt5_client", protocol=mqtt.MQTTv5):
  try:
    global client
    client = mqtt.Client(client_id, protocol=protocol)
    connect(client,broker_address)  # Connect to the MQTT broker
    print(f"\nConnecting to the MQTT broker using {client_id} client_id")
    return client,"SUCCESS"
  except Exception as e:
    print(f"Error setting up MQTT client: {e}")
    return None,"FAILURE"
# -------------------------------------------------------------------------------------------------------------------------
# Subscribes the MQTT client to the specified topic and starts the message processing loop.
# -------------------------------------------------------------------------------------------------------------------------
def subscribe(client, topic):
    client.subscribe(topic)
    client.on_message = on_message  # Assign the on_message callback
    client.loop_start()
# -------------------------------------------------------------------------------------------------------------------------
# Publishes a message to the specified MQTT topic with a response topic.
# Handles message serialization and includes necessary MQTT properties.
# -------------------------------------------------------------------------------------------------------------------------
def publish(client, topic, message, response_topic):
    message = json.dumps(message)
    print("\nPublish message:\n", message)
    properties = Properties(packettypes.PacketTypes.PUBLISH)
    properties.ResponseTopic = response_topic
    client.publish(topic, message, qos=1, properties=properties)
# -------------------------------------------------------------------------------------------------------------------------
# Callback function triggered when a message is received on a subscribed topic.
# Stores the received message payload for later retrieval.
# -------------------------------------------------------------------------------------------------------------------------
def on_message(client, userdata, message):
    global response_payload  # Declare response_payload as a global variable
    #payload = str(message.payload.decode("utf-8"))
    print("\nEntered on_message\n")
    print("\nReceived message on topic:", message.topic)
    print("\nMessage payload:", str(message.payload.decode("utf-8")))
    response_payload = str(message.payload.decode("utf-8"))
# -------------------------------------------------------------------------------------------------------------------------
# Executes a specified MQTT operation based on the provided operation name and device ID.
# Constructs MQTT topics, subscribes to the response topic, prepares and publishes the message,
# and returns the received response payload or an error message.
# -------------------------------------------------------------------------------------------------------------------------
def perform_operation(operation_name, device_id, message_override=None):
    global client
    global response_payload
    response_payload = None  # Reset response_payload before performing operation
    if operation_name in operations:
        operation = operations[operation_name]
        topic = "dab/" + device_id + "/" + operation['topic'].strip()
        response_topic = "dab/_response/" + topic.strip()
        subscribe(client, response_topic)        
        message = operation.get('message', {})
        if  message_override and message_override != "None":
            message = {}  # Reset message_override before performing operation
            message.update(message_override)
        publish(client, topic, message, response_topic)

        # Allow some time for the message to be processed
        time.sleep(6)
        # Return the response payload received from the MQTT broker
        if response_payload !="None":
           return response_payload
        else:
            print("\nNo response payload is received")
            return None


    else:
        print("Operation '{}' not found.".format(operation_name))
#-------------------------------------------------------------------
# Function to check required pattern in proc entry file
#-------------------------------------------------------------------
def checkProcEntry(sshMethod,credentials,validation_script,mode):
    result = "FAILURE"
    validation_script = validation_script.split('.py')[0]
    try:
        lib = importlib.import_module(validation_script)
        method = "check_video_status"
        method_to_call = getattr(lib, method)
        result = method_to_call(sshMethod,credentials,mode)
    except Exception as e:
        print(e);
        print("[ERROR]: Failed to import video validation script file, please check the configuration")
        result = "FAILURE"
    finally:
        return result
#----------------------------------------------------------------------------------
# Function to read proc validation parameters from device
#----------------------------------------------------------------------------------
def checkPROC(check_pause):
        rdkv_performancelib.deviceName = deviceName
        rdkv_performancelib.deviceType = deviceType
        ssh_param = rdkv_performancelib.rdkservice_getSSHParams(libObj.realpath,deviceIP)
        ssh_param_dict = json.loads(ssh_param)
        sshMethod = ssh_param_dict["ssh_method"]
        credentials = ssh_param_dict['credentials']
        validation_script = getDeviceConfig ('VIDEO_VALIDATION_SCRIPT_FILE')
        proc_file_path = libObj.realpath + "/"   + "fileStore/" + validation_script
        print("proc validation file: ",proc_file_path)
        if not os.path.exists(proc_file_path) :
            print(" PROC entry file is missing from fileStore ")
            return "FAILURE"
        mode = getDeviceConfig ('PROC_CHECK_MODE')
        if check_pause == "True":
            mode = mode + "-paused"
        av_status = checkProcEntry(sshMethod,credentials,validation_script,mode)
        return av_status

# -------------------------------------------------------------------------------------------------------------------------
# Validates DAB Get api response against RDK values based on configured mappings.
# Compares DAB and RDK values for each specified setting, handling specific cases and data type conversions.
# Returns a tuple indicating validation success and a list of failed validations.
# -------------------------------------------------------------------------------------------------------------------------
def validate_get_dab_with_rdk(dab_response):
    failed_get_validations = []
    for key, rdk_info in rdk_get_dab_validations.items():
        dab_value = dab_response.get(key)
        rdk_api = rdk_info['rdk_api']
        rdk_param = rdk_info['rdk_param']

        print(f"\nGet the RDK Service Response of {key}:")
        print(f"\nInvoking RDK API {rdk_api}\n")
        print("\n ================================================================================================================ \n")
        if isinstance(rdk_param, tuple):
            rdk_value = {param: rdkservice_getReqValueFromResult(rdk_api, param) for param in rdk_param}

        else:
            rdk_value = rdkservice_getReqValueFromResult(rdk_api, rdk_param)

        if isinstance(dab_value, str):
               dab_value = dab_value.lower()
        if isinstance(rdk_value, str):
               rdk_value = rdk_value.lower()
        # Specific handling for audioVolume
        if key == 'audioVolume':
               print(dab_value)
               dab_value = int(float(dab_value))
               rdk_value = int(float(rdk_value))
           # Apply special case mappings if they exist
        if key in special_case_mappings:
               special_case_map = special_case_mappings[key]
               if dab_value in special_case_map:
                  mapped_value = special_case_map[dab_value]
                  # Check if the mapped_value is a list of possible values
                  if isinstance(mapped_value, list):
                      dab_value = rdk_value
                  else:
                       dab_value = mapped_value


           # Specific handling for outputResolution
        if key == 'outputResolution':
               expected_frequency = round(dab_value.get('frequency'))
               expected_width = dab_value.get('width')
               expected_height = dab_value.get('height')

               # Transform RDK response to match DAB format
               try:
                    rdk_frequency = int(rdk_value['resolution'].rsplit('p', 1)[-1] if 'p' in rdk_value['resolution'] else rdk_value['resolution'].rsplit('i', 1)[-1])
               except (KeyError, ValueError, IndexError):
                    rdk_frequency = None

               rdk_width = int(rdk_value['w'])
               rdk_height = int(rdk_value['h'])

               if expected_frequency == rdk_frequency and expected_width == rdk_width and expected_height == rdk_height:
                   print(f"\nBoth RDK and DAB response are same for {key}: DAB={{'frequency': {expected_frequency}, 'width': {expected_width}, 'height': {expected_height}}}, RDK={{'frequency': '{rdk_frequency}', 'w': {rdk_width}, 'h': {rdk_height}}}\n")
               else:
                   print("\n =================================================================================================== \n")
                   failed_get_validations.append({
                   "parameter": key,
                   "message": f"Mismatch for {key}: DAB={{'frequency': {expected_frequency}, 'width': {expected_width}, 'height': {expected_height}}}, RDK={{'frequency': '{rdk_frequency}', 'w': {rdk_width}, 'h': {rdk_height}}}"})
                   print(f"\nMismatch found for {key}: DAB={{'frequency': {expected_frequency}, 'width': {expected_width}, 'height': {expected_height}}}, RDK={{'frequency': '{rdk_frequency}', 'w': {rdk_width}, 'h': {rdk_height}}}\n")

           # Specific handling for audioOutputSource
        elif key == 'audioOutputSource':
               rdk_value_list = [port.lower() for port in rdk_value]
               if dab_value in rdk_value_list:
                   print(f"\nBoth RDK and DAB response  are the same for {key}: DAB={dab_value}, RDK={rdk_value_list}\n")
               else:
                   print("\n ========================================================================================================= \n")
                   failed_get_validations.append({
                   "parameter": key,
                   "message": f"Mismatch for {key}: DAB={dab_value}, RDK={rdk_value}"})
                   print(f"\nMismatch found for {key}: DAB={dab_value}, RDK={rdk_value_list}\n")

        elif dab_value == rdk_value:
                print("\n ===============================================================================================================\n")
                print(f"\nBoth RDK and DAB response  are the same for {key}: DAB={dab_value}, RDK={rdk_value}\n")
        else:
            print("\n ===============================================================================================================\n")
            failed_get_validations.append({
            "parameter": key,
            "message": f"Mismatch for {key}: DAB={dab_value}, RDK={rdk_value}"})
            print("\n =============================================================================================================== \n")
            print(f"\nMismatch found for {key}: DAB={dab_value}, RDK={rdk_value}\n")
    print("\n ======================================================================================================================= \n")
    return (not failed_get_validations, failed_get_validations)
#--------------------------------------------------------------------------------------------------------------------------------------------
#Calculates and returns the device uptime in minutes.
def get_device_uptime_minutes(uptime_str):
# Calculates device uptime in minutes from a time string in UTC format.
# Args:
# uptime_str (str): Time string in format "Fri, 24 May 2024 05:39:39 UTC".
# Returns:
# int: Device uptime in minutes, or None if the time string is invalid.
  try:
    # Parse the time string and get current time in one line (simplification)
    uptime_minutes = int((datetime.utcnow() - datetime.strptime(uptime_str, "%a, %d %b  %Y %H:%M:%S")).total_seconds() / 60)
    return uptime_minutes
  except ValueError:
    print(f"\nInvalid time format: {uptime_str}\n")
    return None
def calculate_uptime(timestamp_ms):
    # Convert the timestamp from milliseconds to a datetime object
    system_start_time = datetime.utcfromtimestamp(timestamp_ms / 1000.0)
    # Ensure the datetime object is timezone-aware and set to UTC
    system_start_time = system_start_time.replace(tzinfo=timezone.utc)
    # Format the datetime object to a human-readable string
    formatted_time = system_start_time.strftime("%a %b %d %Y %H:%M:%S UTC")
    print(f"\nSystem start time: {formatted_time}\n")
    # Get the current time in UTC
    current_time = datetime.now(timezone.utc)
    # Calculate the difference between the current time and the start time
    uptime_duration = current_time - system_start_time
    # Convert the uptime duration to seconds
    uptime_seconds = int(uptime_duration.total_seconds())
    # Convert the uptime duration to minutes
    uptime_minutes = int(uptime_seconds/60)
    return uptime_minutes

# -------------------------------------------------------------------------------------------------------------------------
# Validates DAB device info api response against RDK values based on configured mappings.
# Compares DAB and RDK values for each specified setting, handling specific cases and data type conversions.
# Returns a tuple indicating validation success and a list of failed validations.
# -------------------------------------------------------------------------------------------------------------------------
def validate_device_info_with_rdk(dab_response):
  failed_devinfo_validations = []
  # Extract MAC addresses from DAB response if networkInterfaces is present
  dab_eth_mac = None
  dab_wifi_mac = None
  if "networkInterfaces" in dab_response:
    for iface in dab_response["networkInterfaces"]:
      if iface["type"] == "Ethernet":
        dab_eth_mac = iface["macAddress"].upper()
      elif iface["type"] == "Wifi":
        dab_wifi_mac = iface["macAddress"].upper()

  for key, validation_info in rdk_devinfo_validations.items():
    dab_param = validation_info['dab_param']
    rdk_api = validation_info['rdk_api']
    rdk_param = validation_info.get('rdk_param')


    dab_value = dab_response.get(dab_param)
    if not dab_value:
      print("Parameter '" + dab_param + "' not found in DAB response.")
      continue
    print("\n =============================================================================================================== \n")
    print(f"\nGet the RDK Service Response of {key}:")
    print(f"\nInvoking RDK API {rdk_api}\n")
    if rdk_api:
      if rdk_param:
        rdk_value = rdkservice_getReqValueFromResult(rdk_api, rdk_param)
      else:
        rdk_value = rdkservice_getValue(rdk_api)
      if dab_param == 'uptimeSince':
        rdk_value =  calculate_uptime(rdk_value)
        #get_device_uptime_minutes(rdk_value)
        dab_value = calculate_uptime(dab_value)  # Assuming calculate_uptime exists

      if key == 'deviceId':
         rdk_value = rdk_value.replace(":", "").upper() if rdk_value else None
      elif key in ['networkInterfaces_eth', 'networkInterfaces_wifi']:
           rdk_value = rdk_value.upper() if rdk_value else None
      # Comparison logic for Wifi and Ethernet MAC addresses (within loop)
      if key == 'networkInterfaces_eth':
        # Compare extracted dab_eth_mac with rdk_value
        if dab_eth_mac is not None and dab_eth_mac == rdk_value.upper():
          print("\n =========================================================================================================== \n")
          print("\nValidation passed for Ethernet MAC: DAB=%s, RDK=%s" % (dab_eth_mac, rdk_value))
        else:
          print("\n ============================================================================================================= \n")
          failed_devinfo_validations.append({
          "parameter": key,
          "message": f"Mismatch for {key}: DAB={dab_eth_mac}, RDK={rdk_value}"})
          print("\nValidation failed for Ethernet MAC: DAB=%s, RDK=%s" % (dab_eth_mac, rdk_value))
      elif key == 'networkInterfaces_wifi':
        # Compare extracted dab_wifi_mac with rdk_value
        if dab_wifi_mac is not None and dab_wifi_mac == rdk_value.upper():
           print("\n ============================================================================================================= \n")
           print("\nValidation passed for WiFi MAC: DAB=%s, RDK=%s" % (dab_wifi_mac, rdk_value))
        else:
          print("\n ============================================================================================================= \n")
          failed_devinfo_validations.append({
          "parameter": key,
          "message": f"Mismatch for {key}: DAB={dab_wifi_mac}, RDK={rdk_value}"})
          print("\nValidation failed for WiFi MAC: DAB=%s, RDK=%s" % (dab_wifi_mac, rdk_value))
          print("\n =============================================================================================================== \n")

      # Apply transform (if provided) and perform value comparison
      if isinstance(dab_value, list) and all(iface.get('type') in ('Ethernet', 'Wifi') for iface in dab_value):

        # Skip printing validation failure for overall 'networkInterfaces'
        continue
      if dab_value == rdk_value:
        print("\n ================================================================================================================== \n")
        print("\nValidation passed for '" + dab_param + "': DAB=%s, RDK=%s" % (dab_value, rdk_value))
      else:
        print("\n =================================================================================================================== \n")
        print("\nValidation failed for '" + dab_param + "': DAB=%s, RDK=%s" % (dab_value, rdk_value))
        failed_devinfo_validations.append({
        "parameter": key,
        "message": f"Mismatch for {key}: DAB={dab_value}, RDK={rdk_value}"})

    else:
      print("\nNo RDK validation configured for '" + dab_param + "'.")
  print("\n =============================================================================================================== \n")
  return (not failed_devinfo_validations, failed_devinfo_validations)
#extracts timestamo from given string
def extract_timestamp(log_string):
  match = re.search(r'\d{2}:\d{2}:\d{2}\.\d+', log_string)
  if match:
    timestamp = match.group()
    milliseconds = timestamp.split('.')[1]
    return timestamp[:-len(milliseconds)] + milliseconds + "000"
  else:
    return None

# -------------------------------------------------------------------------------------------------------------------------
# Validates DAB SettingList response against RDK values based on configured mappings.
# Compares DAB and RDK values for each specified setting, handling specific cases and data type conversions.
# Returns a tuple indicating validation success and a list of failed validations.
# -------------------------------------------------------------------------------------------------------------------------
def validate_settingslist_dab_with_rdk(dab_response):
    """
    Validate DAB settings list with RDK settings list based on the provided validations.
    """
    failed_settingslist_validations = []
    result = "SUCCESS"
    for key, validation_info in rdk_SettingsList_validations.items():
        dab_param = validation_info['dab_param']
        rdk_api = validation_info['rdk_api']
        rdk_param = validation_info.get('rdk_param')
        dab_value = dab_response.get(dab_param)
        if dab_value is None:
            print(f"\nParameter '{dab_param}' not found in DAB response.")
            continue


        if rdk_api:
            print(f"\nGet the RDK Service Response of {key}:\n")
            print(f"\nInvoking RDK API {rdk_api}\n")
            print("\n=================================================================================================================\n")
            if rdk_param:
                rdk_value = rdkservice_getReqValueFromResult(rdk_api, rdk_param)
            else:
                rdk_value = rdkservice_getValue(rdk_api)
            # Convert values to lowercase for case-insensitive comparison
            if isinstance(dab_value, str):
               dab_value = dab_value.lower()
            elif isinstance(dab_value, list):
               dab_value =  [val.lower() for val in dab_value if isinstance(val, str) ]
            #elif isinstance(dab_value, dict):
             #   dab_value = [str(key).lower() for key in dab_value.keys()]
            if isinstance(rdk_value, str):
               rdk_value = rdk_value.lower()
            elif isinstance(rdk_value, list):
               rdk_value = [val.lower() for val in rdk_value if isinstance(val, str) ]
            #elif isinstance(rdk_value, dict):
             #   rdk_value = [str(key).lower() for key in rdk_value.keys()]
            # Handle special cases using dab_value
            original_dab_value = dab_value
            if key in special_case_mappings:
               special_case_map = special_case_mappings[key]
               mapped_dab_values = []
               # If dab_value is a list, iterate over it; otherwise, make it a single-item list
               if isinstance(dab_value, list):
                   for dab_source in dab_value:
                       if dab_source in special_case_map:
                          mapped_value = special_case_map[dab_source]
                          if isinstance(mapped_value, list):
                              mapped_dab_values.extend(mapped_value)
                          else:
                              mapped_dab_values.append(mapped_value)
                       else:
                           mapped_dab_values.append(dab_source)
               else:
                   # Handle the case where dab_value is a single string
                   mapped_value = special_case_map.get(dab_value, dab_value)
                   if isinstance(mapped_value, list):
                      mapped_dab_values.extend(mapped_value)
                   else:
                      mapped_dab_values.append(mapped_value)
               dab_value = mapped_dab_values
               print("testing dab value:",mapped_dab_values)
            if key == 'audioOutputSource':
                print("mapped_dab_value:",dab_value)
                if  (set(dab_value)  == set(rdk_value)):
                    print("\n =====================================================================================================\n")
                    print(f"\nAudio source responses are the same: {original_dab_value} : {rdk_value}.")
                else:
                    result = "FAILURE"
                    failed_settingslist_validations.append({
                    "parameter": key,
                    "message": f"Mismatch for {key}: DAB={dab_value}, RDK={rdk_value}"})
                    print("\nAudio sources are different.")
                    print("\n ===================================================================================================== \n")
                    print(f"\nDAB audio sources: {dab_value}")
                    print(f"\nRDK audio sources (mapped): {rdk_value}.")
            elif key == 'audioOutputMode':
                rdk_audio_modes = set([mode.upper() for mode in rdk_value])
                if dab_value == rdk_audio_modes:
                    print("\n ================================================================================================== \n")
                    print(f"\nAudio mode responses are the same: {dab_value} : {rdk_audio_modes}")
                else:
                    result = "FAILURE"
                    failed_settingslist_validations.append({
                    "parameter": key,
                    "message": f"Mismatch for {key}: DAB={dab_value}, RDK={rdk_audio_modes}"})
                    print("\n ==================================================================================================== \n")
                    print("\nAudio modes are different.")
                    print(f"\nDAB audio modes: {dab_value}")
                    print(f"\nRDK audio modes: {rdk_audio_modes}")

            elif key == 'outputResolution':
                dab_value = dab_response.get(dab_param)
                dab_resolutions_set = set()
                for res in dab_value:
                    # Check if the resolution has a frequency value
                    if res['frequency'] is not None:
                       # Format the resolution as "{height}p{frequency}"
                       resolution_str = f"{res['height']}p{int(res['frequency'])}"
                       # Add the formatted resolution to the set
                       dab_resolutions_set.add(resolution_str)
                # Prepare a list of valid RDK resolutions
                filtered_rdk_resolutions = []
                for res in rdk_value:
                    # Ensure the resolution is progressive and has a frequency
                    if 'p' in res and 'i' not in res and len(res) > 3 and res[-2:].isdigit():
                        # Extract height and frequency
                        p_index = res.find('p')
                        rdk_height = int(res[:p_index])
                        rdk_frequency = int(res[p_index+1:])
                        filtered_rdk_resolutions.append(f"{rdk_height}p{rdk_frequency}")

                # Initialize an empty list to store missing resolutions
                missing_in_dab = []
                for rdk_res in filtered_rdk_resolutions:
                    # If the resolution is not found in the DAB set, add it to missing_in_dab
                    if rdk_res not in dab_resolutions_set:
                       missing_in_dab.append(rdk_res)
                if not missing_in_dab:
                       print("\n ================================================================================================== \n")
                       print("\nResolutions are the same.\n")
                       dab_resolutions = sorted(dab_resolutions_set)
                       filtered_rdk_resolutions = sorted(filtered_rdk_resolutions)
                       print("Dab Resolutions\tRdk Resolutions")
                       for dab, rdk in zip(dab_resolutions, filtered_rdk_resolutions):
                           print(f"{dab}\t \t \t \t \t \t \t{rdk}")
                else:
                       print("\n =================================================================================================== \n")
                       print("\nResolutions are different.")
                       print("Resolutios missing in DAB:", missing_in_dab)
                       failed_settingslist_validations.append({
                       "parameter": key,
                       "message": f"Mismatch for {key}: DAB={dab_resolutions_set}, RDK={filtered_rdk_resolutions}"})

            else:
                if dab_value == rdk_value:
                    print("\n ========================================================================================================= \n")
                    print(f"\n{key} feature is supported in DAB response and its value is {dab_value}.\n")
                else:
                    print("\n ========================================================================================================= \n")
                    failed_settingslist_validations.append({
                    "parameter": key,
                    "message": f"Mismatch for {key}: DAB={dab_value}, RDK={rdk_value}"})
                    print(f"\n{key} feature is available in DAB response but its value is different from RDK response.\n")
                    print(f"\nDAB {key} value: {dab_value}, RDK {key} value: {rdk_value}\n")
                    result = "FAILURE"


    # Validate additional features not specifically listed in the settings
    additional_features = [feature for feature, info in rdk_SettingsList_validations.items() if info['rdk_api'] is None]
    print("\n Below are the DAB Features that doesn't have corresponding RDK API to Validate the response\n")
    print("\n =============================================================================================================== \n")
    for feature in additional_features:
        if feature in dab_response:

            print(f"\n{feature} is supported in device and its value is: {dab_response.get(feature)}\n")
            print("\n =============================================================================================================== \n")
        else:
            result = "FAILURE"
            print(f"\n{feature} is not supported in device\n")
    print("\n =============================================================================================================== \n")
    return(not failed_settingslist_validations,failed_settingslist_validations)

# -------------------------------------------------------------------------------------------------------------------------
# Validates DAB  SET Api response against RDK values based on configured mappings.
# Compares DAB and RDK values for each specified setting, handling specific cases and data type conversions.
# Returns a tuple indicating validation success and a list of failed validations.
# -------------------------------------------------------------------------------------------------------------------------
def validate_set_dab_with_rdk(dab_response,changed_settings):
    failed_validations = []
    for setting_name in changed_settings:
        if setting_name in rdk_set_dab_validations:
           rdk_info = rdk_set_dab_validations[setting_name]
           dab_value = dab_response.get(setting_name)
           rdk_api = rdk_info['rdk_api']
           rdk_param = rdk_info['rdk_param']
           print("\n================================================================================================================ \n")
           print(f"\nGetting the RDK Service Response for {setting_name}:\n")
           print(f"\nInvoking RDK API {rdk_api}\n")

           if isinstance(rdk_param, tuple):
              rdk_value = {param: rdkservice_getReqValueFromResult(rdk_api, param) for param in rdk_param}
           else:
                rdk_value = rdkservice_getReqValueFromResult(rdk_api, rdk_param)

           # Convert values to lowercase for case-insensitive comparison
           if isinstance(dab_value, str):
               dab_value = dab_value.lower()
           elif isinstance(dab_value, list):
               dab_value =  [val.lower() for val in dab_value if isinstance(val, str) ]
           if isinstance(rdk_value, str):
               rdk_value = rdk_value.lower()
           elif isinstance(rdk_value, list):
               rdk_value = [val.lower() for val in rdk_value if isinstance(val, str) ]

           # Specific handling for audioVolume
           if setting_name == 'audioVolume':
               dab_value = int(float(dab_value))
               rdk_value = int(float(rdk_value))

           # Apply special case mappings if they exist
           if setting_name in special_case_mappings:
               special_case_map = special_case_mappings[setting_name]
               if dab_value in special_case_map:
                  mapped_value = special_case_map[dab_value]
                  # Check if the mapped_value is a list of possible values
                  if isinstance(mapped_value, list):
                      dab_value = rdk_value
                  else:
                       dab_value = mapped_value


           # Specific handling for outputResolution
           if setting_name == 'outputResolution':
               expected_frequency = round(dab_value.get('frequency'))
               expected_width = dab_value.get('width')
               expected_height = dab_value.get('height')

               # Transform RDK response to match DAB format
               try:
                    rdk_frequency = int(rdk_value['resolution'].rsplit('p', 1)[-1] if 'p' in rdk_value['resolution'] else rdk_value['resolution'].rsplit('i', 1)[-1])
               except (KeyError, ValueError, IndexError):
                    rdk_frequency = None
               rdk_width = int(rdk_value['w'])
               rdk_height = int(rdk_value['h'])
               if (expected_frequency, expected_width, expected_height) == (rdk_frequency, rdk_width, rdk_height):
               #if expected_frequency == rdk_frequency and expected_width == rdk_width and expected_height == rdk_height:
                   print("\n========================================================================================================== \n")
                   print(f"\nBoth RDK and DAB response are same for {setting_name}: DAB={{'frequency': {expected_frequency}, 'width': {expected_width}, 'height': {expected_height}}}, RDK={{'frequency': '{rdk_frequency}', 'w': {rdk_width}, 'h': {rdk_height}}}\n")
               else:
                   print("\n=========================================================================================================== \n")
                   failed_validations.append({
                   "parameter": setting_name,
                   "message": f"Mismatch for {setting_name}: DAB={{'frequency': {expected_frequency}, 'width': {expected_width}, 'height': {expected_height}}}, RDK={{'frequency': '{rdk_frequency}', 'w': {rdk_width}, 'h': {rdk_height}}}"})
                   print(f"\nMismatch found for {setting_name}: DAB={{'frequency': {expected_frequency}, 'width': {expected_width}, 'height': {expected_height}}}, RDK={{'frequency': '{rdk_frequency}', 'w': {rdk_width}, 'h': {rdk_height}}}\n")

           # Specific handling for audioOutputSource
           elif setting_name == 'audioOutputSource':
               rdk_value_list = [port.lower() for port in rdk_value]
               if dab_value in rdk_value_list:
                   print("\n=========================================================================================================== \n")
                   print(f"\nBoth RDK and DAB response are the same for {setting_name}: DAB={dab_value}, RDK={rdk_value}")
               else:
                   print("\n=========================================================================================================== \n")
                   failed_validations.append({
                   "parameter": setting_name,
                   "message": f"Mismatch for {setting_name}: DAB={dab_value}, RDK={rdk_value}"})
                   print(f"\nMismatch found for {setting_name}: DAB={dab_value}, RDK={rdk_value_list}")

           elif dab_value == rdk_value:
                print("\n=========================================================================================================== \n")
                print(f"\nBoth RDK and DAB response  are the same for {setting_name}: DAB={dab_value}, RDK={rdk_value}")
           else:
                print("\n=========================================================================================================== \n")
                failed_validations.append({
                "parameter": setting_name,
                "message": f"Mismatch for {setting_name}: DAB={dab_value}, RDK={rdk_value}"})
                print(f"\nMismatch found for {setting_name}: DAB={dab_value}, RDK={rdk_value}")
    print("\n=========================================================================================================== \n")
    return (not failed_validations, failed_validations)

# -------------------------------------------------------------------------------------------------------------------------
# Reverts previously modified settings to their original values.
# Iterates through changed settings and attempts to set them back to their initial values using the DAB set API.
# Returns a tuple indicating whether all reverts were successful and a list of failed revert operations.
# -------------------------------------------------------------------------------------------------------------------------
def revert_settings(initial_settings, changed_settings,device_id):
    global client
    failed_reverts =[]
    for setting_name in changed_settings:
        print("\n=========================================================================================================== \n")
        if setting_name in initial_settings:  # Check if setting exists in initial settings
            initial_value = initial_settings[setting_name]
            message_override = {setting_name: initial_value}
            print("\nmessage_override:", message_override)
            if setting_name in changed_settings:
                print("\n=========================================================================================================== \n")
                print(f"\nGetting DAB set API response for reverting setting '{setting_name}' to '{initial_value}'\n")
                revert_set_response_payload = perform_operation(operation_name["dab_set_api"], device_id, message_override)
                # Check if SET operation was successful
                if revert_set_response_payload and  json.loads(revert_set_response_payload)["status"] == 200:
                    print(f"\nReverted setting '{setting_name}' to '{initial_value}' value.\n")
                    print("\n=========================================================================================================== \n")
                else:
                    print(f"\nReverting setting '{setting_name}' to '{initial_value}' value failed.\n")
                    print("\n=========================================================================================================== \n")
                    failed_reverts.append({
                    "parameter": setting_name,
                    "message": f"\nReverting setting '{setting_name}' to '{initial_value}' value failed.\n"})
    print("\n=========================================================================================================== \n")
    return(not failed_reverts,failed_reverts)
#--------------------------------------------------------------------------------------------------------------------------
#Saves an image from base64-encoded data 
#--------------------------------------------------------------------------------------------------------------------------
def dab_save_png(encoded_data):
    try:
      # Decode the base64 data
      image_data = base64.b64decode(encoded_data)

      # Create an image object from the decoded data
      image = Image.open(io.BytesIO(image_data))

      # Resize the image to the fixed resolution (default 800x600)
      resized_image = image.resize((1920, 1080))
      # Define the path with a generic filename and timestamp
      base_path = "/opt/apache-tomcat-7.0.96/webapps/rdk-test-tool/fileStore/"
      timestamp = str(int(time.time()))  # Get current timestamp in milliseconds
      filename = f"dab_screenshot_{timestamp}.png"
      png_path = base_path + filename
      # Save the image (mandatory)
      resized_image.save(png_path)
      if os.path.exists(png_path):
          return "Success"
      else:
          return "File not saved"
    except Exception as e:
      # Handle potential exceptions here
      print(f"Error saving image: {e}")