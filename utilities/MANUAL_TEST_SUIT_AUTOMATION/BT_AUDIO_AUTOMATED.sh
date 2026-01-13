#!/bin/bash
# set -x

#Author : aharil144@cable.comcast.com

source device.conf
source generic_functions.sh

scan_attempts=0

discovered_devices_scan=0

test_step_status="PASS"

paired_list_heading="PAIRED DEVICES DETAILS"

connected_list_heading="CONNECTED DEVICES DETAILS"





#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




#Function to check the Pre-Condition before test TC_EXTERNALAUDIO_MANUAL_01



pre_Check_PairandConnect(){

pre_bt_activate=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc)
sleep 2
JSON_RESPONSE_0_connect=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc)
sleep 1
JSON_RESPONSE_0_pair=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc)
SEARCH_PATTERN_0="\"name\":\"${EXT_BT_devices}\""

pre_paired_Devices_list=$(echo "$JSON_RESPONSE_0_pair" | sed -n 's/.*"pairedDevices":\(\[.*\]\).*/\1/p')

pre_found_device_id=$(echo "$JSON_RESPONSE_0_pair" | grep -o '"deviceID":"[0-9]*"' | cut -d: -f2 | tr -d '"')


if echo "$JSON_RESPONSE_0_pair" | grep -Eq "$SEARCH_PATTERN_0" && echo "$JSON_RESPONSE_0_connect" | grep -Eq "$SEARCH_PATTERN_0"; then

   local json_data=$(printf '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.setAudioStream", "params": {"deviceID": "%s", "audioStreamName": "PRIMARY"}}' "$pre_found_device_id")  
   pre_audio_stream=$(curl -# --header "Content-Type: application/json" --request POST \
   --data "$json_data" \
   http://127.0.0.1:9998/jsonrpc)
   sleep 1
   return 0
else
   if [ -z "$pre_found_device_id" ]; then 
      return 1
   else  
      local json_data=$(printf '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "%s"}}' "$pre_found_device_id")
      local JSON_RESPONSE_pre=$(curl -# --header "Content-Type: application/json" \
                              --request POST \
                              --data "$json_data" \
                              http://127.0.0.1:9998/jsonrpc)
      return 1
   fi   
fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_01 STEP-4 performScan Operation



perform_scan() {

JSON_RESPONSE_4=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "120", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc)
sleep 3

RESULT_VALUE_4=$(echo "$JSON_RESPONSE_4" | sed -n 's/.*"success":\s*\(true\|false\).*/\1/p')

 if [[ "$RESULT_VALUE_4" == 'true' ]]; then 
   return 0
 else
   return 1
 fi
}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_01 STEP-2 check_Bluetooth_status operation



check_Bluetooth_status() {

JSON_RESPONSE_2=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc)
sleep 2

 if echo "$JSON_RESPONSE_2" | grep -q '"state":"activated"'; then
     return 0
 else
     return 1
 fi    
}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_01 STEP-5 perform_scan_and_get_target_devices Operation



perform_scan_and_get_target_devices() {

found_device_id=""

JSON_RESPONSE_5=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc)
sleep 5

while [ "$discovered_devices_scan" -lt "$max_scan_discovered_devices" ]; do
   discovered_devices_scan=$((discovered_devices_scan + 1))
   discovered_devices=$(echo "$JSON_RESPONSE_5" | sed -n 's/.*"discoveredDevices":\(\[.*\]\),"success":true}}.*/\1/p')
   if [ -z "$discovered_devices" ]; then
      printf "\n\ndiscoveredDevices is empty. Checking again in 5 seconds...\n\n"
      sleep 5
   else
      sleep 1
      printf "\n\nDiscoveredDevices list is not empty. Proceeding to pair External Bluetooth Speaker\n\n"
      printf "..................................................................| DiscoveredDevices LIST |.................................................................\n\n"
      printf "%s" "$discovered_devices"
      printf "\n.............................................................................................................................................................\n\n"
      break
   fi
done

target_device_name="$EXT_BT_devices"
echo -e "\nChecking for "$EXT_BT_devices" in DiscoveredDevices LIST....\n\n"
local first_match_target_device=$(echo "$discovered_devices" | \
   sed 's/},{/}\n{/g' | \
   grep -E -m 1 "\"name\":\"$target_device_name\"" | \
   sed -E 's/.*"deviceID":"([^"]+)".*"name":"([^"]+)".*/\1 \2/')
if [ -n "$first_match_target_device" ]; then
   read -r found_device_id found_device_name <<< "$first_match_target_device"
   echo -e "External Bluetooth Device $found_device_name found\n\n"
   echo -e "External Bluetooth Device   :\t$found_device_name\nExternal Bluetooth DeviceID :\t$found_device_id\n\n"
   return 0
else
   return 1
fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_testsuite STEP-6 pair_target_device Operation



pair_target_device() {

  local json_data=$(printf '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "%s"}}' "$found_device_id")
  local JSON_RESPONSE_6=$(curl -# --header "Content-Type: application/json" \
                           --request POST \
                           --data "$json_data" \
                           http://127.0.0.1:9998/jsonrpc)
   sleep 2                        

   RESULT_VALUE_5=$(echo "$JSON_RESPONSE_6" | sed -n 's/.*"success":\s*\(true\|false\).*/\1/p')

   if [[ "$RESULT_VALUE_5" == 'true' ]]; then 
      return 0
   else
      return 1
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_testsuite STEP-14 unpair_target_device Operation



unpair_target_device() {

   local json_data=$(printf '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "%s"}}' "$1")
   local JSON_RESPONSE_14=$(curl -# --header "Content-Type: application/json" \
                           --request POST \
                           --data "$json_data" \
                           http://127.0.0.1:9998/jsonrpc)
   sleep 2

   RESULT_VALUE_6=$(echo "$JSON_RESPONSE_14" | sed -n 's/.*"success":\s*\(true\|false\).*/\1/p')

   if [[ "$RESULT_VALUE_6" == 'true' ]]; then 
      return 0
   else
      return 1
   fi                        
}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_01 STEP-7 get_paired_target_device Operation



get_paired_target_device() {

   JSON_RESPONSE_7=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc)
   local SEARCH_PATTERN="\"deviceID\":\"${1}\".*\"name\":\"${EXT_BT_devices}\""

   paired_Devices_list=$(echo "$JSON_RESPONSE_7" | sed -n 's/.*"pairedDevices":\(\[.*\]\).*/\1/p')
   sleep 2

   if echo "$JSON_RESPONSE_7" | grep -Eq "$SEARCH_PATTERN"; then
      return 0
   else
      return 1
   fi 
}



#Function Definition for Listing Paired device details of TC_EXTERNALAUDIO_MANUAL_01



display_paired_connected_Devices() {
     
   echo " "
   echo " "
   echo -e "\n..................................................................| $2 |.................................................................\n\n"
   echo "$1"
   echo " "
   echo -e ".............................................................................................................................................................\n\n"

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_suite STEP-8 connect_paired_device Operation



connect_paired_target_device() {

   local json_data=$(printf '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "%s", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' "$found_device_id")
   local JSON_RESPONSE_8=$(curl -# --header "Content-Type: application/json" \
                           --request POST \
                           --data "$json_data" \
                           http://127.0.0.1:9998/jsonrpc)
   sleep 3                       

   RESULT_VALUE_8=$(echo "$JSON_RESPONSE_8" | sed -n 's/.*"success":\s*\(true\|false\).*/\1/p')

   if [[ "$RESULT_VALUE_8" == 'true' ]]; then 
      return 0
   else
      return 1
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_suite STEP-12 disconnect_paired_device Operation



disconnect_paired_target_device() {

   local json_data=$(printf '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.disconnect", "params": {"deviceID": "%s"}}' "$1")
   local JSON_RESPONSE_11=$(curl -# --header "Content-Type: application/json" \
                           --request POST \
                           --data "$json_data" \
                           http://127.0.0.1:9998/jsonrpc)
   sleep 2                       

   RESULT_VALUE_9=$(echo "$JSON_RESPONSE_11" | sed -n 's/.*"success":\s*\(true\|false\).*/\1/p')

   if [[ "$RESULT_VALUE_9" == 'true' ]]; then 
      return 0
   else
      return 1
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_01 STEP-9 get_connected_target_device Operation



get_connected_target_device() {

   sleep 2 
   local JSON_RESPONSE_9=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc)
   local SEARCH_PATTERN="\"deviceID\":\"${1}\".*\"name\":\"${EXT_BT_devices}\""

   connected_Devices_list=$(echo "$JSON_RESPONSE_9" | sed -n 's/.*"connectedDevices":\(\[.*\]\).*/\1/p')
   sleep 3

   if echo "$JSON_RESPONSE_9" | grep -Eq "$SEARCH_PATTERN"; then
      return 0
   else
      return 1
   fi 
}



#Function Definition for get_DeviceVolume_and_Mute_Info operation used in TC_EXTERNALAUDIO_MANUAL_05



get_DeviceVolume_and_Mute_Info() {

   sleep 2
   local device_id="$1"
   local fun_choice="$2"
   local json_data=$(printf '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.getDeviceVolumeMuteInfo", "params": {"deviceID": "%s", "deviceType": "WEARABLE HEADSET"}' "$device_id")
   local JSON_RESPONSE_15=$(curl -# --header "Content-Type: application/json" --request POST --data "$json_data"  http://127.0.0.1:9998/jsonrpc)
   
   volume_val=$(echo "$JSON_RESPONSE_15" | grep -o '"volume":"[0-9]*"' | cut -d':' -f2 | tr -d '"')
   mute_info=$(echo "$JSON_RESPONSE_15" | grep -o '"mute":[a-z]*' | cut -d':' -f2)
   
   if [[ "$fun_choice" == "get_mute_status" ]]; then
      if [[ -n "$mute_info" && "$mute_info" == "false" ]]; then
         return 0     # Unmuted state
      else
         return 1     # muted state
      fi   
   else
      if [[ -n "$volume_val" ]]; then
         return 0    
      else
         return 1
      fi
   fi 

}



#Function Definition for set_DeviceVolume_and_Mute_status operation used in TC_EXTERNALAUDIO_MANUAL_05 



set_DeviceVolume_and_Mute_status() {

   sleep 2
   local device_id="$1"
   local fun_choice="$2"
   local vol_type="$3"
   shift 3
   if [[ "$fun_choice" == "set_mute_status" ]]; then
      local default_volume="$1"
      local mute_value="${@: -1}"
      local json_data=$(printf '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.setDeviceVolumeMuteInfo", "params": {"deviceID": "%s", "deviceType": "WEARABLE HEADSET", "volume": "%s", "mute": "%s"}}' "$device_id" "$default_volume" "$mute_value")
      local JSON_RESPONSE_16=$(curl -# --header "Content-Type: application/json" --request POST --data "$json_data" http://127.0.0.1:9998/jsonrpc)
      RESULT_VALUE_10=$(echo "$JSON_RESPONSE_16" | sed -n 's/.*"success":\s*\(true\|false\).*/\1/p')
      if [[ "$RESULT_VALUE_10" == 'true' ]]; then 
         return 0
      else
         return 1
      fi 
   else
      local mute_value="${@: -1}"
      local volume_levels=("${@:1:$#-1}")
      local counter=0
      for vol in "${volume_levels[@]}"; do
         printf "\nSetting the Volume level of %s BT device with Value : %s\n\n\n\n" "$EXT_BT_devices" "$vol"
         local json_data=$(printf '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.setDeviceVolumeMuteInfo", "params": {"deviceID": "%s", "deviceType": "WEARABLE HEADSET", "volume": "%s", "mute": "%s"}}' "$device_id" "$vol" "$mute_value")
         local JSON_RESPONSE_16=$(curl -# --header "Content-Type: application/json" --request POST --data "$json_data" http://127.0.0.1:9998/jsonrpc)
         RESULT_VALUE_11=$(echo "$JSON_RESPONSE_16" | sed -n 's/.*"success":\s*\(true\|false\).*/\1/p')
         if [[ "$RESULT_VALUE_11" == 'true' ]]; then
            local fun_choice_1="get_volume_level"
            get_DeviceVolume_and_Mute_Info "$device_id" "$fun_choice_1"
            local fun_exit_get_DeviceVolume=$?

            if [ "$fun_exit_get_DeviceVolume" -eq 0 ]; then
               if [[ "$vol" == "$volume_val" ]]; then
                  local user_choice_1="user_choice_1"
                  local Query_1="Volume level set to ${vol}. Has the volume level ${vol_type}d in ${EXT_BT_devices} BT device? [yes/no]: "
                  sleep 2
                  printf "\n"
                  user_confirmation "$user_choice_1" "$Query_1"
                  local fun_exit_status29=$?
               
                  if [ "$fun_exit_status29" -eq 0 ]; then
                     counter=$(( counter + 1))
                     printf "\n\nVolume level has %sd in %s BT device. org.rdk.Bluetooth.getDeviceVolumeMuteInfo API return value : %s\n\n\n" "$vol_type" "$EXT_BT_devices" "$volume_val"
                  else
                     printf "\n\nVolume level didn't %sd in %s BT device. But org.rdk.Bluetooth.getDeviceVolumeMuteInfo API return value : %s\n\n\n" "$vol_type" "$EXT_BT_devices" "$volume_val"
                  fi
               else
                  printf "\n\nEven After setting Volume level to %s. org.rdk.Bluetooth.getDeviceVolumeMuteInfo API return incorrect value : %s\n\n\n" "$vol" "$volume_val" 
                  return 1
               fi
            else
               printf '\n\norg.rdk.Bluetooth.getDeviceVolumeMuteInfo API returns empty Value for Volume from %s BT device\n\n\n\n' "$EXT_BT_devices"
               return 1 
            fi        
         else
            printf "\n\nUnable to %s volume level. org.rdk.Bluetooth.setDeviceVolumeMuteInfo API execution returns value : %s\n\n\n" "$vol_type" "$RESULT_VALUE_11" 
            return 1
         fi
      done
      local total_volume_values=${#volume_levels[@]}
      if [[ "$counter" == "$total_volume_values" ]]; then 
         return 0
      else
         return 1
      fi           

   fi
   
}



#Function Definition for getDeviceInfo operation used in TC_EXTERNALAUDIO_MANUAL_05 


extract_getDeviceInfo() {
 
   sleep 2
   deviceInfo_check_flag=0
   local device_id="$1"
   local fun_choice="$2"
   local json_data=$(printf '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.getDeviceInfo", "params": {"deviceID": "%s"}}' "$device_id")
   local JSON_RESPONSE_17=$(curl -# --header "Content-Type: application/json" --request POST --data "$json_data" http://127.0.0.1:9998/jsonrpc)
   RESULT_VALUE_12=$(echo "$JSON_RESPONSE_17" | sed -n 's/.*"success":\s*\(true\|false\).*/\1/p')
   
   if [[ "$RESULT_VALUE_12" == 'true' ]]; then
      case "$fun_choice" in 
         1)
            local SEARCH_PATTERN="\"deviceID\":\"${device_id}\".*\"name\":\"${EXT_BT_devices}\""
            if echo "$JSON_RESPONSE_17" | grep -Eq "$SEARCH_PATTERN"; then
               return 0
            else
               return 1
            fi
            ;;
         2)
            sleep 1
            mac_address_bt=$(echo "$JSON_RESPONSE_17" | grep -o '"MAC":"[^"]*"' | sed 's/"MAC":"//;s/"//') 
            if echo "$mac_address_bt" | grep -Eq '^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$'; then
               return 0
            else
               return 1
            fi
            ;;
         3)
            sleep 1
            manufacturerID_bt=$(echo "$JSON_RESPONSE_17" | grep -o '"manufacturer":"[^"]*"' | sed 's/"manufacturer":"//;s/"//')
            if [[ -n "$manufacturerID_bt" ]]; then
               return 0    
            else
               return 1
            fi
            ;;
         4)
            sleep 1
            device_Type_bt=$(echo "$JSON_RESPONSE_17" | grep -o '"deviceType":"[^"]*"' | sed 's/"deviceType":"//;s/"//')
            if [[ -n "$device_Type_bt" ]]; then
               return 0    
            else
               return 1
            fi
            ;;
         5)
            sleep 1
            battery_per_bt=$(echo "$JSON_RESPONSE_17" | grep -o '"batteryLevel":"[0-9]*"' | sed 's/"batteryLevel":"//;s/"//')
            if [[ "$battery_per_bt" != "0" ]]; then
               return 0    
            else
               return 1
            fi
            ;;   
         *)
            printf '\nInvalid parameter choice\n\n'
            return 1
            ;;
      esac         
   
   else
      deviceInfo_check_flag=1
      return 1  
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_suite STEP_10 



TC_EXTERNALAUDIO_MANUAL_01_STEP_10() {

   
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $1\t\t: Execute curl command to Start AV playback in VA Device to start Audio Streaming in BT device\n\n\n" 
         
   echo -e "curl -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "YouTube.1.deeplink","params":$yt_URL}' http://localhost:9998/jsonrpc \n\ncurl --data-binary '{"jsonrpc": "2.0", "id": 1234567890, "method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "HtmlApp", "type":"", "uri":"$htmlApp_launch_URL"}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc\n\n\n"
   sleep 2

   AV_playback_mode "YouTube"

   local fun_exit_status8=$?
      
   if [ "$fun_exit_status8" -eq 0 ]; then
      echo " "
      echo -e "AV playback started successfully in VA device and Audio Streaming started in BT device\n"
      return 0
   else
      echo " "
      echo -e "Unable to start AV playback in VA device. Audio Streaming via BT device FAILED\n"
      echo -e "Skipping remaining steps and marked as NT\n\n" 
      return 1
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_suite STEP_11 



TC_EXTERNALAUDIO_MANUAL_01_STEP_11() {

   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $1\t\t: AV streaming via External BT device Verification based on User's experience\n\n\n"  
   user_choice_1="user_choice_1"
   Query_1="Are you able to hear the Audio streaming via ${EXT_BT_devices} BT device? [yes/no]: "

   user_confirmation "$user_choice_1" "$Query_1"

   local fun_exit_status9=$?

   if [ "$fun_exit_status9" -eq 0 ]; then
      echo " "
      echo -e "Able to hear the Audio streaming via $EXT_BT_devices BT device\n"
      return 0
   else
      echo " "
      echo -e "Unable to hear the Audio. Audio streaming is not happening via $EXT_BT_devices BT device\n"
      echo -e "Skipping remaining steps and marked as NT\n\n" 
      return 1
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_suite STEP_12 



TC_EXTERNALAUDIO_MANUAL_01_STEP_12() {

   local device_id="$2"
   local step_num="$1"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to Disconnect the paired device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.disconnect", "params": {"deviceID": "$device_id"}}' http://127.0.0.1:9998/jsonrpc \n\n"
   sleep 2
   
   disconnect_paired_target_device "$device_id"

   local fun_exit_status13=$?

   if [ "$fun_exit_status13" -eq 0 ]; then
         echo " "
         echo -e "org.rdk.Bluetooth.1.disonnect API execution success and returns $RESULT_VALUE_9\n"
         return 0
   else
         echo " "
         echo -e "org.rdk.Bluetooth.1.disconnect API execution failure, Returned value is : $RESULT_VALUE_9\n\n\n" 
         return 1
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_suite STEP_13



TC_EXTERNALAUDIO_MANUAL_01_STEP_13() {

   local device_id="$2"
   local step_num="$1"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to verify the Disconnection of paired device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc \n\n"
   sleep 2

   get_connected_target_device "$device_id" 

   local fun_exit_status15=$?

   if [ "$fun_exit_status15" -eq 0 ]; then
         echo " "
         echo -e "External Bt device \"$EXT_BT_devices\" still in connected state. Disconnection failed\n\n\n"
         return 0
   else
         echo " "
         echo -e "External Bt device \"$EXT_BT_devices\" disconnected successfully\n\n\n"
         return 1
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_suite STEP_14



TC_EXTERNALAUDIO_MANUAL_01_STEP_14() {

   local device_id="$2"
   local step_num="$1"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to Unpair the paired device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "$device_id"}}' http://127.0.0.1:9998/jsonrpc \n\n"
   sleep 2
   
   unpair_target_device "$device_id"

   local fun_exit_status17=$?

   if [ "$fun_exit_status17" -eq 0 ]; then
         echo " "
         echo -e "org.rdk.Bluetooth.1.unpair API execution success and returns $RESULT_VALUE_6 \n\n\n"
         return 0
   else
         echo " "
         echo -e "org.rdk.Bluetooth.1.unpair API execution failure, Returned value is : $RESULT_VALUE_6\n\n\n"
         return 1
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_suite STEP_15



TC_EXTERNALAUDIO_MANUAL_01_STEP_15() {

   local device_id="$2"
   local step_num="$1"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to confirm the unpair functionality of paired device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc \n\n"
   sleep 2 

   get_paired_target_device "$device_id"

   local fun_exit_status19=$?

   if [ "$fun_exit_status19" -eq 0 ]; then
         echo " "
         echo -e "External Bt device \"$EXT_BT_devices\" still in paired state. Unpairing failed\n\n\n"
         return 0
   else
         echo " "
         echo -e "External Bt device \"$EXT_BT_devices\" unpaired successfully\n\n\n"
         return 1
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_04  STEP_12 



TC_EXTERNALAUDIO_MANUAL_04_STEP_12() {

   local step_num="$1"
   local device_id="$2"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Audio streaming behaviour after rebooting the External BT device\n\n\n"
   printf 'Reboot the External Bt Device and wait...\n\n\n'
   sleep 3
   local user_choice_1="user_choice_1"
   local Query_1="Are you able to hear the Audio streaming via ${EXT_BT_devices} BT device few seconds after reboot? [yes/no]: "

   user_confirmation "$user_choice_1" "$Query_1"
   local fun_exit_status21=$?

   if [ "$fun_exit_status21" -eq 0 ]; then
      printf '\nAudio streaming via %s is still active even few seconds after reboot\n\n\n' "$EXT_BT_devices"
      return 0
   else
      sleep 15
      get_connected_target_device "$device_id"
      local fun_exit_status22=$?
      if [ "$fun_exit_status22" -eq 0 ]; then
         echo -e "External Bt device \"$EXT_BT_devices\" still in connected state after reboot. But Audio streaming stopped\n\n\n"
         return 1
      else
         printf '\nAudio streaming via %s stopped and disconnected after reboot\n\n\n' "$EXT_BT_devices"
         return 1
      fi   
   fi   

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_04  STEP_13 



TC_EXTERNALAUDIO_MANUAL_04_STEP_13() {

   local device_id="$2"
   local step_num="$1"
   local reconnect_flag=1
   local reconnect_check=0
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to confirm the auto-reconnect functionality of DUT after rebooting the Exteranl BT device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc \n\ncurl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc \n\n"
   sleep 2

   printf '\nWaiting 30s for External BT device to reconnects with DUT\n\n\n'
   sleep 30
      while [ "$reconnect_check" -lt "$max_reconnect_check" ]; do
         reconnect_check=$((reconnect_check + 1))
         get_connected_target_device "$device_id"
         local fun_exit_status23=$?
         if [ "$fun_exit_status23" -eq 0 ]; then
            printf "\nExternal Bt device \"%s\" auto-reconnect with DUT successfully after reboot\n\n" "$EXT_BT_devices"
            display_paired_connected_Devices "$connected_Devices_list" "$connected_list_heading"
            display_paired_connected_Devices "$pre_paired_Devices_list" "$paired_list_heading"
            reconnect_flag=0
            return 0
            break       
         else
            echo " "
            echo -e "\nExternal BT device still in disconnected state. Checking again in 20 seconds...\n\n"
            sleep 20
         fi   
      done

      if [ "$reconnect_flag" != 0 ]; then
         echo -e "\nExternal Bluetooth Device \"$EXT_BT_devices\" is in disconnected state even after $max_reconnect_check auto-reconnect check\n\n\n"
         return 1
      fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_05  STEP_12 



TC_EXTERNALAUDIO_MANUAL_05_STEP_12() {

   local device_id="$2"
   local step_num="$1"
   local choice_2="set_mute_status"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to verify Volume Control setting Mute while Audio streaming through external BT device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.setDeviceVolumeMuteInfo", "params": {"deviceID": "$device_id", "deviceType": "WEARABLE HEADSET", "volume": "$default_volume_level", "mute": "1"}}' http://127.0.0.1:9998/jsonrpc \n\n"
   sleep 2
   
   printf '\nChecking the Current Mute status of %s BT device\n\n\n' "$EXT_BT_devices"
   local choice_1="get_mute_status"
   local mute_set=1
   local volume_type="normal"
   sleep 1
   get_DeviceVolume_and_Mute_Info "$device_id" "$choice_1"
   local fun_exit_status27=$?

   if [ "$fun_exit_status27" -eq 0 ]; then
         printf "\n\nDevice currently in Unmuted state. Returned Value for mute : %s and able to hear the Audio streaming via %s BT device\n\n\n" "$mute_info" "$EXT_BT_devices"
         printf "\nSetting the mute value as %s to Mute the Audio streaming via External BT device\n\n\n" "$mute_set"
         sleep 2
         set_DeviceVolume_and_Mute_status "$device_id" "$choice_2" "$volume_type" "$default_volume_level" "$mute_set"
         local fun_exit_status30=$?
         
         if [ "$fun_exit_status30" -eq 0 ]; then
            local user_choice_2="user_choice_2"
            local Query_2="Are you able to hear the Audio streaming via ${EXT_BT_devices} BT device? [yes/no]: "
            printf "\n"
            user_confirmation "$user_choice_2" "$Query_2"
            local fun_exit_status31=$?
            
            if [ "$fun_exit_status31" -eq 0 ]; then
               printf '\nAble to hear Audio streaming via %s BT device even after its muted\n\n\n\n' "$EXT_BT_devices"
               return 1
            else
               printf '\nUnable to hear audio. Audio streaming via %s BT device is muted.\n\n\n\n' "$EXT_BT_devices" 
               return 0
            fi
         else
            printf "\nSetting the mute value as %s to Mute the Audio streaming failed. org.rdk.Bluetooth.setDeviceVolumeMuteInfo API returns : %s\n\n\n" "$mute_set" "$RESULT_VALUE_10"
            return 1
         fi   
   else
      printf '\n%s BT device already in muted state and org.rdk.Bluetooth.getDeviceVolumeMuteInfo API returns : %s\n\n\n' "$EXT_BT_devices" "$mute_info"
      return 1   
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_05  STEP_13 



TC_EXTERNALAUDIO_MANUAL_05_STEP_13() {

   local device_id="$2"
   local step_num="$1"
   local choice="get_mute_status"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to verify Volume Control get Mute status while Audio streaming through external BT device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.getDeviceVolumeMuteInfo", "params": {"deviceID": "$device_id", "deviceType": "WEARABLE HEADSET"}' http://127.0.0.1:9998/jsonrpc \n\n"
   sleep 2
   get_DeviceVolume_and_Mute_Info "$device_id" "$choice"
   local fun_exit_status33=$?

   if [ "$fun_exit_status33" -eq 0 ]; then
      printf "\n%s BT device current mute status [ Unmuted ] returned value : %s.\n\n\n" "$EXT_BT_devices" "$mute_info"
      return 1
   else
      printf "\n%s BT device current mute status [ Muted ] returned value : %s.\n\n\n" "$EXT_BT_devices" "$mute_info"
      return 0
   fi      

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_05  STEP_14 



TC_EXTERNALAUDIO_MANUAL_05_STEP_14() {

   local device_id="$2"
   local step_num="$1"
   local choice_2="set_mute_status"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to verify Volume Control setting UnMute while Audio streaming through external BT device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.setDeviceVolumeMuteInfo", "params": {"deviceID": "$device_id", "deviceType": "WEARABLE HEADSET", "volume": "$default_volume_level", "mute": "0"}}' http://127.0.0.1:9998/jsonrpc \n\n"
   sleep 2

   printf '\nChecking the Current Mute status of %s BT device\n\n\n' "$EXT_BT_devices"
   local choice_1="get_mute_status"
   local mute_set=0
   local volume_type="normal"
   sleep 1
   get_DeviceVolume_and_Mute_Info "$device_id" "$choice_1"
   local fun_exit_status35=$?

   if [ "$fun_exit_status35" -eq 0 ]; then
      printf "\nDevice currently in Unmuted state. Returned Value for mute : %s and able to hear the Audio streaming via %s BT device\n\n\n" "$mute_info" "$EXT_BT_devices"
      return 1 
   else
      printf '\n\n%s BT device currently in muted state and org.rdk.Bluetooth.getDeviceVolumeMuteInfo API returns : %s\n\n\n' "$EXT_BT_devices" "$mute_info"
      printf "\nSetting the mute value as %s to UnMute the Audio streaming via External BT device\n\n\n" "$mute_set"
      sleep 2
      set_DeviceVolume_and_Mute_status "$device_id" "$choice_2" "$volume_type" "$default_volume_level" "$mute_set"
      local fun_exit_status36=$?
      
      if [ "$fun_exit_status36" -eq 0 ]; then
         local user_choice_2="user_choice_2"
         local Query_2="Are you able to hear the Audio streaming via ${EXT_BT_devices} BT device? [yes/no]: "
         printf "\n"
         user_confirmation "$user_choice_2" "$Query_2"
         local fun_exit_status37=$?
         
         if [ "$fun_exit_status37" -eq 0 ]; then
            printf '\nAble to hear Audio streaming via %s BT device after it is Unmuted\n\n\n\n' "$EXT_BT_devices"
            return 0
         else
            printf '\nUnable to hear audio. Audio streaming via %s BT device is muted.\n\n\n\n' "$EXT_BT_devices" 
            return 1
         fi
      else
         printf "\nSetting the mute value as %s to UnMute the Audio streaming failed. org.rdk.Bluetooth.setDeviceVolumeMuteInfo API returns : %s\n\n\n" "$mute_set" "$RESULT_VALUE_10"
         return 1
      fi
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_06  STEP_12 



TC_EXTERNALAUDIO_MANUAL_06_STEP_12() {

   local device_id="$2"
   local step_num="$1"
   local volume_type="$3"
   local choice_2="set_volume_levels"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to verify Volume $volume_type while Audio streaming through external BT device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.setDeviceVolumeMuteInfo", "params": {"deviceID": "$device_id", "deviceType": "WEARABLE HEADSET", "volume": "$default_volume_level", "mute": "0"}}' http://127.0.0.1:9998/jsonrpc \n\n"
   sleep 2

   printf '\nChecking the Current Volume level of %s BT device\n\n\n' "$EXT_BT_devices"
   local choice_1="get_volume_levels"
   local mute_set=0
   sleep 1
   get_DeviceVolume_and_Mute_Info "$device_id" "$choice_1"
   local fun_exit_status40=$?

   if [ "$fun_exit_status40" -eq 0 ]; then
      printf "\n%s BT device current Volume level : %s\n\n\n\n" "$EXT_BT_devices" "$volume_val"
      sleep 2
      printf "\nVolume Level of %s BT device %ss\n\n\n\n" "$EXT_BT_devices" "$volume_type"
      set_DeviceVolume_and_Mute_status "$device_id" "$choice_2" "$volume_type" "${@:4:3}" "$mute_set"
      local fun_exit_status41=$?
      
      if [ "$fun_exit_status41" -eq 0 ]; then
         printf '\nAble to hear %sed volume levels during Audio streaming via %s BT device\n\n\n\n' "$volume_type" "$EXT_BT_devices" 
         return 0
      else 
         printf '\nUnable to hear %sed volume levels during Audio streaming via %s BT device\n\n\n\n' "$volume_type" "$EXT_BT_devices"
         return 1
      fi     
   else
      printf '\norg.rdk.Bluetooth.getDeviceVolumeMuteInfo API returns empty Value for Volume during Audio streaming via %s BT device\n\n\n\n' "$EXT_BT_devices"
      return 1
   fi   
   
}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_07 STEPS



TC_EXTERNALAUDIO_MANUAL_07_STEPS() {

   local device_id="$2"
   local step_num="$1"
   local choice="$3"
   local device_info_param="$4"
   local device_info_param_ID="$5"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n"
   echo " "
   echo -e "Step $step_num\t\t: Execute curl command to verify the $device_info_param from API response of connected external BT Device\n\n\n"
   echo -e "curl --header "Content-Type: application/json" --request POST --data ' {"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.getDeviceInfo", "params": {"deviceID": "$device_id"}}' http://127.0.0.1:9998/jsonrpc \n\n"
   extract_getDeviceInfo "$device_id" "$choice"
   if [[ "$device_info_param_ID" -eq 2 ]]; then
      extracted_deviceinfo="$mac_address_bt"
   elif [[ "$device_info_param_ID" -eq 3 ]]; then  
      extracted_deviceinfo="$manufacturerID_bt"
   elif [[ "$device_info_param_ID" -eq 4 ]]; then
      extracted_deviceinfo="$device_Type_bt"
   elif [[ "$device_info_param_ID" -eq 5 ]]; then
      extracted_deviceinfo="$battery_per_bt"   
   else
      extracted_deviceinfo=" "
   fi 

   local fun_exit_status46=$?
      
   if [ "$fun_exit_status46" -eq 0 ]; then
      printf '\norg.rdk.Bluetooth.getDeviceInfo API returns %s of %s Bt device\n\n\n' "$RESULT_VALUE_12" "$EXT_BT_devices" 
      if [[ "$choice" -gt 1 ]]; then
         printf "\n%s BT device's %s  :  %s\n\n\n" "$EXT_BT_devices" "$device_info_param" "$extracted_deviceinfo"
      fi   
      return 0
   else
      if [[ "$deviceInfo_check_flag" -eq 1 ]]; then
         printf "\n\norg.rdk.Bluetooth.getDeviceInfo API returns value : %s\n\n\n" "$RESULT_VALUE_12"
         return 1
      else
         printf "\norg.rdk.Bluetooth.getDeviceInfo API response doesn't have valid %s of %s Bt device\n\n\n" "$device_info_param" "$EXT_BT_devices" 
         return 1
      fi
   fi
   
}



#Function definition for Post-conditions TC_EXTERNALAUDIO_MANUAL



postCondition_Execution_BT_audio() {

   local device_id="$2"
   local test_case_id="$1"
   if [[ "$test_case_id" == "TC_EXTERNALAUDIO_MANUAL_04" ]]; then
      test_step_status="PASS"
      reconnect_check=0
      printf '\n\n\nPostCondition execution Sucess!!!\n\n\n'
   fi 

   if [[ "$test_case_id" == "TC_EXTERNALAUDIO_MANUAL_07" ]]; then
      test_step_status="PASS"
      deviceInfo_check_flag=0
      printf '\n\n\nPostCondition execution Sucess!!!\n\n\n'
   fi

   if [[ "$test_case_id" == "TC_EXTERNALAUDIO_MANUAL_06" ]]; then 
      step1_step10_pass=true
      for ((i=1; i<=10; i++)); do 
         local step_var="tc6_step$i"
         local step_val="${!step_var}"
         
         if [[ "$step_val" != "PASSED" ]]; then
            step1_step10_pass=false
            break
         fi
      done 

      if [[ "$step1_step10_pass" == false ]]; then 
         test_step_status="PASS"
      else   
         test_step_status="PASS"
         local choice_postCon="set_volume_levels"
         local mute_set_post=0
         local volume_type_postCon="normalis"
         sleep 2
         set_DeviceVolume_and_Mute_status "$device_id" "$choice_postCon" "$volume_type_postCon" "$default_volume_level" "$mute_set_post"
         sleep 2
      fi   
   fi    


   if [[ "$test_case_id" == "TC_EXTERNALAUDIO_MANUAL_05" ]]; then
      test_step_status="PASS"
      local choice_postCon="set_mute_status"
      local volume_type_postCon="normal"
      local mute_set_post=0
      sleep 2
      set_DeviceVolume_and_Mute_status "$device_id" "$choice_postCon" "$volume_type_postCon" "$default_volume_level" "$mute_set_post"
      local fun_exit_status39=$?

      if [ "$fun_exit_status39" -eq 0 ]; then
         printf '\n\n\nPostCondition execution Success!!!\n\n\n' "$mute_set_post"
      else
          printf '\n\n\nPostCondition execution Failure!!!\n\n\n' "$mute_set_post"
      fi
      sleep 2
   fi   


   if [[ "$test_case_id" == "TC_EXTERNALAUDIO_MANUAL_02" || "$test_case_id" == "TC_EXTERNALAUDIO_MANUAL_03" || "$test_case_id" == "TC_EXTERNALAUDIO_MANUAL_04" || "$test_case_id" == "TC_EXTERNALAUDIO_MANUAL_05" || "$test_case_id" == "TC_EXTERNALAUDIO_MANUAL_06" ]]; then      
      sleep 2
      local res_var="${testcase_prefix}10"
      if [[ "${!res_var}" == "PASSED" ]]; then
         if [ "$av_check_flag" == 1 ]; then
            printf '\nDeactivating active Youtube instance\n\n'
            JSON_RESPONSE_13_1=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.deactivate", "params": {"callsign": "YouTube"}}' http://127.0.0.1:9998/jsonrpc)
            sleep 2
            preApp_status_check "YouTube"
                        
            cobalt_status_exit_post=$?
      
            if [ "$cobalt_status_exit_post" -eq 0 ]; then
               printf '\nYoutube still in Active state. Deactivation Failed\n\n\n'
            else
               printf '\nAV playback via Youtube stopped and Youtube deactivated\n\n\n'   
            fi
            test_step_status="PASS"
         else
            printf '\nDeactivating active XUMO App instance\n\n\n'   
            JSON_RESPONSE_13_2=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0","id": 1234567890,"method":"Controller.1.deactivate","params": {"callsign": "HtmlApp"}}' http://127.0.0.1:9998/jsonrpc)
            sleep 2
            xumo_status_check

            xumo_status_exit_post=$?

            if [ "$xumo_status_exit_post" -eq 0 ]; then
               printf '\nXUMO App still in Active state. Deactivation Failed\n\n\n'
            else
               printf '\n\nAV playback via XUMO stopped and XUMO App deactivated\n\n\n'   
            fi   
            test_step_status="PASS"
         fi
      else
         test_step_status="PASS"      
         scan_attempts=0
         discovered_devices_scan=0
      fi 

   fi    

}



#Function Definition for TestCase : TC_EXTERNALAUDIO_MANUAL_testsuite



tc_EXTERNALAUDIO_MANUAL_testsuite() {

   TestcaseID="$2"
   testcase_prefix="$1"
   test_step_status="PASS"

   #Precondition Check code block    

   printf "\n"
   printf "Pre-Conditon check\t\t: Checks whether %s BT device is already paired and connected to DUT\n\n" "$EXT_BT_devices"

   pre_Check_PairandConnect

   fun_exit_status_0_pre=$?

   if [ "$fun_exit_status_0_pre" -eq 0 ]; then
      printf "\n"
      printf "\n%s BT device already in paired and connected state\n\n" "$EXT_BT_devices"

      dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
      dynamic_nt_pass_updator "$current_step_num" "PASSED" "1"

      get_paired_target_device "$pre_found_device_id"
      display_paired_connected_Devices "$paired_Devices_list" "$paired_list_heading"

      get_connected_target_device "$pre_found_device_id"
      display_paired_connected_Devices "$connected_Devices_list" "$connected_list_heading"
      printf '\n'

# Step 10 & 11 code block

      if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_02" || "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_03" || "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_04" || "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_05" || "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_06" ]]; then

         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_10=10"
            dynamic_var_name_1="${testcase_prefix}_num_10"
            TC_EXTERNALAUDIO_MANUAL_01_STEP_10 "${!dynamic_var_name_1}"

            fun_exit_status10=$?   

            if [ "$fun_exit_status10" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_1} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}10" "PASSED"

               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_11=11"
                  dynamic_var_name_2="${testcase_prefix}_num_11"
                  TC_EXTERNALAUDIO_MANUAL_01_STEP_11 "${!dynamic_var_name_2}"

                  fun_exit_status11=$?   

                  if [ "$fun_exit_status11" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_2} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}11" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_2} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}11" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 11, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}11" "NT" 
               fi      
            else
               echo -e "Step ${!dynamic_var_name_1} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}10" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 10, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}10" "NT"
         fi 
         dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
      fi

# Step 12 code block for TC_EXTERNALAUDIO_MANUAL_03

      if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_03" ]]; then
         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_12=12"
            dynamic_var_name_5="${testcase_prefix}_num_12"
            TC_EXTERNALAUDIO_MANUAL_01_STEP_12 "${!dynamic_var_name_5}" "$pre_found_device_id"

            fun_exit_status12=$?   

            if [ "$fun_exit_status12" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_5} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}12" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_5} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}12" "FAILED"
            fi
         else
            echo -e "\nSkipping Step 12, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}12" "NT"
         fi            

# Step 13 code block for TC_EXTERNALAUDIO_MANUAL_03

         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_13=13"
            dynamic_var_name_6="${testcase_prefix}_num_13"
            TC_EXTERNALAUDIO_MANUAL_01_STEP_13 "${!dynamic_var_name_6}" "$pre_found_device_id"

            fun_exit_status14=$?

            if [ "$fun_exit_status14" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_6} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}13" "FAILED"
               test_step_status="FAIL"
            else
               echo -e "Step ${!dynamic_var_name_6} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}13" "PASSED"
            fi
         else
            echo -e "\nSkipping Step 13, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}13" "NT"
         fi

# Step 14 code block for TC_EXTERNALAUDIO_MANUAL_03

         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_14=14"
            dynamic_var_name_7="${testcase_prefix}_num_14"
            TC_EXTERNALAUDIO_MANUAL_01_STEP_14 "${!dynamic_var_name_7}" "$pre_found_device_id"

            fun_exit_status16=$?

            if [ "$fun_exit_status16" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_7} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}14" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_7} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}14" "FAILED"
            fi
         else
            echo -e "\nSkipping Step 14, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}14" "NT"
         fi

# Step 15 code block for TC_EXTERNALAUDIO_MANUAL_03

         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_15=15"
            dynamic_var_name_8="${testcase_prefix}_num_15"
            TC_EXTERNALAUDIO_MANUAL_01_STEP_15 "${!dynamic_var_name_8}" "$pre_found_device_id"

            fun_exit_status18=$?

            if [ "$fun_exit_status18" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_8} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}15" "FAILED"
               test_step_status="FAIL"
            else
               echo -e "Step ${!dynamic_var_name_8} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}15" "PASSED"
            fi
         else
            echo -e "\nSkipping Step 15, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}15" "NT"
         fi           
         dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
      fi
   
# Step 12 code block for TC_EXTERNALAUDIO_MANUAL_04         

      if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_04" ]]; then
         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_12=12"
            dynamic_var_name_9="${testcase_prefix}_num_12"
            TC_EXTERNALAUDIO_MANUAL_04_STEP_12 "${!dynamic_var_name_9}" "$pre_found_device_id"

            fun_exit_status20=$?

            if [ "$fun_exit_status20" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_9} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}12" "FAILED"
               test_step_status="FAIL"
            else
               echo -e "Step ${!dynamic_var_name_9} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}12" "PASSED"
            fi
         else
            echo -e "\nSkipping Step 12, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}12" "NT"
         fi

# Step 13 code block for TC_EXTERNALAUDIO_MANUAL_04 

         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_13=13"
            dynamic_var_name_10="${testcase_prefix}_num_13"
            TC_EXTERNALAUDIO_MANUAL_04_STEP_13 "${!dynamic_var_name_10}" "$pre_found_device_id"

            fun_exit_status24=$?

            if [ "$fun_exit_status24" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_10} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}13" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_10} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}13" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 13, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}13" "NT"
         fi
         dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"          
      fi     

# Step 12 code block for TC_EXTERNALAUDIO_MANUAL_05

      if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_05" ]]; then
         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_12=12"
            dynamic_var_name_11="${testcase_prefix}_num_12"
            TC_EXTERNALAUDIO_MANUAL_05_STEP_12 "${!dynamic_var_name_11}" "$pre_found_device_id"

            fun_exit_status26=$?   

            if [ "$fun_exit_status26" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_11} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}12" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_11} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}12" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 12, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}12" "NT"
         fi 

# Step 13 code block for TC_EXTERNALAUDIO_MANUAL_05           

         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_13=13"
            dynamic_var_name_12="${testcase_prefix}_num_13"
            TC_EXTERNALAUDIO_MANUAL_05_STEP_13 "${!dynamic_var_name_12}" "$pre_found_device_id"

            fun_exit_status32=$?   

            if [ "$fun_exit_status32" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_12} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}13" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_12} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}13" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 13, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}13" "NT"
         fi

# Step 14 code block for TC_EXTERNALAUDIO_MANUAL_05   

         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_14=14"
            dynamic_var_name_13="${testcase_prefix}_num_14"
            TC_EXTERNALAUDIO_MANUAL_05_STEP_14 "${!dynamic_var_name_13}" "$pre_found_device_id"

            fun_exit_status34=$?   

            if [ "$fun_exit_status34" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_13} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}14" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_13} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}14" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 14, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}14" "NT"
         fi        

# Step 15 code block for TC_EXTERNALAUDIO_MANUAL_05

         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_15=15"
            dynamic_var_name_14="${testcase_prefix}_num_15"
            TC_EXTERNALAUDIO_MANUAL_05_STEP_13 "${!dynamic_var_name_14}" "$pre_found_device_id"

            fun_exit_status38=$?   

            if [ "$fun_exit_status38" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_14} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}15" "FAILED"
               test_step_status="FAIL"
            else
               echo -e "Step ${!dynamic_var_name_14} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}15" "PASSED"
            fi
         else
            echo -e "\nSkipping Step 15, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}15" "NT"
         fi
         dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
      fi

# Step 12 code block for TC_EXTERNALAUDIO_MANUAL_06

      if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_06" ]]; then
         volume_type_param="increase"
         if [[ "$test_step_status" != "FAIL" ]]; then
            declare "${testcase_prefix}_num_12=12"
            dynamic_var_name_15="${testcase_prefix}_num_12"
            TC_EXTERNALAUDIO_MANUAL_06_STEP_12 "${!dynamic_var_name_15}" "$pre_found_device_id" "$volume_type_param" "${increase_volume[@]}"

            fun_exit_status42=$?   

            if [ "$fun_exit_status42" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_15} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}12" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_15} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}12" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 12, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}12" "NT"
         fi

# Step 13 code block for TC_EXTERNALAUDIO_MANUAL_06

         if [[ "$test_step_status" != "FAIL" ]]; then
            volume_type_param="decrease"
            declare "${testcase_prefix}_num_13=13"
            dynamic_var_name_16="${testcase_prefix}_num_13"
            TC_EXTERNALAUDIO_MANUAL_06_STEP_12 "${!dynamic_var_name_16}" "$pre_found_device_id" "$volume_type_param" "${decrease_volume[@]}"

            fun_exit_status43=$?   

            if [ "$fun_exit_status43" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_16} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}13" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_16} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}13" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 13, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}13" "NT"
         fi
         dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
      fi
      
# Step 10 code block for TC_EXTERNALAUDIO_MANUAL_07

      if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_07" ]]; then
         if [[ "$test_step_status" != "FAIL" ]]; then
            step_choice_1=1
            device_info_type_1="deviceInfo"
            device_info_type_ID_1=1
            declare "${testcase_prefix}_num_10=10"
            dynamic_var_name_17="${testcase_prefix}_num_10"
            TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_17}" "$pre_found_device_id" "$step_choice_1" "$device_info_type_1" "$device_info_type_ID_1"

            fun_exit_status45=$?   

            if [ "$fun_exit_status45" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_17} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}10" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_17} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}10" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 10, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}10" "NT"
         fi
               
# Step 11 code block for TC_EXTERNALAUDIO_MANUAL_07

         if [[ "$test_step_status" != "FAIL" ]]; then
            step_choice_2=2
            device_info_type_2="MAC Address"
            device_info_type_ID_2=2
            declare "${testcase_prefix}_num_11=11"
            dynamic_var_name_18="${testcase_prefix}_num_11"
            TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_18}" "$pre_found_device_id" "$step_choice_2" "$device_info_type_2" "$device_info_type_ID_2"

            fun_exit_status47=$?   

            if [ "$fun_exit_status47" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_18} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}11" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_18} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}11" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 11, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}11" "NT"
         fi
                        
# Step 12 code block for TC_EXTERNALAUDIO_MANUAL_07

         if [[ "$test_step_status" != "FAIL" ]]; then
            step_choice_3=3
            device_info_type_3="manufacturerID"
            device_info_type_ID_3=3
            declare "${testcase_prefix}_num_12=12"
            dynamic_var_name_19="${testcase_prefix}_num_12"
            TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_19}" "$pre_found_device_id" "$step_choice_3" "$device_info_type_3" "$device_info_type_ID_3"

            fun_exit_status48=$?   

            if [ "$fun_exit_status48" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_19} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}12" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_19} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}12" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 12, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}12" "NT"
         fi
                                 
# Step 13 code block for TC_EXTERNALAUDIO_MANUAL_07

         if [[ "$test_step_status" != "FAIL" ]]; then
            step_choice_4=4
            device_info_type_4="deviceType"
            device_info_type_ID_4=4
            declare "${testcase_prefix}_num_13=13"
            dynamic_var_name_20="${testcase_prefix}_num_13"
            TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_20}" "$pre_found_device_id" "$step_choice_4" "$device_info_type_4" "$device_info_type_ID_4"

            fun_exit_status49=$?   

            if [ "$fun_exit_status49" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_20} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}13" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_20} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}13" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 13, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}13" "NT"
         fi
                                          
# Step 14 code block for TC_EXTERNALAUDIO_MANUAL_07

         if [[ "$test_step_status" != "FAIL" ]]; then
            step_choice_5=5
            device_info_type_5="batteryLevel"
            device_info_type_ID_5=5
            declare "${testcase_prefix}_num_14=14"
            dynamic_var_name_21="${testcase_prefix}_num_14"
            TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_21}" "$pre_found_device_id" "$step_choice_5" "$device_info_type_5" "$device_info_type_ID_5"

            fun_exit_status50=$?   

            if [ "$fun_exit_status50" -eq 0 ]; then
               echo -e "Step ${!dynamic_var_name_21} status\t:  PASS\n\n\n"
               update_test_status "${testcase_prefix}14" "PASSED"
            else
               echo -e "Step ${!dynamic_var_name_21} status\t:  FAIL\n\n\n"
               update_test_status "${testcase_prefix}14" "FAILED"
               test_step_status="FAIL"
            fi
         else
            echo -e "\nSkipping Step 14, as the previous step failed\n\n"
            update_test_status "${testcase_prefix}14" "NT"
         fi
         dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
      fi   

      dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}"


#Postcondition code block


      printf '\nExecuting Post-condition Steps for Testcase : %s\n\n\n' "$TestcaseID"
      sleep 3
      postCondition_Execution_BT_audio "$TestcaseID" "$pre_found_device_id"
      printf '\nPost-condition Execution Successfull. Exiting Test Case : %s\n\n\n' "$TestcaseID"

   else 
      echo " "
      echo -e "$EXT_BT_devices BT device not in paired or connected state. Executing from Step 1\n\n"
      

   #Step 1 code block

      
      if [[ "$test_step_status" != "FAIL" ]]; then
         printf "\n_________________________________________________________________________________________________________________________________________________________\n"
         echo " "
         echo -e "Step 1\t\t: Execute curl command to activate org.rdk.Bluetooth plugin\n\n"

         echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc \n" 

         JSON_RESPONSE_1=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc)

         RESULT_VALUE_1=$(echo "$JSON_RESPONSE_1" | sed -n 's/.*"result":\([^,}]*\).*/\1/p')
         sleep 2


         if [[ "$RESULT_VALUE_1" == "null" ]]; then
            echo " "
            echo -e "curl execution success\n"
            echo -e "Step 1 status\t:  PASS\n\n\n"    
            update_test_status "${testcase_prefix}1" "PASSED"
         else
            echo -e "Curl execution failed. Returned value is : $RESULT_VALUE_1\n\n"
            echo -e "Step 1 status\t:  FAIL\n\n\n"
            update_test_status "${testcase_prefix}1" "FAILED"
            test_step_status="FAIL"
         fi
      else
         echo -e "\nSkipping remaining steps and marked as NT\n\n"
      fi    

   #Step 2 code block

      
      if [[ "$test_step_status" != "FAIL" ]]; then
         printf "\n_________________________________________________________________________________________________________________________________________________________\n"
         echo " "
         echo -e "Step 2\t\t: Execute curl command to check the status of org.rdk.Bluetooth plugin\n\n"

         echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc \n"

         check_Bluetooth_status

         fun_exit_status2=$?    

         if [ "$fun_exit_status2" -eq 0 ]; then
            echo " "
            echo -e "org.rdk.Bluetooth plugin is in activated state\n"
            echo -e "Step 2 status\t:  PASS\n\n\n" 
            update_test_status "${testcase_prefix}2" "PASSED"


   #Step 3 code block


            if [[ "$test_step_status" != "FAIL" ]]; then
               printf "\n_________________________________________________________________________________________________________________________________________________________\n"
               echo " "
               echo -e "Step 3\t\t: Execute curl command to enable org.rdk.Bluetooth\n\n"

               echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc \n"

               JSON_RESPONSE_3=$(curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc)
               sleep 2

               RESULT_VALUE_3=$(echo "$JSON_RESPONSE_3" | sed -n 's/.*"result":{\(.*[^}]*\)}.*/\1/p' | sed 's/}$//')
               echo " "

               if [[ "$RESULT_VALUE_3" == '"success":true' ]]; then
                  echo -e "org.rdk.Bluetooth is in enabled state\n"
                  echo -e "Step 3 status\t:  PASS\n\n\n"
                  update_test_status "${testcase_prefix}3" "PASSED"

               else
                  echo " "
                  echo -e "org.rdk.Bluetooth plugin is in disabled state. Returned value is :  $RESULT_VALUE_3\n\n"
                  echo -e "Step 3 status\t:  FAIL\n\n"
                  update_test_status "${testcase_prefix}3" "FAILED"
                  test_step_status="FAIL"
               fi
            else
               echo -e "\nSkipping Step 3, as the previous step failed\n\n"
               update_test_status "${testcase_prefix}3" "NT"
            fi   


   #Step 4 code block

            
            if [[ "$test_step_status" != "FAIL" ]]; then
               printf "\n_________________________________________________________________________________________________________________________________________________________\n"
               echo " "
               echo -e "Step 4\t\t: Execute curl command to start the bluetooth scanning\n\n"

               echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "120", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc \n"
            
               perform_scan

               fun_exit_status1=$?    

               if [ "$fun_exit_status1" -eq 0 ]; then
                  echo " "
                  echo -e "Bluetooth scanning has started...\n"
                  echo -e "Step 4 status\t:  PASS\n\n\n"
                  update_test_status "${testcase_prefix}4" "PASSED"
               else
                  echo " "
                  echo -e "Unable to start Bluetooth scanning. Returned value is :  $RESULT_VALUE_4\n\n"
                  echo -e "Step 4 status\t:  FAIL\n\n"
                  update_test_status "${testcase_prefix}4" "FAILED"
                  test_step_status="FAIL"
               fi
            else
               echo -e "\nSkipping Step 4, as the previous step failed\n\n"
               update_test_status "${testcase_prefix}4" "NT"
            fi
                  

   #Step 5 code block

            if [[ "$test_step_status" != "FAIL" ]]; then
               printf "\n_________________________________________________________________________________________________________________________________________________________\n"
               echo " "
               echo -e "Step 5\t\t: Execute curl command to get discovered devices list\n\n"

               echo -e "curl -# --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc \n"

               sleep "$sleep_timer"

               perform_scan_and_get_target_devices

               fun_exit_status3=$?

               if [ "$fun_exit_status3" -eq 0 ]; then
                  echo -e "External BT device succesfully obtained from discovered devices list\n\n"
                  echo -e "Step 5 status\t:  PASS\n\n\n"
                  update_test_status "${testcase_prefix}5" "PASSED"
               else
                  while [ "$scan_attempts" -lt "$max_scan_retries" ]; do
                        scan_attempts=$((scan_attempts + 1))
                        echo -e "\nExternal Bluetooth Device $target_device_name not found retrying after 5sec\n\n"
                        sleep 5
                        perform_scan
                        perform_scan_fun_return=$?
                        if [ "$perform_scan_fun_return" -eq 0 ]; then
                           sleep 3 
                           perform_scan_and_get_target_devices
                           fun_return=$?
                           if [ "$fun_return" -eq 0 ]; then
                              echo -e "External BT device succesfully obtained from discovered devices list\n"
                              echo -e "Step 5 status\t:  PASS\n\n\n"
                              update_test_status "${testcase_prefix}5" "PASSED"
                              loop_exit=0
                              break 
                           fi    
                        else
                           echo " "
                           echo -e "Bluetooth scanning FAILED...!\n\n"
                           echo -e "Skipping remaining steps and marked as NT\n\n"   
                           break
                        fi    
                  done
                        if [ "$loop_exit" != 0 ]; then
                           echo -e "External Bluetooth Device \"$target_device_name\" not found after $max_scan_retries retries in discovered_device list\n\n"
                           echo -e "Step 5 status\t:  FAIL\n\n"
                           update_test_status "${testcase_prefix}5" "FAILED"
                           test_step_status="FAIL"
                        fi    
               fi
            else
               echo -e "\nSkipping Step 5, as the previous step failed\n\n"
               update_test_status "${testcase_prefix}5" "NT"
            fi      


   #Step 6 code block
         

            if [[ "$test_step_status" != "FAIL" ]]; then
               printf "\n_________________________________________________________________________________________________________________________________________________________\n"
               echo " "
               echo -e "Step 6\t\t: Execute curl command to pair the discovered device\n\n"

               echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "$found_device_id"}}' http://127.0.0.1:9998/jsonrpc \n"
               
               pair_target_device

               fun_exit_status4=$?    

               if [ "$fun_exit_status4" -eq 0 ]; then
                  echo " "
                  echo -e "org.rdk.Bluetooth.1.pair API execution success and returns $RESULT_VALUE_6 \n"
                  echo -e "Step 6 status\t:  PASS\n\n\n"
                  update_test_status "${testcase_prefix}6" "PASSED"
               else
                  echo " "
                  echo -e "org.rdk.Bluetooth.1.pair API execution, Returned value is :  $RESULT_VALUE_6\n\n"
                  echo -e "Step 6 status\t:  FAIL\n\n"
                  update_test_status "${testcase_prefix}6" "FAILED"
                  test_step_status="FAIL"
               fi
            else
               echo -e "\nSkipping Step 6, as the previous step failed\n\n"
               update_test_status "${testcase_prefix}6" "NT"
            fi


   #Step 7 code block


            if [[ "$test_step_status" != "FAIL" ]]; then
               printf "\n_________________________________________________________________________________________________________________________________________________________\n"
               echo " "
               echo -e "Step 7\t\t: Execute curl command to get list of paired device Details\n\n"

               echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc\n" 
               sleep 2
               
               

               get_paired_target_device "$found_device_id"

               fun_exit_status5=$?    

               if [ "$fun_exit_status5" -eq 0 ]; then
                  display_paired_connected_Devices "$paired_Devices_list" "$paired_list_heading"
                  echo -e "\nExternal Bt device \"$target_device_name\" paired succesfully...!!!\n"
                  echo -e "Step 7 status\t:  PASS\n\n\n"
                  update_test_status "${testcase_prefix}7" "PASSED"
               else
                  echo " "
                  echo -e "External Bt device \"$target_device_name\" pairing failed\n\n"
                  echo -e "Step 7 status\t:  FAIL\n\n"
                  update_test_status "${testcase_prefix}7" "FAILED"
                  test_step_status="FAIL"
                  echo -e "Retrying pairing for \"$target_device_name\"\n\n"
                  sleep 3
                  pair_target_device
                  pair_target_device_fun_return=$?

                  if [ "$pair_target_device_fun_return" -eq 0 ]; then

                     get_paired_target_device "$found_device_id"
                     get_paired_target_device_fun_return=$?

                     if [ "$get_paired_target_device_fun_return" -eq 0 ]; then
                           display_paired_connected_Devices "$paired_Devices_list" "$paired_list_heading"
                           echo -e "\nExternal Bt device \"$target_device_name\" paired succesfully on Attempt : 2\n"
                           echo -e "Step 7 status\t:  FAIL\n\n"
                           update_test_status "${testcase_prefix}7" "FAILED"
                           test_step_status="FAIL"
                     else
                           echo " "
                           echo -e "External Bt device \"$target_device_name\" pairing Attempt : 2 failed\n\n"
                           echo -e "Step 7 status\t:  FAIL\n\n"
                           echo -e "Skipping remaining steps and marked as NT\n\n"
                           update_test_status "${testcase_prefix}7" "FAILED"
                           test_step_status="FAIL"
                     fi   
                  else
                     echo " "
                     echo -e "org.rdk.Bluetooth.1.pair API execution, Returned value is :  $RESULT_VALUE_6\n\n"
                     echo -e "Skipping remaining steps and marked as NT\n\n" 
                     update_test_status "${testcase_prefix}7" "FAILED"
                     test_step_status="FAIL"    
                  fi
               fi
            else
               echo -e "\nSkipping Step 7, as the previous step failed\n\n"
               update_test_status "${testcase_prefix}7" "NT"
            fi  


   #Step 8 code block

            
            if [[ "$test_step_status" != "FAIL" ]]; then
               printf "\n_________________________________________________________________________________________________________________________________________________________\n"
               echo " "
               echo -e "Step 8\t\t: Execute curl command to connect the paired device\n\n"

               echo -e "curl --header "Content-Type: application/json" --request POST --data ' {"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "$found_device_id", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc\n"
               sleep 2

               connect_paired_target_device

               fun_exit_status6=$?
            
               if [ "$fun_exit_status6" -eq 0 ]; then
                  echo " "
                  echo -e "org.rdk.Bluetooth.1.connect API execution success and returns $RESULT_VALUE_8\n"
                  echo -e "Step 8 status\t:  PASS\n\n\n"
                  update_test_status "${testcase_prefix}8" "PASSED"
               else
                  echo " "
                  echo -e "org.rdk.Bluetooth.1.connect API execution, Returned value is : $RESULT_VALUE_8\n\n"
                  echo -e "Step 8 status\t:  FAIL\n\n"
                  update_test_status "${testcase_prefix}8" "FAILED"
                  test_step_status="FAIL" 
               fi
            else
               echo -e "\nSkipping Step 8, as the previous step failed\n\n"
               update_test_status "${testcase_prefix}8" "NT"
            fi


   #Step 9 code block

            
            if [[ "$test_step_status" != "FAIL" ]]; then
               printf "\n_________________________________________________________________________________________________________________________________________________________\n"
               echo " "
               echo -e "Step 9\t\t: Execute curl command to get list of connected device Details\n\n"

               echo -e "curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc\n" 
               sleep 2

               get_connected_target_device "$found_device_id"

               fun_exit_status7=$?
               
               if [ "$fun_exit_status7" -eq 0 ]; then
                  display_paired_connected_Devices "$connected_Devices_list" "$connected_list_heading"
                  echo -e "\nExternal Bt device \"$target_device_name\" connected succesfully...!!!\n"
                  echo -e "Step 9 status\t:  PASS\n\n\n"
                  update_test_status "${testcase_prefix}9" "PASSED"
               else
                  echo " "
                  echo -e "External Bt device \"$target_device_name\" connection failed\n\n"
                  echo -e "Step 9 status\t:  FAIL\n\n"
                  update_test_status "${testcase_prefix}9" "FAILED"
                  test_step_status="FAIL"
                  echo -e "Retrying connection for \"$target_device_name\"\n\n"
                  sleep 3
                  connect_paired_target_device
                  connect_paired_target_device_fun_return=$?

                  if [ "$connect_paired_target_device_fun_return" -eq 0 ]; then

                     get_connected_target_device "$found_device_id"
                     get_connected_target_device_fun_return=$?

                     if [ "$get_connected_target_device_fun_return" -eq 0 ]; then
                        display_paired_connected_Devices "$connected_Devices_list" "$connected_list_heading"
                        echo -e "\nExternal Bt device \"$target_device_name\" connected succesfully on Attempt : 2\n"
                        echo -e "Step 9 status\t:  FAIL\n\n"
                        update_test_status "${testcase_prefix}9" "FAILED"
                        test_step_status="FAIL"
                     else
                        echo " "
                        echo -e "External Bt device \"$target_device_name\" connecting Attempt : 2 failed\n\n"
                        echo -e "Step 9 status\t:  FAIL\n\n"
                        update_test_status "${testcase_prefix}9" "FAILED"
                        echo -e "Skipping remaining steps and marked as NT\n\n"
                        test_step_status="FAIL"
                     fi   
                  else
                     echo " "
                     echo -e "org.rdk.Bluetooth.1.connect API execution, Returned value is :  $RESULT_VALUE_8\n\n"
                     echo -e "Skipping remaining steps and marked as NT\n\n" 
                     update_test_status "${testcase_prefix}9" "FAILED"
                     test_step_status="FAIL"   
                  fi
               fi
            else
               echo -e "\nSkipping Step 9, as the previous step failed\n\n"
               update_test_status "${testcase_prefix}9" "NT"
            fi  
            dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
              
            
   #Step 10 code block
      
            
            if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_02" || "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_03" || "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_04" || "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_05" || "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_06" ]]; then
               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_10=10"
                  dynamic_var_name_3="${testcase_prefix}_num_10"
                  TC_EXTERNALAUDIO_MANUAL_01_STEP_10 "${!dynamic_var_name_3}"

                  fun_exit_status10=$?   

                  if [ "$fun_exit_status10" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_3} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}10" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_3} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}10" "FAILED"
                     test_step_status="FAIL" 
                  fi
               else
                  echo -e "\nSkipping Step 10, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}10" "NT"
               fi 


   # Step 11 code block

            
               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_11=11"
                  dynamic_var_name_4="${testcase_prefix}_num_11"
                  TC_EXTERNALAUDIO_MANUAL_01_STEP_11 "${!dynamic_var_name_4}"

                  fun_exit_status11=$?   

                  if [ "$fun_exit_status11" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_4} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}11" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_4} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}11" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 11, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}11" "NT"
               fi
               dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
            fi


   # Step 12 code block


            if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_03" ]]; then
               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_12=12"
                  dynamic_var_name_5="${testcase_prefix}_num_12"
                  TC_EXTERNALAUDIO_MANUAL_01_STEP_12 "${!dynamic_var_name_5}" "$found_device_id"

                  fun_exit_status12=$?   

                  if [ "$fun_exit_status12" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_5} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}12" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_5} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}12" "FAILED"
                  fi
               else
                  echo -e "\nSkipping Step 12, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}12" "NT"
               fi


   # Step 13 code block           
         
       
               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_13=13"
                  dynamic_var_name_6="${testcase_prefix}_num_13"
                  TC_EXTERNALAUDIO_MANUAL_01_STEP_13 "${!dynamic_var_name_6}" "$found_device_id"

                  fun_exit_status14=$?

                  if [ "$fun_exit_status14" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_6} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}13" "FAILED"
                     test_step_status="FAIL"
                  else
                     echo -e "Step ${!dynamic_var_name_6} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}13" "PASSED"
                  fi
               else
                  echo -e "\nSkipping Step 13, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}13" "NT"
               fi


   # Step 14 code block   


               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_14=14"
                  dynamic_var_name_7="${testcase_prefix}_num_14"
                  TC_EXTERNALAUDIO_MANUAL_01_STEP_14 "${!dynamic_var_name_7}" "$found_device_id"

                  fun_exit_status16=$?

                  if [ "$fun_exit_status16" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_7} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}14" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_7} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}14" "FAILED"
                  fi
               else
                  echo -e "\nSkipping Step 14, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}14" "NT"
               fi 


   # Step 15 code block 


               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_15=15"
                  dynamic_var_name_8="${testcase_prefix}_num_15"
                  TC_EXTERNALAUDIO_MANUAL_01_STEP_15 "${!dynamic_var_name_8}" "$found_device_id"

                  fun_exit_status18=$?

                  if [ "$fun_exit_status18" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_8} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}15" "FAILED"
                     test_step_status="FAIL"
                  else
                     echo -e "Step ${!dynamic_var_name_8} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}15" "PASSED"
                  fi
               else
                  echo -e "\nSkipping Step 15, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}15" "NT"
               fi           
               dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
            fi


   # Step 12 code block for TC_EXTERNALAUDIO_MANUAL_04
            

            if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_04" ]]; then
               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_12=12"
                  dynamic_var_name_9="${testcase_prefix}_num_12"
                  TC_EXTERNALAUDIO_MANUAL_04_STEP_12 "${!dynamic_var_name_9}" "$found_device_id"

                  fun_exit_status20=$?

                  if [ "$fun_exit_status20" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_9} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}12" "FAILED"
                     test_step_status="FAIL"
                  else
                     echo -e "Step ${!dynamic_var_name_9} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}12" "PASSED"
                  fi
               else
                  echo -e "\nSkipping Step 12, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}12" "NT"
               fi


   # Step 13 code block for TC_EXTERNALAUDIO_MANUAL_04 


               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_13=13"
                  dynamic_var_name_10="${testcase_prefix}_num_13"
                  TC_EXTERNALAUDIO_MANUAL_04_STEP_13 "${!dynamic_var_name_10}" "$found_device_id"

                  fun_exit_status25=$?

                  if [ "$fun_exit_status25" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_10} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}13" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_10} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}13" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 13, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}13" "NT"
               fi
               dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"         
            fi                        


   # Step 12 code block for TC_EXTERNALAUDIO_MANUAL_05


            if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_05" ]]; then
               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_12=12"
                  dynamic_var_name_11="${testcase_prefix}_num_12"
                  TC_EXTERNALAUDIO_MANUAL_05_STEP_12 "${!dynamic_var_name_11}" "$found_device_id"

                  fun_exit_status26=$?   

                  if [ "$fun_exit_status26" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_11} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}12" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_11} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}12" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 12, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}12" "NT"
               fi 


   # Step 13 code block for TC_EXTERNALAUDIO_MANUAL_05           


               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_13=13"
                  dynamic_var_name_12="${testcase_prefix}_num_13"
                  TC_EXTERNALAUDIO_MANUAL_05_STEP_13 "${!dynamic_var_name_12}" "$found_device_id"

                  fun_exit_status32=$?   

                  if [ "$fun_exit_status32" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_12} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}13" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_12} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}13" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 13, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}13" "NT"
               fi


   # Step 14 code block for TC_EXTERNALAUDIO_MANUAL_05   


               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_14=14"
                  dynamic_var_name_13="${testcase_prefix}_num_14"
                  TC_EXTERNALAUDIO_MANUAL_05_STEP_14 "${!dynamic_var_name_13}" "$found_device_id"

                  fun_exit_status34=$?   

                  if [ "$fun_exit_status34" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_13} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}14" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_13} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}14" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 14, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}14" "NT"
               fi        


   # Step 15 code block for TC_EXTERNALAUDIO_MANUAL_05


               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_15=15"
                  dynamic_var_name_14="${testcase_prefix}_num_15"
                  TC_EXTERNALAUDIO_MANUAL_05_STEP_13 "${!dynamic_var_name_14}" "$found_device_id"

                  fun_exit_status38=$?   

                  if [ "$fun_exit_status38" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_14} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}15" "FAILED"
                     test_step_status="FAIL"
                  else
                     echo -e "Step ${!dynamic_var_name_14} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}15" "PASSED"
                  fi
               else
                  echo -e "\nSkipping Step 15, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}15" "NT"
               fi
               dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
            fi  


   # Step 12 code block for TC_EXTERNALAUDIO_MANUAL_06


            if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_06" ]]; then
               volume_type_param="increase"
               if [[ "$test_step_status" != "FAIL" ]]; then
                  declare "${testcase_prefix}_num_12=12"
                  dynamic_var_name_15="${testcase_prefix}_num_12"
                  TC_EXTERNALAUDIO_MANUAL_06_STEP_12 "${!dynamic_var_name_15}" "$found_device_id" "$volume_type_param" "${increase_volume[@]}"

                  fun_exit_status42=$?   

                  if [ "$fun_exit_status42" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_15} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}12" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_15} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}12" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 12, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}12" "NT"
               fi


   # Step 13 code block for TC_EXTERNALAUDIO_MANUAL_06


               if [[ "$test_step_status" != "FAIL" ]]; then
                  volume_type_param="decrease"
                  declare "${testcase_prefix}_num_13=13"
                  dynamic_var_name_16="${testcase_prefix}_num_13"
                  TC_EXTERNALAUDIO_MANUAL_06_STEP_12 "${!dynamic_var_name_16}" "$found_device_id" "$volume_type_param" "${decrease_volume[@]}"

                  fun_exit_status43=$?   

                  if [ "$fun_exit_status43" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_16} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}13" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_16} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}13" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 13, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}13" "NT"
               fi
               dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
            fi
   

   # Step 10 code block for TC_EXTERNALAUDIO_MANUAL_07


            if [[ "$TestcaseID" == "TC_EXTERNALAUDIO_MANUAL_07" ]]; then
               if [[ "$test_step_status" != "FAIL" ]]; then
                  step_choice_1=1
                  device_info_type_1="deviceInfo"
                  device_info_type_ID_1=1
                  declare "${testcase_prefix}_num_10=10"
                  dynamic_var_name_17="${testcase_prefix}_num_10"
                  TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_17}" "$found_device_id" "$step_choice_1" "$device_info_type_1" "$device_info_type_ID_1" 


                  fun_exit_status45=$?   

                  if [ "$fun_exit_status45" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_17} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}10" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_17} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}10" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 10, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}10" "NT"
               fi


   # Step 11 code block for TC_EXTERNALAUDIO_MANUAL_07


               if [[ "$test_step_status" != "FAIL" ]]; then
                  step_choice_2=2
                  device_info_type_2="MAC Address"
                  device_info_type_ID_2=2
                  declare "${testcase_prefix}_num_11=11"
                  dynamic_var_name_18="${testcase_prefix}_num_11"
                  TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_18}" "$found_device_id" "$step_choice_2" "$device_info_type_2" "$device_info_type_ID_2"

                  fun_exit_status47=$?   

                  if [ "$fun_exit_status47" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_18} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}11" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_18} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}11" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 11, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}11" "NT"
               fi


   # Step 12 code block for TC_EXTERNALAUDIO_MANUAL_07


               if [[ "$test_step_status" != "FAIL" ]]; then
                  step_choice_3=3
                  device_info_type_3="manufacturerID"
                  device_info_type_ID_3=3
                  declare "${testcase_prefix}_num_12=12"
                  dynamic_var_name_19="${testcase_prefix}_num_12"
                  TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_19}" "$found_device_id" "$step_choice_3" "$device_info_type_3" "$device_info_type_ID_3"

                  fun_exit_status48=$?   

                  if [ "$fun_exit_status48" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_19} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}12" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_19} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}12" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 12, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}12" "NT"
               fi


   # Step 13 code block for TC_EXTERNALAUDIO_MANUAL_07


               if [[ "$test_step_status" != "FAIL" ]]; then
                  step_choice_4=4
                  device_info_type_4="deviceType"
                  device_info_type_ID_4=4
                  declare "${testcase_prefix}_num_13=13"
                  dynamic_var_name_20="${testcase_prefix}_num_13"
                  TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_20}" "$found_device_id" "$step_choice_4" "$device_info_type_4" "$device_info_type_ID_4"

                  fun_exit_status49=$?   

                  if [ "$fun_exit_status49" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_20} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}13" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_20} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}13" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 13, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}13" "NT"
               fi


   # Step 14 code block for TC_EXTERNALAUDIO_MANUAL_07


               if [[ "$test_step_status" != "FAIL" ]]; then
                  step_choice_5=5
                  device_info_type_5="batteryLevel"
                  device_info_type_ID_5=5
                  declare "${testcase_prefix}_num_14=14"
                  dynamic_var_name_21="${testcase_prefix}_num_14"
                  TC_EXTERNALAUDIO_MANUAL_07_STEPS "${!dynamic_var_name_21}" "$found_device_id" "$step_choice_5" "$device_info_type_5" "$device_info_type_ID_5"

                  fun_exit_status50=$?   

                  if [ "$fun_exit_status50" -eq 0 ]; then
                     echo -e "Step ${!dynamic_var_name_21} status\t:  PASS\n\n\n"
                     update_test_status "${testcase_prefix}14" "PASSED"
                  else
                     echo -e "Step ${!dynamic_var_name_21} status\t:  FAIL\n\n\n"
                     update_test_status "${testcase_prefix}14" "FAILED"
                     test_step_status="FAIL"
                  fi
               else
                  echo -e "\nSkipping Step 14, as the previous step failed\n\n"
                  update_test_status "${testcase_prefix}14" "NT"
               fi
               dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"
            fi


         else
            echo " "
            echo -e "org.rdk.Bluetooth plugin is in deactivated state\n\n"
            echo -e "Step 2 status\t:  FAIL\n\n"
            update_test_status "${testcase_prefix}2" "FAILED"
            test_step_status="FAIL"
            dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"

            # for handling  step 3 to step_last to set with NT value 

            if [[ "$test_step_status" == "FAIL" ]]; then
               dynamic_nt_pass_updator "$current_step_num" "NT" "3"
            fi
         fi

      else
         echo -e "\nSkipping Step 2, as the previous step failed\n\n"
         update_test_status "${testcase_prefix}2" "NT" 
         dynamic_current_step_finder "$testcase_prefix" "TC_EXTERNALAUDIO_MANUAL"

      # for handling  step 3 to step_last to set with NT value   
         dynamic_nt_pass_updator "$current_step_num" "NT" "3"
      fi 

      dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}"

   #Postcondition code block    

      printf '\nExecuting Post-condition Steps for Testcase : %s\n\n\n' "$TestcaseID"
      sleep 3
      postCondition_Execution_BT_audio "$TestcaseID" "$found_device_id"  
      printf '\nPost-condition Execution Successfull. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"

   fi

}





#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




while true; do

   echo " "
   printf "\n=============================================================================================================================================================\n\n";
   echo "                                                   ******* External Bluetooth Device Automated Test *******                                                                    ";
   printf "=============================================================================================================================================================\n\n\n";
   printf '1. Run TestCase : TC_EXTERNALAUDIO_MANUAL_01  :\t[ Pair and connect an external BT Device ] \n\n'
   printf '2. Run TestCase : TC_EXTERNALAUDIO_MANUAL_02  :\t[ Start Audio streaming in external BT Device ] \n\n'
   printf '3. Run TestCase : TC_EXTERNALAUDIO_MANUAL_03  :\t[ Unpair and Disconnect external BT Device ] \n\n'
   printf '4. Run TestCase : TC_EXTERNALAUDIO_MANUAL_04  :\t[ Reboot External BT device while Audio streaming ] \n\n'
   printf '5. Run TestCase : TC_EXTERNALAUDIO_MANUAL_05  :\t[ Volume Control (Mute/Unmute) while Audio streaming ] \n\n'
   printf '6. Run TestCase : TC_EXTERNALAUDIO_MANUAL_06  :\t[ Volume Control (Increase/Decrease) while Audio streaming ] \n\n'
   printf '7. Run TestCase : TC_EXTERNALAUDIO_MANUAL_07  :\t[ DeviceInfo verification of connected external BT Device ] \n\n'
   printf '8. Show TestCase Execution Results\n\n'
   printf '9. Exit\n\n'
   printf "\n=============================================================================================================================================================\n\n\n";


   # ----- Main Testcaes Execution Menu -----

   
   read -p "Enter an Option to proceed : " menu_choice
   printf '\n\n\n'
   case "$menu_choice" in 
      1)
         exec_start "TC_EXTERNALAUDIO_MANUAL_01"
         tc_EXTERNALAUDIO_MANUAL_testsuite "tc1_step" "TC_EXTERNALAUDIO_MANUAL_01"
         ;;
      2)
         exec_start "TC_EXTERNALAUDIO_MANUAL_02"
         tc_EXTERNALAUDIO_MANUAL_testsuite "tc2_step" "TC_EXTERNALAUDIO_MANUAL_02"
         ;;
      3)
         exec_start "TC_EXTERNALAUDIO_MANUAL_03"
         tc_EXTERNALAUDIO_MANUAL_testsuite "tc3_step" "TC_EXTERNALAUDIO_MANUAL_03"
         ;;
      4)
         exec_start "TC_EXTERNALAUDIO_MANUAL_04"
         tc_EXTERNALAUDIO_MANUAL_testsuite "tc4_step" "TC_EXTERNALAUDIO_MANUAL_04"
         ;;
      5)
         exec_start "TC_EXTERNALAUDIO_MANUAL_05"
         tc_EXTERNALAUDIO_MANUAL_testsuite "tc5_step" "TC_EXTERNALAUDIO_MANUAL_05"
         ;; 
      6)
         exec_start "TC_EXTERNALAUDIO_MANUAL_06"
         tc_EXTERNALAUDIO_MANUAL_testsuite "tc6_step" "TC_EXTERNALAUDIO_MANUAL_06"
         ;;
      7)
         exec_start "TC_EXTERNALAUDIO_MANUAL_07"
         tc_EXTERNALAUDIO_MANUAL_testsuite "tc7_step" "TC_EXTERNALAUDIO_MANUAL_07"
         ;;    
      8)
         testcase_result_display_menu "TC_EXTERNALAUDIO_MANUAL"
         ;;
      9)
         printf '\nExiting External Bluetooth Device Automated Test\n\n\n' 
         break
         ;;  
      *)
         printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
         ;;      
   esac
done








