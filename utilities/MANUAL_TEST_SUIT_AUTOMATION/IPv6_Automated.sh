#!/bin/bash


source device.conf
source generic_functions.sh

#Author : aharil144@cable.comcast.com
#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________






#Function defnition for ipv6_valid_check to check the IPV6 address obtained is valid or not.



ipv6_valid_check() {

    local s="$1"
    # This regex checks for the standard IPv6 patterns, including shorthand '::'
    local regex="^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))$"
    
    [[ "$s" =~ $regex ]]

}



#Function Definition to check the Pre-Condition before executing TC_IPv6_MANUAL TestSuite



preCon_IPv6() {

    local conf_SSID="$1"
    local testcaseID="$2"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nPre-Condition\t\t:Execute curl command to verify connected ipv6 SSID details and Ethernet connection status\n\n\n"
    local curl_to_GetConnectedSSID="curl -d '{ \"jsonrpc\": \"2.0\", \"id\": 42, \"method\": \"org.rdk.NetworkManager.1.GetConnectedSSID\" }'"
    printf "\n$curl_to_GetConnectedSSID\n\n\n"   
    sleep 1
    local getConnectedSSID_payload=$(printf '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.GetConnectedSSID" }')
    local extracted_ipv6_addr=$(ip -o -6 addr show dev wlan0 scope global | awk '/secondary dynamic/ {split($4,a,"/"); print a[1]}')
    local extracted_ipv4_addr=$(ip -4 addr show eth0 | awk '/inet / {split($2,a,"/"); print a[1]}')
    if [[ "$testcaseID" == "TC_IPv6_MANUAL_02" ]] || [[ "$testcaseID" == "TC_IPv6_MANUAL_04" ]]; then
        ipv6_extract_API_key_values "$getConnectedSSID_payload" "ssid" "success"
        local ipv6_extract_API_key_values_exit=$?

        if [ "$ipv6_extract_API_key_values_exit" -eq 100 ]; then
            return 1
        else
            if [ -z "$ipv6_ssid" ]; then
                printf "\n\nDEBUG : connected IPv6 SSID returns empty Value. Please connect DUT to an IPv6 Supported SSID\n\n\n"
                return 1    
            else    
                if ipv6_valid_check "$extracted_ipv6_addr" && [ "$ipv6_ssid" = "$conf_SSID" ] && [ -n "$extracted_ipv4_addr" ] && [ "$ipv6_success" = "true" ]; then
                    printf "\n\nConnected IPv6 SSID name returns [ %s ] and IPv6 address is [ %s ]\n\nEthernet is Connected IPv4 address is [ %s ]\n\n\n" "$ipv6_ssid" "$extracted_ipv6_addr" "$extracted_ipv4_addr"
                    return 0
                elif [ "$ipv6_success" != "true" ]; then 
                    printf "\n\norg.rdk.NetworkManager.1.GetConnectedSSID API return value : %s\n\n\n" "$ipv6_success"
                    return 1
                elif [ -z "$extracted_ipv4_addr" ]; then
                    printf "\n\nEthernet is not connected to DUT. Unable to fetch IPV4 address : %s\n\n\n" "$extracted_ipv4_addr"
                    return 1     
                else
                    printf "\n\nConnected IPv6 SSID returns [ %s ] and IPv6 address returns [ %s ].But config_SSID and ipv6 SSID mismatches\n\n\n" "$ipv6_ssid" "$extracted_ipv6_addr"
                    return 1
                fi           
            fi
        fi    
    else
        ipv6_extract_API_key_values "$getConnectedSSID_payload" "ssid" "success"
        local ipv6_extract_API_key_values_exit=$?

        if [ "$ipv6_extract_API_key_values_exit" -eq 100 ]; then
            return 1
        else
            if [ -z "$ipv6_ssid" ]; then
                printf "\n\nDEBUG : connected IPv6 SSID returns empty Value. Please connect DUT to an IPv6 Supported SSID\n\n\n"
                return 1    
            else    
                printf "\n\nSSID name : %s\n\n" "$ipv6_ssid"
                printf "\n\nstatus : %s\n\n" "$ipv6_success"
                printf "\n\nCONFIG_SSID : %s\n\n" "$conf_SSID"
                if ipv6_valid_check "$extracted_ipv6_addr" &&[ "$ipv6_ssid" = "$conf_SSID" ] && [ -z "$extracted_ipv4_addr" ] && [ "$ipv6_success" = "true" ]; then
                    printf "\n\nConnected IPv6 SSID name returns [ %s ] and IPv6 address is [ %s ]\n\nEthernet is disConnected IPv4 address returns empty [ %s ]\n\n\n" "$ipv6_ssid" "$extracted_ipv6_addr" "$extracted_ipv4_addr"
                    return 0
                elif [ "$ipv6_success" != "true" ]; then 
                    printf "\n\norg.rdk.NetworkManager.1.GetConnectedSSID API return value : %s\n\n\n" "$ipv6_success"
                    return 1
                elif [ -n "$extracted_ipv4_addr" ]; then
                    printf "\n\nEthernet is connected to DUT.Able to fetch IPV4 address : %s\n\nDisconnect ethernet cable and try again\n\n\n" "$extracted_ipv4_addr"
                    return 1     
                else
                    printf "\n\nConnected IPv6 SSID returns [ %s ] and IPv6 address returns [ %s ].But config_SSID and ipv6 SSID mismatches\n\n\n" "$ipv6_ssid" "$extracted_ipv6_addr"
                    return 1
                fi
            fi
        fi    
    fi 

}




#Function defnition for ipv6_extract_API_key_values to extract key values



ipv6_extract_API_key_values() {

    local index=1
    # Loop through all arguments provided to the function
    for arg in "$@"; do
        if [[ -z "$arg" ]]; then
            echo "\n\nDEBUG : Argument $index is empty or missing in ipv6_extract_API_key_values!\n\n"
            #error code specific for params empty error
            return 100 
        fi
        ((index++))
    done
    local json_payload_ipv6="$1"
    shift # The rest of the arguments are the keys we want (e.g., "success" "isConnected" "hdcpReason", etc) 
    local json_Res_ipv6=$(curl -# -d "$json_payload_ipv6" http://127.0.0.1:9998/jsonrpc)
    for _key_ in "$@"; do
        local ipv6_key_value=$(get_JSON_KEY_values "$_key_" "$json_Res_ipv6")
        # Example: if key is "success", it creates a variable $success
        # It results in: success="true"
        eval "ipv6_${_key_}=\"\$ipv6_key_value\""
    done

}



#Function defnition for IsConnectedToInternet_key_Extract keys status checking in multiple test steps



isConnectedToInternet_key_Extract() {

    local step_num="$1"
    local step_head="$2"
    local expected_interface="$3"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: %s\n\n\n" "$step_num" "$step_head"
    local curl_to_get_IP_Settings="curl -d '{ \"jsonrpc\": \"2.0\", \"id\": 42, \"method\": \"org.rdk.NetworkManager.1.IsConnectedToInternet\", \"params\": { \"ipversion\": \"IPv6\" } }' http://127.0.0.1:9998/jsonrpc"
    printf "\n$curl_to_get_IP_Settings\n\n\n" 
    sleep 1
    local json_payload_IsConnectedToInternet=$(printf '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.IsConnectedToInternet", "params": { "ipversion": "IPv6" } }')
    ipv6_extract_API_key_values "$json_payload_IsConnectedToInternet" "interface" "connected" "status" "success"
    local ipv6_extract_API_key_values_exit=$?

    if [ "$ipv6_extract_API_key_values_exit" -eq 100 ]; then
        return 1
    else
        if [ "$ipv6_interface" = "$expected_interface" ] && [ "$ipv6_connected" = "true" ] && [ "$ipv6_status" = "FULLY_CONNECTED" ] && [ "$ipv6_success" = "true" ]; then
            printf "\n\nInterface Obtained\t:\t%s\n\nConnected\t\t:\t%s\n\nConnected status\t:\t%s\n\n\n" "$ipv6_interface" "$ipv6_connected" "$ipv6_status"
            return 0 
        elif [ "$ipv6_success" != "true" ]; then  
            printf "\n\norg.rdk.NetworkManager.1.GetConnectedSSID API return value : %s\n\n\n" "$ipv6_success"
            return 1
        elif [ "$ipv6_status" != "FULLY_CONNECTED" ] || [ "$ipv6_connected" != "true" ]; then
            printf "\n\nIPv6 Connected returns : %s and Connection returns invalid status : %s\n\n\n" "$ipv6_connected" "$ipv6_status"
            return 1
        else
            printf "\n\nIPv6 interface returns different value : %s\n\n\n" "$ipv6_interface"
            return 1
        fi 
    fi

}



#Function defnition for GetPublicIP_key_Extract keys status checking in multiple test steps



getPublicIP_key_Extract() {

    local step_num="$1"
    local step_head="$2"
    local expected_interface="$3"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: %s\n\n\n" "$step_num" "$step_head"
    local curl_to_GetPublicIP="curl -d '{ \"jsonrpc\": \"2.0\", \"id\": 42, \"method\": \"org.rdk.NetworkManager.1.GetPublicIP\", \"params\": { \"ipversion\": \"IPv6\" } }' http://127.0.0.1:9998/jsonrpc"
    printf "\n$curl_to_GetPublicIP\n\n\n" 
    sleep 1
    local json_payload_GetPublicIP=$(printf '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.GetPublicIP", "params": { "ipversion": "IPv6" } }')
    ipv6_extract_API_key_values "$json_payload_GetPublicIP" "interface" "ipaddress" "success"
    local ipv6_extract_API_key_values_exit=$?

    if [ "$ipv6_extract_API_key_values_exit" -eq 100 ]; then
        return 1
    else
        if ipv6_valid_check "$ipv6_ipaddress" && [ "$ipv6_interface" = "$expected_interface" ] && [ "$ipv6_success" = "true" ]; then 
            printf "\n\nInterface Obtained\t:\t%s\n\nIPv6 Address\t\t:\t[ %s ]\n\nAPI response\t\t:\t%s\n\n\n" "$ipv6_interface" "$ipv6_ipaddress" "$ipv6_success"
            return 0 
        elif [ "$ipv6_success" != "true" ]; then  
            printf "\n\norg.rdk.NetworkManager.1.GetPublicIP API return value : %s\n\n\n" "$ipv6_success"
            return 1
        elif [ "$ipv6_interface" != "$expected_interface" ]; then
            printf "\n\nIPv6 Interface returns : %s different value\n\n\n" "$ipv6_connected" "$ipv6_status"
            return 1
        else
            printf "\n\nExtracted IPv6 address is invalid : %s\n\n\n" "$ipv6_ipaddress"
            return 1
        fi 
    fi

}



#Function defnition for ping_key_Extract keys status checking in multiple test steps



ping_key_Extract() {

    local step_num="$1"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Verify the ping API when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n\n" "$step_num"
    local curl_to_ping="curl -d '{ \"jsonrpc\": \"2.0\", \"id\": 42, \"method\": \"org.rdk.NetworkManager.1.Ping\", \"params\": { \"endpoint\": \"2001:4860:4860::8888\", \"ipversion\": \"IPv6\", \"packets\": 10 } }' http://127.0.0.1:9998/jsonrpc"
    printf "\n$curl_to_ping\n\n\n" 
    sleep 1
    local json_payload_ping=$(printf '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.Ping", "params": { "endpoint": "2001:4860:4860::8888", "ipversion": "IPv6", "packets": 10 } }')
    ipv6_extract_API_key_values "$json_payload_ping" "success" "packetLoss" "packetsReceived" "packetsTransmitted"
    local ipv6_extract_API_key_values_exit=$?

    if [ "$ipv6_extract_API_key_values_exit" -eq 100 ]; then
        return 1
    else
        if [ "$ipv6_packetLoss" = "0" ] && [ "$ipv6_packetsReceived" -gt 0 ] && [ "$ipv6_packetsTransmitted" -gt 0 ] && [ "$ipv6_success" = "true" ]; then
            printf "\n\nPacketLoss\t\t:\t%s\n\nPacketsRecieved\t\t:\t%s\n\nPacketsTransmitted\t:\t%s\n\nAPI response\t\t:\t%s\n\n\n" "$ipv6_packetLoss" "$ipv6_packetsReceived" "$ipv6_packetsTransmitted" "$ipv6_success"
            return 0 
        elif [ "$ipv6_success" != "true" ]; then  
            printf "\n\norg.rdk.NetworkManager.1.Ping API return value : %s\n\n\n" "$ipv6_success"
            return 1
        elif [ "$ipv6_packetsReceived" -eq 0 ] || [ "$ipv6_packetsTransmitted" -eq 0 ]; then 
            printf "\n\nPacketsRecieved\t:\t%s\n\nPacketsTransmitted\t:\t%s\n\nInvalid packet transmittion\n\n\n" 
            return 1   
        else 
            printf "\n\nPacketLoss : %s value is grater than 0\n\n\n" "$ipv6_packetLoss"
            return 1
        fi         
    fi

}



#Function defnition for trace_key_Extract keys status checking in multiple test steps



trace_key_Extract() {

    local step_num="$1"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Verify the trace API when connected to an IPv6 supported SSID and Ethernet is disconnected\n\n\n" "$step_num"
    local curl_to_trace="curl -d '{ \"jsonrpc\": \"2.0\", \"id\": 42, \"method\": \"org.rdk.NetworkManager.1.Trace\", \"params\": { \"endpoint\": \"2001:4860:4860::8888\", \"ipversion\": \"IPv6\", \"packets\": 1 } }' http://127.0.0.1:9998/jsonrpc"
    printf "\n$curl_to_trace\n\n\n" 
    sleep 1
    local json_payload_trace=$(printf '{ "jsonrpc": "2.0", "id": 42, "method": "org.rdk.NetworkManager.1.Trace", "params": { "endpoint": "2001:4860:4860::8888", "ipversion": "IPv6", "packets": 1 } }')
    local json_Res_trace=$(curl -# -d "$json_payload_trace" http://127.0.0.1:9998/jsonrpc)
    ipv6_extract_API_key_values "$json_payload_trace" "success" "endpoint"
    local ipv6_extract_API_key_values_exit=$?

    #Counts how many asterisks appear in the response
    local timeout_count=$(echo "$json_Res_trace" | grep -o "\*" | wc -l)
    #This removes the "endpoint" part of the JSON so we only look at the 'results'
    local actual_stop=$(echo "$json_Res_trace" | sed 's/"endpoint".*//' | grep -oE '[a-fA-F0-9:]+:[a-fA-F0-9:]+' | tail -n 1)

    if [ "$ipv6_extract_API_key_values_exit" -eq 100 ]; then
        return 1
    else
        if [ "$ipv6_endpoint" = "2001:4860:4860::8888" ] && [ "$actual_stop" = "2001:4860:4860::8888" ] && [ "$ipv6_success" = "true" ]; then
            printf "\n\nEndpoint\t:\t%s\n\nLast hops\t:\t%s\n\nAPI response\t:\t%s\n\n\n" "$ipv6_endpoint" "$actual_stop" "$ipv6_success"
            return 0
        elif [ "$ipv6_endpoint" != "$actual_stop" ]; then
            printf "\n\nEndpoint\t:\t%s\n\nLast hops\t:\t%s\n\nEndpoint and last Hops should be same\n\n\n" "$ipv6_endpoint" "$actual_stop"       
            return 1
        else
            printf "\n\norg.rdk.NetworkManager.1.Trace API return value : %s\n\n\n" "$ipv6_success" 
            return 1
        fi
    fi

}



#Function defnition for testcase TC_IPv6_MANUAL_01



TC_IPv6_MANUAL_01() {

    local step="$1"
    local step_mesg="Execute the curl command to get the IP Settings when connected to a IPv6 Supported SSID and ethernet is disconnected" 
    local interface="wlan0"
    isConnectedToInternet_key_Extract "$step" "$step_mesg" "$interface"
    local IsConnectedToInternet_fun_exit=$?

    if [ "$IsConnectedToInternet_fun_exit" -eq 0 ]; then
        return 0
    else
        return 1
    fi

}



#Function defnition for testcase TC_IPv6_MANUAL_02



TC_IPv6_MANUAL_02() {

    local step="$1"
    local step_mesg="Execute the curl command to get the public IPV6 IP when connected to a IPv6 Supported SSID and ethernet is connected" 
    local interface="eth0"
    getPublicIP_key_Extract "$step" "$step_mesg" "$interface"
    local IsConnectedToInternet_fun_exit=$?

    if [ "$IsConnectedToInternet_fun_exit" -eq 0 ]; then
        return 0
    else
        return 1
    fi    

}



#Function defnition for testcase TC_IPv6_MANUAL_03



TC_IPv6_MANUAL_03() {
    
    local step="$1"
    local step_mesg="Execute the curl command to get the public IPV6 IP when connected to a IPv6 Supported SSID and ethernet is disconnected" 
    local interface="wlan0"
    getPublicIP_key_Extract "$step" "$step_mesg" "$interface"
    local IsConnectedToInternet_fun_exit=$?

    if [ "$IsConnectedToInternet_fun_exit" -eq 0 ]; then
        return 0
    else
        return 1
    fi

}



#Function defnition for testcase TC_IPv6_MANUAL_04



TC_IPv6_MANUAL_04() {

    local step="$1"
    local app="$2"
    if [ "$eth0_wlan0_flag" -eq 0 ]; then
        local step_mesg="Execute the curl command to check internet accessibility when connected to IPv6 supported SSID and Ethernet is connected" 
        local interface="eth0"
    else
        local step_mesg="Execute the curl command to check internet accessibility when connected to IPv6 supported SSID and Ethernet is disconnected" 
        local interface="wlan0"
    fi        
    if [ "$step" = "1" ]; then
        isConnectedToInternet_key_Extract "$step" "$step_mesg" "$interface"
        local IsConnectedToInternet_fun_exit=$?

        if [ "$IsConnectedToInternet_fun_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step" = "2" ]; then
        immediate_playback_start "$step" "$app"
        local immediate_playback_start_exit=$?

        if [ "$immediate_playback_start_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    else
        printf "\n\nTeststep Not Defined!!!\n\n\n"
        return 1
    fi         

}



#Function defnition for testcase TC_IPv6_MANUAL_06



TC_IPv6_MANUAL_06() {

    local step="$1"
    trace_key_Extract "$step"
    local trace_key_Extract_exit=$?

    if [ "$trace_key_Extract_exit" -eq 0 ]; then
        return 0
    else
        return 1
    fi

}


#Function defnition for testcase TC_IPv6_MANUAL_07



TC_IPv6_MANUAL_07() {

    local step="$1"
    ping_key_Extract "$step"
    local ping_key_Extract_exit=$?

    if [ "$ping_key_Extract_exit" -eq 0 ]; then
        return 0
    else
        return 1
    fi

}



#Function Definition for TestCase : tc_IPv6_MANUAL_testsuite



tc_IPv6_MANUAL_testsuite() {

    local TestcaseID="$2"
    local testcase_prefix="$1"
    test_step_status="PASS"
    eth0_wlan0_flag=0

    #Precondition Check code block
    
    printf "\n"
    printf "Pre-Conditon check\t\t: Checking whether DUT is already connected to an IPv6 Supported SSID\n\n\n"
    sleep 1
    preCon_IPv6 "$ipv6_conf_SSID" "$TestcaseID"
    local preCon_IPv6_fun_exit=$?
    
    if [ "$preCon_IPv6_fun_exit" -eq 0 ]; then
        sleep 1
        printf "\n\nPre-condition check success. Starting Testcase execution!\n\n\n"
            

    #Step 1 code block for TC_IPv6_MANUAL_01 


        if [[ "$TestcaseID" == "TC_IPv6_MANUAL_01" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IPv6_MANUAL_01"
            sleep 1
            dynamic_current_step_finder "$testcase_prefix" "TC_IPv6_MANUAL" 
        fi    
            

    #Step 1 code block for TC_IPv6_MANUAL_02 


        if [[ "$TestcaseID" == "TC_IPv6_MANUAL_02" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IPv6_MANUAL_02"
            sleep 1
            dynamic_current_step_finder "$testcase_prefix" "TC_IPv6_MANUAL" 
        fi    
            

    #Step 1 code block for TC_IPv6_MANUAL_03 


        if [[ "$TestcaseID" == "TC_IPv6_MANUAL_03" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IPv6_MANUAL_03"
            sleep 1
            dynamic_current_step_finder "$testcase_prefix" "TC_IPv6_MANUAL" 
        fi
        

    #Step 1 code block for TC_IPv6_MANUAL_04 


        if [[ "$TestcaseID" == "TC_IPv6_MANUAL_04" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IPv6_MANUAL_04" "YouTube"
            sleep 1
            

    #Step 2 code block for TC_IPv6_MANUAL_04         


            execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_IPv6_MANUAL_04" "YouTube"
            sleep 1
            dynamic_current_step_finder "$testcase_prefix" "TC_IPv6_MANUAL" 
        fi
       

    #Step 1 code block for TC_IPv6_MANUAL_05 


        if [[ "$TestcaseID" == "TC_IPv6_MANUAL_05" ]]; then
            eth0_wlan0_flag=1
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IPv6_MANUAL_04" "YouTube"
            sleep 1
            

    #Step 2 code block for TC_IPv6_MANUAL_05         


            execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_IPv6_MANUAL_04" "YouTube"
            sleep 1
            dynamic_current_step_finder "$testcase_prefix" "TC_IPv6_MANUAL" 
        fi
                 

    #Step 1 code block for TC_IPv6_MANUAL_07 


        if [[ "$TestcaseID" == "TC_IPv6_MANUAL_07" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IPv6_MANUAL_07"
            sleep 1
            dynamic_current_step_finder "$testcase_prefix" "TC_IPv6_MANUAL" 
        fi
           

    #Step 1 code block for TC_IPv6_MANUAL_06 


        if [[ "$TestcaseID" == "TC_IPv6_MANUAL_06" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IPv6_MANUAL_06"
            sleep 1
            dynamic_current_step_finder "$testcase_prefix" "TC_IPv6_MANUAL" 
        fi

        #TestCase execution Result dynamic updating Function     
        dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}"

        #Postcondition code block    
        printf "\nExecuting Post-condition Steps for Testcase : %s\n\n\n" "$TestcaseID"
        sleep 1
        postCondition_Execution_IPv6 "$TestcaseID" 
        local postCondition_Execution_IPv6_exit=$?

        if [ "$postCondition_Execution_IPv6_exit" -eq 0 ]; then
            printf '\nPost-condition Execution Success. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
        elif [ "$postCondition_Execution_IPv6_exit" -eq 55 ]; then
            printf "\n\nPost-condition: None\n\n"    
        else
            printf '\nPost-condition Execution failed. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
        fi
    else
        printf "\n\nPre-condition check failure. Exiting IPv6 Automated Test!\n\n\n" 
    fi

}

     


#Function Definition for postCondition checking of IPv6


postCondition_Execution_IPv6() {

    local testcaseID="$1" 
    if [[ "$testcaseID" == "TC_IPv6_MANUAL_04" ]] || [[ "$testcaseID" == "TC_IPv6_MANUAL_05" ]]; then
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
  printf "                                                      ******* IPv6 Automated Test *******                                                                    \n";
  printf "\n=============================================================================================================================================================\n\n\n";
  printf '01. Run TestCase : TC_IPv6_MANUAL_01        :\t[ Verify the IP Settings when connected to an IPv6 supported SSID ] \n\n'
  printf '02. Run TestCase : TC_IPv6_MANUAL_02        :\t[ Verify the public IPv6 IP when connected to an IPv6 supported SSID and Ethernet is connected ] \n\n'
  printf '03. Run TestCase : TC_IPv6_MANUAL_03        :\t[ Verify the public IPv6 IP when connected to an IPv6 supported SSID and Ethernet is disconnected ] \n\n'
  printf '04. Run TestCase : TC_IPv6_MANUAL_04        :\t[ Verify the internet accessibility when connected to an IPv6 supported SSID and Ethernet is connected ] \n\n'
  printf '05. Run TestCase : TC_IPv6_MANUAL_05        :\t[ Verify the internet accessibility when connected to an IPv6 supported SSID and Ethernet is disconnected ] \n\n'
  printf '06. Run TestCase : TC_IPv6_MANUAL_06        :\t[ Verify the trace API when connected to an IPv6 supported SSID and Ethernet is disconnected ] \n\n'
  printf '07. Run TestCase : TC_IPv6_MANUAL_07        :\t[ Verify the ping API when connected to an IPv6 supported SSID and Ethernet is disconnected ] \n\n'
  printf '08. Show TestCase Execution Results\n\n'
  printf '09. Exit [ IPv6 Automated Test ]\n\n'
  printf "\n=============================================================================================================================================================\n\n\n";


  # ----- Main Testcaes Execution Menu -----

  
  read -p "Enter an Option to proceed : " menu_choice
  printf '\n\n\n'
  case "$menu_choice" in 
    1)
        exec_start "TC_IPv6_MANUAL_01"
        tc_IPv6_MANUAL_testsuite "tc1_step" "TC_IPv6_MANUAL_01"
        ;;
    2)
        exec_start "TC_IPv6_MANUAL_02"
        tc_IPv6_MANUAL_testsuite "tc2_step" "TC_IPv6_MANUAL_02"
        ;;
    3)
        exec_start "TC_IPv6_MANUAL_03"
        tc_IPv6_MANUAL_testsuite "tc3_step" "TC_IPv6_MANUAL_03"
        ;;
    4)
        exec_start "TC_IPv6_MANUAL_04"
        tc_IPv6_MANUAL_testsuite "tc4_step" "TC_IPv6_MANUAL_04"
        ;;
    5)
        exec_start "TC_IPv6_MANUAL_05"
        tc_IPv6_MANUAL_testsuite "tc5_step" "TC_IPv6_MANUAL_05"
        ;;
    6)
        exec_start "TC_IPv6_MANUAL_06"
        tc_IPv6_MANUAL_testsuite "tc6_step" "TC_IPv6_MANUAL_06"
        ;;                                 
    7)
        exec_start "TC_IPv6_MANUAL_07"
        tc_IPv6_MANUAL_testsuite "tc7_step" "TC_IPv6_MANUAL_07"
        ;;
    8)              
        testcase_result_display_menu "TC_IPv6_MANUAL"  
        ;;       
    9)   
        printf '\nExited IPv6 Automated Test\n\n\n' 
        break
        ;; 
    *)
        printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
        ;;      
  esac
done

