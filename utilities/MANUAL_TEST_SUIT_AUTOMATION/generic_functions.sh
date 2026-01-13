########################################## Generic Functions Used for All TestCases Executions ####################################################
#Author : aharil144@cable.comcast.com

source device.conf

#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________



#Function to perfom the generate key operation for RDK UI navigation



generateKey_RDKUI_navigation(){

   local keyvalue="$1"
   local keycode_json=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.generateKey", "params":{"keys":[ {"keyCode": %s,"modifiers": [],"delay":1.0}]}}' "$keyvalue")
   local json_res_3=$(curl -s -# -H "Content-Type: application/json" -X POST -d "$keycode_json" http://127.0.0.1:9998/jsonrpc)
   local keycode_json_extracted=$(echo "$json_res_3" | grep -o '"success":[^,}]*' | cut -d: -f2 | tr -d '[:space:]')
   sleep 1

   if [[ "$keycode_json_extracted" == 'true' ]]; then
      return 0
   else
      return 102
   fi

}



#Function to perfom the app launch using generate key on RDK UI



generateKey_applaunch_operation(){
  
   # local variable to store length of both arrays passed as parameter to generateKey_applaunch_operatio
   local key_arr_len=$1
   local keycount_len=$2
   shift 2
   local exit_outer_loop=false
   local keys_executed=0
   
   if [[ $key_arr_len -ne $keycount_len || $key_arr_len -eq 0 ]]; then
      printf "\n\nError: App launch KeyCombination array lengths do not match or Array is empty\n\n\n"
      printf "\n\n\nDEBUG : generateKey_applaunch_operation function recieved either empty or incorrect Array values\n\n\n" 
      #Unique error code for empty array values passed to generateKey_applaunch_operation function
      return 226  
   fi

   # Extract values of nav_keys array inside function
   local nav_keycodes=("${@:1:$key_arr_len}")

   # Extract values of key_counts array inside function after the key_arr_len array end.
   local keycode_counts=("${@:$((key_arr_len + 1)):$keycount_len}")

   for ((i=0; i<key_arr_len; i++)); do
      key="${nav_keycodes[$i]}"
      keycount="${keycode_counts[$i]}"
   #Start the inner loop in the background
      (
         for ((j=0; j<keycount; j++)); do
            generateKey_RDKUI_navigation "$key"
            local generatekey_exit=$?
            if [ "$i" -eq 13 ]; then
               sleep 3
            fi      
            if [ "$generatekey_exit" -eq 102 ]; then
               printf "\n\nRDK UI generateKey navigation failed for keycode : %s at iteration %s\n\n\n" "$key" "$j"
               printf '\n\nDEBUG : generateKey_RDKUI_navigation function failed and returns %s\n\n\n' "$generatekey_exit"
               exit_outer_loop=true
               break
            fi
         done
      )&
      innerloop_pid=$!
   #Animate dots while the background process is running
      dots=""
      while kill -0 "$innerloop_pid" 2>/dev/null; do
         dots="${dots}."
         if [ "${#dots}" -gt 15 ]; then
            dots="."
         fi
         echo -ne "\rRDK generateKey keyCode : $key Navigation is in progress$dots"
         sleep 2
      done
      echo -e "\r\nRDK generateKey keyCode : $key Navigation is completed\n\n"
      keys_executed=$((keys_executed + 1))
      if $exit_outer_loop; then 
         break
      fi   
   done
   
   if [[ "$keys_executed" == "$key_arr_len" ]] && [[ "$exit_outer_loop" != "true" ]]; then
      return 0
   else
      if [ "$generatekey_exit" -eq 102 ]; then
         return $generatekey_exit
      else   
         return 106
      fi   
   fi      

}



#Function to handle the pre-condition description of different test cases



pre_condition_description() {

   local test_case="$1"
   pre_description_arr=(
            $'\n\n\nTestcaseID : TC_EXTERNALAUDIO_MANUAL_01\n\nTestcase description : Pair and connect an external BT Device\n\n[TEST STEPS]\n\nPre-condition   : 1. Box should be rebooted prior to execute shellscript\n\t\t  2. Test need to be conducted in an environment where there is no disturbance from multiple BT devices\n\t\t  3. External BT device used in the test is either a headphone or BT Sound bar\n\t\t  4. Put the External BT device in pairing mode\n\n\n'
            $'\n\n\nTestcaseID : TC_EXTERNALAUDIO_MANUAL_02\n\nTestcase description : Start Audio streaming in external BT Device\n\n[TEST STEPS]\n\nPre-condition   : 1. Test need to be conducted in an environment where there is no disturbance from multiple BT devices\n\t\t  2. External BT device used in the test is either a headphone or BT Sound bar\n\t\t  3. Put the External BT device in pairing mode\n\t\t  4. For AV playback Streaming YouTube / XYUMO App should be logged in prior to test\n\n'
            $'\n\n\nTestcaseID : TC_EXTERNALAUDIO_MANUAL_03\n\nTestcase description : Unpair and Disconnect external BT Device\n\n[TEST STEPS]\n\nPre-condition   : 1. Test need to be conducted in an environment where there is no disturbance from multiple BT devices\n\t\t  2. External BT device used in the test is either a headphone or BT Sound bar\n\t\t  3. Put the External BT device in pairing mode\n\t\t  4. For AV playback Streaming YouTube / XYUMO App should be logged in prior to test\n\n'
            $'\n\n\nTestcaseID : TC_EXTERNALAUDIO_MANUAL_04\n\nTestcase description : Reboot External BT device while Audio streaming\n\n[TEST STEPS]\n\nPre-condition   : 1. Test need to be conducted in an environment where there is no disturbance from multiple BT devices\n\t\t  2. External BT device used in the test is either a headphone or BT Sound bar\n\t\t  3. Put the External BT device in pairing mode\n\t\t  4. For AV playback Streaming YouTube / XYUMO App should be logged in prior to test\n\t\t  5. Audio streaming should be working while rebooting the External BT device\n\n'
            $'\n\n\nTestcaseID : TC_EXTERNALAUDIO_MANUAL_05\n\nTestcase description : Volume Control (Mute/Unmute) while Audio streaming\n\n[TEST STEPS]\n\nPre-condition   : 1. Test need to be conducted in an environment where there is no disturbance from multiple BT devices\n\t\t  2. External BT device used in the test is either a headphone or BT Sound bar\n\t\t  3. Put the External BT device in pairing mode\n\t\t  4. For AV playback Streaming YouTube / XYUMO App should be logged in prior to test\n\t\t  5. Audio streaming should be working while performing Mute/Unmute in the External BT device\n\n'
            $'\n\n\nTestcaseID : TC_EXTERNALAUDIO_MANUAL_06\n\nTestcase description : Volume Control (Increase/Decrease) while Audio streaming\n\n[TEST STEPS]\n\nPre-condition   : 1. Test need to be conducted in an environment where there is no disturbance from multiple BT devices\n\t\t  2. External BT device used in the test is either a headphone or BT Sound bar\n\t\t  3. Put the External BT device in pairing mode\n\t\t  4. For AV playback Streaming YouTube / XYUMO App should be logged in prior to test\n\t\t  5. Audio streaming should be working while volume Increase/Decrease in the External BT device\n\n'
            $'\n\n\nTestcaseID : TC_EXTERNALAUDIO_MANUAL_07\n\nTestcase description : DeviceInfo verification of connected external BT Device\n\n[TEST STEPS]\n\nPre-condition   : 1. Test need to be conducted in an environment where there is no disturbance from multiple BT devices\n\t\t  2. External BT device used in the test is either a headphone or BT Sound bar\n\t\t  3. Put the External BT device in pairing mode\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_01\n\n\nTestcase description : Check the memcr status\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_02\n\n\nTestcase description : Check the state of YouTube app after pressing the Home button post-launch\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Premium App Youtube should be available in DUT for memcr test\n\t\t  3. YouTube should be sign in with a valid user account prior to the memcr test\n\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_03\n\n\nTestcase description : Verify whether memory usage decreases after pressing the Home button from YouTube App\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Premium App Youtube should be available in DUT for memcr test\n\t\t  3. YouTube should be sign in with a valid user account prior to the memcr test\n\t\t  4. YouTube AV playback should be fine during this test\n\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_04\n\n\nTestcase description : Verify YouTube State Serialization after Hibernate and Resume\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Premium App Youtube should be available in DUT for memcr test\n\t\t  3. YouTube should be sign in with a valid user account prior to the memcr test\n\t\t  4. YouTube AV playback should be fine during this test\n\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_05\n\n\nTestcase description : Check the state of YouTubeTV app after pressing the Home button post-launch\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Premium App YoutubeTV should be available in DUT for memcr test\n\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_06\n\n\nTestcase description : Verify whether memory usage decreases after pressing the Home button from YouTubeTV App\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Premium App YoutubeTV should be available in DUT for memcr test\n\t\t  3. YouTubeTV Homepage should be loaded properly during this test\n\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_07\n\n\nTestcase description : Verify YouTubeTV State Serialization after Hibernate and Resume\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Premium App YoutubeTV should be available in DUT for memcr test\n\t\t  3. YouTubeTV Homepage should be loaded properly during this test\n\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_08\n\n\nTestcase description : Check the state of Amazon app after pressing the Home button post-launch\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Premium App Amazon should be available in DUT for memcr test\n\t\t  3. Amazon should be sign in with a valid user account prior to the memcr test\n\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_09\n\n\nTestcase description : Verify whether memory usage decreases after pressing the Home button from Amazon App\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Premium App Amazon should be available in DUT for memcr test\n\t\t  3. Amazon should be sign in with a valid user account prior to the memcr test\n\t\t  4. Amazon AV playback should be fine during this test\n\n\n'
            $'\n\n\nTestcaseID : TC_MEMCR_MANUAL_10\n\n\nTestcase description : Verify Amazon State Serialization after Hibernate and Resume\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Premium App Amazon should be available in DUT for memcr test\n\t\t  3. Amazon should be sign in with a valid user account prior to the memcr test\n\t\t  4. Amazon AV playback should be fine during this test\n\n\n'
            $'\n\n\nTestcaseID : TC_IMAGEFORMATS_MANUAL_01\n\n\nTestcase description : Check jpeg image Format Support via WebkitBrowser\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visisble on DUT prior to test\n\t\t  3. Testing [.jpg] image formats should be available in the configured server and make sure its accessible via the URL in browser\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_IMAGEFORMATS_MANUAL_02\n\n\nTestcase description : Check png image Format Support via WebkitBrowser\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visisble on DUT prior to test\n\t\t  3. Testing [.png] image formats should be available in the configured server and make sure its accessible via the URL in browser\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_IMAGEFORMATS_MANUAL_03\n\n\nTestcase description : Check svg image Format Support via WebkitBrowser\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visisble on DUT prior to test\n\t\t  3. Testing [.svg] image formats should be available in the configured server and make sure its accessible via the URL in browser\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_IMAGEFORMATS_MANUAL_04\n\n\nTestcase description : Check webp image Format Support via WebkitBrowser\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visisble on DUT prior to test\n\t\t  3. Testing [.webp] image formats should be available in the configured server and make sure its accessible via the URL in browser\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_RDKSHELL_MANUAL_01\n\n\nTestcase description : Verify webkitbrowser can be launched with RDKShell and load the preset urls\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visisble on DUT prior to test\n\t\t  3. Testing preset URLs should be available in the configured server and make sure its accessible via the URL in browser\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_RDKSHELL_MANUAL_02\n\n\nTestcase description : Verify HtmlApp launch with RDKShell and Load Url multiple times\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visisble on DUT prior to test\n\t\t  3. Testing preset URLs should be available in the configured server and make sure its accessible via the URL in browser\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_RDKSHELL_MANUAL_03\n\n\nTestcase description : Verify the Opacity behavior in WebKitBrowser\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visible on DUT prior to test\n\t\t  3. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_RDKSHELL_MANUAL_04\n\n\nTestcase description : Verify the Scale behavior in WebKitBrowser\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visible on DUT prior to test\n\t\t  3. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_RDKSHELL_MANUAL_05\n\n\nTestcase description : Verify the Bounds behavior in WebKitBrowser\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visible on DUT prior to test\n\t\t  3. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_RDKSHELL_MANUAL_06\n\n\nTestcase description : Verify the Animation behavior in WebKitBrowser\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visible on DUT prior to test\n\t\t  3. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_RDKSHELL_MANUAL_07\n\n\nTestcase description : Verify the setScreenResolution behaviour in RDKShell plugin using curl command\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visible on DUT prior to test\n\t\t  3. TV should be connected with the HDMI port and source should be selected\n\n\n'
            $'\n\n\nTestcaseID : TC_HDCPCOMPLIANCE_MANUAL_01\n\n\nTestcase description : Verify whether the HDMI cable has connected or disconnected from the DUT\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Initially HDMI should be connected with DUT and source should be selected on TV\n\t\t  3. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_HDCPCOMPLIANCE_MANUAL_02\n\n\nTestcase description : Verify whether the HDCP authentication has been initiated or not\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. No Audio video playback should happen on DUT during the test \n\t\t  3. TV should be connected with the HDMI port and source should be selected\n\t\t  4. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_HDCPCOMPLIANCE_MANUAL_03\n\n\nTestcase description : Verify whether HDCP authentication has initiated and it has authenticated\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. TV should be connected with the HDMI port and source should be selected\n\t\t  3. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_HDCPCOMPLIANCE_MANUAL_04\n\n\nTestcase description : Verify whether the testing device is supporting HDCP protocol or not\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. TV should be connected with the HDMI port and source should be selected\n\t\t  3. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_HDCPCOMPLIANCE_MANUAL_05\n\n\nTestcase description : Verify whether the testing device is HDCP enabled or not\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. TV should be connected with the HDMI port and source should be selected\n\t\t  3. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_HDCPCOMPLIANCE_MANUAL_06\n\n\nTestcase description : Verify whether the testing device is supported, received and current HDCP version\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. TV should be connected with the HDMI port and source should be selected\n\t\t  3. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_01\n\n\nTestcase description : Verify the IP Settings when connected to an IPv6 supported SSID\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi  SSID which supports IPV6\n\t\t  3. Ethernet should be disconnected after connecting to Wifi SSID\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_02\n\n\nTestcase description : Verify the public IPv6 IP when connected to an IPv6 supported SSID and Ethernet is connected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi SSID which supports IPV6\n\t\t  3.  Ethernet should be in connected state always\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_03\n\n\nTestcase description : Verify the public IPv6 IP when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi SSID which supports IPV6\n\t\t  3. Ethernet should be disconnected after connecting to Wifi SSID\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_04\n\n\nTestcase description : Verify the internet accessibility when connected to an IPv6 supported SSID and Ethernet is connected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi SSID which supports IPV6\n\t\t  3.  Ethernet should be in connected state after connecting to Wifi SSID\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\t\t  5. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_05\n\n\nTestcase description : Verify the internet accessibility when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi SSID which supports IPV6\n\t\t  3.  Ethernet should be disconnected after connecting to Wifi SSID\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\t\t  5. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_06\n\n\nTestcase description : Verify the trace API when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi  SSID which supports IPV6\n\t\t  3. Ethernet should be disconnected after connecting to Wifi SSID\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_07\n\n\nTestcase description : Verify the ping API when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi  SSID which supports IPV6\n\t\t  3. Ethernet should be disconnected after connecting to Wifi SSID\n\n\n'
   )
    
   case "$test_case" in
   "TC_EXTERNALAUDIO_MANUAL_01") printf "%s" "${pre_description_arr[0]}" ;;
   "TC_EXTERNALAUDIO_MANUAL_02") printf "%s" "${pre_description_arr[1]}" ;;
   "TC_EXTERNALAUDIO_MANUAL_03") printf "%s" "${pre_description_arr[2]}" ;;
   "TC_EXTERNALAUDIO_MANUAL_04") printf "%s" "${pre_description_arr[3]}" ;;
   "TC_EXTERNALAUDIO_MANUAL_05") printf "%s" "${pre_description_arr[4]}" ;;
   "TC_EXTERNALAUDIO_MANUAL_06") printf "%s" "${pre_description_arr[5]}" ;;
   "TC_EXTERNALAUDIO_MANUAL_07") printf "%s" "${pre_description_arr[6]}" ;;
   "TC_MEMCR_MANUAL_01")         printf "%s" "${pre_description_arr[7]}" ;;
   "TC_MEMCR_MANUAL_02")         printf "%s" "${pre_description_arr[8]}" ;;
   "TC_MEMCR_MANUAL_03")         printf "%s" "${pre_description_arr[9]}" ;;
   "TC_MEMCR_MANUAL_04")         printf "%s" "${pre_description_arr[10]}" ;;
   "TC_MEMCR_MANUAL_05")         printf "%s" "${pre_description_arr[11]}" ;;
   "TC_MEMCR_MANUAL_06")         printf "%s" "${pre_description_arr[12]}" ;;
   "TC_MEMCR_MANUAL_07")         printf "%s" "${pre_description_arr[13]}" ;;
   "TC_MEMCR_MANUAL_08")         printf "%s" "${pre_description_arr[14]}" ;;
   "TC_MEMCR_MANUAL_09")         printf "%s" "${pre_description_arr[15]}" ;;
   "TC_MEMCR_MANUAL_10")         printf "%s" "${pre_description_arr[16]}" ;;
   "TC_IMAGEFORMATS_MANUAL_01")  printf "%s" "${pre_description_arr[17]}" ;;
   "TC_IMAGEFORMATS_MANUAL_02")  printf "%s" "${pre_description_arr[18]}" ;;
   "TC_IMAGEFORMATS_MANUAL_03")  printf "%s" "${pre_description_arr[19]}" ;;
   "TC_IMAGEFORMATS_MANUAL_04")  printf "%s" "${pre_description_arr[20]}" ;;
   "TC_RDKSHELL_MANUAL_01")      printf "%s" "${pre_description_arr[21]}" ;;
   "TC_RDKSHELL_MANUAL_02")      printf "%s" "${pre_description_arr[22]}" ;;
   "TC_RDKSHELL_MANUAL_03")      printf "%s" "${pre_description_arr[23]}" ;;
   "TC_RDKSHELL_MANUAL_04")      printf "%s" "${pre_description_arr[24]}" ;;
   "TC_RDKSHELL_MANUAL_05")      printf "%s" "${pre_description_arr[25]}" ;;
   "TC_RDKSHELL_MANUAL_06")      printf "%s" "${pre_description_arr[26]}" ;;
   "TC_RDKSHELL_MANUAL_07")      printf "%s" "${pre_description_arr[27]}" ;;
   "TC_HDCPCOMPLIANCE_MANUAL_01")      printf "%s" "${pre_description_arr[28]}" ;;
   "TC_HDCPCOMPLIANCE_MANUAL_02")      printf "%s" "${pre_description_arr[29]}" ;;
   "TC_HDCPCOMPLIANCE_MANUAL_03")      printf "%s" "${pre_description_arr[30]}" ;;
   "TC_HDCPCOMPLIANCE_MANUAL_04")      printf "%s" "${pre_description_arr[31]}" ;;
   "TC_HDCPCOMPLIANCE_MANUAL_05")      printf "%s" "${pre_description_arr[32]}" ;;
   "TC_HDCPCOMPLIANCE_MANUAL_06")      printf "%s" "${pre_description_arr[33]}" ;;
   "TC_IPv6_MANUAL_01")          printf "%s" "${pre_description_arr[34]}" ;;
   "TC_IPv6_MANUAL_02")          printf "%s" "${pre_description_arr[35]}" ;;
   "TC_IPv6_MANUAL_03")          printf "%s" "${pre_description_arr[36]}" ;;
   "TC_IPv6_MANUAL_04")          printf "%s" "${pre_description_arr[37]}" ;;
   "TC_IPv6_MANUAL_05")          printf "%s" "${pre_description_arr[38]}" ;;
   "TC_IPv6_MANUAL_06")          printf "%s" "${pre_description_arr[39]}" ;;
   "TC_IPv6_MANUAL_07")          printf "%s" "${pre_description_arr[40]}" ;;
   *) printf "\nInvalid Testcase ID !!\n" ;;
   esac

}



#Function to handle the nt_pass updation on precondition and step 2 failure case for TC_EXTERNALAUDIO_MANUAL testcase



dynamic_nt_pass_updator(){

   local status="$2"
   local step_count="$1"
   local start_loop_from="$3"
   local var_name test_step_array=() 

   for ((i="$start_loop_from"; i<="$step_count"; i++)); do
      test_step_array+=("${testcase_prefix}$i")
   done
   for var_name in "${test_step_array[@]}"; do
   eval "$var_name='$status'"
   done
}



#Function to find the current_step number based on the testcase



dynamic_current_step_finder(){

   local tc_prifix="$1"
   local testcase_name="$2"
   if [[ "$testcase_name" == "TC_EXTERNALAUDIO_MANUAL" ]]; then
      case "$tc_prifix" in
      "tc1_step") current_step_num=9 ;;
      "tc2_step") current_step_num=11 ;;
      "tc3_step"|"tc5_step") current_step_num=15 ;;
      "tc4_step"|"tc6_step") current_step_num=13 ;;
      "tc7_step") current_step_num=14 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   elif [[ "$testcase_name" == "TC_MEMCR_MANUAL" ]]; then   
      case "$tc_prifix" in
      "tc1_step") current_step_num=1 ;;
      "tc2_step"|"tc5_step"|"tc8_step") current_step_num=4 ;;
      "tc3_step"|"tc4_step"|"tc6_step"|"tc7_step"|"tc9_step"|"tc10_step") current_step_num=6 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   elif [[ "$testcase_name" == "TC_IMAGEFORMATS_MANUAL" ]]; then
      case "$tc_prifix" in
      "tc1_step"|"tc2_step"|"tc3_step"|"tc4_step") current_step_num=1 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   elif [[ "$testcase_name" == "TC_RDKSHELL_MANUAL" ]]; then
      case "$tc_prifix" in
      "tc1_step"|"tc7_step") current_step_num=6 ;;
      "tc2_step") current_step_num=4 ;;
      "tc3_step") current_step_num=5 ;;
      "tc4_step"|"tc5_step"|"tc6_step") current_step_num=3 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   elif [[ "$testcase_name" == "TC_HDCPCOMPLIANCE_MANUAL" ]]; then   
      case "$tc_prifix" in
      "tc1_step"|"tc2_step"|"tc4_step"|"tc5_step"|"tc6_step")  current_step_num=3 ;;
      "tc3_step") current_step_num=4 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   elif [[ "$testcase_name" == "TC_IPv6_MANUAL" ]]; then
      case "$tc_prifix" in
      "tc1_step"|"tc2_step"|"tc3_step"|"tc6_step"|"tc7_step")  current_step_num=1 ;;
      "tc4_step"|"tc5_step") current_step_num=2 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   else
      printf "\nInvalid testCase name. Unable to detect current step number!!!\n\n\n"
   fi
}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_01 STEP-10 AV_playback_mode sub Function for Youtube deeplink launch 



sub_AV_playback_yt_deeplink() {

   local app="$1"
   sleep 2
   youtube_deeplink_launch
   local youtube_deeplink_exit=$?

   if [ "$youtube_deeplink_exit" -eq 0 ]; then
      sleep 2
      generateKey_RDKUI_navigation "13"
      generate_key_exit_77=$?
      sleep 1
      if [ "$generate_key_exit_77" -eq 0 ]; then
         yt_playback="true"
      else
         printf '\n\n%s App launched,But Unable to start AV playback\n\n\n' "$app"
         printf "\n\n\nDEBUG : generateKey_RDKUI_navigation function failed with error code : %s\n\n" "$generate_key_exit_77"
         yt_playback="false"
      fi
   else
      printf "\n\n\Unable to launch %s and start AV playback with deeplink\n\n\n" "$app" 
      printf "\n\n\nDEBUG : youtube_deeplink_launch function failed with error code : %s\n\n" "$youtube_deeplink_exit"     
      yt_playback="false"
   fi

}



#Function Definition for TC_EXTERNALAUDIO_MANUAL_01 STEP-10 AV_playback_mode Operation



AV_playback_mode() {

   local app_name="$1"
   local JSON_RESPONSE_10=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@YouTube"}' http://127.0.0.1:9998/jsonrpc)
   local SEARCH_KEY="\"state\":"

    if echo "$JSON_RESPONSE_10" | grep -qE "$SEARCH_KEY" || [[ "$app_name" == "YouTube" ]]; then
        av_check_flag=1
        local extracted_state_value=$(echo "$JSON_RESPONSE_10" | sed -n -E 's/.*"state":"([^"]*)".*/\1/p')
        case "$extracted_state_value" in
            'resumed'|'activated')
               printf "\n%s App in Active state and starting AV playback with deeplink\n\n" "$app_name"
               sub_AV_playback_yt_deeplink "$app_name"             
               ;;
            'deactivated')
               printf "\nYoutube is in %s state..Activating Youtube with method \"Controller.1.activate\" \n\n" "$extracted_state_value"
               local JSON_RESPONSE_10_2=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "YouTube"}}' http://127.0.0.1:9998/jsonrpc)
               sleep 2
               preApp_status_check "$app_name"
                
               preApp_status_check_exit=$?

               if [ "$preApp_status_check_exit" -eq 0 ]; then
                  sub_AV_playback_yt_deeplink "$app_name"
               else
                  echo -e "\nUnable to Activate Youtube with method \"Controller.1.activate\" \n\n"
                  yt_playback=false
               fi
               ;;
            'hibernated')
               printf "\n\n%s App in %s state and starting AV playback using deeplink on a new instance\n\n" "$app_name" "$extracted_state_value"
               destroy_app "$app_name"
               local destroy_app_exit=$?
      
               if [ "$destroy_app_exit" -eq 0 ]; then
                  local JSON_RESPONSE_10_2=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "YouTube"}}' http://127.0.0.1:9998/jsonrpc)
                  sleep 2
                  preApp_status_check "$app_name"
                  
                  preApp_status_check_exit=$?

                  if [ "$preApp_status_check_exit" -eq 0 ]; then
                     sub_AV_playback_yt_deeplink "$app_name"
                  else
                     printf "\nUnable to Activate Youtube with method \"Controller.1.activate\" \n\n"
                     yt_playback=false
                  fi
               else
                  printf "\n\n\nDEBUG : destroy_app function failed with error code : %s\n\n" "$destroy_app_exit"
                  yt_playback=false     
               fi
               ;;
            *)
               yt_playback=false 
               ;;
        esac
    else
        av_check_flag=2
        printf "\nUnable to Start AV playback via Youtube...! Starting AV playback via XUMO\n\n"
        local json_data_10_3=$(printf '{"jsonrpc": "2.0", "id": 1234567890, "method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "HtmlApp", "type":"", "uri":"%s"}}' "$htmlApp_launch_URL")
        local JSON_RESPONSE_10_3=$(curl -# --data-binary \
        "$json_data_10_3" \
        -H 'content-type:text/plain;' \
        http://127.0.0.1:9998/jsonrpc)
        sleep 10
        extracted_value_10_3=$(echo "$JSON_RESPONSE_10_3" | grep -o '"success":[^,}]*' | cut -d: -f2 | tr -d '[:space:]')
        if [[ "$extracted_value_10_3" == 'true' ]]; then
            sleep 2
            xumo_status_check
            
            local xumo_status_check_exit=$?

            if [ "$xumo_status_check_exit" -eq 0 ]; then
                echo -e "\nXUMO App launched and starting AV playback\n\n"
                xumo_playback=true
            else
                echo -e "\nUnable to launch XUMO App and start AV playback\n\n" 
                xumo_playback=false
            fi   
        else
            echo -e "\nXUMO App launch curl execution failed. Returned Value is : $extracted_value_10_3\n\n" 
            xumo_playback=false
        fi
    fi 
    if [[ "$av_check_flag" == 1 && "$yt_playback" == "true" || "$av_check_flag" == 2 && "$xumo_playback" == "true" ]]; then
       return 0
    else
       return 1
    fi                    
}



#Function Definition for youtube_deeplink_launch function to launch YouTube with deeplink  



youtube_deeplink_launch() {

   local json_data_10_1=$(printf '{"jsonrpc": "2.0", "id": 1234567890, "method": "YouTube.1.deeplink","params":"%s"}' "$yt_URL")
   local JSON_RESPONSE_10_1=$(curl -# -d "$json_data_10_1" http://127.0.0.1:9998/jsonrpc)
   sleep 3
   local extracted_value_10_1=$(echo "$JSON_RESPONSE_10_1" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
   if [ "$extracted_value_10_1" == "null" ]; then
      return 0
   else
      #YouTube specific deeplink launch error return code for function youtube_deeplink_launch
      return 122   
   fi

}



#Function Definition for amazon_deeplink_launch function to launch Amazon prime with deeplink  



amazon_deeplink_launch() {

   local json_data_10_2=$(printf '{"jsonrpc": "2.0", "id": 1234567890, "method": "Amazon.1.deepLinkUrl","params":{"url":"%s"}}' "$amz_URL")
   local JSON_RESPONSE_10_5=$(curl -# -H "Content-Type: application/json" -X POST -d "$json_data_10_2" http://127.0.0.1:9998/jsonrpc)
   sleep 5
   local extracted_value_10_2=$(echo "$JSON_RESPONSE_10_5" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
   if [ "$extracted_value_10_2" == "null" ]; then
      return 0
   else
      #Amazon Prime specific deeplink launch error return code for function amazon_deeplink_launch
      return 124    
   fi

}



# Function Definition for TC_EXTERNALAUDIO_MANUAL_01 STEP-10.2 Youtube Status check operation



preApp_status_check() {

   name="$1"
   local json_data_10_4=$(printf '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@%s"}' "$name")
   local JSON_RESPONSE_10_4=$(curl -# -d "$json_data_10_4"  http://127.0.0.1:9998/jsonrpc )
   local extracted_state_value_10_4=$(echo "$JSON_RESPONSE_10_4" | sed -n -E 's/.*"state":"([^"]*)".*/\1/p')

   if [[ "$extracted_state_value_10_4" == 'resumed' || "$extracted_state_value_10_4" == 'activated' ]]; then
      return 0
   else
      return 1
   fi 

}



#Function to check the status of Apps used for TC_MEMCR_MANUAL TestSuite



memcr_app_status() {
    
   sleep 1 
   local app_name="$1"
   local payload=$(printf '{"jsonrpc": "2.0", "id": 1234567890, "method":"Controller.1.status@%s"}' "$app_name")
   local JSON_RESPONSE=$(curl -# -s -d "$payload" http://127.0.0.1:9998/jsonrpc)
   local SEARCH_KEY="\"state\":"

   if echo "$JSON_RESPONSE" | grep -qE "$SEARCH_KEY"; then
      return 0
   else
      return 1
   fi

}



#Function to check the status of Apps used for TC_MEMCR_MANUAL TestSuite



apphibernate_status() {

   sleep 1
   data_model_exec=$(tr181 -d Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.AppHibernate.Enable | tail -n 1 | awk -F'::' '{print $NF}' | tr -d '[:space:]' | tr -d '\r')
   
   if [[ "$data_model_exec" == "true" ]]; then
      return 0
   else
      return 1
   fi    

}



# Function Definition for premium_app Launch using RDKshell and Starting playback using deeplink



premium_app_Launch_and_check() {
   
   local appname="$1"
   app_launch_flag=0
   memcr_app_status "$appname"
   local memcr_app_status_exit=$? 
   sleep 2

   if [ "$memcr_app_status_exit" -eq 0 ]; then
      local launch_json=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.launch", "params":{ "callsign": "%s", "type": "","uri": ""}}' "$appname")
      local json_res_1=$(curl -s -# -H "Content-Type: application/json" -X POST -d "$launch_json" http://127.0.0.1:9998/jsonrpc)
      local launch_extracted_value=$(echo "$json_res_1" | grep -o '"success":[^,}]*' | cut -d: -f2 | tr -d '[:space:]')
      sleep 3

      if [[ "$launch_extracted_value" == 'true' ]]; then
         if [[ "$appname" == "YouTube" ]]; then
            sleep 3
            youtube_deeplink_launch
            local youtube_deeplink_exit=$?
            
            if [ "$youtube_deeplink_exit" -eq 0 ]; then            
               sleep 8
               generateKey_RDKUI_navigation "13"
               generate_key_exit_1=$?
               sleep 3
               if [ "$generate_key_exit_1" -eq 0 ]; then  
                  return 0
               else
                  printf "\n\n\nDEBUG : generateKey_RDKUI_navigation function failed with error code : %s\n\n" "$generate_key_exit_1"
                  return $generate_key_exit_1
               fi
            else
               printf "\n\n\Unable to launch %s and start AV playback with deeplink\n\n\n" "$appname" 
               printf "\n\n\nDEBUG : youtube_deeplink_launch function failed with error code : %s\n\n" "$youtube_deeplink_exit"     
               return 1
            fi         
         elif [[ "$appname" == "Amazon" ]]; then 
            sleep 3
            amazon_deeplink_launch
            local amazon_deeplink_exit=$?
            
            if [ "$amazon_deeplink_exit" -eq 0 ]; then  
               generateKey_RDKUI_navigation "13"
               local generate_key_exit_3=$?
               sleep 7
               generateKey_RDKUI_navigation "13"
               if [ "$generate_key_exit_3" -eq 0 ]; then  
                  return 0
               else
                  printf "\n\n\nDEBUG : generateKey_RDKUI_navigation function failed with error code : %s\n\n" "$generate_key_exit_3"
                  return $generate_key_exit_3
               fi
            else
               printf "\n\n\Unable to launch %s and start AV playback with deeplink\n\n\n" "$appname" 
               printf "\n\n\nDEBUG : amazon_deeplink_launch function failed with error code : %s\n\n" "$amazon_deeplink_exit"     
               return 1
            fi         
         else
            return 0
         fi      
      else
         printf '\n\nUnable to launch %s with org.rdk.RDKShell.1.launch API\n\n\n' "$appname"
         app_launch_flag=1           
         return 1
      fi
   else
      printf '\n\n%s App not available in device\n\n\n' "$appname"
      printf "\n\n\nDEBUG : memcr_app_status function failed with error code : %s\n\n" "$memcr_app_status_exit"
      return 1   
   fi

}



# Function Definition for HtmlApp_XUMO status check in Post Condition for TC_EXTERNALAUDIO_MANUAL



xumo_status_check() {

   local JSON_RESPONSE_12=$(curl -# -d '{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@HtmlApp"}' http://127.0.0.1:9998/jsonrpc)
   local extracted_state_value_12=$(echo "$JSON_RESPONSE_12" | sed -n -E 's/.*"state":"([^"]*)".*/\1/p')

   if [[ "$extracted_state_value_12" == 'resumed' || "$extracted_state_value_12" == 'activated' ]]; then
      return 0
   else
      return 1
   fi 

}



# Function Definition for User's experience and choice input



user_confirmation() {

   local choice_var="$1"
   local query="$2"
   # Check if exactly 2 parameters are provided
   if [[ -z "$1" || -z "$2" ]]; then
      printf "\n\nError: Missing or empty parameters. Usage: user_confirmation <variable_name> <prompt_message>\n"
      return 1
   fi
   while true; do
      read -p "$query" "$choice_var"
      printf "\n"
      user_choice_lower=$(echo "${!choice_var}" | tr '[:upper:]' '[:lower:]')

      if [[ "$user_choice_lower" == "yes" ]]; then
         return 0
      elif [[ "$user_choice_lower" == "no" ]]; then
         return 1
      else
         printf "\nInvalid choice. Please enter 'yes' or 'no'.\n\n"
      fi
   done

}



#Function Definition for Dynamic Testcase step execution status updation



update_test_status() {

  local var_name="$1"
  local status="$2"
  printf -v "$var_name" "%s" "$status"

}



#Function Definition for Test Case Execution result check



testcase_result_checker() {

   local prefix="$1"
   local last_step_number="$2"
   local test_case="$3"
   local timestamp
   timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
   mkdir -p $result_directory
   output_file="$result_directory/result_${test_case}_${timestamp}.txt"
   local i varname var_value
   local -a failed_steps_arr=()

   #counters for summary steps status count

   local pass_count=0
   local nt_count=0
   local fail_count=0
   local unset_count=0

   #Headers for the Output result txt File
   printf '\n\n-----------------------|  TestCase Execution Report  |-----------------------\n\n\n' | tee -a "$output_file"
   printf "\n\nTestCase : %s  Total Steps : %d\n\n\n\n" "$test_case" "$last_step_number" | tee -a "$output_file"

   for ((i=1; i<=last_step_number; i++)); do

      varname="${prefix}${i}"
      var_value="${!varname-UNSET}"

      #Test Execution result of Each step to output_file
      formatted_line=$(printf "%s\t  : %s\n\n" "$varname" "$var_value")

      if [[ "$var_value" == "PASSED" ]]; then
         printf "\e[1;32m%s\e[0m\n" "$formatted_line"
      elif [[ "$var_value" == "FAILED" ]]; then
         printf "\e[1;31m%s\e[0m\n" "$formatted_line"
      else
         printf "\e[1;33m%s\e[0m\n" "$formatted_line"   
      fi
      # Write plain text to file
      echo "$formatted_line" >> "$output_file"
        

      case "$var_value" in
         PASSED)
           ((pass_count++))
           ;;
         NT)
           ((nt_count++))
           ;;
         UNSET)
           failed_steps_arr+=("$varname=UNSET")
           ((unset_count++))
           ;;
         *)
           failed_steps_arr+=("$varname=$var_value")
           ((fail_count++))
           ;;  
      esac

   done
    
   if ((${#failed_steps_arr[@]}==0)); then
      printf '\n\n----------------------- TEST SUMMARY -----------------------\n\n\nPASS : %d\tN/T : %d\t\tFAIL : %d\tUNSET : %d\n' \
      "$pass_count" "$nt_count" "$fail_count" "$unset_count" | tee -a "$output_file"
      printf '\n\n------------------------------------------------------------\n\n' | tee -a "$output_file"
      return 0
   else
      printf '\n\n\nSteps Failed :\n\n' | tee -a "$output_file"
      printf '%s\n' "${failed_steps_arr[@]}" | tee -a "$output_file"
      printf '\n\n' | tee -a "$output_file"
      printf '\n\n----------------------- TEST SUMMARY -----------------------\n\n\nPASS : %d\tN/T : %d\t\tFAIL : %d\tUNSET : %d\n' \
      "$pass_count" "$nt_count" "$fail_count" "$unset_count" | tee -a "$output_file"
      printf '\n\n------------------------------------------------------------\n\n' | tee -a "$output_file"
      return 1  
   fi

}



#Function to display the Test result of user selected TestCases



display_execution_reports_and_wait() {
   
   if [ -d "$result_directory" ]; then
      local latest_report=$(ls -1r "$result_directory"/result_${1}_*.txt | head -n 1)
      if [ -n "$latest_report" ]; then
         echo -e "\n\n-------- Displaying the latest report : $(basename "$latest_report") -------\n\n"
         cat "$latest_report"
         echo -e "\n-------------------------------| End of Report |------------------------------\n\n\n"

         # Wait for the user to press any key to handle result displaying time

         printf '\n\n'
         read -n 1 -s -r -p "Press any key to return to the TestCase Execution Results Menu....."
         printf '\n\n\n'
         return 0
      else
         printf '\n\nNo TestCase Execution Report file found for %s\n\n' "$1"
         return 1
      fi
   else
      printf '\n\n%s directory is not available. TestCase Execution Report Unavailable right now\n\n\n' "$result_directory"
      return 1
   fi

}



#Function to cleanUp and delete TestExecution report history



cleanup_testExecution_reports() {
   
   local testsuit_prefix="$1"
   local testcase files_to_delete old_file
   if [ -d "$result_directory" ] && [ "$(ls -A "$result_directory" | wc -l)" -ge 2 ]; then
      printf '\n\nDeleting and cleaning Up all the Execution reports\n\n\n'
      local unique_testcases=$(find "$result_directory" -type f -name "result_${1}*.txt" | sed -E "s/.*(${testsuit_prefix}[0-9]+).*/\1/" | sort -u)
      echo -e "\nFound the following testcases :\n\n$unique_testcases\n\n\n"

      for testcase in $unique_testcases; do
         echo -e "\n--------- Processing test case : $testcase ----------\n\n\n"
         files_to_delete=$(ls -1t "$result_directory"/result_"$testcase"_*.txt | tail -n +2)
         if [ -n "$files_to_delete" ]; then
            for old_file in $files_to_delete; do
               rm -r "$old_file"
               printf 'DELETED : %s\n' "$old_file"
               sleep 2
            done
            printf '\n\nCleanup for %s is completed\n\n\n' "$testcase"
         else
            printf '\n\nOlder execution results are Not Available for %s to delete\n\n\n' "$testcase" 
         fi
      done   
   elif [ -d "$result_directory" ]; then
      printf '\n\n%s directory is available. But cleanUp is not required!!!\n\n\n' "$result_directory"
   else   
      printf '\n\n%s directory is not available. TestCase Execution result history is empty\n\n\n' "$result_directory"
   fi   

}



#Function to display the Overall TestSuite Execution Status



overall_testsuite_execution_status() {

   # Initialize grand total counters
   local grand_pass=0
   local grand_fail=0
   local grand_nt=0
   local grand_total=0
   local grand_total_calcu=0
   local grand_nt_percent grand_fail_percent grand_pass_percent
   local pass_count fail_count testcase nt_count total_tests total_tests_calcu
   local pass_percentage fail_percentage nt_percentage
   local testsuit_prefix="$1"
   sleep 2

   local unique_testcases=$(find "$result_directory" -type f -name "result_${1}*.txt" | sed -E "s/.*(${testsuit_prefix}[0-9]+).*/\1/" | sort -u)
   for testcase in $unique_testcases; do
      pass_count=$(grep -o "PASSED" $result_directory/result_${testcase}_*.txt | wc -l)
      sleep 1
      fail_count=$(grep -o "FAILED" $result_directory/result_${testcase}_*.txt | wc -l)
      if [[ "$fail_count" -gt 1 ]]; then
         fail_count=$((fail_count - 1))
      fi   
      sleep 1
      nt_count=$(grep -o "NT" $result_directory/result_${testcase}_*.txt | wc -l)

      total_tests=$((pass_count + fail_count + nt_count))
      total_tests_calcu=$((pass_count + fail_count))
      if [ "$total_tests" -gt 0 ]; then
         # Use bc for floating-point percentage calculation
         pass_percentage=$(awk "BEGIN {printf \"%.2f\", ($pass_count / $total_tests_calcu) * 100}")
         fail_percentage=$(awk "BEGIN {printf \"%.2f\", ($fail_count / $total_tests_calcu) * 100}")
         nt_percentage=$(awk "BEGIN {printf \"%.2f\", ($nt_count / $total_tests_calcu) * 100}")
         
         printf '\n========== %s TestExecution Results ==========\n\n' "$testcase"
         printf '\nTotal Teststeps         \t: %d\n' "$total_tests"
         printf '\nTotal Executed teststeps\t: %d\n' "$total_tests_calcu"
         printf '\nPASSED Teststeps        \t: %d\n (%s%%)\n' "$pass_count" "$pass_percentage"
         printf '\nFAILED Teststeps        \t: %d\n (%s%%)\n' "$fail_count" "$fail_percentage"
         printf '\nNT Teststeps            \t: %d\n (%s%%)\n' "$nt_count" "$nt_percentage"
      else
         printf '\n\nNo Testcase Execution results found for %s\n\n\n' "$testcase"
      fi   
      # Add to the grand totals
      printf '\n'
      grand_pass=$((grand_pass + pass_count))
      grand_fail=$((grand_fail + fail_count))
      grand_nt=$((grand_nt + nt_count))
   done

   # Calculate and display the grand total 
   grand_total=$((grand_pass + grand_fail + grand_nt))
   grand_total_calcu=$((grand_pass + grand_fail))

   if [ "$grand_total" -gt 0 ]; then
      grand_pass_percent=$(awk "BEGIN {printf \"%.2f\", ($grand_pass / $grand_total_calcu) * 100}")
      grand_fail_percent=$(awk "BEGIN {printf \"%.2f\", ($grand_fail / $grand_total_calcu) * 100}")
      grand_nt_percent=$(awk "BEGIN {printf \"%.2f\", ($grand_nt / $grand_total_calcu) * 100}")
      
      echo -e "\n\n=========================================================================================================================\n\n"
      echo -e "\t\t\t\t\t\tOverall TestSuite Execution Status\t\t\t"
      echo -e "\n\n=========================================================================================================================\n\n"
      echo -e "Total Steps Run   \t: $grand_total_calcu\n"
      echo -e "Total Passed      \t: $grand_pass\n"
      echo -e "Total Failed      \t: $grand_fail\n"
      echo -e "Total NT          \t: $grand_nt\n"
      echo -e "Pass Percentage   \t: ${grand_pass_percent}%\n"
      echo -e "Fail Percentage   \t: ${grand_fail_percent}%\n"
      echo -e "NT Percentage     \t: ${grand_nt_percent}%\n\n"
      printf '===========================================================================================================================\n'
      printf '\n\n'
      read -n 1 -s -r -p "Press any key to return to the TestCase Execution Results Menu....."
      printf '\n\n\n'
   else
      printf '\n\nNo TestCase Execution result available to process!!!\n\n\n'
   fi

}



#Function to handle the dynamic steps result updator



dynamic_test_result_update(){

   local test_last_step=$1
   local test_caseid="$2"
   local testcase_prefix="$3"
   testcase_result_checker "$testcase_prefix" "$test_last_step" "$test_caseid"

   local fun_exit_status_result=$?   

   if [ "$fun_exit_status_result" -eq 0 ]; then
      echo " "
      printf '\n%s  Testcase Status  : PASS\n\n\n' "$TestcaseID" | tee -a "$output_file"
      printf "\n-----------------------------------------------------------------------------\n\n\n" | tee -a "$output_file"
   else
      echo " "
      printf '\n%s  Testcase Status  : FAIL\n\n\n' "$TestcaseID" | tee -a "$output_file"
      printf "\n-----------------------------------------------------------------------------\n\n\n" | tee -a "$output_file"
   fi

}



#Function to handle the Testcase execution from Execution Result menu



trigger_from_Execution_Result_menu() {

   local trigger_from_tc_id="$1"
   local trigger_from_tcstep="$2"
   local test_suite_name="$3"
   display_execution_reports_and_wait "$trigger_from_tc_id"
   display_execution_reports_and_wait_fun_exit=$?

   if [ "$display_execution_reports_and_wait_fun_exit" -eq 1 ]; then
      user_choice_2="user_choice_2" 
      Query_2="Do you want to trigger testcase : $trigger_from_tc_id? [yes/no]: "
      
      user_confirmation "$user_choice_2" "$Query_2"
      local user_confirmation_fun_exit=$?

      if [ "$user_confirmation_fun_exit" -eq 0 ]; then 
         printf '\n\n%s TestCase Execution triggered\n\n\n' "$trigger_from_tc_id"
         printf "\n_______________________________________________________________________________________________________________________________________________\n\n"
         pre_condition_description "$trigger_from_tc_id"
         "$test_suite_name" "$trigger_from_tcstep" "$trigger_from_tc_id"
         printf '\n\n\nChecking Test Execution Result : %s\n\n\n' "$trigger_from_tc_id"
         sleep 8
         display_execution_reports_and_wait "$trigger_from_tc_id"
      else
         printf '\n\n%s TestCase Execution Triggering cancelled\n\n' "$trigger_from_tc_id"  
      fi
   fi  
}



#Function Definition for getting the current state of App for memecr



get_Premium_App_state() {

  sleep 2
  hibernated_app_state=0
  local app_name="$1"
  local JSON_RESPONSE=$(curl -# --data-binary '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.getState", "params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc) 
  app_state=$(echo "$JSON_RESPONSE" | grep -o "\"callsign\":\"$app_name\",\"state\":\"[^\"]*\"" | awk -F':"' '{print $3}' | tr -d '",')

   if [[ "$app_state" == "resumed" || "$app_state" == "activated" ]]; then
      return 0
   elif [[ -z "$app_state" ]]; then
      printf '\n\norg.rdk.RDKShell.1.getState API returns empty value for %s state\n\n\n' "$app_name"
      return 1               
   else
      if [[ "$app_state" == "hibernated" ]]; then
         hibernated_app_state=1
      fi   
      return 1
   fi 

}



#Function defenition to destroy the App instance



destroy_app() {

   local app_to_destroy="$1"
   local destroy_json=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.destroy", "params":{"callsign": "%s"}}' "$app_to_destroy" )
   local destroy_response=$(curl -# --data-binary "$destroy_json" -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc)
   local destroy_status=$(echo "$destroy_response" | grep -o '"success":[^,}]*' | cut -d: -f2 | tr -d '[:space:]')
   sleep 1

   if [[ "$destroy_status" == "true" ]]; then
      printf '\n\nInstance of %s App destroyed successfully\n\n\n' "$app_to_destroy"
      return 0
   else
      printf '\n\nUnable to destroy the Instance of %s App\n\n\n' "$app_to_destroy"
      return 278
   fi

}



#Function Definition for Identifying Device model or type



platform_type_finder() {
   
   invalid_platform="false"
   platform_model=$(grep -i "^MODEL_NUM=" /etc/device.properties | tail -n 1 | cut -d'=' -f2)
   if [[ "$platform_model" == "RPI4" ]]; then
      printf '\n\nDUT model is RaspberryPi [%s]\n\n\n' "$platform_model"
   elif [[ "$platform_model" == "AH212" ]]; then 
      printf '\n\nDUT model is Amlogic Reference [%s]\n\n\n' "$platform_model"
   elif [[ "$platform_model" == "REALTEKHANK" ]]; then 
      printf '\n\nDUT model is Realtek Reference [%s]\n\n\n' "$platform_model" 
   elif [[ "$platform_model" == "BCM972126OTT" ]]; then
      printf '\n\nDUT model is Broadcom Reference [%s]\n\n\n' "$platform_model"
   else
      printf '\n\nInvalid/Unidentified DUT model name [%s]\n\n\n' "$platform_model"
      invalid_platform="true" 
   fi           

}



#Function Definition for dynamically selecting Keycode and key count for individual platforms



platform_keycode_count_finder() {

   local prem_app="$1"
   sleep 1
   platform_type_finder
   case "$platform_model" in
      RPI4)
         if [[ "$prem_app" == "YouTube" ]]; then
            yt_nav_keys=(36 38 40 37 38 40 13 13)
            yt_key_counts=(1 5 1 4 4 1 1 1)
         elif [[ "$prem_app" == "YouTubeTV" ]]; then 
            yttv_nav_keys=(36 38 40 37 38 40 39 13)
            yttv_key_counts=(1 5 1 4 4 1 1 1)  
         elif [[ "$prem_app" == "Amazon" ]]; then
            amz_nav_keys=()
            amz_key_counts=()
         else
            printf '\n\n%s App not available in %s device\n\n\n' "$prem_app" "$platform_model"  
            return 104   
         fi
         return 0
         ;;
      AH212)
         if [[ "$prem_app" == "YouTube" ]]; then
            yt_nav_keys=(36 38 40 37 38 40 39 13 13)
            yt_key_counts=(1 5 1 4 4 1 1 1 1)
         elif [[ "$prem_app" == "YouTubeTV" ]]; then 
            yttv_nav_keys=(36 38 40 37 38 40 39 13)
            yttv_key_counts=(1 5 1 3 4 1 2 1)  
         elif [[ "$prem_app" == "Amazon" ]]; then
            amz_nav_keys=(36 38 40 37 38 40 13 13)
            amz_key_counts=(1 5 1 4 4 1 1 1)
         else
            printf '\n\n%s App not available in %s device\n\n\n' "$prem_app" "$platform_model"  
            return 104 
         fi
         return 0
         ;;
      REALTEKHANK)
         if [[ "$prem_app" == "YouTube" ]]; then
            yt_nav_keys=(36 38 40 37 38 40 39 13 13)
            yt_key_counts=(1 5 1 4 4 1 1 1 1 )
         elif [[ "$prem_app" == "YouTubeTV" ]]; then 
            yttv_nav_keys=(36 38 40 37 38 40 39 13)
            yttv_key_counts=(1 5 1 3 4 1 2 1)  
         elif [[ "$prem_app" == "Amazon" ]]; then
            amz_nav_keys=(36 38 40 37 38 40 13 13)
            amz_key_counts=(1 5 1 4 4 1 1 1)
         else
            printf '\n\n%s App not available in %s device\n\n\n' "$prem_app" "$platform_model"  
            return 104  
         fi
         return 0
         ;;
      BCM972126OTT)
         if [[ "$prem_app" == "YouTube" ]]; then
            yt_nav_keys=(36 38 40 37 38 40 13 13)
            yt_key_counts=(1 5 1 4 4 1 1 1)
         elif [[ "$prem_app" == "YouTubeTV" ]]; then 
            yttv_nav_keys=(36 38 40 37 38 40 39 13)
            yttv_key_counts=(1 5 1 4 4 1 1 1)  
         elif [[ "$prem_app" == "Amazon" ]]; then
            amz_nav_keys=()
            amz_key_counts=()
         else
            printf '\n\n%s App not available in %s device\n\n\n' "$prem_app" "$platform_model"  
            return 104   
         fi
         return 0
         ;;      
      *)
         printf '\n\nInvalid/Unidentified DUT model name [%s]\n\n\n' "$platform_model"
         printf "\n\nDEBUG : Error response returned from FUNC :: platform_type_finder to FUNC :: platform_keycode_count_finder\n\n\n"
         return 104
         ;;
   esac         

}




#Function Definition for YT Apps launch via RDK_service_API or generativeKey 



app_launch_type_handle(){

   local func_rdk_ui_app_launch="$1"
   local ytapp="$2"
   if [[ "$app_launch_type" == "RDK_service_API" ]]; then
      if [[ "$ytapp" == "YouTubeTV" ]]; then
         printf "\nLaunching %s app and loading Homepage\n\n\n" "$ytapp"
      else
         printf "\nLaunching %s app and Starting AV playback\n\n\n" "$ytapp"
      fi   
      premium_app_Launch_and_check "$ytapp"
      premium_app_Launch_exit=$?
      preApp_status_check "$ytapp"
      preApp_status_check_exit=$? 
      if [[ "$ytapp" != "YouTube" ]]; then
         local Query=$(printf "\n\n\nIs %s App launched and Homepage is loaded? [yes/no]: " "$ytapp" )
      else
         local Query=$(printf "\n\n\nIs %s App launched and AV playback started? [yes/no]: " "$ytapp" )
      fi   
      user_confirmation "user_choice" "$Query"
      local user_confirmation_fun_exit=$?

      if [ "$premium_app_Launch_exit" -eq 0 ] && [ "$preApp_status_check_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then 
         sleep 4  
         return 0
      else
         sleep 2
         if [[ "$app_launch_flag" == 1 ]]; then
            printf '\n\nTrying to launch %s from RDK UI via generateKeys method\n\n\n' "$ytapp"
            "$func_rdk_ui_app_launch" "$ytapp"
            local func_rdk_ui_app_exit=$?

            if [ "$func_rdk_ui_app_exit" -eq 0 ]; then
               return 0
            else
               printf '\n\nDEBUG : %s function failed with error code %s\n\n\n' "$func_rdk_ui_app_launch" "$func_rdk_ui_app_exit"
               return $func_rdk_ui_app_exit
            fi      
         else           
            for var in premium_app_Launch_exit preApp_status_check_exit user_confirmation_fun_exit; do
               if [ "${!var}" -ne 0 ]; then
                  return ${!var}
               fi
            done
         fi
      fi
   else
      printf '\n\nLaunching %s app from RDK UI via generateKeys method\n\n\n' "$ytapp"
      "$func_rdk_ui_app_launch" "$ytapp"
      func_rdk_ui_app_exit=$?

      if [ "$func_rdk_ui_app_exit" -ne 0 ]; then
         printf '\n\nDEBUG : %s function failed with error code %s\n\n\n' "$func_rdk_ui_app_launch" "$func_rdk_ui_app_exit"
         return $func_rdk_ui_app_exit
      else
         return 0
      fi   
   fi

}



#Function Definition for Launching Premium Apps from RDK UI platform based logic



platform_launch_sub_handle() {

   local app="$1"
   if [[ "$app" == "YouTube" ]]; then
      app_launch_type_handle rdk_ui_youtube_launch "$app"
      local app_launch_type_handle_fun_exit=$?
      sleep 3

      if [ "$app_launch_type_handle_fun_exit" -eq 0 ]; then    
         return 0
      else
         printf '\n\nDEBUG : app_launch_type_handle function failed and returns %s\n\n\n' "$app_launch_type_handle_fun_exit"
         return $app_launch_type_handle_fun_exit
      fi 
   elif [[ "$app" == "YouTubeTV" ]]; then
      app_launch_type_handle rdk_ui_youtube_TV_launch "$app" 
      local app_launch_type_handle_fun_exit=$?
      sleep 3

      if [ "$app_launch_type_handle_fun_exit" -eq 0 ]; then
         return 0
      else
         printf '\n\nDEBUG : app_launch_type_handle function failed and returns %s\n\n\n' "$app_launch_type_handle_fun_exit"
         return $app_launch_type_handle_fun_exit
      fi                
   elif [[ "$app" == "Amazon" ]]; then
      app_launch_type_handle rdk_ui_amazon_launch "$app" 
      local app_launch_type_handle_fun_exit=$?
      sleep 3

      if [ "$app_launch_type_handle_fun_exit" -eq 0 ]; then
         return 0
      else
         printf '\n\nDEBUG : app_launch_type_handle function failed and returns %s\n\n\n' "$app_launch_type_handle_fun_exit"
         return $app_launch_type_handle_fun_exit
      fi          
   else
      printf '\n\n%s App not available in %s device\n\n\n' "$app" "$platform_model" 
      return 1    
   fi

}



#Function definition for Execution start syntax and Main Function call


exec_start() {

   local testcase_id="$1"
   printf "\n%s TestCase Execution Started...!\n\n\n" "$testcase_id"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   pre_condition_description "$testcase_id"

}



#Function Definition for the pid extraction of premium Apps



premiumApp_PID_extract() {

   local app_name="$1"
   if [[ "$app_name" == "YouTube" ]]; then
      app_name="Cobalt"
   fi
   premiumApp_PID=$(ps -aux | grep "$app_name" | grep -v 'grep' | awk '{print $2}' | head -n 1 | tr -d '[:space:]')
   if [[ -n "$premiumApp_PID" ]]; then
      printf "\n\n\nPID of %s App is :-> %s\n\n\n" "$app_name" "$premiumApp_PID"
      return 0
   else
      printf "\n\n\nUnable to detect PID of %s App\n\n\n" "$app_name"
      return 108
   fi      

}



#Function Definition for detecting the memory usage of premium Apps



memcr_apps_memoryUsage() {

   local proc_id="$1"
   local current_dir="/proc/$proc_id"
   if [[ "$current_dir" != "$(pwd)" ]]; then
      printf "\n\n\nDirectory Mismatched!! Unable to fetch memory usage for the processID : %s\n\n" "$proc_id"
      return 1
   else
      memory_used=$(grep -i 'VmRSS' status | awk '{print $2$3}' | sed 's/kB//')
      if [[ -n "$memory_used" ]]; then
         return 0
      else
         return 120
      fi
   fi   

}



#Function Definition for Launching Premium Apps from RDK UI platform based logic



launch_premium_apps() {

   local app="$1"
   platform_type_finder
   case "$platform_model" in
      RPI4)
         platform_launch_sub_handle "$app"
         local platform_launch_sub_handle_exit=$?

         if [ "$platform_launch_sub_handle_exit" -eq 0 ]; then
            return 0
         else
            printf '\n\nDEBUG : platform_launch_sub_handle function failed and returns %s\n\n\n' "$platform_launch_sub_handle_exit"
            return $platform_launch_sub_handle_exit
         fi
         ;;
      AH212)
         platform_launch_sub_handle "$app"
         local platform_launch_sub_handle_exit=$?

         if [ "$platform_launch_sub_handle_exit" -eq 0 ]; then
            return 0
         else
            printf '\n\nDEBUG : platform_launch_sub_handle function failed and returns %s\n\n\n' "$platform_launch_sub_handle_exit"
            return $platform_launch_sub_handle_exit
         fi
         ;;
      REALTEKHANK)
         platform_launch_sub_handle "$app"
         local platform_launch_sub_handle_exit=$?

         if [ "$platform_launch_sub_handle_exit" -eq 0 ]; then
            return 0
         else
            printf '\n\nDEBUG : platform_launch_sub_handle function failed and returns %s\n\n\n' "$platform_launch_sub_handle_exit"
            return $platform_launch_sub_handle_exit
         fi
         ;;
      BCM972126OTT)
         platform_launch_sub_handle "$app"
         local platform_launch_sub_handle_exit=$?

         if [ "$platform_launch_sub_handle_exit" -eq 0 ]; then
            return 0
         else
            printf '\n\nDEBUG : platform_launch_sub_handle function failed and returns %s\n\n\n' "$platform_launch_sub_handle_exit"
            return $platform_launch_sub_handle_exit
         fi
         ;;   
      *)
         printf '\n\nInvalid/Unidentified DUT model name [%s]\n\n' "$platform_model"
         printf "\n\nDEBUG : Error response returned from FUNC :: platform_type_finder to FUNC :: launch_premium_apps\n\n\n"
         return 1
         ;; 
   esac
      
}



#Function Definition for execute_stepStatusUpdate_steps function used in all Automated Testcases 



execute_stepStatusUpdate_steps() {
  
   local step_no="$1"
   local testcase_prefix="$2"
   local step_func_name="$3"
   local test_app="$4"
   local step_msg="$5"
   local playbackPositionfunc="$6"
   local app_PID="$7"
   local img_format="$8"
   

   if [[ "$test_step_status" != "FAIL" ]]; then
      declare "${testcase_prefix}_num_${step_no}=${step_no}"
      local tc_dynamic_var_name="${testcase_prefix}_num_${step_no}"
      case "$step_func_name" in
         "TC_MEMCR_MANUAL_01"|"TC_HDCPCOMPLIANCE_MANUAL_01"|"TC_HDCPCOMPLIANCE_MANUAL_02"|"TC_HDCPCOMPLIANCE_MANUAL_03"|"TC_HDCPCOMPLIANCE_MANUAL_04"|"TC_HDCPCOMPLIANCE_MANUAL_05"|"TC_HDCPCOMPLIANCE_MANUAL_06"|"TC_IPv6_MANUAL_01"|"TC_IPv6_MANUAL_02"|"TC_IPv6_MANUAL_03"|"TC_IPv6_MANUAL_06"|"TC_IPv6_MANUAL_07")
            "$step_func_name" "${!tc_dynamic_var_name}"
            ;;
         "TC_MEMCR_MANUAL_02_step2"|"TC_MEMCR_MANUAL_02_step4") 
            "$step_func_name" "$step_msg" "$test_app"
            ;; 
         "memcr_app_homekey_close"|"TC_MEMCR_MANUAL_04_step3")
            "$step_func_name" "${!tc_dynamic_var_name}" "$test_app" "$playbackPositionfunc"
            ;;
         "TC_MEMCR_MANUAL_03_step2"|"TC_MEMCR_MANUAL_04_step2"|"TC_IPv6_MANUAL_04"|"TC_IPv6_MANUAL_05") 
            "$step_func_name" "${!tc_dynamic_var_name}" "$test_app"
            ;;
         "TC_MEMCR_MANUAL_03_step3"|"TC_MEMCR_MANUAL_03_step4"|"TC_MEMCR_MANUAL_03_step6")
            "$step_func_name" "${!tc_dynamic_var_name}" "$app_PID" "$test_app"
            ;;
         "TC_MEMCR_MANUAL_04_step5")
            "$step_func_name" "${!tc_dynamic_var_name}" "$test_app" "$playbackPos"
            ;;
         "TC_IMAGEFORMATS_MANUAL_test")
             #Here imgformat_URL's passed as parameter to function from device config file
            if [ "$testcase_prefix" = "tc1_step" ]; then
               "$step_func_name" "${!tc_dynamic_var_name}" "$imgformat_jpeg_url" "$img_format"
            elif [ "$testcase_prefix" = "tc2_step" ]; then 
               "$step_func_name" "${!tc_dynamic_var_name}" "$imgformat_png_url" "$img_format"
            elif [ "$testcase_prefix" = "tc3_step" ]; then 
               "$step_func_name" "${!tc_dynamic_var_name}" "$imgformat_svg_url" "$img_format"
            elif [ "$testcase_prefix" = "tc4_step" ]; then 
               "$step_func_name" "${!tc_dynamic_var_name}" "$imgformat_webp_url" "$img_format"
            else
               printf "\n\nTestcase prefix name invalid...!!!\n\n\n"
               test_step_status="FAIL"
               printf "\nSkipping Step %s,Invalid Testcase prefix name \n\n" "$step_no"
               update_test_status "${testcase_prefix}${step_no}" "NT"
               return 1   
            fi         
            ;;
         "TC_RDKSHELL_MANUAL_01")
            #Here WebkitBrowser_preset_urls passed as parameter to function from device config file
            "$step_func_name" "${!tc_dynamic_var_name}" "${WebkitBrowser_preset_urls[$((step_no-1))]}"
            ;; 
         "TC_RDKSHELL_MANUAL_02")
            #Here HtmlApp_preset_urls passed as parameter to function from device config file
            "$step_func_name" "${!tc_dynamic_var_name}" "${HtmlApp_preset_urls[$((step_no-1))]}"
            ;;
         "TC_RDKSHELL_MANUAL_03")
            #Here WebkitBrowser_default_url and opacity_values passed as parameter to function from device config file
            "$step_func_name" "${!tc_dynamic_var_name}" "${opacity_values[$((step_no-1))]}" "$WebkitBrowser_default_url"
            ;;
         "TC_RDKSHELL_MANUAL_04"|"TC_RDKSHELL_MANUAL_05"|"TC_RDKSHELL_MANUAL_06"|"TC_RDKSHELL_MANUAL_07")
            #Here WebkitBrowser_default_url passed as parameter to function from device config file
            "$step_func_name" "${!tc_dynamic_var_name}" "$WebkitBrowser_default_url"
            ;;                                     
         *)
            printf "\n\nFunction not defined or Invalid function name !!!\n\n\n"
            test_step_status="FAIL"
            printf "\nSkipping Step %s,Invalid function name \n\n" "$step_no"
            update_test_status "${testcase_prefix}${step_no}" "NT"
            return 1
            ;;
      esac

      local tc_fun_exit_status=$?

      if [ "$tc_fun_exit_status" -eq 0 ]; then
            printf "\nStep ${step_no} status\t:  PASS\n\n\n"
            update_test_status "${testcase_prefix}${step_no}" "PASSED"
      else
         if [ "$tc_fun_exit_status" -eq 5 ] && [ "$step_func_name" == "TC_MEMCR_MANUAL_04_step2" ] && [ "$step_no" == "4" ]; then
            printf "\nStep ${step_no} status\t:  PASS\n\n\n"
            update_test_status "${testcase_prefix}${step_no}" "PASSED"
         elif [ "$tc_fun_exit_status" -eq 222 ]; then
            printf "\nStep ${step_no} status\t:  NT\n\n\n"
            echo -e "\nSkipping Step ${step_no}, due to file not found in server\n\n"
            update_test_status "${testcase_prefix}${step_no}" "NT"  
         else   
            printf "\nStep ${step_no} status\t:  FAIL\n\n\n"
            update_test_status "${testcase_prefix}${step_no}" "FAILED"
            test_step_status="FAIL"
         fi   
      fi      
   else
      echo -e "\nSkipping Step ${step_no}, as the previous step failed\n\n"
      update_test_status "${testcase_prefix}${step_no}" "NT"
   fi

}



#Function Definition for checking the file availabililty in the configured Server



check_file_on_serve() {

   local file_url="$1"
   local status_code=$(curl -s -o /dev/null -w "%{http_code}" -L "$file_url")
   
   if [ "$status_code" -eq 200 ]; then
      return 0
   else
      #222 error code return specific for file not found in server
      return 222
   fi

}



#Function Definition for deactivate operations on WebkitBrowser and HtmlApp instances



browserInstance_deactivate() {

   local wkt_instance="$1"
   local json_payload_deactivate=$(printf '{"jsonrpc": "2.0","id": 1234567890,"method": "Controller.1.deactivate","params": {"callsign": "%s"}}' "$wkt_instance")
   local json_Res_deactivate=$(curl -# --data-binary "$json_payload_deactivate" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
   local deactivate_status=$(echo "$json_Res_deactivate" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
   sleep 1
   webkitInstance_statusCheck "$wkt_instance"
   local webkitInstance_statusCheck_exit=$?
   
   local json_payload_getclients=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.getClients", "params":{ }}')
   local json_Res_getclients=$(curl -# --data-binary "$json_payload_getclients" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
   local getclients_success=$(echo "$json_Res_getclients" | sed -n 's/.*"success":[[:space:]]*\([^,}]*\).*/\1/p')
   local getclients_first=$(echo "$json_Res_getclients" | sed -n 's/.*"clients":\[\([^]]*\)\].*/\1/p' | cut -d',' -f1 | tr -d '"[:space:]')
   sleep 1
   if [ "$webkitInstance_statusCheck_exit" -ne 0 ] && [ "$getclients_success" = "true" ] && [ "$getclients_first" = "residentapp" ]; then
      return 0
   else
      #229 error code return specific for webkitInstance deactivate via Controller.1.deactivate API's
      return 229
   fi   

} 



#Function Definition for Suspend operations on RDK Instances like Residentapp | htmlApp | WebkitBrowser etc



rdkshell_suspend_operation() {

   local suspend_obj="$1"
   local json_payload_suspend=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.suspend", "params":{"callsign": "%s"}}' "$suspend_obj")
   local json_Res_suspend=$(curl -# --data-binary "$json_payload_suspend" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
   local suspend_status=$(echo "$json_Res_suspend" | sed -n 's/.*"success":[[:space:]]*\([^,}]*\).*/\1/p')
   sleep 1
   if [ "$suspend_status" = "true" ]; then
      return 0
   else
     #228 error code return specific for WebkitBrowser URL launch via rdkshell.1.launch API's
      return 228
   fi    
}




#Function Definition for launching different URL's via HtmlApp | WebkiBrowser etc



rdkshell_URL_launch() {

   local launch_url="$1"
   local callsign="$2"
   local json_payload_rdkshell=$(printf '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.RDKShell.1.launch", "params": {"callsign": "%s", "type":"%s","uri":"%s", "x":0, "y":0, "w":1920, "h":1080}}' "$callsign" "$callsign" "$launch_url")
   local json_Response_rdkshell=$(curl -# --data-binary "$json_payload_rdkshell" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
   local rdkshell_launch_status=$(echo "$json_Response_rdkshell" | grep -o '"success":[^,}]*' | cut -d: -f2 | tr -d '[:space:]')
   sleep 1

   webkitInstance_statusCheck "$callsign"
   local webkitInstance_statusCheck_exit=$?

   if [ "$rdkshell_launch_status" = "true" ] && [ "$webkitInstance_statusCheck_exit" -eq 0 ]; then
      return 0
   else
      #227 error code return specific for HtmlApp or WebkitBrowser URL launch via rdkshell.1.launch API's
      printf "\n\nDEBUG : rdkshell_URL_launch function failed with error code - %s and status %s\n\n" "$webkitInstance_statusCheck_exit" "$rdkshell_launch_status"
      return 227 
   fi

}




# Function Definition for WebkitInstance  like WebKitBrowser | htmlApp | ResidentApp status check 



webkitInstance_statusCheck() {

   local statusCheck_obj="$1"
   local json_payload_statusCheck=$(printf '{"jsonrpc": "2.0","id": 1234567890,"method": "Controller.1.status@%s"}' "$statusCheck_obj")
   local json_Response_statusCheck=$(curl -# --data-binary "$json_payload_statusCheck" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
   local extracted_value=$(echo "$json_Response_statusCheck" | sed -n -E 's/.*"state":"([^"]*)".*/\1/p' | tr -d '[:space:]')

   if [ "$extracted_value" = "resumed" ] || [ "$extracted_value" = "activated" ]; then
      return 0
   else
      #226 error code return specific for WebkitBrowser URL launch via rdkshell.1.launch API's
      return 226
   fi 

}




#Function Definition for getScreenResolution via org.rdk.RDKShell plugin



rdkshell_getScreenResolution() {

   local json_payload_getScreenRes=$(printf '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.RDKShell.1.getScreenResolution"}')
   local json_Res_getScreenRes=$(curl -# --data-binary "$json_payload_getScreenRes" -H "Content-Type:text/plain;" http://127.0.0.1:9998/jsonrpc)
   local getScreenRes_status=$(echo "$json_Res_getScreenRes" | sed -n 's/.*"success":[[:space:]]*\([^,}]*\).*/\1/p')
   #Extract the value of 'w' (width)
   getScreenRes_width=$(echo "$json_Res_getScreenRes" | grep -o '"w":[0-9]*' | sed 's/"w"://')
   #Extract the value of 'h' (height)
   getScreenRes_height=$(echo "$json_Res_getScreenRes" | grep -o '"h":[0-9]*' | sed 's/"h"://')
   sleep 1

   if [ "$getScreenRes_status" = "true" ] && [ -n "$getScreenRes_width" ] && [ -n "$getScreenRes_height" ]; then
      printf "\n\nCurrent ScreenResolution width : %s\n\nCurrent ScreenResolution height : %s\n\n\n" "$getScreenRes_width" "$getScreenRes_height"
      return 0
   else
      if [ "$getScreenRes_status" != "true" ]; then
         #237 error code return specific for opacity value setting error
         printf "\n\nDEBUG : org.rdk.RDKShell.1.getScreenResolution return false value\n\n\n"
         return 237
      else
         printf "\n\nWidth : [ %s ] and Height : [ %s ] return empty value from org.rdk.RDKShell.1.getScreenResolution\n\n\n" "$getScreenRes_width" "$getScreenRes_height"
         return 1
      fi
   fi

}




#Function Definition for setScreenResolution via org.rdk.RDKShell plugin



rdkshell_setScreenResolution() {
   
   local w="$1"
   local h="$2"
   local json_payload_setScreenRes=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.setScreenResolution", "params":{ "w": %s, "h": %s }}' "$w" "$h")
   local json_Res_setScreenRes=$(curl -# --data-binary "$json_payload_setScreenRes" -H "Content-Type:text/plain;" http://127.0.0.1:9998/jsonrpc)
   local setScreenRes_status=$(echo "$json_Res_setScreenRes" | sed -n 's/.*"success":[[:space:]]*\([^,}]*\).*/\1/p')
   sleep 1

   if [ "$setScreenRes_status" = "true" ]; then
      return 0
   else
      #238 error code return specific for opacity value setting error
      printf "\n\nDEBUG : org.rdk.RDKShell.1.setScreenResolution return false value\n\n\n"
      return 238
   fi
       
}




#Function Definition for org.rdk.RDKShell.1.launch of Apps 



rdkshell_launch_operation() {

   local launch_obj="$1"
   local json_payload_launch=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "%s", "type":"", "uri":""}}' "$launch_obj")
   local json_Res_launch=$(curl -# --data-binary "$json_payload_launch" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
   local launch_status=$(echo "$json_Res_launch" | sed -n 's/.*"success":[[:space:]]*\([^,}]*\).*/\1/p')
   sleep 1
   if [ "$launch_status" = "true" ]; then
      return 0
   else
     #223 error code return specific for apps launch via rdkshell.1.launch API's
      return 223
   fi    
} 



#Function defnition for sub function to handle immediate playback start on Ipv6 testcase and HDCP testcases



immediate_playback_start() {

   local step_no="$1"
   local app="$2"
   local user_choice_av="user_choice_av"
   local query_AV_playback=$(printf "\n\nIs Youtube | XUMO App launched and AV playback started? [yes/no]: ")
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "\nStep %s\t\t: Execute curl command to start Immediate AV plyback from Youtube | XUMO App\n\n\n" "$step_num"
   local curl_to_launch="curl --data-binary '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"YouTube.1.deeplink\",\"params\": \"$yt_URL\"}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc"
   printf "\n$curl_to_launch\n\n\n" 
   AV_playback_mode "$app"
   local AV_playback_mode_exit=$?

   user_confirmation "$user_choice_av" "$query_AV_playback"
   local user_confirmation_fun_exit=$?

   if [ "$AV_playback_mode_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
      return 0
   else
      return 1
   fi

}



#Function Definition for check_log_for_string to string match in given logs  



check_log_for_string() {
   
   local log_file="$1"
   local search_string="$2"
   
   if [[ -z "$log_file" || -z "$search_string" ]]; then
      printf 'ERROR: log_file or search_string is empty\n' >&2
      #2 error code return specific for log_file or search_string is empty
      return 2
   fi

   if [[ ! -f "$log_file" ]]; then
      printf 'ERROR: log file not found: %s\n' "$log_file" >&2
      #2 error code return specific for log_file not found
      return 2
   fi

   last_match=$(tail -n 500 "$log_file" | grep -F -i -o "$search_string" | tail -n 1)
   if [[ -n "$last_match" ]]; then
      printf "\n\nExpected logs : %s found on log file : %s\n\n\n" "$search_string" "$log_file"
      return 0
   else
      printf "\n\nFailed to detect Expected logs : %s from log file : %s\n\n\n" "$search_string" "$log_file"
      #7 error code return specific for expected logs not found from function : check_log_for_string
      return 7
   fi   

}



#Function Definition for get_JSON_KEY_values to extract key values from HDCP JsonRpc response  



get_JSON_KEY_values() {
    local key="$1"
    local jsonRpc="$2"

    # STEP 1: Extract the raw value after the key
    # It looks for the key, then grabs everything until a comma or closing brace
    local raw_value=$(echo "$jsonRpc" | sed -n 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*\([^,}]*\).*/\1/p')

    # STEP 2: Clean the value
    # We use 'tr' to delete unwanted symbols and 'xargs' to trim whitespace
    # tr -d '[]"{}' deletes those specific characters globally from the string
    clean_value=$(echo "$raw_value" | tr -d '[]"{}\r' | xargs)

    echo "$clean_value"

}




#Function Definition for postcondition image formats postCondition_Execution_WebKitInst



postCondition_Execution_WebKitInst() {
 
  local testcaseID="$1"
  local rdkshell_suspend_exit rdkshell_launch_exit
  if [[ "$testcaseID" == "TC_RDKSHELL_MANUAL_02" ]]; then
    rdkshell_suspend_operation "HtmlApp"
    rdkshell_suspend_exit=$?

    rdkshell_launch_operation "ResidentApp"
    rdkshell_launch_exit=$?
  else    
    rdkshell_suspend_operation "WebKitBrowser"
    rdkshell_suspend_exit=$?

    rdkshell_launch_operation "ResidentApp"
    rdkshell_launch_exit=$?
  fi  
  if [ "$rdkshell_suspend_exit" -eq 0 ] && [ "$rdkshell_launch_exit" -eq 0 ]; then
    printf "\n\nWebkitBrowser instance suspended and RDK UI loaded on TV\n\n\n"
    return 0
  else
    printf "\n\nFailed to suspended WebkitBrowser instance and load RDK UI on TV\n\n\n"
    return 1
  fi    

}




#Function to handle the submenu for Testcases execution result



testcase_result_display_menu() {

   local testCase_ID="$1"
   while true; do
      case "$testCase_ID" in
         "TC_EXTERNALAUDIO_MANUAL") 
            printf "\n"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n'
            printf "                                                   ******* TestCase Execution Results Menu :  %s *******                                                                    " "$testCase_ID"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'
            printf '01. Test Execution Result : TC_EXTERNALAUDIO_MANUAL_01  :\t[ Pair and connect an external BT Device ] \n\n'
            printf '02. Test Execution Result : TC_EXTERNALAUDIO_MANUAL_02  :\t[ Start Audio streaming in external BT Device ] \n\n'
            printf '03. Test Execution Result : TC_EXTERNALAUDIO_MANUAL_03  :\t[ Unpair and Disconnect external BT Device ] \n\n'
            printf '04. Test Execution Result : TC_EXTERNALAUDIO_MANUAL_04  :\t[ Reboot External BT device while Audio streaming ] \n\n'
            printf '05. Test Execution Result : TC_EXTERNALAUDIO_MANUAL_05  :\t[ Volume Control (Mute/Unmute) while Audio streaming ] \n\n'
            printf '06. Test Execution Result : TC_EXTERNALAUDIO_MANUAL_06  :\t[ Volume Control (Increase/Decrease) while Audio streaming ] \n\n'
            printf '07. Test Execution Result : TC_EXTERNALAUDIO_MANUAL_07  :\t[ DeviceInfo verification of connected external BT Device ] \n\n'
            printf '08. Overall TestSuite Execution Status\n\n'
            printf '09. Delete all Test Execution reports\n\n'
            printf '10. Return to the Main Menu\n\n'
            printf "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n";

            read -p "Enter an Option to proceed : " menu_choice_1_1
            printf '\n\n'
            case "$menu_choice_1_1" in 
               1)
                  trigger_from_Execution_Result_menu "TC_EXTERNALAUDIO_MANUAL_01" "tc1_step" "tc_EXTERNALAUDIO_MANUAL_testsuite"
                  ;;
               2)
                  trigger_from_Execution_Result_menu "TC_EXTERNALAUDIO_MANUAL_02" "tc2_step" "tc_EXTERNALAUDIO_MANUAL_testsuite"
                  ;;
               3)
                  trigger_from_Execution_Result_menu "TC_EXTERNALAUDIO_MANUAL_03" "tc3_step" "tc_EXTERNALAUDIO_MANUAL_testsuite"
                  ;;
               4)
                  trigger_from_Execution_Result_menu "TC_EXTERNALAUDIO_MANUAL_04" "tc4_step" "tc_EXTERNALAUDIO_MANUAL_testsuite"
                  ;;
               5)
                  trigger_from_Execution_Result_menu "TC_EXTERNALAUDIO_MANUAL_05" "tc5_step" "tc_EXTERNALAUDIO_MANUAL_testsuite"
                  ;;
               6)
                  trigger_from_Execution_Result_menu "TC_EXTERNALAUDIO_MANUAL_06" "tc6_step" "tc_EXTERNALAUDIO_MANUAL_testsuite"
                  ;;
               7)
                  trigger_from_Execution_Result_menu "TC_EXTERNALAUDIO_MANUAL_07" "tc7_step" "tc_EXTERNALAUDIO_MANUAL_testsuite"
                  ;;            
               8)
                  overall_testsuite_execution_status "TC_EXTERNALAUDIO_MANUAL_"
                  ;;
               9)
                  cleanup_testExecution_reports "TC_EXTERNALAUDIO_MANUAL_"
                  ;;    
               10)
                  printf '\n\nExiting TestCase Execution Results Menu\n\n\n' 
                  break
                  ;;  
               *)
                  printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
                  ;;      
            esac
            ;;   
         "TC_MEMCR_MANUAL")
            printf "\n"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n'
            printf "                                                        ******* TestCase Execution Results Menu :  %s *******                                                                    " "$testCase_ID"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'
            printf '01. Test Execution Result : TC_MEMCR_MANUAL_01       :\t[ Check the memcr status ] \n\n'
            printf '02. Test Execution Result : TC_MEMCR_MANUAL_02       :\t[ Check the state of YouTube app after pressing the Home button post-launch ] \n\n'
            printf '03. Test Execution Result : TC_MEMCR_MANUAL_03       :\t[ Verify whether memory usage decreases after pressing the Home button from YouTube App ] \n\n'
            printf '04. Test Execution Result : TC_MEMCR_MANUAL_04       :\t[ Verify YouTube State Serialization after Hibernate and Resume ] \n\n'
            printf '05. Test Execution Result : TC_MEMCR_MANUAL_05       :\t[ Check the state of YouTubeTV app after pressing the Home button post-launch ] \n\n'
            printf '06. Test Execution Result : TC_MEMCR_MANUAL_06       :\t[ Verify whether memory usage decreases after pressing the Home button from YouTubeTV App ] \n\n'
            printf '07. Test Execution Result : TC_MEMCR_MANUAL_07       :\t[ Verify YouTubeTV State Serialization after Hibernate and Resume ] \n\n'
            printf '08. Test Execution Result : TC_MEMCR_MANUAL_08       :\t[ Check the state of Amazon app after pressing the Home button post-launch ] \n\n'
            printf '09. Test Execution Result : TC_MEMCR_MANUAL_09       :\t[ Verify whether memory usage decreases after pressing the Home button from Amazon App ] \n\n'
            printf '10. Test Execution Result : TC_MEMCR_MANUAL_10       :\t[ Verify Amazon State Serialization after Hibernate and Resume ] \n\n'
            printf '11. Overall TestSuite Execution Status\n\n'
            printf '12. Delete all Test Execution reports\n\n'
            printf '13. Return to the Main Menu\n\n'
            printf "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n";

            read -p "Enter an Option to proceed : " menu_choice_1_1
            printf '\n\n'
            case "$menu_choice_1_1" in
               1)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_01" "tc1_step" "tc_MEMCR_MANUAL_testsuite"
                  ;;
               2)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_02" "tc2_step" "tc_MEMCR_MANUAL_testsuite"
                  ;;
               3)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_03" "tc3_step" "tc_MEMCR_MANUAL_testsuite"
                  ;;
               4)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_04" "tc4_step" "tc_MEMCR_MANUAL_testsuite"
                  ;;
               5)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_05" "tc5_step" "tc_MEMCR_MANUAL_testsuite"
                  ;;
               6)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_06" "tc6_step" "tc_MEMCR_MANUAL_testsuite"
                  ;;
               7)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_07" "tc7_step" "tc_MEMCR_MANUAL_testsuite"
                  ;;
               8)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_08" "tc8_step" "tc_MEMCR_MANUAL_testsuite"
                  ;;
               9)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_09" "tc9_step" "tc_MEMCR_MANUAL_testsuite"
                  ;; 
               10)
                  trigger_from_Execution_Result_menu "TC_MEMCR_MANUAL_10" "tc10_step" "tc_MEMCR_MANUAL_testsuite"
                  ;;                              
               11)
                  overall_testsuite_execution_status "TC_MEMCR_MANUAL_"
                  ;;
               12)
                  cleanup_testExecution_reports "TC_MEMCR_MANUAL_"
                  ;;    
               13)
                  printf '\n\nExiting TestCase Execution Results Menu\n\n\n' 
                  break
                  ;;  
               *)
                  printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
                  ;;      
            esac
            ;;
         "TC_IMAGEFORMATS_MANUAL")  
            printf "\n"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n'
            printf "                                                   ******* TestCase Execution Results Menu :  %s *******                                                                    " "$testCase_ID"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'
            printf '01. Test Execution Result : TC_IMAGEFORMATS_MANUAL_01        :\t[ Verify the Jpeg image format launch via WebkitBrowser] \n\n'
            printf '02. Test Execution Result : TC_IMAGEFORMATS_MANUAL_02        :\t[ Verify the png image format launch via WebkitBrowser ] \n\n'
            printf '03. Test Execution Result : TC_IMAGEFORMATS_MANUAL_03        :\t[ Verify the svg image format launch via WebkitBrowser ] \n\n'
            printf '04. Test Execution Result : TC_IMAGEFORMATS_MANUAL_04        :\t[ Verify the webp image format launch via WebkitBrowser ] \n\n'
            printf '05. Overall TestSuite Execution Status\n\n'
            printf '06. Delete all Test Execution reports\n\n'
            printf '07. Return to the Main Menu\n\n'
            printf "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n";

            read -p "Enter an Option to proceed : " menu_choice_1_1
            printf '\n\n'
            case "$menu_choice_1_1" in 
               1)
                  trigger_from_Execution_Result_menu "TC_IMAGEFORMATS_MANUAL_01" "tc1_step" "tc_IMAGEFORMATS_MANUAL_testsuite"
                  ;;
               2)
                  trigger_from_Execution_Result_menu "TC_IMAGEFORMATS_MANUAL_02" "tc2_step" "tc_IMAGEFORMATS_MANUAL_testsuite"
                  ;;
               3)
                  trigger_from_Execution_Result_menu "TC_IMAGEFORMATS_MANUAL_03" "tc3_step" "tc_IMAGEFORMATS_MANUAL_testsuite"
                  ;;
               4)
                  trigger_from_Execution_Result_menu "TC_IMAGEFORMATS_MANUAL_04" "tc4_step" "tc_IMAGEFORMATS_MANUAL_testsuite"
                  ;;
               5)
                  overall_testsuite_execution_status "TC_IMAGEFORMATS_MANUAL_"
                  ;;
               6)
                  cleanup_testExecution_reports "TC_IMAGEFORMATS_MANUAL_"
                  ;;    
               7)
                  printf '\n\nExiting TestCase Execution Results Menu.....\n\n\n' 
                  break
                  ;;  
               *)
                  printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
                  ;;      
            esac
            ;;
         "TC_RDKSHELL_MANUAL")  
            printf "\n"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n'
            printf "                                                   ******* TestCase Execution Results Menu :  %s *******                                                                    " "$testCase_ID"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'
            printf '01. Test Execution Result : TC_RDKSHELL_MANUAL_01        :\t[ Verify the HTML preset Url launch via WebkitBrowser with RDKShell ] \n\n'
            printf '02. Test Execution Result : TC_RDKSHELL_MANUAL_02        :\t[ Verify HtmlApp launch with RDKShell and Load Url multiple times ] \n\n'
            printf '03. Test Execution Result : TC_RDKSHELL_MANUAL_03        :\t[ Verify the Opacity behavior in WebKitBrowser ] \n\n'
            printf '04. Test Execution Result : TC_RDKSHELL_MANUAL_04        :\t[ Verify the Scale behavior in WebKitBrowser ] \n\n'
            printf '05. Test Execution Result : TC_RDKSHELL_MANUAL_05        :\t[ Verify the Bounds behavior in WebKitBrowser ] \n\n'
            printf '06. Test Execution Result : TC_RDKSHELL_MANUAL_06        :\t[ Verify the Animation behavior in WebKitBrowser ] \n\n'
            printf '07. Test Execution Result : TC_RDKSHELL_MANUAL_07        :\t[ Verify the setScreenResolution behaviour in RDKShell plugin using curl command ] \n\n'
            printf '08. Overall TestSuite Execution Status\n\n'
            printf '09. Delete all Test Execution reports\n\n'
            printf '10. Return to the Main Menu\n\n'
            printf "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n";

            read -p "Enter an Option to proceed : " menu_choice_1_1
            printf '\n\n'
            case "$menu_choice_1_1" in 
               1)
                  trigger_from_Execution_Result_menu "TC_RDKSHELL_MANUAL_01" "tc1_step" "tc_RDKSHELL_MANUAL_testsuite"
                  ;;
               2)
                  trigger_from_Execution_Result_menu "TC_RDKSHELL_MANUAL_02" "tc2_step" "tc_RDKSHELL_MANUAL_testsuite"
                  ;;
               3)
                  trigger_from_Execution_Result_menu "TC_RDKSHELL_MANUAL_03" "tc3_step" "tc_RDKSHELL_MANUAL_testsuite"
                  ;;
               4)
                  trigger_from_Execution_Result_menu "TC_RDKSHELL_MANUAL_04" "tc4_step" "tc_RDKSHELL_MANUAL_testsuite"
                  ;;
               5)
                  trigger_from_Execution_Result_menu "TC_RDKSHELL_MANUAL_05" "tc5_step" "tc_RDKSHELL_MANUAL_testsuite"
                  ;;
               6)
                  trigger_from_Execution_Result_menu "TC_RDKSHELL_MANUAL_06" "tc6_step" "tc_RDKSHELL_MANUAL_testsuite"
                  ;;
               7)
                  trigger_from_Execution_Result_menu "TC_RDKSHELL_MANUAL_07" "tc7_step" "tc_RDKSHELL_MANUAL_testsuite"
                  ;;         
               8)
                  overall_testsuite_execution_status "TC_RDKSHELL_MANUAL_"
                  ;;
               9)
                  cleanup_testExecution_reports "TC_RDKSHELL_MANUAL_"
                  ;;    
               10)
                  printf '\n\nExiting TestCase Execution Results Menu.....\n\n\n' 
                  break
                  ;;  
               *)
                  printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
                  ;;      
            esac
            ;; 
         "TC_HDCPCOMPLIANCE_MANUAL")
            printf "\n"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n'
            printf "                                                   ******* TestCase Execution Results Menu :  %s *******                                                                    " "$testCase_ID"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'
            printf '01. Test Execution Result : TC_HDCPCOMPLIANCE_MANUAL_01        :\t[ Verify the HDMI cable connected status ] \n\n'
            printf '02. Test Execution Result : TC_HDCPCOMPLIANCE_MANUAL_02        :\t[ Verify the HDCP authentication initiated status  ] \n\n'
            printf '03. Test Execution Result : TC_HDCPCOMPLIANCE_MANUAL_03        :\t[ Verify the HDCP authenticated status ] \n\n'
            printf '04. Test Execution Result : TC_HDCPCOMPLIANCE_MANUAL_04        :\t[ Verify the HDCP protocol support ] \n\n'
            printf '05. Test Execution Result : TC_HDCPCOMPLIANCE_MANUAL_05        :\t[ Verify the HDCP enabled status ] \n\n'
            printf '06. Test Execution Result : TC_HDCPCOMPLIANCE_MANUAL_06        :\t[ Verify the device is supported, received and current HDCP version ] \n\n'
            printf '07. Overall TestSuite Execution Status\n\n'
            printf '08. Delete all Test Execution reports\n\n'
            printf '09. Return to the Main Menu\n\n'
            printf "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n"

            read -p "Enter an Option to proceed : " menu_choice_1_1
            printf '\n\n'
            case "$menu_choice_1_1" in 
               1)
                  trigger_from_Execution_Result_menu "TC_HDCPCOMPLIANCE_MANUAL_01" "tc1_step" "tc_HDCPCOMPLIANCE_MANUAL_testsuite"
                  ;;
               2)
                  trigger_from_Execution_Result_menu "TC_HDCPCOMPLIANCE_MANUAL_02" "tc2_step" "tc_HDCPCOMPLIANCE_MANUAL_testsuite"
                  ;;
               3)
                  trigger_from_Execution_Result_menu "TC_HDCPCOMPLIANCE_MANUAL_03" "tc3_step" "tc_HDCPCOMPLIANCE_MANUAL_testsuite"
                  ;;
               4)
                  trigger_from_Execution_Result_menu "TC_HDCPCOMPLIANCE_MANUAL_04" "tc4_step" "tc_HDCPCOMPLIANCE_MANUAL_testsuite"
                  ;;
               5)
                  trigger_from_Execution_Result_menu "TC_HDCPCOMPLIANCE_MANUAL_05" "tc5_step" "tc_HDCPCOMPLIANCE_MANUAL_testsuite"
                  ;;
               6)
                  trigger_from_Execution_Result_menu "TC_HDCPCOMPLIANCE_MANUAL_06" "tc6_step" "tc_HDCPCOMPLIANCE_MANUAL_testsuite"
                  ;;       
               7)
                  overall_testsuite_execution_status "TC_HDCPCOMPLIANCE_MANUAL_"
                  ;;
               8)
                  cleanup_testExecution_reports "TC_HDCPCOMPLIANCE_MANUAL_"
                  ;;    
               9)
                  printf '\n\nExiting TestCase Execution Results Menu.....\n\n\n' 
                  break
                  ;;  
               *)
                  printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
                  ;;      
            esac
            ;;
         "TC_IPv6_MANUAL")
            printf "\n"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n'
            printf "                                                   ******* TestCase Execution Results Menu :  %s *******                                                                    " "$testCase_ID"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'
            printf '01. Test Execution Result : TC_IPv6_MANUAL_01        :\t[ Verify the IP Settings when connected to an IPv6 supported SSID ] \n\n'
            printf '02. Test Execution Result : TC_IPv6_MANUAL_02        :\t[ Verify the public IPv6 IP when connected to an IPv6 supported SSID and Ethernet is connected ] \n\n'
            printf '03. Test Execution Result : TC_IPv6_MANUAL_03        :\t[ Verify the public IPv6 IP when connected to an IPv6 supported SSID and Ethernet is disconnected ] \n\n'
            printf '04. Test Execution Result : TC_IPv6_MANUAL_04        :\t[ Verify the internet accessibility when connected to IPv6 supported SSID and Ethernet is connected ] \n\n'
            printf '05. Test Execution Result : TC_IPv6_MANUAL_05        :\t[ Verify the internet accessibility when connected to IPv6 supported SSID and Ethernet is disconnected ] \n\n'
            printf '06. Test Execution Result : TC_IPv6_MANUAL_06        :\t[ Verify the trace API when connected to an IPv6 supported SSID and Ethernet is disconnected ] \n\n'
            printf '07. Test Execution Result : TC_IPv6_MANUAL_07        :\t[ Verify the ping API when connected to an IPv6 supported SSID and Ethernet is disconnected ] \n\n'
            printf '08. Overall TestSuite Execution Status\n\n'
            printf '09. Delete all Test Execution reports\n\n'
            printf '10. Return to the Main Menu\n\n'
            printf "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n"

            read -p "Enter an Option to proceed : " menu_choice_1_1
            printf '\n\n'
            case "$menu_choice_1_1" in 
               1)
                  trigger_from_Execution_Result_menu "TC_IPv6_MANUAL_01" "tc1_step" "tc_IPv6_MANUAL_testsuite"
                  ;;
               2)
                  trigger_from_Execution_Result_menu "TC_IPv6_MANUAL_02" "tc2_step" "tc_IPv6_MANUAL_testsuite"
                  ;;
               3)
                  trigger_from_Execution_Result_menu "TC_IPv6_MANUAL_03" "tc3_step" "tc_IPv6_MANUAL_testsuite"
                  ;;
               4)
                  trigger_from_Execution_Result_menu "TC_IPv6_MANUAL_04" "tc4_step" "tc_IPv6_MANUAL_testsuite"
                  ;;
               5)
                  trigger_from_Execution_Result_menu "TC_IPv6_MANUAL_05" "tc5_step" "tc_IPv6_MANUAL_testsuite"
                  ;;
               6)
                  trigger_from_Execution_Result_menu "TC_IPv6_MANUAL_06" "tc6_step" "tc_IPv6_MANUAL_testsuite"
                  ;;  
               7)
                  trigger_from_Execution_Result_menu "TC_IPv6_MANUAL_07" "tc7_step" "tc_IPv6_MANUAL_testsuite"
                  ;;         
               8)
                  overall_testsuite_execution_status "TC_IPv6_MANUAL_"
                  ;;
               9)
                  cleanup_testExecution_reports "TC_IPv6_MANUAL_"
                  ;;    
               10)
                  printf '\n\nExiting TestCase Execution Results Menu.....\n\n\n' 
                  break
                  ;;  
               *)
                  printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
                  ;;      
            esac
            ;;
         *)
           printf "\nInvalid Testsuite ID :[ %s ] detected.|...Exiting...|\n\n\n"
           break
           ;;
      esac      
   done

}



#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________







