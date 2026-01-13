#!/bin/bash


source device.conf
source generic_functions.sh

#Author : aharil144@cable.comcast.com
#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




#Function Definition to check the Pre-Condition before executing TC_HDCPCOMPLIANCE_MANUAL TestSuite



preCon_HDCPCOMPLIANCE() {

    local json_payload_HDMI=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}')
    local json_Res_HDMI=$(curl -# --data-binary "$json_payload_HDMI" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
    local display_connected_Status=$(get_JSON_KEY_values "connectedVideoDisplays" "$json_Res_HDMI")

    if [ -z "$display_connected_Status" ]; then
        printf "\n\nDEBUG : connectedVideoDisplays returns empty Value. Please check the HDMI Connection to DUT\n\n\n"
        return 1
    else
        if [ "$display_connected_Status" = "HDMI0" ]; then
            printf "\n\nconnectedVideoDisplays returns [%s], DUT have active HDMI connection\n\n\n" "$display_connected_Status"
            return 0
        else
            printf "\n\nDEBUG : connectedVideoDisplays returns [%s], invalid response\n\n\n"
            return 1 
        fi       
    fi

}



#Function defnition for HDMI connection/ disconnection animated print message



blink_HDMI_Query() {

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
        printf "\n\nDEBUG : Empty query msg passed to function -> blink_HDMI_Query\n\n" 
    fi       

}



#Function defnition for expected_HDCP_logsCheck for getting expected logs/prints from log files



expected_HDCP_logsCheck() {

    local step_num="$1"
    local logs_path="$2"
    local expected_log="$3"
    if [ "$get_keyValue_only" -eq 0 ]; then
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Check for expected %s logs or prints in device\n\n\n" "$step_num" "$expected_log"
        printf '\ntail -n 500 "$logs_path" | grep -F -i -o "$expected_log" | tail -n 1\n\n\n' "$logs_path" "$expected_log"
        sleep 1
        check_log_for_string "$logs_path" "$expected_log"
        check_log_for_string_exit=$?

        if [ "$check_log_for_string_exit" -eq 0 ]; then
            return 0
        else
            return $check_log_for_string_exit
        fi
    else
        sleep 1
        check_log_for_string "$logs_path" "$expected_log"
        check_log_for_string_exit=$?

        if [ "$check_log_for_string_exit" -eq 0 ]; then
            return 0
        else
            return $check_log_for_string_exit
        fi
    fi        

}




#Function defnition for getHDCPStatus_key_values for getting values of each keys in jsonRpc



getHDCPStatus_key_values() {
  
    local step_num="$1"
    shift # The rest of the arguments are the keys we want (e.g., "success" "isConnected" "hdcpReason", etc)
    if [ "$get_keyValue_only" -eq 0 ]; then
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to verify HdcpProfile HDCPStatus\n\n\n" "$step_num" 
        local curl_to_getHDCPStatus="curl --data-binary '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"org.rdk.HdcpProfile.getHDCPStatus\", \"params\":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_getHDCPStatus\n\n\n"   
        sleep 1
        local json_payload_HDCPStatus=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.HdcpProfile.getHDCPStatus", "params":{}}')
        local json_Res_HDCPStatus=$(curl -# --data-binary "$json_payload_HDCPStatus" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
        for _key_ in "$@"; do
            local hdcp_key_value=$(get_JSON_KEY_values "$_key_" "$json_Res_HDCPStatus")
            # Example: if key is "success", it creates a variable $success
            # It results in: success="true"
            eval "hdcp_$_key_=\"$hdcp_key_value\""
        done
    else
        local json_payload_HDCPStatus=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.HdcpProfile.getHDCPStatus", "params":{}}')
        local json_Res_HDCPStatus=$(curl -# --data-binary "$json_payload_HDCPStatus" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
        for _key_ in "$@"; do
            local hdcp_key_value=$(get_JSON_KEY_values "$_key_" "$json_Res_HDCPStatus")
            # Example: if key is "success", it creates a variable $success
            # It results in: success="true"
            eval "hdcp_$_key_=\"$hdcp_key_value\""
        done
    fi            

}



#Function defnition for sub function  to handle HDMI Hotplug Operation



hdmi_HotPlug_subFunc() {

    local step="$1"
    local user_HDMI_choice="user_HDMI_choice"
    local query_HDMI_hotplug=$(printf "\n\nIs HDMI cable hotplugged from DUT and RDK UI showing on TV [yes/no]: ")
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Perform Manual operation : Hotplug the HDMI cable from DUT\n\n\n" "$step" 
    sleep 1
    connection_Query="PLEASE DISCONNECT HDMI CABLE AND CONNECT IT BACK TO DUT TO PROCEED TEST!!!"
    blink_HDMI_Query "$connection_Query"

    user_confirmation "$user_HDMI_choice" "$query_HDMI_hotplug"
    local user_confirmation_fun_exit=$?

    if [ "$user_confirmation_fun_exit" -eq 0 ]; then
        return 0
    else
        return 1
    fi

}



#Function defnition for sub function  to handle getHDCPStatus Operation



getHDCPStatus_subFunc() {
     
    local step="$1"
    getHDCPStatus_key_values "$step" "isConnected" "success"

    if [ "$hdcp_isConnected" = "true" ] && [ "$hdcp_success" = "true" ]; then
        printf "\n\nHDMI connection check param isConnected returns value : %s and getHDCPStatus returns value : %s.\n\nHDMI is in connected state\n\n\n" "$hdcp_isConnected" "$hdcp_success"
        return 0
    elif [ "$hdcp_success" != "true" ]; then
        printf "\n\n org.rdk.HdcpProfile.getHDCPStatus API returns value : %s\n\n\n" "$hdcp_success"
        return 1
    else
        printf "\n\nHDMI connection check param isConnected returns value : %s.\n\nHDMI is not in connected state\n\n\n" "$hdcp_isConnected"
        return 1
    fi

}



#Function defnition for sub function to extract required key values from getHDCPStatus



getHDCPStatus_keyval_subfun() {

    local step="$1"
    local key="$2"
    hdcp_keyname="hdcp_$key"
    : "${key:?getHDCPStatus 'key' is missing}"
    getHDCPStatus_key_values "$step" "$key" "success"

    if [ "${!hdcp_keyname}" = "true" ] && [ "$hdcp_success" = "true" ]; then
        printf "\n\ngetHDCPStatus param %s returns value : %s and getHDCPStatus params success returns value : %s\n\n\n" "$key" "${!hdcp_keyname}" "$hdcp_success"
        return 0
    elif [ "$hdcp_success" != "true" ]; then
        printf "\n\n org.rdk.HdcpProfile.getHDCPStatus API returns value : %s\n\n\n" "$hdcp_success"
        return 1
    else  
        printf "\n\nDEBUG : getHDCPStatus param %s check failed returns value : %s\n\n\n" "$key" "${!hdcp_keyname}" 
        return 1
    fi 

}



#Function defnition to extract required key values from getSettopHDCPSupport



getSettopHDCPSupport_extract() {

    local step_num="$1"
    shift # The rest of the arguments are the keys we want (e.g., "success" "isConnected" "hdcpReason", etc) 
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Execute curl command to verify HdcpProfile getSettopHDCPSupport\n\n\n" "$step_num" 
    local curl_to_getSettopHDCPSupport="curl --data-binary '{\"jsonrpc\":\"2.0\",\"id\":42,\"method\":\"org.rdk.HdcpProfile.getSettopHDCPSupport\"}'  -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc"
    printf "\n$curl_to_getSettopHDCPSupport\n\n\n"   
    sleep 1
    local json_payload_getSettopHDCPSupport=$(printf '{"jsonrpc":"2.0","id":42,"method":"org.rdk.HdcpProfile.getSettopHDCPSupport"}')
    local json_Res_getSettopHDCPSupport=$(curl -# --data-binary "$json_payload_getSettopHDCPSupport" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
    for _key_ in "$@"; do
        local hdcp_key_value=$(get_JSON_KEY_values "$_key_" "$json_Res_getSettopHDCPSupport")
        # Example: if key is "success", it creates a variable $success
        # It results in: success="true"
        eval "hdcp_$_key_=\"$hdcp_key_value\""
    done

}



#Function defnition for sub function to extract required key values from getSettopHDCPSupport



getSettopHDCPSupport_keyval() {
    
    local step_num="$1"
    local key_name="$2"
    : "${key_name:?getSettopHDCPSupport 'key' is missing}"
    getSettopHDCPSupport_extract "$step_num" "$key_name" "success"
    
    if [ "$hdcp_isHDCPSupported" = "true" ] && [ "$hdcp_success" = "true" ]; then
        printf "\n\n param %s returns value : %s and getHDCPStatus params success returns value : %s\n\n\n" "$key_name" "$hdcp_isHDCPSupported" "$hdcp_success"
        return 0
    elif [ "$hdcp_success" != "true" ]; then
        printf "\n\ngetSettopHDCPSupport org.rdk.HdcpProfile.getSettopHDCPSupport API returns value : %s\n\n\n" "$hdcp_success"
        return 1
    else  
        printf "\n\nDEBUG : getSettopHDCPSupport param %s check failed returns value : %s\n\n\n" "$key_name" "$hdcp_isHDCPSupported" 
        return 1
    fi 

}



#Function defnition for testcase TC_HDCPCOMPLIANCE_MANUAL_01 



TC_HDCPCOMPLIANCE_MANUAL_01() {

    local step_num="$1"
    local user_HDMI_choice="user_HDMI_choice"
    local query_HDMI_disconnected=$(printf "\n\nIs HDMI cable disconnected from DUT and RDK UI not showing on TV [yes/no]: ")
    if [ "$step_num" = "1" ]; then
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Perform Manual operation : Disconnect HDMI cable from DUT\n\n\n" "$step_num" 
        sleep 1
        connection_Query="PLEASE DISCONNECT HDMI CABLE FROM DUT TO PROCEED TEST!!!"
        blink_HDMI_Query "$connection_Query"

        user_confirmation "$user_HDMI_choice" "$query_HDMI_disconnected"
        local user_confirmation_fun_exit=$?

        if [ "$user_confirmation_fun_exit" -eq 0 ]; then
           return 0
        else
           return 1
        fi 
    elif [ "$step_num" = "2" ]; then
        sleep 1
        getHDCPStatus_key_values "$step_num" "isConnected" "success"

        if [ "$hdcp_isConnected" = "false" ] && [ "$hdcp_success" = "true" ]; then
            printf "\n\nHDMI connection check param isConnected returns value : %s and getHDCPStatus returns value : %s.\n\nHDMI is in disconnected state\n\n\n" "$hdcp_isConnected" "$hdcp_success"
            return 0
        elif [ "$hdcp_success" != "true" ]; then
            printf "\n\n org.rdk.HdcpProfile.getHDCPStatus API returns value : %s\n\n\n" "$hdcp_success"
            return 1
        else
            printf "\n\nHDMI connection check param isConnected returns value : %s.\n\nHDMI is in connected state\n\n\n" "$hdcp_isConnected"
            return 1
        fi
    else
        sleep 1
        #Here hdcp_logs_path is passed from device config
        expected_HDCP_logsCheck "$step_num" "$hdcp_logs_path" "Updated hotplug to DISCONNECTED"
        local expected_HDCP_logsCheck_exit=$?

        get_keyValue_only=1
        getHDCPStatus_key_values "$step_num" "hdcpReason" 

        if [ "$hdcp_hdcpReason" = "0" ] && [ "$expected_HDCP_logsCheck_exit" -eq 0 ]; then
            printf "\n\nhdcpReason returns value : %s and 'Updated hotplug to DISCONNECTED' prints are available in DUT logs\n\n\n" "$hdcp_hdcpReason" 
            return 0
        elif [ "$hdcp_hdcpReason" != "0" ]; then
            printf "\n\nDEBUG : hdcpReason returns value : %s. HDMI is in connected state\n\n\n" "$hdcp_hdcpReason"
            return 1
        else
            printf "\n\nDEBUG : Expected logs 'Updated hotplug to DISCONNECTED' not available in %s\n\n\n" "$hdcp_logs_path"
            return 1    
        fi 
    fi            

}



#Function defnition for testcase TC_HDCPCOMPLIANCE_MANUAL_02 



TC_HDCPCOMPLIANCE_MANUAL_02() {

    local step_num="$1"
    if [ "$step_num" = "1" ]; then
        hdmi_HotPlug_subFunc "$step_num"
        local hotPlug_subFunc_exit=$?

        if [ "$hotPlug_subFunc_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "2" ]; then
        sleep 1
        getHDCPStatus_subFunc "$step_num"
        local getHDCPStatus_subFunc_exit=$?

        if [ "$getHDCPStatus_subFunc_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    else
        sleep 1
        #Here hdcp_logs_path is passed from device config
        expected_HDCP_logsCheck "$step_num" "$hdcp_logs_path" "Updated hotplug to CONNECTED"
        local expected_HDCP_logsCheck_exit=$?
        get_keyValue_only=1
        expected_HDCP_logsCheck "$step_num" "$hdcp_logs_path" "Updated hdcp_status to AUTHENTICATED"
        local expected_HDCP_logsCheck_exit_1=$?

        if [ "$expected_HDCP_logsCheck_exit" -eq 0 ] && [ "$expected_HDCP_logsCheck_exit_1" -eq 0 ]; then
            return 0
        elif [ "$expected_HDCP_logsCheck_exit" -ne 0 ]; then
            printf "\n\nDEBUG : Expected logs 'Updated hotplug to CONNECTED' unavailable in log file : %s\n\n\n" "$hdcp_logs_path"
            return 1
        else
            printf "\n\nDEBUG : Expected logs 'Updated hdcp_status to AUTHENTICATED' unavailable in log file : %s\n\n\n" "$hdcp_logs_path"
            return 1    
        fi 
    fi

}



#Function defnition for testcase TC_HDCPCOMPLIANCE_MANUAL_03 



TC_HDCPCOMPLIANCE_MANUAL_03() {

    local step_num="$1"
    if [ "$step_num" = "1" ]; then
        hdmi_HotPlug_subFunc "$step_num"
        local hotPlug_subFunc_exit=$?

        if [ "$hotPlug_subFunc_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "2" ]; then
        immediate_playback_start "$step_num" "YouTube"
        local immediate_playback_start_exit=$?

        if [ "$immediate_playback_start_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "3" ]; then
        sleep 1
        getHDCPStatus_subFunc "$step_num"
        local getHDCPStatus_subFunc_exit=$?

        if [ "$getHDCPStatus_subFunc_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    else
        sleep 1
        #Here hdcp_logs_path is passed from device config
        expected_HDCP_logsCheck "$step_num" "$hdcp_logs_path" "Updated hdcp_status to AUTHENTICATED"
        local expected_HDCP_logsCheck_exit=$?

        get_keyValue_only=1
        getHDCPStatus_key_values "$step_num" "hdcpReason" 

        if [ "$hdcp_hdcpReason" = "2" ] && [ "$expected_HDCP_logsCheck_exit" -eq 0 ]; then
            printf "\n\nhdcpReason returns value : %s and 'Updated hdcp_status to AUTHENTICATED' prints are available in DUT logs\n\n\n" "$hdcp_hdcpReason" 
            return 0
        elif [ "$hdcp_hdcpReason" != "2" ]; then
            printf "\n\nDEBUG : hdcpReason returns value : %s. HDMI is in connected state\n\n\n" "$hdcp_hdcpReason"
            return 1
        else
            printf "\n\nDEBUG : Expected logs 'Updated hdcp_status to AUTHENTICATED' not available in %s\n\n\n" "$hdcp_logs_path"
            return 1    
        fi
    fi    
}



#Function defnition for testcase TC_HDCPCOMPLIANCE_MANUAL_04 



TC_HDCPCOMPLIANCE_MANUAL_04() {

    local step_num="$1"
    if [ "$step_num" = "1" ]; then
        hdmi_HotPlug_subFunc "$step_num"
        local hotPlug_subFunc_exit=$?

        if [ "$hotPlug_subFunc_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "2" ]; then
        immediate_playback_start "$step_num" "YouTube"
        local immediate_playback_start_exit=$?

        if [ "$immediate_playback_start_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "3" ]; then
        sleep 1
        getSettopHDCPSupport_keyval "$step_num" "isHDCPSupported"
        local getSettopHDCPSupport_keyval_exit=$?

        if [ "$getSettopHDCPSupport_keyval_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    fi
}



#Function defnition for testcase TC_HDCPCOMPLIANCE_MANUAL_05 



TC_HDCPCOMPLIANCE_MANUAL_05() {

    local step_num="$1"
    if [ "$step_num" = "1" ]; then
        hdmi_HotPlug_subFunc "$step_num"
        local hotPlug_subFunc_exit=$?

        if [ "$hotPlug_subFunc_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "2" ]; then
        immediate_playback_start "$step_num" "YouTube"
        local immediate_playback_start_exit=$?

        if [ "$immediate_playback_start_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "3" ]; then
        sleep 1
        getHDCPStatus_keyval_subfun "$step_num" "isHDCPEnabled"
        local getHDCPStatus_keyval_subfun_exit=$?

        if [ "$getHDCPStatus_keyval_subfun_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    fi
}



#Function defnition for testcase TC_HDCPCOMPLIANCE_MANUAL_06 



TC_HDCPCOMPLIANCE_MANUAL_06() {

    local step_num="$1"
    if [ "$step_num" = "1" ]; then
        hdmi_HotPlug_subFunc "$step_num"
        local hotPlug_subFunc_exit=$?

        if [ "$hotPlug_subFunc_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "2" ]; then
        immediate_playback_start "$step_num" "YouTube"
        local immediate_playback_start_exit=$?

        if [ "$immediate_playback_start_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "3" ]; then
        sleep 1
        getHDCPStatus_key_values "$step_num" "supportedHDCPVersion" "receiverHDCPVersion" "currentHDCPVersion" "success"

        if [[ "$hdcp_supportedHDCPVersion" == "2.2" && \
        "$hdcp_receiverHDCPVersion" == "2.2" && \
        "$hdcp_currentHDCPVersion" == "2.2" && \
        "$hdcp_success" == "true" ]]; then
            printf "\n\nsupportedHDCPVersion : %s | receiverHDCPVersion : %s | currentHDCPVersion : %s returns same value and getHDCPStatus API returns value success : %s\n\n\n" "$hdcp_supportedHDCPVersion" "$hdcp_receiverHDCPVersion" "$hdcp_currentHDCPVersion" "$hdcp_success"
            return 0
        elif [ "$hdcp_success" != "true" ]; then
            printf "\n\n org.rdk.HdcpProfile.getHDCPStatus API returns value : %s\n\n\n" "$hdcp_success"
            return 1
        else
            printf "\n\nsupportedHDCPVersion : %s | receiverHDCPVersion : %s | currentHDCPVersion : %s returned value are not same and getHDCPStatus API returns value success : %s\n\n\n" "$hdcp_supportedHDCPVersion" "$hdcp_receiverHDCPVersion" "$hdcp_currentHDCPVersion" "$hdcp_success"
            return 1
        fi
    fi
}



#Function Definition for TestCase : tc_RDKSHELL_MANUAL_testsuite



tc_HDCPCOMPLIANCE_MANUAL_testsuite() {

  local TestcaseID="$2"
  local testcase_prefix="$1"
  test_step_status="PASS"
  get_keyValue_only=0  #flag used for HDCPCompliance testcases

  #Precondition Check code block
  
  printf "\n"
  printf "Pre-Conditon check\t\t: Checking whether Active HDMI Connection is available on DUT\n\n\n"
  sleep 1
  preCon_HDCPCOMPLIANCE
  local preCon_HDCPCOMPLIANCE_fun_exit=$?
  
  if [ "$preCon_HDCPCOMPLIANCE_fun_exit" -eq 0 ]; then
    sleep 1
    printf '\n\nPre-condition check success. Starting Testcase execution!\n\n\n'
        

#Step 1 code block for TC_HDCPCOMPLIANCE_MANUAL_01 


    if [[ "$TestcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_01" ]]; then
        execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_01"
        sleep 1


#Step 2 code block for TC_HDCPCOMPLIANCE_MANUAL_01         


        execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_01"
        sleep 1
      

#Step 3 code block for TC_HDCPCOMPLIANCE_MANUAL_01         


        execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_01"
        sleep 1
        dynamic_current_step_finder "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL" 
    fi 
       

#Step 1 code block for TC_HDCPCOMPLIANCE_MANUAL_02 


    if [[ "$TestcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_02" ]]; then
        execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_02"
        sleep 1


#Step 2 code block for TC_HDCPCOMPLIANCE_MANUAL_02         


        execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_02"
        sleep 1
      

#Step 3 code block for TC_HDCPCOMPLIANCE_MANUAL_02        


        execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_02"
        sleep 1
        dynamic_current_step_finder "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL" 
    fi 
       

#Step 1 code block for TC_HDCPCOMPLIANCE_MANUAL_03


    if [[ "$TestcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_03" ]]; then
        execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_03"
        sleep 1


#Step 2 code block for TC_HDCPCOMPLIANCE_MANUAL_03         


        execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_03"
        sleep 1
      

#Step 3 code block for TC_HDCPCOMPLIANCE_MANUAL_03        


        execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_03"
        sleep 1
           

#Step 4 code block for TC_HDCPCOMPLIANCE_MANUAL_03        


        execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_03"
        sleep 1  
        dynamic_current_step_finder "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL" 
    fi 
        

#Step 1 code block for TC_HDCPCOMPLIANCE_MANUAL_04 


    if [[ "$TestcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_04" ]]; then
        execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_04"
        sleep 1


#Step 2 code block for TC_HDCPCOMPLIANCE_MANUAL_04         


        execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_04"
        sleep 1
      

#Step 3 code block for TC_HDCPCOMPLIANCE_MANUAL_04         


        execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_04"
        sleep 1
        dynamic_current_step_finder "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL" 
    fi
       

#Step 1 code block for TC_HDCPCOMPLIANCE_MANUAL_05 


    if [[ "$TestcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_05" ]]; then
        execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_05"
        sleep 1


#Step 2 code block for TC_HDCPCOMPLIANCE_MANUAL_05         


        execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_05"
        sleep 1
      

#Step 3 code block for TC_HDCPCOMPLIANCE_MANUAL_05         


        execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_05"
        sleep 1
        dynamic_current_step_finder "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL" 
    fi
      

#Step 1 code block for TC_HDCPCOMPLIANCE_MANUAL_06 


    if [[ "$TestcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_06" ]]; then
        execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_06"
        sleep 1


#Step 2 code block for TC_HDCPCOMPLIANCE_MANUAL_06         


        execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_06"
        sleep 1
      

#Step 3 code block for TC_HDCPCOMPLIANCE_MANUAL_06         


        execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL_06"
        sleep 1
        dynamic_current_step_finder "$testcase_prefix" "TC_HDCPCOMPLIANCE_MANUAL" 
    fi

    #TestCase execution Result dynamic updating Function     
    dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}" 

    #Postcondition code block    
    printf '\nExecuting Post-condition Steps for Testcase : %s\n\n\n' "$TestcaseID"
    sleep 1
    postCondition_Execution_HDCP "$TestcaseID" 
    local postCondition_Execution_HDCP_exit=$?

    if [ "$postCondition_Execution_HDCP_exit" -eq 0 ]; then
        printf '\nPost-condition Execution Success. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
    elif [ "$postCondition_Execution_HDCP_exit" -eq 55 ];   then
        printf "\n\nPost-condition: None\n\n"    
    else
        printf '\nPost-condition Execution failed. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
    fi
  else
    printf '\n\nPre-condition check failure. Exiting HDCP COMPLIANCE Automated Test!\n\n\n' 
  fi 

}



#Function Definition for postCondition checking of HDCP COMPLIANCE


postCondition_Execution_HDCP() {

    local testcaseID="$1"
    local user_HDMI_choice="user_HDMI_choice"
    local query_HDMI_connected=$(printf "\n\nIs HDMI cable connected back to DUT and RDK UI is visible on TV [yes/no]: ")
    if [[ "$testcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_01" ]]; then
        connection_Query="PLEASE CONNECT HDMI CABLE BACK TO DUT!!!"
        blink_HDMI_Query "$connection_Query"

        user_confirmation "$user_HDMI_choice" "$query_HDMI_connected"
        local user_confirmation_fun_exit=$?

        if [ "$user_confirmation_fun_exit" -eq 0 ]; then
           return 0
        else
           return 1
        fi
    elif [[ "$testcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_03" ]] || [[ "$testcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_04" ]] || [[ "$testcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_05" ]] || [[ "$testcaseID" == "TC_HDCPCOMPLIANCE_MANUAL_06" ]]; then
        if [[ "$av_check_flag" == "2" ]]; then  
            destroy_app "HtmlApp"
        else
            destroy_app "YouTube" 
        fi       
        local destroy_app_exit=$?
        if [ "$destroy_app_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi    
    else
        return 55
    fi     

}






#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





while true; do
  printf "\n"
  printf "\n=============================================================================================================================================================\n\n";
  printf "                                                      ******* HDCP COMPLIANCE Automated Test *******                                                                    ";
  printf "\n=============================================================================================================================================================\n\n\n";
  printf '01. Run TestCase : TC_HDCPCOMPLIANCE_MANUAL_01        :\t[ Verify the HDMI cable connected status ] \n\n'
  printf '02. Run TestCase : TC_HDCPCOMPLIANCE_MANUAL_02        :\t[ Verify the HDCP authentication initiated status  ] \n\n'
  printf '03. Run TestCase : TC_HDCPCOMPLIANCE_MANUAL_03        :\t[ Verify the HDCP authenticated status ] \n\n'
  printf '04. Run TestCase : TC_HDCPCOMPLIANCE_MANUAL_04        :\t[ Verify the HDCP protocol support ] \n\n'
  printf '05. Run TestCase : TC_HDCPCOMPLIANCE_MANUAL_05        :\t[ Verify the HDCP enabled status ] \n\n'
  printf '06. Run TestCase : TC_HDCPCOMPLIANCE_MANUAL_06        :\t[ Verify the device is supported, received and current HDCP version ] \n\n'
  printf '07. Show TestCase Execution Results\n\n'
  printf '08. Exit [ HDCP COMPLIANCE Automated Test ]\n\n'
  printf "\n=============================================================================================================================================================\n\n\n";


  # ----- Main Testcaes Execution Menu -----

  
  read -p "Enter an Option to proceed : " menu_choice
  printf '\n\n\n'
  case "$menu_choice" in 
    1)
        exec_start "TC_HDCPCOMPLIANCE_MANUAL_01"
        tc_HDCPCOMPLIANCE_MANUAL_testsuite "tc1_step" "TC_HDCPCOMPLIANCE_MANUAL_01"
        ;;
    2)
        exec_start "TC_HDCPCOMPLIANCE_MANUAL_02"
        tc_HDCPCOMPLIANCE_MANUAL_testsuite "tc2_step" "TC_HDCPCOMPLIANCE_MANUAL_02"
        ;;
    3)
        exec_start "TC_HDCPCOMPLIANCE_MANUAL_03"
        tc_HDCPCOMPLIANCE_MANUAL_testsuite "tc3_step" "TC_HDCPCOMPLIANCE_MANUAL_03"
        ;;
    4)
        exec_start "TC_HDCPCOMPLIANCE_MANUAL_04"
        tc_HDCPCOMPLIANCE_MANUAL_testsuite "tc4_step" "TC_HDCPCOMPLIANCE_MANUAL_04"
        ;;
    5)
        exec_start "TC_HDCPCOMPLIANCE_MANUAL_05"
        tc_HDCPCOMPLIANCE_MANUAL_testsuite "tc5_step" "TC_HDCPCOMPLIANCE_MANUAL_05"
        ;;
    6)
        exec_start "TC_HDCPCOMPLIANCE_MANUAL_06"
        tc_HDCPCOMPLIANCE_MANUAL_testsuite "tc6_step" "TC_HDCPCOMPLIANCE_MANUAL_06"
        ;;                                 
    7)
        testcase_result_display_menu "TC_HDCPCOMPLIANCE_MANUAL"  
        ;;       
    8)   
        printf '\nExited HDCP COMPLIANCE Automated Test\n\n\n' 
        break
        ;; 
    *)
        printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
        ;;      
  esac
done

