#!/bin/bash


source device.conf


#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________



#Function Definition for step 10.1 YT deeplink launch operation



yt_deeplink_launch() {

   local json_data_10_1=$(printf '{"jsonrpc": "2.0", "id": 1234567890, "method": "Cobalt.1.deeplink","params":"%s"}' "$yt_URL")
   local JSON_RESPONSE_10_1=$(curl -# -d "$json_data_10_1" http://127.0.0.1:9998/jsonrpc)
   sleep 2
   local extracted_value_10_1=$(echo "$JSON_RESPONSE_10_1" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
   if [ "$extracted_value_10_1" == "null" ]; then
      yt_playback=true
   fi

}



#Function Definition for step 10.2 Youtube Status check operation



Cobalt_status_check() {

   local JSON_RESPONSE_10_4=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@Cobalt"}' http://127.0.0.1:9998/jsonrpc)
   local extracted_state_value_10_4=$(echo "$JSON_RESPONSE_10_4" | sed -n -E 's/.*"state":"([^"]*)".*/\1/p')

   if [[ "$extracted_state_value_10_4" == 'resumed' || "$extracted_state_value_10_4" == 'activated' ]]; then
      return 0
   else 
      return 1
   fi 

}



# Function Definition for HtmlApp_XUMO status check in Post Condition



xumo_status_check() {

   local JSON_RESPONSE_12=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@HtmlApp"}' http://127.0.0.1:9998/jsonrpc)
   local extracted_state_value_12=$(echo "$JSON_RESPONSE_12" | sed -n -E 's/.*"state":"([^"]*)".*/\1/p')

   if [[ "$extracted_state_value_12" == 'resumed' || "$extracted_state_value_12" == 'activated' ]]; then
      return 0
   else
      return 1
   fi 

}



#Function Definition for step 10 AV_playback_mode Operation



AV_playback_mode() {

   local JSON_RESPONSE_10=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@Cobalt"}' http://127.0.0.1:9998/jsonrpc)
   local SEARCH_KEY="\"state\":"

   if echo "$JSON_RESPONSE_10" | grep -qE "$SEARCH_KEY"; then
         av=1
         local extracted_state_value=$(echo "$JSON_RESPONSE_10" | sed -n -E 's/.*"state":"([^"]*)".*/\1/p')
         case "$extracted_state_value" in
              'resumed'|'activated')
                  echo -e "\nYoutube in Active state and starting AV playback with deeplink\n\n"
                  sleep 2
                  yt_deeplink_launch
                  ;;
              'deactivated')
                  echo -e "\nYoutube is in $extracted_state_value state..Activating Youtube with method \"Controller.1.activate\" \n\n"
                  local JSON_RESPONSE_10_2=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "Cobalt"}}' http://127.0.0.1:9998/jsonrpc)
                  sleep 2
                  Cobalt_status_check
                  
                  cobalt_status_check_exit=$?

                  if [ "$cobalt_status_check_exit" -eq 0 ]; then
                     sleep 2
                     yt_deeplink_launch
                  else
                     yt_playback=false
                     echo -e "\nUnable to Activate Youtube with method \"Controller.1.activate\" \n\n"
                  fi
                  ;;
               *)
                  yt_playback=false 
                  ;;
         esac
   else
         av=2
         echo -e "\nUnable to Start AV playback via Youtube...! Starting AV playback via XUMO\n\n"
         local json_data_10_3=$(printf '{"jsonrpc": "2.0", "id": 1234567890, "method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "HtmlApp", "type":"", "uri":"%s"}}' "$htmlApp_launch_URL")
         local JSON_RESPONSE_10_3=$(curl -# --data-binary \
         "$json_data_10_3" \
         -H 'content-type:text/plain;' \
         http://127.0.0.1:9998/jsonrpc)
         sleep 10
         extracted_value_10_3=$(echo "$JSON_RESPONSE_10_3" | grep -o '"success":[^,}]*' | cut -d: -f2 | tr -d '[:space:]')
         if [[ "$extracted_value_10_3" == 'true' ]]; then
             echo -e "\nXUMO App launched and starting AV playback\n\n"
             xumo_playback=true
         else
             echo -e "\nUnable to launch XUMO App and start AV playback\n\n" 
             xumo_playback=false
         fi
   fi 
   if [[ "$av" == 1 && "$yt_playback" == "true" || "$av" == 2 && "$xumo_playback" == "true" ]]; then
       return 0
   else
       return 1
   fi                    
}
   




#Step 10 code block
 
 
   echo "__________________________________________________________________________________________"
   echo " "
   echo -e "Step 10\t\t: Start AV playback in VA Device to start Audio Streaming in BT device\n\n\n" 
   
   echo -e "curl -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Cobalt.1.deeplink","params":$yt_URL}' http://localhost:9998/jsonrpc \n\ncurl --data-binary '{"jsonrpc": "2.0", "id": 1234567890, "method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "HtmlApp", "type":"", "uri":"$htmlApp_launch_URL"}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc\n\n\n"
   sleep 2

   AV_playback_mode

   fun_exit_status8=$?
 
      if [ "$fun_exit_status8" -eq 0 ]; then
          echo " "
          echo -e "AV playback started successfully in VA device and Audio Streaming started in BT device\n"
          echo -e "Step 10 status\t:  PASS\n\n\n"
          tc1_step10=PASS
      else
          echo " "
          echo -e "Unable to start AV playback in VA device. Audio Streaming via BT device FAILED\n"
          echo -e "Step 10 status\t:  FAIL\n\n\n"
          tc1_step10=FAIL
      fi        


#Postcondition code block    


   printf '\nExecuting Postcondition Steps in DUT:\n\n\n'
   if [ "$tc1_step10" == "PASS" ]; then
      if [ "$av" == 1 ]; then
         printf '\nDeactivating active Youtube instance\n\n'
         JSON_RESPONSE_13_1=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.deactivate", "params": {"callsign": "Cobalt"}}' http://127.0.0.1:9998/jsonrpc)
         sleep 2
         Cobalt_status_check
                     
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
            printf '\nAV playback via XUMO stopped and XUMO App deactivated\n\n\n'   
         fi   
         test_step_status="PASS"
      fi
   else
      test_step_status="PASS"      
      scan_attempts=0
      discovered_devices_scan=0
      printf '\nPost-condition Execution Successfull. Exiting Test Case : TC_EXTERNALAUDIO_MANUAL_01\n\n\n'
   fi
