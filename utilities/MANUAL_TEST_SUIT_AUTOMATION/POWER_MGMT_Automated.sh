#!/bin/bash


source device.conf
source generic_functions.sh

#Author : aharil144@cable.comcast.com
#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




#Function defnition for ipv6_extract_API_key_values to extract key values



power_extract_API_key_values() {

    local index=1
    # Loop through all arguments provided to the function
    for arg in "$@"; do
        if [[ -z "$arg" ]]; then
            echo "\n\nDEBUG : Argument $index is empty or missing in power_extract_API_key_values!\n\n"
            #error code specific for params empty error
            return 100 
        fi
        ((index++))
    done
    local json_payload_power="$1"
    shift # The rest of the arguments are the keys we want (e.g., "success" "isConnected" "hdcpReason", etc) 
    local json_Res_power=$(curl -# --data-binary "$json_payload_power" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
    for _key_ in "$@"; do
        local power_key_value=$(get_JSON_KEY_values "$_key_" "$json_Res_power")
        # Example: if key is "success", it creates a variable $success
        # It results in: success="true"
        eval "power_${_key_}=\"\$power_key_value\""
    done

}



#Function Definition to check the Pre-Condition before executing TC_POWER_MANUAL TestSuite



preCon_POWER() {

    local user_choice="user_choice"
    local query_power=$(printf "\n\nIs RDK UI Homepage visible on TV [yes/no]: ")
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nPre-Condition\t\t:Execute curl command to verify the current powerstate of device and RDK UI is visible\n\n\n"
    local curl_to_Getpowerstate="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\":\"2.0\",\"id\":\"3\",\"method\":\"org.rdk.System.1.getPowerState\",\"params\":{}}' http://127.0.0.1:9998/jsonrpc"
    printf "\n$curl_to_Getpowerstate\n\n\n"   
    sleep 1
    set_and_get_powerState "0" "ON"
    local set_and_get_powerState_exit=$?
       
    user_confirmation "$user_choice" "$query_power"
    local user_confirmation_fun_exit=$?

    if [ "$user_confirmation_fun_exit" -eq 0 ] && [ "$set_and_get_powerState_exit" -eq 0 ]; then
        printf "\n\nRDK UI is Visible and DUT is in %s state\n\n\n" "$power_powerState"
        return 0
    elif [ "$user_confirmation_fun_exit" -ne 0 ]; then
        printf "\n\nRDK UI Homepage is not visible on TV\n\n\n"
        return 1 
    elif [ "$set_and_get_powerState_exit" -eq 90 ]; then  
        printf "\n\nPower state is not ON returns value : %s setting the powerstate to ON\n\n\n" "$power_powerstate"
        set_and_get_powerState "1" "ON"
        local set_and_get_powerState_exit_1=$?

        set_and_get_powerState "0" "ON"
        local set_and_get_powerState_exit_2=$?

        if [ "$set_and_get_powerState_exit_1" -eq 0 ] && [ "$set_and_get_powerState_exit_2" -eq 0 ]; then
            return 0
        elif [ "$set_and_get_powerState_exit_2" -eq 90 ]; then
            printf "\n\nEven After setting the powerstate to ON. getPowerState API returns state : %s\n\n\n" "$power_powerState" 
            return 1
        else
            printf "\n\nUnable to set the DUT powerstate to ON\n\n\n" 
        fi         
    else
        return 1      
    fi 

}



#Function Definition for set_and_get_powerStates to set powerstates



set_and_get_powerState() {

    local get_or_set="$1"
    local power_state="$2"
    #(0 for get powerstate and 1 for set the powerstate)
    if [ "$get_or_set" = "0" ]; then
        local getpowerstate_payload=$(printf '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}')
        power_extract_API_key_values "$getpowerstate_payload" "powerState" "success"
        local power_extract_API_key_values_exit=$?
        if [ "$power_extract_API_key_values_exit" -eq 100 ]; then
            return 1
        else
            if [ "$power_powerState" = "ON" ] && [ "$power_success" = "true" ]; then
                printf "\n\nPower state\t:\t%s\n\nAPI Response\t:\t%s\n\n\n" "$power_powerState" "$power_success"
                return 0
            elif [ "$power_success" != "true" ]; then  
                printf "\n\norg.rdk.System.1.getPowerState API return value : %s\n\n\n" "$power_success"
                return 1 
            elif [ "$power_powerState" = "STANDBY" ] || [ "$power_powerState" = "LIGHTSLEEP" ]; then  
                printf "\n\nPower state\t:\t%s\n\n\n" "$power_powerState"
                return 90              
            else
                printf "\n\nPower state is not ON returns value : %s\n\n\n" "$power_powerState"
                return 1
            fi 
        fi    
    else
        local setpowerstate_payload=$(printf '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.setPowerState","params":{"powerState":"%s", "standbyReason":"For Testing"}}' "$power_state")
        power_extract_API_key_values "$setpowerstate_payload" "success"
        local power_extract_API_key_values_exit=$?
        if [ "$power_extract_API_key_values_exit" -eq 100 ]; then
            return 1
        else    
            if [ "$power_success" = "true" ]; then
                printf "\n\norg.rdk.System.1.setPowerState API execution success value : %s\n\n\n" "$power_success"
                return 0
            else
                printf "\n\norg.rdk.System.1.setPowerState API execution failed value : %s\n\n\n" "$power_success"
                return 1
            fi
        fi 
    fi               

}



#Function defnition for subfunction to Verify RDK UI powerstate settings



powerstate_RDKUI() {

    local step="$1"
    local user_choice="user_choice"
    local query_RDKUI_powerstate=$(printf "\n\nIs Light sleep is in ticked state on Settings/Other Settings/Energy Saver [yes/no]: ")
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Perform Manual operation : Navigate to Settings/Other Settings/Energy Saver and select Light Sleep\n\n\n" "$step" 
    sleep 1
    local selection_Query="PLEASE SELECT LIGHT SLEEP FROM ENERGY SAVER TO PROCEED TEST!!!"
    blink_HDMI_Query "$selection_Query"

    user_confirmation "$user_choice" "$query_RDKUI_powerstate"
    local user_confirmation_fun_exit=$?

    if [ "$user_confirmation_fun_exit" -eq 0 ]; then
        return 0
    else
        return 1
    fi 

}



#Function defnition for subfunction to get the powerstate



get_Set_Powerstate_subFun() {

    local step="$1"
    local get_set_type="$2"
    if [ "$get_set_type" = "0" ] 
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute Curl command to get the current Powerstate of DUT\n\n\n" "$step" 
        local curl_to_getPowerstate="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\":\"2.0\",\"id\":\"3\",\"method\":\"org.rdk.System.1.getPowerState\",\"params\":{}}' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_getPowerstate\n\n\n" 
        sleep 1
        set_and_get_powerState "$get_set_type"
        local set_and_get_powerState_exit=$?

        if [ "$set_and_get_powerState_exit" -eq 0 ]; then
            return 0
        elif [ "$set_and_get_powerState_exit" -eq 90 ]; then
            if [ "$step" = "4" ]; then 
                return 0
            else
                return 1
            fi        
        else
            return 1
        fi
    else
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute Curl command to set the current Powerstate of DUT to LIGHT SLEEP\n\n\n" "$step" 
        local curl_to_setPowerstate="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\":\"2.0\",\"id\":\"3\",\"method\":\"org.rdk.System.1.setPowerState\",\"params\":{\"powerState\":\"LIGHT_SLEEP\", \"standbyReason\":\"For Testing\"}}' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_setPowerstate\n\n\n" 
        sleep 1
        set_and_get_powerState "$get_set_type" "LIGHT_SLEEP"
        local set_and_get_powerState_exit=$?

        if [ "$set_and_get_powerState_exit" -eq 0 ]; then
            return 0       
        else
            return 1
        fi
    fi     

}



#Function defnition for testcase TC_POWER_MANUAL_01



TC_POWER_MANUAL_01() {

    local step_num="$1"
    local user_choice="user_choice"
    local query_power=$(printf "\n\nIs RDK UI Homepage visible on TV [yes/no]: ")
    if [ "$step_num" = "1" ]; then
       powerstate_RDKUI "$step_num"
       local powerstate_RDKUI_exit=$?

        if [ "$powerstate_RDKUI_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "2" ]; then
        get_Set_Powerstate_subFun "$step_num" "1"
        local get_Set_Powerstate_subFun_exit=$?

        if [ "$get_Set_Powerstate_subFun_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "3" ]; then  
        get_Set_Powerstate_subFun "$step_num" "0"
        local get_Set_Powerstate_subFun_exit=$?

        user_confirmation "$user_choice" "$query_power"
        local user_confirmation_fun_exit=$?

        if [ "$get_Set_Powerstate_subFun_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 1 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step_num" = "4" ]; then     
    fi    

}



#Function Definition for TestCase : tc_POWER_MANUAL_testsuite



tc_POWER_MANUAL_testsuite() {

    local TestcaseID="$2"
    local testcase_prefix="$1"
    test_step_status="PASS"
    
    #Precondition Check code block
    
    printf "\n"
    printf "Pre-Conditon check\t\t: Checking whether the current powerstate of device is expected and RDK UI is visible\n\n\n"
    sleep 1
    preCon_POWER 
    local preCon_POWER_fun_exit=$?
    
    if [ "$preCon_POWER_fun_exit" -eq 0 ]; then
        sleep 1
        printf "\n\nPre-condition check success. Starting Testcase execution!\n\n\n"
            

    #Step 1 code block for TC_POWER_MANUAL_01



    else
        printf "\n\nPre-condition check failure. Exiting IPv6 Automated Test!\n\n\n" 
    fi          

}










#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





while true; do

  printf "\n"
  printf "\n=============================================================================================================================================================\n\n";
  printf "                                                      ******* POWER MANAGEMENT Automated Test *******                                                                    \n";
  printf "\n=============================================================================================================================================================\n\n\n";
  printf '01. Run TestCase : TC_POWER_MANUAL_01        :\t[ Verify DUT can be set to LIGHT SLEEP and then wakeup with the help of RDK service APIs ] \n\n'
  printf '02. Show TestCase Execution Results\n\n'
  printf '03. Exit [ POWER MANAGEMENT Automated Test ]\n\n'
  printf "\n=============================================================================================================================================================\n\n\n";


  # ----- Main Testcaes Execution Menu -----

  
  read -p "Enter an Option to proceed : " menu_choice
  printf '\n\n\n'
  case "$menu_choice" in 
    1)
        exec_start "TC_POWER_MANUAL_01"
        tc_POWER_MANUAL_testsuite "tc1_step" "TC_POWER_MANUAL_01"
        ;;
    2)              
        testcase_result_display_menu "TC_POWER_MANUAL"  
        ;;       
    3)   
        printf '\nExited POWER MANAGEMENT Automated Test\n\n\n' 
        break
        ;; 
    *)
        printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
        ;;      
  esac
done
