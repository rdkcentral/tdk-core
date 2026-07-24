########################################## Generic Functions Used for All TestCases Executions ####################################################
#Author : aharil144@cable.comcast.com

source device.conf

#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




#Function to perfom the generate key operation for RDK UI navigation



_generateKey_RDKUI_navigation() {

   local keyvalue="$1"
   case $keyvalue in
    ''|*[!0-9]*)
        printf '\n\nERROR : keyvalue must be numeric, got [%s]\n\n\n' "$keyvalue" >&2
        return 1
        ;;
   esac
   local clientId="$2"
   local inner_keys_json=$(printf '{"keys":[{"keyCode":%d,"modifiers":[],"delay":0}]}' "$keyvalue")
   local escaped_inner_keys_json=$(printf '%s' "$inner_keys_json" | sed 's/\\/\\\\/g; s/"/\\"/g')
   local keycode_json=$(printf '{"jsonrpc":"2.0","id":"1","method":"org.rdk.RDKWindowManager.generateKey","params":{"client":"%s","keys":"%s"}}' "$clientId" "$escaped_inner_keys_json")
   printf '\n\n%s\n\n' "$keycode_json"
   local key_json_res=$(curl -s -# -H 'Content-Type: application/json' -d "$keycode_json" http://127.0.0.1:9998/jsonrpc)
   local keycode_json_extracted=$(echo "$key_json_res" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
   sleep 1

   if [ "$keycode_json_extracted" == "null" ]; then
      return 0
   else
      printf "\n\nDEBUG => key json response returns : %s\n\n" "$key_json_res"
      return 102
   fi

}



#Function to perfom the app launch using generate key on RDK UI



generateKey_inApp_navigation(){
  
   # local variable to store length of both arrays passed as parameter to generateKey_inApp_navigation
   local key_arr_len=$1
   local keycount_len=$2
   shift 2
   local exit_outer_loop=false
   local keys_executed=0
   
   if [[ $key_arr_len -ne $keycount_len || $key_arr_len -eq 0 ]]; then
      printf "\n\nError: App launch KeyCombination array lengths do not match or Array is empty\n\n\n"
      printf "\n\n\nDEBUG : generateKey_inApp_navigation function recieved either empty or incorrect Array values\n\n\n" 
      #Unique error code for empty array values passed to generateKey_inApp_navigation function
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
            #dynamic_appInstanceId variable is passed to the function from device.conf
            _generateKey_RDKUI_navigation "$key" "$dynamic_appInstanceId"
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
         printf "\n\n"
         printf "\rRDK generateKey keyCode : %s Navigation is in progress%s" "$key" "$dots"
         sleep 2
      done
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
            $'\n\n\nTestcaseID : TC_HDCPCOMPLIANCE_MANUAL_07\n\n\nTestcase description : Verify whether the testing device is HDCP Compliant or not\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. TV should be connected with the HDMI port and source should be selected\n\t\t  3. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_01\n\n\nTestcase description : Verify the IP Settings when connected to an IPv6 supported SSID\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi  SSID which supports IPV6\n\t\t  3. Ethernet should be disconnected after connecting to Wifi SSID\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_02\n\n\nTestcase description : Verify the public IPv6 IP when connected to an IPv6 supported SSID and Ethernet is connected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi SSID which supports IPV6\n\t\t  3.  Ethernet should be in connected state always\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_03\n\n\nTestcase description : Verify the public IPv6 IP when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi SSID which supports IPV6\n\t\t  3. Ethernet should be disconnected after connecting to Wifi SSID\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_04\n\n\nTestcase description : Verify the internet accessibility when connected to an IPv6 supported SSID and Ethernet is connected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi SSID which supports IPV6\n\t\t  3.  Ethernet should be in connected state after connecting to Wifi SSID\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\t\t  5. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_05\n\n\nTestcase description : Verify the internet accessibility when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi SSID which supports IPV6\n\t\t  3.  Ethernet should be disconnected after connecting to Wifi SSID\n\t\t  4. TV should be connected with the HDMI port and source should be selected\n\t\t  5. RDK UI Home page should be visible on DUT prior to test\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_06\n\n\nTestcase description : Verify the trace API when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi  SSID which supports IPV6\n\t\t  3. Ethernet should be disconnected after connecting to Wifi SSID\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_07\n\n\nTestcase description : Verify the ping API when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi  SSID which supports IPV6\n\t\t  3. Ethernet should be disconnected after connecting to Wifi SSID\n\n\n'
            $'\n\n\nTestcaseID : TC_IPv6_MANUAL_08\n\n\nTestcase description : Verify the getPublicIP API response when connected to an IPv6 supported SSID and Ethernet is connected\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. DUT should be connected to a WiFi SSID which supports IPV6\n\t\t  3.  Ethernet should be in connected state always\n\n\n'
            $'\n\n\nTestcaseID : TC_POWER_MANUAL_01\n\n\nTestcase description : Verify DUT can be set to LIGHT SLEEP and then wakeup with the help of RDK service APIs\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. RDK UI Home page should be visible on DUT prior to test\n\t\t  3. Device should be connected to network\n\n\n'
            $'\n\n\nTestcaseID : TC_SYSTEM_MANUAL_01\n\n\nTestcase description : Verify the SSH dropbear service and status\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Device should be connected to either Wifi or etherent network\n\t\t  3. Device Should have a valid IP address to SSH\n\n\n'
            $'\n\n\nTestcaseID : TC_SYSTEM_MANUAL_02\n\n\nTestcase description : Verify the running status of Wpe framework processes\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\t\t  2. Device should be connected to either Wifi or etherent network\n\n\n'
            $'\n\n\nTestcaseID : TC_SYSTEM_MANUAL_03\n\n\nTestcase description : Verify the log rollover RDK functionality\n\n[TEST STEPS]\n\nPre-condition   : 1. DUT should be rebooted prior to the testcase execution\n\n\n'
            $'\n\n\nTestcaseID : __TC_ID__\n\n\nTestcase description : Verify the Speech synthesis TTS | Audio decoding | Audio Context details via WebAudio App\n\n[TEST STEPS]\n\nPre-condition   : 1. WebAudio App should be installed if its not installed in device\n\t\t  2. TV should be connected with the HDMI port and source should be selected\n\t\t  3. Required Audio files and inner Htmls should be hosted in the same server where Webaudio App is hosted\n\t\t  4. Device should be connected to network\n\n\n'

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
   "TC_HDCPCOMPLIANCE_MANUAL_07")      printf "%s" "${pre_description_arr[34]}" ;;
   "TC_IPv6_MANUAL_01")          printf "%s" "${pre_description_arr[35]}" ;;
   "TC_IPv6_MANUAL_02")          printf "%s" "${pre_description_arr[36]}" ;;
   "TC_IPv6_MANUAL_03")          printf "%s" "${pre_description_arr[37]}" ;;
   "TC_IPv6_MANUAL_04")          printf "%s" "${pre_description_arr[38]}" ;;
   "TC_IPv6_MANUAL_05")          printf "%s" "${pre_description_arr[39]}" ;;
   "TC_IPv6_MANUAL_06")          printf "%s" "${pre_description_arr[40]}" ;;
   "TC_IPv6_MANUAL_07")          printf "%s" "${pre_description_arr[41]}" ;;
   "TC_IPv6_MANUAL_08")          printf "%s" "${pre_description_arr[42]}" ;;
   "TC_POWER_MANUAL_01")         printf "%s" "${pre_description_arr[43]}" ;;
   "TC_SYSTEM_MANUAL_01")        printf "%s" "${pre_description_arr[44]}" ;;
   "TC_SYSTEM_MANUAL_02")        printf "%s" "${pre_description_arr[45]}" ;; 
   "TC_SYSTEM_MANUAL_03")        printf "%s" "${pre_description_arr[46]}" ;;
   TC_WEBAUDIO_MANUAL_0[1-9]|TC_WEBAUDIO_MANUAL_1[0-5]) printf "%s" "${pre_description_arr[47]//__TC_ID__/$testcase_id}" ;;
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
      "tc3_step"|"tc7_step") current_step_num=4 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   elif [[ "$testcase_name" == "TC_IPv6_MANUAL" ]]; then
      case "$tc_prifix" in
      "tc1_step"|"tc2_step"|"tc3_step"|"tc6_step"|"tc7_step"|"tc8_step")  current_step_num=1 ;;
      "tc4_step"|"tc5_step") current_step_num=2 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   elif [[ "$testcase_name" == "TC_POWER_MANUAL" ]]; then 
      case "$tc_prifix" in
      "tc1_step") current_step_num=6 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   elif [[ "$testcase_name" == "TC_SYSTEM_MANUAL" ]]; then 
      case "$tc_prifix" in
      "tc1_step"|"tc3_step") current_step_num=2 ;;
      "tc2_step") current_step_num=1 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac
   elif [[ "$testcase_name" == "TC_WEBAUDIO_MANUAL" ]]; then
      case "$tc_prifix" in
      "tc1_step"|"tc2_step"|"tc3_step"|"tc6_step"|"tc7_step"|"tc8_step") current_step_num=4 ;;
      "tc4_step"|"tc5_step"|"tc9_step"|"tc10_step"|"tc11_step"|"tc12_step"|"tc13_step"|"tc14_step"|"tc15_step")  current_step_num=3 ;;
      *) printf "\nInvalid testCase step number. Unable to detect current step number!!!\n\n\n" ;;
      esac    
   else
      printf "\nInvalid testCase name. Unable to detect current step number!!!\n\n\n"
   fi
}




#Function definition for any_app_installer to perfom the App installation on precondition prior to test if its not already installed



any_app_installer() {

   local app_name="$1"
   local app_bundle="$2"
   local download_URL="$3"
   local app_version="$4"
   isAppInstalled "$app_name"
   local isAppInstalled_exit=$?
   local app_to_install="$app_to_check_lc"
   if [ "$isAppInstalled_exit" -eq 1 ]; then
      printf "\n\n\nDEBUG : %s App is not installed on device. Starting App download and Installation!!!\n\n\n" "$app_name"
      [ -z "$app_bundle" ] || [ -z "$download_URL" ] && { printf "\n\nDEBUG : app_bundle or download_URL param is empty\n\n" >&2; return 1; }

      check_file_on_serve "$download_URL/$app_bundle"
      local check_file_on_serve_exit=$?

      if [ "$check_file_on_serve_exit" -eq 0 ]; then      
         local json_pay_app_download=$(printf '{ "jsonrpc": 2.0, "id": 2, "method": "org.rdk.DownloadManager.1.download", "params": { "url": "%s/%s", "options": {"priority": true, "retries": 0, "rateLimit": 0} } }' "$download_URL" "$app_bundle")
         local json_res_app_download=$(curl -# -d "$json_pay_app_download"  http://127.0.0.1:9998/jsonrpc)
         sleep 3
         local download_ID=$(printf '%s\n' "$json_res_app_download" | sed -n 's/.*"result":"\([^"]*\)".*/\1/p')
         local error_msg=$(printf '%s\n' "$json_res_app_download" | sed -n 's/.*"message":"\([^"]*\)".*/\1/p')
         [ -z "$download_ID" ] && [ -n "$error_msg" ] && { printf "\n\n\nDEBUG : App bundle download failed due to error : %s\n\n" "$error_msg" >&2; return 1; }
         case $download_ID in
            [0-9][0-9][0-9][0-9])
               local package_ID="package$download_ID"
               printf "\n\n\nDownlaoded app packageID : %s\n\n\n" "$package_ID"
               ;;
            *)
               printf "\n\nDEBUG : invalid download_ID response [%s]\n\n" "$download_ID" >&2
               return 1
               ;;
         esac
         platform_type_finder
         if [ "$platform_model" == "BCM974116SFF" ] && [ "$invalid_platform" == "false" ]; then
            local fileLocator_path="/mnt/media/apps/dac_apps/CDL/"
         else
            local fileLocator_path="/opt/CDL/"  
         fi
         sleep 2
         local json_pay_app_install=$(printf '{"jsonrpc":2.0,"id":1,"method":"org.rdk.PackageManagerRDKEMS.install","params":{"packageId":"com.rdkcentral.%s","version":"%s","fileLocator":"%s%s"}}' "$app_to_install" "$app_version" "$fileLocator_path" "$package_ID")
         local json_res_app_install=$(curl -# -H "Content-Type: application/json" -X POST -d "$json_pay_app_install" http://127.0.0.1:9998/jsonrpc)
         sleep 1
         local install_status=$(printf '%s\n' "$json_res_app_install" | sed -n 's/.*"result":"\([^"]*\)".*/\1/p')
         local install_error=$(printf '%s\n' "$json_res_app_install" | sed -n 's/.*"message":"\([^"]*\)".*/\1/p')
         if [ "$install_status" == "NONE" ] && [ -z "$install_error" ]; then
            isAppInstalled "$app_name"
            local isAppInstalled_exit=$?
            if [ "$isAppInstalled_exit" -eq 1 ]; then
               printf "\n\n\nDEBUG : %s App is not installed and not listed in getInstalledApps\n\n" "$app_name"
               return 1
            else
               printf "\n\n\n%s App intallation Successful!!!\n\n" "$app_name"
               installed_appID="$isAppInstalled_appid"
               return 0
            fi
         else
            printf "\n\n\nDEBUG : %s App install status returns error : %s\n\n" "$app_name" "$install_error"
            return 1        
         fi
      else
         printf "\n\n\nDEBUG : Unable to access App bundle -> [ %s ] from server -> [ %s ]\n\n" "$app_bundle" "$download_URL"
         return "$check_file_on_serve_exit"
      fi   
   else
      printf "\n\n\n%s App already installed on device!!!\n\n\n" "$app_name" 
      installed_appID="$isAppInstalled_appid"
      return 0 
   fi      

}




#Function Definition to check whether app is installed or not using isAppInstalled function



isAppInstalled(){

   local app_to_check="$1"
   local entry
   local appID_value
   local appID_value_lc
   local appID_found="false"

   #convert the app name to lowercase and remove spaces to match the appId format in the JSON response
   app_to_check_lc=$(printf '%s' "$app_to_check" | tr '[:upper:]' '[:lower:]' | tr -d ' ')
   printf "\n\n\napp_to_check_lc : %s\n\n\n" "$app_to_check_lc"

   local json_res_getInstalledApps=$(curl -# -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 5, "method": "org.rdk.AppManager.getInstalledApps"}' http://127.0.0.1:9998/jsonrpc)
   local clean_json=$(printf "%s" "$json_res_getInstalledApps" | tr -d '[:space:]')

   # Break JSON into lines using characters { } , as separators
   for entry in $(printf "%s" "$clean_json" | tr '{},' '\n' | grep 'appId'); do
      # entry = "appId":"com.rdkcentral.youtube"
      appID_value=$(printf "%s" "$entry" | sed 's/.*appId":"//; s/"$//')
      appID_value_lc=$(printf '%s' "$appID_value" | tr '[:upper:]' '[:lower:]')
            
      case "$appID_value_lc" in
         *"$app_to_check_lc"*)
            isAppInstalled_appid="$appID_value"
            local appID_found="true"
            #isAppInstalled_appid is a global variable which will hold the appId of the matched app which is to be checked for isInstalled
            local json_pay_isInstalled=$(printf '{"jsonrpc": 2.0, "id": 7, "method": "org.rdk.AppManager.isInstalled", "params": {"appId": "%s"}}' "$isAppInstalled_appid")
            local json_res_isInstalled=$(curl -# -H 'content-type:text/plain;' --data-binary "$json_pay_isInstalled"  http://127.0.0.1:9998/jsonrpc)
            local installed_status=$(echo "$json_res_isInstalled" | sed -n 's/.*"result":[[:space:]]*\([^,}]*\).*/\1/p')
            [ "$installed_status" = "true" ] && return 0
            printf "\n\n\nDEBUG : AppManager.isInstalled API returns error [ %s ]\n\n\n" "$json_res_isInstalled"
            return 1
            ;;
      esac      
   done
   if [ "$appID_found" == "false" ]; then
      return 1
   else
      return 0
   fi
  
}



#Function Definition for get_appInstance_id function which will get the appInstanceId of the launched App using the appId



get_instance_id_by_appid() {
   [ $# -eq 1 ] || return 2

   app_id=$1
   local json_pay_loadedApps=$(printf '{"jsonrpc":"2.0","id":"3","method": "org.rdk.AppManager.getLoadedApps", "params":{}}')
   local json_res_loadedApps=$(curl -# -H "Content-Type: application/json" -d "$json_pay_loadedApps" http://localhost:9998/jsonrpc)

   printf '%s\n' "$json_res_loadedApps" | tr '{},' '\n' | awk -F'"' -v app="$app_id" '
      $2=="appId" {
         want = ($4==app)
         next
      }
      want && $2 == "appInstanceId" {
         printf "%s", $4
         found = 1 
         exit 0
      }
      END {
         if (!found) exit 1   
      }   
   '
}



#Function Definition for setfocus_on_App function which will setFocus on active App using AppinstanceID



setfocus_on_App() {
   
   local app_id="$1"
   local app_client_ID=$(get_instance_id_by_appid "$app_id")
   local get_instance_id_by_appid_exit=$?
   printf "\n\nAppInstanceId : %s\n\n\n" "$app_client_ID"

   if [ "$get_instance_id_by_appid_exit" -eq 1 ] || [ -z "$app_client_ID" ]; then
      printf "\n\n\nDEBUG : Unable to get the appInstanceId for the appId : %s\n\n" "$app_id"
      return 1
   fi
   if [ "$get_instance_id_by_appid_exit" -eq 2 ]; then
      printf "\n\n\nDEBUG : Inavlid params Usage Error!!\n\n"
      return 3
   fi
   dynamic_appInstanceId="$app_client_ID"   
   local json_pay_setfocus=$(printf '{"jsonrpc":"2.0", "id":"3", "method": "org.rdk.RDKWindowManager.setFocus", "params":{"client":"%s"}}' "$app_client_ID")
   local json_res_setfocus=$(curl -# -H "Content-Type: application/json" -d "$json_pay_setfocus" http://localhost:9998/jsonrpc)
   local setfocus_value=$(echo "$json_res_setfocus" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
   if [ "$setfocus_value" == "null" ]; then
      return 0
   else
      printf "\n\nsetFocus operation to appId : %s Failed\n\n" "$app_id"
      return 1
   fi

} 



#Function Definition for start_av_playback function which will select random video from the launched App's homepage and start the AV playback 



start_av_playback() {

   local playback_app_id="$1"
   setfocus_on_App "$playback_app_id"
   local setfocus_on_App_exit="$?"

   if [ "$setfocus_on_App_exit" -eq 0 ]; then
      _generateKey_RDKUI_navigation "39" "$app_client_ID"
      local generateKey_RDKUI_navigation_exit1=$?
      sleep 1
      _generateKey_RDKUI_navigation "13" "$app_client_ID"
      local generateKey_RDKUI_navigation_exit2=$?
      if [ "$generateKey_RDKUI_navigation_exit1" -ne 0 ] && [ "$generateKey_RDKUI_navigation_exit2" -ne 0 ]; then
         printf "\n\n\nDEBUG : RDK UI generateKey navigation failed for keycode : %s\n\n" "13 | 39"
         return 1
      fi
      return 0
   else
      return 1   
   fi   

}



#Function Definition for dynamic_imageformat_loader function which will navigate through the browser_test App and load required image formats. 



dynamic_inApp_loader() {

   local app_id="$1"
   local test_prefix="$2"
   local app_used="$3"
   
   setfocus_on_App "$app_id"
   local setfocus_on_App_exit=$?

   if [ "$setfocus_on_App_exit" -eq 0 ]; then
      inApp_navigation_keycount_finder "$app_used" "$test_prefix"
      local inApp_navigation_keycount_finder_exit=$?

      [ "$inApp_navigation_keycount_finder_exit" -eq 1 ] && return 1
      generateKey_inApp_navigation ${#inapp_nav_keys[@]} ${#inapp_key_counts[@]} "${inapp_nav_keys[@]}" "${inapp_key_counts[@]}"
      local generateKey_inApp_navigation_exit=$?

      if [ "$generateKey_inApp_navigation_exit" -ne 0 ]; then
         printf "\n\n\nDEBUG : generateKey_inApp_navigation function failed with error code : %s\n\n" "$generateKey_inApp_navigation_exit"
         return $generateKey_inApp_navigation_exit
      else
         return 0
      fi
   else
      return 1
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



#Function Definition for Staring AV playback using AV_playback_mode function



AV_playback_handle() {

   local app_name="$1"
   local launch_options="$2"
   isAppInstalled "$app_name"
   local isAppInstalled_exit=$?

   if [ "$isAppInstalled_exit" -eq 1 ]; then
      printf "\n\n\nDEBUG : %s App is not installed on device. Please install and try again!!!\n\n\n" "$app_name"
      return 1
   else
      if [ "$launch_options" == "deeplink" ]; then
         printf "\n\n\n%s App already installed on device. Proceeding the app launch with deeplink url\n\n" "$app_name"
         deeplink_URL_selector "$app_name"
         if [ "$deeplink_flag" -eq 1 ]; then
            printf "\n\n\nDEBUG : %s App deeplink url unavailable or doesn't support deeplink launch\n\n" "$app_name"
            return 1
         else
            anyApp_deeplink_launch "$isAppInstalled_appid" "$deeplink_url" "$app_name"
            anyApp_deeplink_launch_exit=$?
            if [ "$anyApp_deeplink_launch_exit" -ne 0 ]; then
               printf "\n\n\nDEBUG : %s App launch with deeplink failed with error code : %s\n\n" "$app_name" "$anyApp_deeplink_launch_exit"
               return "$anyApp_deeplink_launch_exit"
            fi
            printf "\n\n\n%s App launched with deeplink and AV playback started\n\n" "$app_name"
            return 0
         fi     
      fi
      printf "\n\n\n%s App already installed on device. Proceeding with normal app launch\n\n" "$app_name"
      anyApp_launch "$isAppInstalled_appid" "$app_name"
      local anyApp_launch_exit=$?
      start_av_playback "$isAppInstalled_appid"
      local start_av_playback_exit=$?

      if [ "$anyApp_launch_exit" -ne 0 ] || [ "$start_av_playback_exit" -ne 0 ]; then
         printf "\n\n\nDEBUG : Normal %s App launch and AV playback failed.Launch exit code : %s, Playback exit code : %s\n\n" "$app_name" "$anyApp_launch_exit" "$start_av_playback_exit"
         
         if [ "$anyApp_launch_exit" -ne 0 ]; then
            return "$anyApp_launch_exit"
         fi
         return "$start_av_playback_exit"
      fi
      printf "\n\n\n%s App launched normally and AV playback started\n\n" "$app_name"
      return 0
   fi   

}




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



#Function Definition for deeplink_URL_selector function to select the correct the deeplink URL for the selected App



deeplink_URL_selector() {

   local app="$1"
   deeplink_flag=0
   #Deeplink Urls used here as taken from device conf file
   case "$app" in
      'YouTube') deeplink_url="$yt_URL" ;;
      'Amazon')  deeplink_url="$amz_URL" ;;
      *) 
         deeplink_flag=1 
         ;;
   esac   

}



#Function Definition for anyApp_deeplink_launch function to launch any supported app with deeplink  



anyApp_deeplink_launch() {

   local app_id="$1"
   local deeplink_video_id="$2"
   local app_name="$3"
   local user_choice="user_choice"
   local query_deeplink_launch=$(printf "\n\nIs %s App launched and started AV playback with deeplink URL [yes/no]: " "$app_name")
   local json_pay_launch=$(printf '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "%s", "intent": "playback", "launchArgs": "%s" }}' "$app_id" "$deeplink_video_id")
   local JSON_RESPONSE_launch=$(curl -# -d "$json_pay_launch" http://localhost:9998/jsonrpc)
   sleep 3
   local extracted_value_launch=$(echo "$JSON_RESPONSE_launch" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
   user_confirmation "$user_choice" "$query_deeplink_launch"
   local user_confirmation_fun_exit=$?
   if [ "$extracted_value_launch" == "null" ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
      return 0
   else
      #Any App specific deeplink launch error return code for function anyApp_deeplink_launch
      return 122   
   fi

}



#Function Definition for anyApp_launch function to launch any installed app 


anyApp_launch() {

   local app_id="$1"
   local app_name="$2"
   local user_choice="user_choice"
   local query_app_launch=$(printf "\n\nIs %s App launched successfully [yes/no]: " "$app_name")
   [ -z "$app_id" ] && { printf "\n\n\n AppID is empty, Unable to proceed App launch operation!!!\n\n" >&2; return 1; }
   printf "\n\n\nappID : %s\n\n" "$app_id"
   local json_pay_loadedApps=$(printf '{"jsonrpc":"2.0","id":"3","method": "org.rdk.AppManager.getLoadedApps", "params":{}}')
   local json_res_loadedApps=$(curl -# -H "Content-Type: application/json" -d "$json_pay_loadedApps" http://localhost:9998/jsonrpc)
   if echo "$json_res_loadedApps" | grep -Fq "\"appId\":\"$app_id\""; then
      printf "\n\n\n%s App already have an active instance\n\n" "$app_name"
      return 0
   else    
      local json_pay_launch=$(printf '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "%s", "intent": "", "launchArgs": "" }}' "$app_id")
      local JSON_RESPONSE_launch=$(curl -# -d "$json_pay_launch" http://localhost:9998/jsonrpc)
      sleep 3
      local extracted_value_launch=$(echo "$JSON_RESPONSE_launch" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
      check_log_for_string "$app_Operations_logs_path" "Failed to identify dependency version"
      local check_log_for_string_exit1=$?
      check_log_for_string "$app_Operations_logs_path" "Package not found in mounted packages"
      local check_log_for_string_exit2=$?

      [ "$check_log_for_string_exit1" -eq 0 ] && [ "$check_log_for_string_exit2" -eq 0 ] && { printf "\n\n\nDEBUG : %s App launch operation failed due to dependency version issue\n\n" "$app_name" >&2; return 1; }
      user_confirmation "$user_choice" "$query_app_launch"
      local user_confirmation_fun_exit=$?
      if [ "$extracted_value_launch" == "null" ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
         return 0
      else
         #Any App specific launch error return code for function anyApp_launfich
         return 123   
      fi
   fi   

}



#Function Definition for youtube_deeplink_launch function to launch YouTube with deeplink  


#need to remove this function 
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



#Function defenition for active_anyApp_instance_kill to kill any App's active instance before testcase execution



active_anyApp_instance_kill() {

    local app="$1"
    local app_ID="$2"
    local json_pay_loadedApps=$(printf '{"jsonrpc":"2.0","id":"3","method": "org.rdk.AppManager.getLoadedApps", "params":{}}')
    local json_res_loadedApps=$(curl -# -H "Content-Type: application/json" -d "$json_pay_loadedApps" http://localhost:9998/jsonrpc)
    if echo "$json_res_loadedApps" | grep -Fq "\"appId\":\"$app_ID\""; then
        printf "\n\n\n%s App already have an active instance. Killing the active instance prior to Test Execution\n\n" "$app"
        kill_app "$app" "$app_ID"  
        local kill_app_exit=$?
        if [ "$kill_app_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    fi
    return 0  
      
}



#Function defenition to kill the App instance by actually killing the app



kill_app() {

   local app_to_kill="$1"
   local app_id="$2"
   local kill_app_json=$(printf '{"jsonrpc":"2.0","id":"3","method": "org.rdk.AppManager.killApp", "params":{"appId": "%s"}}' "$app_id" )
   local kill_app_response=$(curl -# -H "Content-Type: application/json" --request POST --data "$kill_app_json" http://127.0.0.1:9998/jsonrpc)
   local kill_app_status=$(echo "$kill_app_response" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
   sleep 1

   if [ "$kill_app_status" == "null" ]; then
      printf '\n\nInstance of %s App killed successfully\n\n\n' "$app_to_kill"
      return 0
   else
      printf '\n\nUnable to Kill the Instance of %s App\n\n\n' "$app_to_kill"
      return 20
   fi

}



#Function defenition to close the App instance by terminating the app



terminate_app() {

   local app_to_terminate="$1"
   local app_id="$2"
   local terminate_app_json=$(printf '{"jsonrpc": 2.0, "id": 15, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "%s"}}' "$app_id" )
   local terminate_app_response=$(curl -# -H "Content-Type: application/json" --data-binary "$terminate_app_json" http://127.0.0.1:9998/jsonrpc)
   local terminate_app_status=$(echo "$terminate_app_response" | sed -n -E 's/.*"result":([^},]*).*/\1/p')
   sleep 1

   if [ "$terminate_app_status" == "null" ]; then
      printf '\n\nInstance of %s App closed successfully\n\n\n' "$app_to_terminate"
      return 0
   else
      printf '\n\nUnable to close/terminate the Instance of %s App\n\n\n' "$app_to_terminate"
      return 20
   fi

}


#Function Definition for Identifying Device model or type



platform_type_finder() {

   invalid_platform="false"
   platform_model=$(awk -F'=' 'BEGIN{IGNORECASE=1} /^MODEL_NUM=/{v=$2} END{print v}' /etc/device.properties)

   case "$platform_model" in
      RPI4)
         printf '\n\nDUT model is RaspberryPi [%s]\n\n\n' "$platform_model"
         ;;
      AH212)
         printf '\n\nDUT model is Amlogic Reference [%s]\n\n\n' "$platform_model"
         ;;
      REALTEKHANK)
         printf '\n\nDUT model is Realtek Reference [%s]\n\n\n' "$platform_model"
         ;;
      BCM972126OTT)
         printf '\n\nDUT model is Broadcom Reference : [%s]\n\n\n' "$platform_model"
         ;;
      BCM974116SFF)
         printf '\n\nDUT model is Broadcom Reference : [%s]\n\n\n' "$platform_model"
         ;;  
      *)
         printf '\n\nDEBUG : Invalid/Unidentified DUT model name [%s]\n\n\n' "$platform_model"
         invalid_platform="true"
         ;;
   esac

}



#Function Definition for inApp_navigation_keycount_finder to dynamically selecting Keycode and key count for inApp naviagtion and selections



inApp_navigation_keycount_finder() {

   local inapp_used="$1"
   local testcase_ID="$2"
   if [ "$inapp_used" == "Browser_test" ]; then
      case "$testcase_ID" in
         tc1_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(1 1)
            ;;
         tc2_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(2 1)
            ;;
         tc3_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(3 1)
            ;;
         tc4_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(4 1)
            ;;
         *)
            printf "\n\n\nnav_keys and key_counts not avaialble for testcase : %s\n\n\n" "$testcase_ID"
            return 1
            ;;
      esac  
      return 0

   elif [ "$inapp_used" == "webaudio_manual" ]; then
      case "$testcase_ID" in
         tc1_step)
            inapp_nav_keys=(9 13 9 13)
            inapp_key_counts=(1 1 2 1)
            ;;
         tc2_step)
            inapp_nav_keys=(9 13 9 13)
            inapp_key_counts=(2 1 2 1)
            ;;
         tc3_step)
            inapp_nav_keys=(9 13 9 13)
            inapp_key_counts=(3 1 2 1)
            ;;
         tc4_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(4 1)
            ;;
         tc5_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(5 1)
            ;;
          tc6_step)
            inapp_nav_keys=(9 13 9 13)
            inapp_key_counts=(6 1 4 1)    
            ;;
         tc7_step)
            inapp_nav_keys=(9 13 9 13)
            inapp_key_counts=(7 1 1 1)   
            ;; 
         tc8_step)
            inapp_nav_keys=(9 13 9 13 9 13 9 13)
            inapp_key_counts=(8 1 1 1 8 1 1 1)   
            ;;    
         tc9_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(9 1)   
            ;;
         tc10_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(10 1)   
            ;; 
         tc11_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(11 1)   
            ;;
         tc12_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(12 1)   
            ;;
         tc13_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(13 1)   
            ;; 
         tc14_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(14 1)   
            ;;
         tc15_step)
            inapp_nav_keys=(9 13)
            inapp_key_counts=(15 1)   
            ;;                          
         *)
            printf "\n\n\nnav_keys and key_counts not avaialble for testcase : %s\n\n\n" "$testcase_ID"
            return 1
            ;;
      esac  
      return 0
   else
      printf "\n\n\nDEBUG : Invalid/unidentified App -> %s\n\n\n" "$inapp_used"
      return 1
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
         "TC_MEMCR_MANUAL_01"|"TC_HDCPCOMPLIANCE_MANUAL_01"|"TC_HDCPCOMPLIANCE_MANUAL_02"|"TC_HDCPCOMPLIANCE_MANUAL_03"|"TC_HDCPCOMPLIANCE_MANUAL_04"|"TC_HDCPCOMPLIANCE_MANUAL_05"|"TC_HDCPCOMPLIANCE_MANUAL_06"|"TC_HDCPCOMPLIANCE_MANUAL_07"|"TC_IPv6_MANUAL_01"|"TC_IPv6_MANUAL_02"|"TC_IPv6_MANUAL_03"|"TC_IPv6_MANUAL_06"|"TC_IPv6_MANUAL_07"|"TC_IPv6_MANUAL_08"|"TC_POWER_MANUAL_01"|"TC_SYSTEM_MANUAL_01"|"TC_SYSTEM_MANUAL_02"|"TC_SYSTEM_MANUAL_03")
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
            "$step_func_name" "${!tc_dynamic_var_name}" "$img_format" "$test_app" "$testcase_prefix"       
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
         "TC_WEBAUDIO_MANUAL_test")
            "$step_func_name" "${!tc_dynamic_var_name}" "$test_app" "$testcase_prefix" 
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
            opt_log_flag="true"
            failed_step_num="${testcase_prefix}${step_no}"
         fi   
      fi      
   else
      echo -e "\nSkipping Step ${step_no}, as the previous step failed\n\n"
      update_test_status "${testcase_prefix}${step_no}" "NT"
      opt_log_flag="true"
   fi

}



#Function Definition for checking the file availabililty in the configured Server



check_file_on_serve() {

   local file_url="$1"
   local http_code curl_exit err_file err_msg

   # Validate input
   if [ -z "$file_url" ]; then
      printf "\n\nDEBUG : file_url parameter is empty\n\n" >&2
      return 201
   fi
   #Create a temporary error-file path in TMPDIR if available, otherwise in /tmp, and make the filename unique by appending the current shell’s process ID.
   err_file="${TMPDIR:-/tmp}/check_file_on_serve.$$"

   http_code=$(curl -sS -o /dev/null -w "%{http_code}" -L "$file_url" 2>"$err_file")
   curl_exit=$?
   err_msg=$(tr '\n' ' ' < "$err_file" 2>/dev/null)
   rm -f "$err_file"

   # Success case
   if [ "$curl_exit" -eq 0 ] && [ "$http_code" = "200" ]; then
      return 0
   fi

   # No HTTP response received
   if [ "$http_code" = "000" ]; then
      case "$curl_exit" in
         35|51|60)
               printf '\n\nDEBUG : SSL/TLS certificate or handshake issue for URL [%s] : %s\n\n' \
                  "$file_url" "$err_msg" >&2
               return 210
               ;;
         6)
               printf '\n\nDEBUG : Could not resolve host for URL [%s] : %s\n\n' \
                  "$file_url" "$err_msg" >&2
               return 211
               ;;
         7)
               printf '\n\nDEBUG : Failed to connect to host for URL [%s] : %s\n\n' \
                  "$file_url" "$err_msg" >&2
               return 212
               ;;
         28)
               printf '\n\nDEBUG : Connection timed out for URL [%s] : %s\n\n' \
                  "$file_url" "$err_msg" >&2
               return 213
               ;;
         *)
               printf '\n\nDEBUG : No valid HTTP response received for URL [%s]. curl_exit=[%s], error=[%s]\n\n' \
                  "$file_url" "$curl_exit" "$err_msg" >&2
               return 214
               ;;
      esac
   fi

   # HTTP response received, but not 200
   case "$http_code" in
      401|403)
         printf '\n\nDEBUG : Access denied for URL [%s]. HTTP code = %s\n\n' \
               "$file_url" "$http_code" >&2
         return 221
         ;;
      404)
         printf '\n\nDEBUG : File not found on server for URL [%s]. HTTP code = 404\n\n' \
               "$file_url" >&2
         return 222
         ;;
      5??)
         printf '\n\nDEBUG : Server error for URL [%s]. HTTP code = %s\n\n' \
               "$file_url" "$http_code" >&2
         return 223
         ;;
      *)
         printf '\n\nDEBUG : Unexpected HTTP response for URL [%s]. HTTP code = %s\n\n' \
               "$file_url" "$http_code" >&2
         return 224
         ;;
   esac

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




#Function defnition for sub function to handle immediate playback start on Ipv6 testcase and HDCP testcases



immediate_playback_start() {

   local step_no="$1"
   local app="$2"
   #local user_choice_av="user_choice_av"
   #local query_AV_playback=$(printf "\n\nIs Video App launched and AV playback started? [yes/no]: ")
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "\nStep %s\t\t: Execute curl command to start Immediate AV plyback via any Video App from RDK UI\n\n\n" "$step_num"
   #local curl_to_launch="curl --data-binary '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"YouTube.1.deeplink\",\"params\": \"$yt_URL\"}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc"
   local curl_to_launch="curl -d '{ \"jsonrpc\": \"2.0\", \"id\": 2, \"method\": \"org.rdk.AppManager.launchApp\", \"params\": { \"appId\": \"com.rdkcentral.youtube\", \"intent\": \"playback\", \"launchArgs\": \"$yt_URL\" }}' http://localhost:9998/jsonrpc"
   printf "\n$curl_to_launch\n\n\n" 
   AV_playback_handle "$app" "normal"
   local AV_playback_handle_exit=$?


   if [ "$AV_playback_handle_exit" -eq 0 ]; then
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
      return 0
   else
      #7 error code return specific for expected logs not found from function : check_log_for_string
      return 7
   fi   

}



#Function Definition for checking server connectivity from DUT using HTTP HEAD request
#Usage : check_server_connectivity "<server_url>"
#        e.g. check_server_connectivity "https://xconf.rdkcentral.com"
#             check_server_connectivity "https://example.com"
#Return : 0   - Server is reachable (HTTP 2xx or 3xx)
#         231 - curl/network level failure (unreachable, DNS failure, timeout)
#         232 - Server responded with unexpected HTTP status (4xx / 5xx)



check_server_connectivity() {

   local server_url="$1"
   local http_status_code
   local curl_exit_code

   if [[ -z "$server_url" ]]; then
      printf "\n\ncheck_server_connectivity : No server URL provided. Usage : check_server_connectivity <server_url>\n\n\n"
      return 231
   fi

   printf "\n\nChecking server connectivity : %s\n\n\n" "$server_url"

   http_status_code=$(curl -sI --connect-timeout 5 -o /dev/null -w "%{http_code}" "$server_url")
   curl_exit_code=$?

   if [ "$curl_exit_code" -ne 0 ]; then
      printf "\n\nServer [ %s ] is unreachable from DUT. curl exit code : %s\n\n\n" "$server_url" "$curl_exit_code"
      #231 error code return specific for server connectivity failure (curl/network level error)
      return 231
   fi

   if [[ "$http_status_code" =~ ^[23][0-9]{2}$ ]]; then
      printf "\n\nServer [ %s ] is reachable from DUT. HTTP Status : %s\n\n\n" "$server_url" "$http_status_code"
      return 0
   else
      printf "\n\nServer [ %s ] returned unexpected HTTP Status : %s from DUT\n\n\n" "$server_url" "$http_status_code"
      #232 error code return specific for unexpected HTTP response from server
      return 232
   fi

}


#Function Definition for opt logs tar core function



opt_logs_tar_fun() {

   local file_name="$1"
   tar -czf "$file_name" *
   local tar_success=$?
   sync
   [ "$tar_success" -ne 0 ] && { printf "\n\nDEBUG : Opt logs tar command failed with error code -> %s\n\n\n" "$tar_success"; return $tar_success; }
   if [ -f "$file_name" ] && [ -s "$file_name" ]; then
      printf "\n\nOptlogs Archive %s created successfully\n\n\n" "$file_name"
      return 0
   else
      printf "\n\nDEBUG : Opt logs tar success.But %s is missing or empty\n\n\n" "$file_name"
      return 11
   fi

} 



#Function Definition for opt_failure_log_generate to tar opt logs and moved to testresults folder under Opt_logs directory



opt_failure_log_generate() {

   local test_step_id="$1"
   local issue_testcase="$2"
   log_moved_flag="false"
    
   [ ! -d "/opt/logs" ] && { printf "\n\nError: /opt/logs directory missing/unavailble\n\n\n"; return 138; }
    
   printf "\n\n\n-----------Opt Logs Tar Process Started for Failure Testcase-----------\n\n\n"

   platform_type_finder
   case "$platform_model" in
      "REALTEKHANK") tar_file_name="opt_RTD_${test_step_id}_${issue_testcase}_issue.tgz" ;;
      "BCM974116SFF") tar_file_name="opt_BCM_${test_step_id}_${issue_testcase}_issue.tgz" ;;
      *)    tar_file_name="opt_${platform_model}_${test_step_id}_${issue_testcase}_issue.tgz" ;;
   esac
   
   # Use subshell ( ) to CD so the main script stays in its original directory
   (
      cd /opt/logs || exit 139
      opt_logs_tar_fun "$tar_file_name"
   )
   local rc=$?
   [ "$rc" -ne 0 ] && { printf "\n\nDEBUG : Opt logs tar operation failed\n\n\n"; return "$rc"; }

   mkdir -p "$issue_logs_directory"
   sync

   if mv "/opt/logs/$tar_file_name" "$issue_logs_directory/"; then
      if [ -s "$issue_logs_directory/$tar_file_name" ]; then
         printf "\n%s log file sucessfully moved to %s\n\n\n" "$tar_file_name" "$issue_logs_directory"
         log_moved_flag="true"
         return 0
      fi
   fi

   printf "\nMove failed or %s log file is 0 bytes in %s\n\n\n" "$tar_file_name" "$issue_logs_directory"
   return 1
   
}


#Function Definition for upload_logs_to_server uploading log_files to https server



upload_logs_to_server() {

   local log_to_upload="$1"
   local log_upload_server="$2"
   local upload_server_loc="$3"
   local log_dwld_url="${log_upload_server%/}/images/${log_to_upload}"
   printf "\n\n\n-----------OptLog upload to server Operation started-----------\n\n\n"
   [ "$log_moved_flag" != "true" ] && { printf "\n\nError: Log file Empty/unavailable for upload to server\n\n\n"; return 1; }
   check_server_connectivity "$log_upload_server"
   local check_server_connectivity_exit=$?
   [ "$check_server_connectivity_exit" -ne 0 ] && { printf "\n\nServer connectivity check failed for %s with error code %s\n\n\n" "$log_upload_server" "$check_server_connectivity_exit"; return "$check_server_connectivity_exit"; }
   printf "\n\n%s is up and able to connect.Proceed with Uploading Logs to server\n\n\n" "$log_upload_server"
   local upload_response=$(curl -s -X POST -F "file=@${issue_logs_directory}/${log_to_upload}" "$upload_server_loc")
   if echo "$upload_response" | grep -q "File uploaded successfully"; then
      check_file_on_serve "$log_dwld_url"
      local check_file_on_serve_exit=$?

      [ "$check_file_on_serve_exit" -ne 0 ] && { printf "\n\nFile not found on server.Log upload to server Failed\n\n\n"; return "$check_file_on_serve_exit"; }

      server_filesize_compare "$log_to_upload" "$log_upload_server"
      local server_filesize_compare_exit=$?

      [ "$server_filesize_compare_exit" -ne 0 ] && { printf "\n\nLog upload to the server failed\n\n\n"; return 1; }
      
      printf "\n\nLog file : %s Successfully uploaded to the server and verified\n\nLog download URL : %s\n\n\n" "$log_to_upload" "$log_dwld_url"
      return 0
   else
      printf "\n\nFile upload to server failure or Invalid upload response : %s\n\n\n" "$upload_response"
      return 1 
   fi    

}



#Function Definition for server_file_size_compare to compare the filesize in server and device



server_filesize_compare() {

   local log_file_name="$1"
   local log_upload_server="$2"
   local full_path="$issue_logs_directory/$log_file_name"
   local url_to_check="${log_upload_server%/}/images/$log_file_name"

   [ ! -f "$full_path" ] && return 1
   local log_file_size=$(stat -c "%s" "$full_path")
   local http_code_res=$(curl -sI --connect-timeout 5 -o /dev/null -w "%{http_code}" "$url_to_check")
   local server_info=$(curl -sI --connect-timeout 5 "$url_to_check")

   if [ "$http_code_res" != "200" ]; then
      printf "\n\nDEBUG: File not found on server (HTTP %s)\n\n\n" "$http_code_res"
      return 1
   fi

   local server_file_size=$(echo "$server_info" | grep -i "Content-Length" | grep -oE '[0-9]+')
   if [ -n "$server_file_size" ] && [ "$log_file_size" -eq "$server_file_size" ]; then
      printf "\n\nFile size of server log file : %s bytes\n\nFile size of local log file : %s bytes\n\n\n" "$server_file_size" "$log_file_size"
      return 0
   else
      printf "\n\nFile size of server log file : %s bytes\n\nFile size of local log file : %s bytes\n\n\n" "$server_file_size" "$log_file_size"
      return 1
   fi

}



#Function Definition for log_generate_operations to perform Opt_logs_creation and server upload for failure test cases



log_generate_operations() {

   local failed_step="$1"
   local failure_testcase="$2"
   local user_choice_tarlog="user_choice_tarlog"
   local query_log_upload=$(printf "\n\nDo you want to upload the tar Log file into server? [yes/no]: ")

   if [ "$opt_log_flag" = "true" ] && [ "$test_step_status" = "FAIL" ]; then
      opt_failure_log_generate "$failed_step" "$failure_testcase"
      local opt_failure_log_generate_exit=$?

      [ "$opt_failure_log_generate_exit" -ne 0 ] && return 1

      user_confirmation "$user_choice_tarlog" "$query_log_upload"
      local user_confirmation_fun_exit=$?

      [ "$user_confirmation_fun_exit" -ne 0 ] && { printf "\n\nLog upload to server operation canceled by user. Tarred opt logs are available in the directory : %s\n\n\n" "$issue_logs_directory"; return 0; }

      #log_upload_server and upload_server_loc these two variables are passed from device.conf
      upload_logs_to_server "$tar_file_name" "$log_upload_server" "$upload_server_loc"
      local upload_logs_to_server_exit=$?

      [ "$upload_logs_to_server_exit" -ne 0 ] && return 1

      opt_log_flag="false"
      failed_step_num=""   #flag used for passing parameter for log_generate function
      return 0     
   else
      printf "\n\nNo need to generate logs. ALL TESTCASE PASSED!!!\n\n\n"
      return 1
   fi

}    



#Function Definition for get_JSON_KEY_values to extract key values from JsonRpc response  



get_JSON_KEY_values() {
   local key="$1"
   local jsonRpc="$2"

   # STEP 1: Extract the raw value after the key
   # It looks for the key, then grabs everything until a comma or closing brace
   local raw_value=$(echo "$jsonRpc" | sed -n 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*\([^,}]*\).*/\1/p')

   # We use 'tr' to delete unwanted symbols and 'xargs' to trim whitespace
   # tr -d '[]"{}' deletes those specific characters globally from the string
   clean_value=$(echo "$raw_value" | tr -d '[]"{}\r' | xargs)

   echo "$clean_value"
   
}



#Function definition for get_XCONF_key_values to extract key values from XCONF json response



get_XCONF_key_values() {
   local key="$1"
   local jsonRpc="$2"
   local value=""

   # This captures everything between the double quotes accurately.
   value=$(echo "$jsonRpc" | sed -n 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

   # Attempt 2: If value is still empty, look for unquoted values (Booleans/Numbers)
   if [ -z "$value" ]; then
      # This captures until the next comma or closing brace
      value=$(echo "$jsonRpc" | sed -n 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*\([^,}]*\).*/\1/p')
      # Strip JSON formatting characters and whitespace
      value=$(echo "$value" | tr -d ' \r\n{}[]')
   fi

   # Final Polish: remove any stray carriage returns and trim whitespace
   final_value=$(echo "$value" | tr -d '\r' | xargs)
   echo "$final_value"

}



#Function defnition for animated print message



blink_Query() {

    local msg="$1"
    if [ -n "$msg" ]; then
        for i in {1..10}; do
            printf "\r%s" "$msg"
            sleep 0.4
            printf "\r%${#msg}s" " "   # clear line with spaces
            sleep 0.2
        done
        printf "\r%s\n\n\n" "$msg"      # final static message 
    else
        printf "\n\nDEBUG : Empty query msg passed to function -> blink_Query\n\n" 
    fi       

}




#Function to extract specific network interface information
#
# Usage  : get_iface_info <interface> <field>
# Params : interface - Interface name  (e.g. eth0, wlan0, p2p0, lo)
#          field     - Information to extract. Supported values:
#                        ip        -> IPv4 address        (e.g. 192.168.162.40)
#                        mac       -> MAC / HW address    (e.g. 00:10:20:30:B3:76)
#                        ipv6      -> IPv6 link-local address (e.g. fe80::7b81:2483:178:9155)
#                        mask      -> Subnet prefix length (e.g. 24) via ip cmd | dotted via ifconfig fallback
#                        bcast     -> Broadcast address   (e.g. 192.168.162.255)
#
# MAC  source : /sys/class/net/<iface>/address  -- pure sysfs, no tool needed on any Linux kernel
# IP   source : 'ip addr show' (iproute2) -> fallback 'ifconfig'
# Iface check : /sys/class/net/<iface>/          -- sysfs, no tool needed
#
# Return : 0  - Success   (extracted value printed to stdout)
#          1  - Missing / invalid parameter
#          2  - No network tool available (neither 'ip' nor 'ifconfig')
#          3  - Interface not found in /sys/class/net/
#          4  - Unsupported field requested
#          5  - Field not assigned / not present for the given interface



get_iface_info() {

    local interface="$1"
    local field="$2"
    get_iface_result=""

    # ── Parameter validation ──────────────────────────────────────────────────
    if [[ -z "$interface" ]]; then
        printf "\n\n[ERROR] get_iface_info : Interface name cannot be empty\n\n\n" >&2
        return 1
    fi

    if [[ -z "$field" ]]; then
        printf "\n\n[ERROR] get_iface_info : Field parameter cannot be empty.\n" >&2
        printf "\nSupported fields:[ ip | mac | ipv6 | bcast ]\n\n\n" >&2
        return 1
    fi

    # ── Interface existence check via sysfs (no external tool needed) ─────────
    if [[ ! -d "/sys/class/net/$interface" ]]; then
        printf "\n[ERROR] get_iface_info : Interface '%s' not found in /sys/class/net/\n" "$interface" >&2
        return 3
    fi

    # ── Normalize field name ──────────────────────────────────────────────────
    local field_lower
    field_lower=$(echo "$field" | tr '[:upper:]' '[:lower:]')

    case "$field_lower" in

        mac|hwaddr)
            # ── sysfs read – zero tool dependency, always available on Linux ──
            get_iface_result=$(cat "/sys/class/net/$interface/address" 2>/dev/null)
            ;;

        ip|ipv4)
            if command -v ip &>/dev/null; then
                # iproute2 output: "    inet 192.168.162.40/24 brd ..."
                get_iface_result=$(ip -4 addr show "$interface" 2>/dev/null \
                         | awk '/inet /{print $2}' \
                         | cut -d/ -f1 \
                         | head -1)
            elif command -v ifconfig &>/dev/null; then
                # legacy ifconfig output: "inet addr:192.168.162.40  Bcast:..."
                get_iface_result=$(ifconfig "$interface" 2>/dev/null \
                         | grep 'inet addr:' \
                         | awk '{print $2}' \
                         | cut -d: -f2 \
                         | head -1)
            else
                printf "\n\n[ERROR] get_iface_info : Neither 'ip' nor 'ifconfig' found on this device\n\n\n" >&2
                return 2
            fi
            ;;

        ipv6)
            if command -v ip &>/dev/null; then
                # iproute2 output: "    inet6 fe80::30e6:f885:1b1b:6638/64 scope link"
                get_iface_result=$(ip -6 addr show "$interface" 2>/dev/null \
                         | awk '/inet6 /{print $2}' \
                         | grep -v '^::1' \
                         | cut -d/ -f1 \
                         | head -1)
            elif command -v ifconfig &>/dev/null; then
                # legacy ifconfig output: "inet6 addr: fe80::30e6:f885:1b1b:6638/64 Scope:Link"
                get_iface_result=$(ifconfig "$interface" 2>/dev/null \
                         | grep 'inet6 addr:' \
                         | awk '{print $3}' \
                         | cut -d/ -f1 \
                         | head -1)
            else
                printf "\n[ERROR] get_iface_info : Neither 'ip' nor 'ifconfig' found on this device\n" >&2
                return 2
            fi
            ;;

        bcast|broadcast)
            if command -v ip &>/dev/null; then
                # iproute2 output: "    inet 192.168.162.40/24 brd 192.168.162.255 scope global eth0"
                get_iface_result=$(ip -4 addr show "$interface" 2>/dev/null \
                         | awk '/inet /{
                               for (i=1; i<=NF; i++) {
                                  if ($i == "brd") { print $(i+1); break }
                               }
                            }' \
                         | head -1)
            elif command -v ifconfig &>/dev/null; then
                get_iface_result=$(ifconfig "$interface" 2>/dev/null \
                         | grep 'Bcast:' \
                         | awk -F'Bcast:' '{print $2}' \
                         | awk '{print $1}' \
                         | head -1)
            else
                printf "\n[ERROR] get_iface_info : Neither 'ip' nor 'ifconfig' found on this device\n" >&2
                return 2
            fi
            ;;

        *)
            printf "\n\n[ERROR] get_iface_info : Unsupported field '%s'\n" "$field" >&2
            printf "\nSupported fields: ip | mac | ipv6 | mask | bcast\n\n\n" >&2
            return 4
            ;;
    esac

    # ── Strip any residual whitespace ─────────────────────────────────────────
    get_iface_result=$(echo "$get_iface_result" | tr -d '[:space:]')

    # ── Check if the field was actually assigned on this interface ────────────
    if [[ -z "$get_iface_result" ]]; then
        printf "\n[DEBUG]  get_iface_info : Field '%s' is not assigned / not available on interface '%s'\n" \
               "$field" "$interface" >&2
        return 5
    fi

    # ── Success – print clean value to stdout ─────────────────────────────────
    return 0

}



#Function Definition for post_cond_UI_focus_set to set Focus back on RDK UI


post_cond_UI_focus_set() {

   local app="$1"
   isAppInstalled "$app"
   local isAppInstalled_exit=$?
   if [ "$isAppInstalled_exit" -eq 1 ]; then
      printf "\n\n\nDEBUG : refui App bundle is not installed on device\n\n\n"
      return 1
   else
      setfocus_on_App "$isAppInstalled_appid"
      local setfocus_on_App_exit=$?
      if [ "$setfocus_on_App_exit" -eq 1 ]; then
         return 1
      else
         isAppInstalled_appid=""
         return 0
      fi    
   fi

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
            printf '07. Test Execution Result : TC_HDCPCOMPLIANCE_MANUAL_07        :\t[ Verify the HDCP Compliant enabled status ] \n\n'
            printf '08. Overall TestSuite Execution Status\n\n'
            printf '09. Delete all Test Execution reports\n\n'
            printf '10. Return to the Main Menu\n\n'
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
                  trigger_from_Execution_Result_menu "TC_HDCPCOMPLIANCE_MANUAL_07" "tc7_step" "tc_HDCPCOMPLIANCE_MANUAL_testsuite"
                  ;;          
               8)
                  overall_testsuite_execution_status "TC_HDCPCOMPLIANCE_MANUAL_"
                  ;;
               9)
                  cleanup_testExecution_reports "TC_HDCPCOMPLIANCE_MANUAL_"
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
            printf '08. Test Execution Result : TC_IPv6_MANUAL_08        :\t[ Verify the getPublicIP API response when connected to an IPv6 supported SSID and Ethernet is connected ] \n\n'
            printf '09. Overall TestSuite Execution Status\n\n'
            printf '10. Delete all Test Execution reports\n\n'
            printf '11. Return to the Main Menu\n\n'
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
                  trigger_from_Execution_Result_menu "TC_IPv6_MANUAL_08" "tc8_step" "tc_IPv6_MANUAL_testsuite"
                  ;;
               9)
                  overall_testsuite_execution_status "TC_IPv6_MANUAL_"
                  ;;
               10)
                  cleanup_testExecution_reports "TC_IPv6_MANUAL_"
                  ;;    
               11)
                  printf '\n\nExiting TestCase Execution Results Menu.....\n\n\n' 
                  break
                  ;;  
               *)
                  printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
                  ;;      
            esac
            ;;
         "TC_POWER_MANUAL") 
            printf "\n"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n'
            printf "                                                   ******* TestCase Execution Results Menu :  %s *******                                                                    " "$testCase_ID"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'
            printf '01. Test Execution Result : TC_POWER_MANUAL_01       :\t[ Verify DUT can be set to LIGHT SLEEP and then wakeup with the help of RDK service APIs ] \n\n'
            printf '02. Overall TestSuite Execution Status\n\n'
            printf '03. Delete all Test Execution reports\n\n'
            printf '04. Return to the Main Menu\n\n'
            printf "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n"

            read -p "Enter an Option to proceed : " menu_choice_1_1
            printf '\n\n'
            case "$menu_choice_1_1" in 
               1)
                  trigger_from_Execution_Result_menu "TC_POWER_MANUAL_01" "tc1_step" "tc_POWER_MANUAL_testsuite"
                  ;;
               2)
                  overall_testsuite_execution_status "TC_POWER_MANUAL_"
                  ;;
               3)
                  cleanup_testExecution_reports "TC_POWER_MANUAL_"
                  ;;    
               4)
                  printf '\n\nExiting TestCase Execution Results Menu.....\n\n\n' 
                  break
                  ;;  
               *)
                  printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
                  ;;      
            esac
            ;;
         "TC_SYSTEM_MANUAL") 
            printf "\n"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n'
            printf "                                                   ******* TestCase Execution Results Menu :  %s *******                                                                    " "$testCase_ID"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'
            printf '01. Test Execution Result : TC_POWER_MANUAL_01       :\t[ Verify the SSH connection and functionality via SSH loopback ] \n\n'
            printf '02. Test Execution Result : TC_POWER_MANUAL_02       :\t[ Verify the running status of Wpe framework processes ] \n\n'
            printf '03. Test Execution Result : TC_POWER_MANUAL_03       :\t[ Verify the log rollover RDK functionality ] \n\n'
            printf '04. Overall TestSuite Execution Status\n\n'
            printf '05. Delete all Test Execution reports\n\n'
            printf '06. Return to the Main Menu\n\n'
            printf "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n"

            read -p "Enter an Option to proceed : " menu_choice_1_1
            printf '\n\n'
            case "$menu_choice_1_1" in 
               1)
                  trigger_from_Execution_Result_menu "TC_SYSTEM_MANUAL_01" "tc1_step" "tc_SYSTEM_MANUAL_testsuite" 
                  ;;
               2)
                  trigger_from_Execution_Result_menu "TC_SYSTEM_MANUAL_02" "tc2_step" "tc_SYSTEM_MANUAL_testsuite"
                  ;;
               3)
                  trigger_from_Execution_Result_menu "TC_SYSTEM_MANUAL_03" "tc3_step" "tc_SYSTEM_MANUAL_testsuite"
                  ;;      
               4)
                  overall_testsuite_execution_status "TC_SYSTEM_MANUAL_"
                  ;;
               5)
                  cleanup_testExecution_reports "TC_SYSTEM_MANUAL_"
                  ;;    
               6)
                  printf '\n\nExiting TestCase Execution Results Menu.....\n\n\n' 
                  break
                  ;;  
               *)
                  printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
                  ;;      
            esac
            ;;
         "TC_WEBAUDIO_MANUAL") 
            printf "\n"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n'
            printf "                                                   ******* TestCase Execution Results Menu :  %s *******                                                                    " "$testCase_ID"
            printf '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n'
            printf '01. Test Execution Result : TC_WEBAUDIO_MANUAL_01  :\t[ Verify the speech_synthesis_test_1 via Webaudio App ] \n\n'
            printf '02. Test Execution Result : TC_WEBAUDIO_MANUAL_02  :\t[ Verify the speech_synthesis_test_2 (supported audio languages) via Webaudio App ] \n\n'
            printf '03. Test Execution Result : TC_WEBAUDIO_MANUAL_03  :\t[ Verify the speech_synthesis_test_3 (3 different audio languages continously) via Webaudio App ] \n\n'
            printf '04. Test Execution Result : TC_WEBAUDIO_MANUAL_04  :\t[ Verify the creation of an AudioContext object via Webaudio App ] \n\n'
            printf '05. Test Execution Result : TC_WEBAUDIO_MANUAL_05  :\t[ Verify the creation of an Audiocontext_creation_destruction object via Webaudio App ] \n\n'
            printf '06. Test Execution Result : TC_WEBAUDIO_MANUAL_06  :\t[ Verify the Audio_Playback using webaudio API via Webaudio App ] \n\n'
            printf '07. Test Execution Result : TC_WEBAUDIO_MANUAL_07  :\t[ Verify the Generated_Sound_FM playback using webaudio API via Webaudio App ] \n\n'
            printf '08. Test Execution Result : TC_WEBAUDIO_MANUAL_08  :\t[ Verify the Multi_media_playback via Webaudio App ] \n\n'
            printf '09. Test Execution Result : TC_WEBAUDIO_MANUAL_09  :\t[ Verify the Audio decoding of aac -> vbr-128kbps-44khz via Webaudio App ] \n\n'
            printf '10. Test Execution Result : TC_WEBAUDIO_MANUAL_10  :\t[ Verify the Audio decoding of mp3 -> 128kbps-44khz via Webaudio App ] \n\n'
            printf '11. Test Execution Result : TC_WEBAUDIO_MANUAL_11  :\t[ Verify the Audio decoding of vorbis -> vbr-70kbps-44khz via Webaudio App ] \n\n'
            printf '12. Test Execution Result : TC_WEBAUDIO_MANUAL_12  :\t[ Verify the Audio decoding of vorbis -> vbr-96kbps-44khz via Webaudio App ] \n\n'
            printf '13. Test Execution Result : TC_WEBAUDIO_MANUAL_13  :\t[ Verify the Audio decoding of vorbis -> vbr-128kbps-44khz via Webaudio App ] \n\n'
            printf '14. Test Execution Result : TC_WEBAUDIO_MANUAL_14  :\t[ Verify the Audio decoding of wav -> 24bit-22khz-resample via Webaudio App ] \n\n'
            printf '15. Test Execution Result : TC_WEBAUDIO_MANUAL_15  :\t[ Verify the Audio decoding of wav -> 24bit-44khz via Webaudio App ] \n\n'
            printf '16. Overall TestSuite Execution Status\n\n'
            printf '17. Delete all Test Execution reports\n\n'
            printf '18. Return to the Main Menu\n\n'
            printf "\n-------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n";

            read -p "Enter an Option to proceed : " menu_choice_1_1
            printf '\n\n'
            case "$menu_choice_1_1" in 
               1)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_01" "tc1_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               2)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_02" "tc2_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               3)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_03" "tc3_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               4)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_04" "tc4_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               5)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_05" "tc5_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               6)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_06" "tc6_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               7)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_07" "tc7_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               8)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_08" "tc8_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               9)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_09" "tc9_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               10)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_10" "tc10_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               11)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_11" "tc11_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               12)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_12" "tc12_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               13)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_13" "tc13_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               14)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_14" "tc14_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;
               15)
                  trigger_from_Execution_Result_menu "TC_WEBAUDIO_MANUAL_15" "tc15_step" "tc_WEBAUDIO_MANUAL_testsuite"
                  ;;                                    
               16)
                  overall_testsuite_execution_status "TC_WEBAUDIO_MANUAL_"
                  ;;
               17)
                  cleanup_testExecution_reports "TC_WEBAUDIO_MANUAL_"
                  ;;    
               18)
                  printf '\n\nExiting TestCase Execution Results Menu\n\n\n' 
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







