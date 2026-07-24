#!/bin/bash


source device.conf
source generic_functions.sh

#Author : aharil144@cable.comcast.com
#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




#Function Definition get_xconf_id_by_description for extracting firmware config ID by name


get_xconf_id_by_description() {
    local target_desc="$1"
    local json_data="$2"
    # 1. Use sed to put each JSON object on its own line
    # 2. Use awk to find the line with the description and print the ID field
    echo "$json_data" | sed 's/},{/}\n{/g' | awk -F'"' -v desc="$target_desc" '
        $0 ~ desc {
            for (i=1; i<=NF; i++) {
                if ($i == "id") {
                    print $(i+2)
                    exit
                }
            }
        }
    '
}





#Function Definition to check the Pre-Condition before executing TC_XCONF_MANUAL TestSuite


preCon_XCONF() {
    
    local preCon_XCONF_status=0
    local server_url="$1"
    local xconf_applicable="true"
    local build_prefix=""
    local build_suffix=""


    #Check for connectivity to xconf server from DUT
    check_server_connectivity "$server_url"
    local check_server_connectivity_fun_exit=$?
    
    if [ "$check_server_connectivity_fun_exit" -ne 0 ]; then
        preCon_XCONF_status=1
    fi

    #check the platform model to perform XCONF image upgrade
    local dut_platform=$(platform_type_finder)
    case "$dut_platform" in
        RPI4)
            build_prefix="RPI4"
            build_suffix="wic.tar.gz"
            ;;
        AH212) 
            build_prefix="AH212"
            build_suffix=".img"
            ;;
        REALTEKHANK)
            build_prefix="REALTEKHANK"
            build_suffix=".img"
            ;;  
        BCM974116SFF)
            xconf_applicable="false"
            preCon_XCONF_status=1 
            ;;     
        *)
            printf '\n\nInvalid/Unidentified DUT model name [%s]\n\n\n' "$dut_platform"
            xconf_applicable="false"
            preCon_XCONF_status=1
            ;;
    esac

    [ "$xconf_applicable" == "false" ] && { printf '\n\nXCONF image upgrade feature not applicable for DUT platform : %s\n\n\n' "$dut_platform"
        return $preCon_XCONF_status
    }

    #Check for valid XCONF rules/Configuration returning from xconf server to DUT
    printf "\n\nChecking for valid XCONF rules/Configuration from xconf server for DUT : %s\n\n\n" "$dut_platform"
    get_iface_info "eth0" "mac"
    local get_iface_info_exit=$?
    if [ "$get_iface_info_exit" -ne 0 ]; then
        printf '\n\n[ERROR] Failed to get MAC address of DUT. Unable to validate XCONF rules/Configuration from xconf server\n\n\n'
        preCon_XCONF_status=1
    else
        local device_mac_id="$get_iface_result"
        check_XCONF_rules_config "$device_mac_id" "$xconf_config_check_url" "$dut_platform" 
        local check_XCONF_rules_config_fun_exit=$? 
        
        
        if [ "$check_XCONF_rules_config_fun_exit" -ne 0 ]; then
            printf '\n\nXCONF rules/Configuration check failed. Please fix the issue and try again!!!\n\n\n'
            preCon_XCONF_status=1  
        else
            printf '\n\nXCONF rules/Configuration check passed successfully!\n\n\n'
        fi

    fi

    return $preCon_XCONF_status

}



#Function Definition for firmwareconfig_rule_check_core to check for firmware config rules from DUT based on MAC address



firmwareconfig_rule_check_core() {

    local final_url="$1"
    local response=$(curl --silent --location --connect-timeout 10 "$final_url")

    firmware_Filename=$(get_XCONF_key_values "$response" "firmwareFilename")
    firmware_Location=$(get_XCONF_key_values "$response" "firmwareLocation")
    firmware_Version=$(get_XCONF_key_values "$response" "firmwareVersion")

}
   




#Function Definition for check_XCONF_rules_config to check whether DUT have a valid XCONF rules/Configuration from xconf server



check_XCONF_rules_config() {

    local device_mac_id="$1"
    local xconf_check_url="$2"
    local platform_name="$3"
    local check_XCONF_rules_config_status=0
    local final_url="${xconf_check_url}${device_mac_id}"
    local user_choice_buildname="user_choice_buildname"
    local query_log_buildname=$(printf "\n\nDo you want to update the firmware config in XCONF with build %s? [yes/no]: " "$xconf_imagefile_to_upgrade")

    firmwareconfig_rule_check_core "$final_url"                             
    
    if [ -z "$firmware_Filename" ] && [ -z "$firmware_Location" ] && [ -z "$firmware_Version" ]; then
        printf "\n\n[ERROR] : 404 Not Found any Rules|configurations available for device MAC : %s\n\n\n" "$device_mac_id" 
        check_XCONF_rules_config_status=1 
    else
        if [[ "$firmware_Filename" == "$xconf_imagefile_to_upgrade" ]] && [[ "$firmware_Location" == "$xconf_firmware_dwld_location" ]]; then
            if [[ "$firmware_Filename" == "$build_prefix"* ]] && [[ "$firmware_Filename" == *"$build_suffix" ]]; then
                printf "\n\nValid XCONF rules/Configuration found for DUT %s with MAC : %s\n\n\n" "$platform_name" "$device_mac_id"
                check_XCONF_rules_config_status=0
            else
                printf "\n\n[ERROR] Invalid XCONF rules/Configuration found for DUT %s with MAC : %s. Firmware filename in XCONF rules doesn't match with expected format for DUT model : %s\n\n\n" "$platform_name" "$device_mac_id" "$platform_name"
                check_XCONF_rules_config_status=1
            fi
        else
            printf "\n\n[ERROR] XCONF rules/Configuration found for DUT %s with MAC : %s from XCONF server doesn't match with expected values in device config\n\n\n" "$platform_name" "$device_mac_id"
            user_confirmation "$user_choice_buildname" "$query_log_buildname"
            local user_confirmation_fun_exit=$?

            [ "$user_confirmation_fun_exit" -ne 0 ] && { printf "\n\nXCONF Firmware config update operation canceled by user.\n\n\n"; return 1; }

            #xconf_firmwareConfig_name, xconf_API_key_token, xconf_firmwareConfig_query_url are defined in device.conf file
            update_XCONF_firmware_config "$xconf_firmwareConfig_name" "$xconf_API_key_token" "$xconf_firmwareConfig_query_url" "$platform_name"
            local update_XCONF_firmware_config_fun_exit=$?
            [ "$update_XCONF_firmware_config_fun_exit" -ne 0 ] && check_XCONF_rules_config_status=1
        fi
    fi

    return $check_XCONF_rules_config_status

}




#Function Definition for update_XCONF_firmware_config to update the XCONF firmware configuration for the DUT.



update_XCONF_firmware_config() {

    local firmware_config_name="$1"
    local api_token="$2"
    local query_url_firmware_conf="$3"
    local platform_name="$4"
    
    # Wait 10s to connect, 20s total for the download
    json_response=$(curl -sS --connect-timeout 10 --max-time 20 \
    -H "X-API-KEY:$api_token" \
    "$query_url_firmware_conf")

    if [ $? -ne 0 ] || [ -z "$json_response" ]; then
        printf "\n\n[ERROR] Unable to query|fetch firmware config ID's from XCONF server\n\n\n"
        return 1
    fi

    xconf_firmware_config_ID=$(get_xconf_id_by_description "$firmware_config_name" "$json_response")

    if [ -z "$xconf_firmware_config_ID" ]; then
        printf "\n\n[ERROR] Failed to retrieve firmware config ID from XCONF server for firmware config name : %s. Please check the XCONF firmware config and try again.\n\n\n" "$firmware_config_name"
        return 1
    fi  
    printf "\n\nFirmware config ID\t:\t%s\n\nfirmware config name\t:\t%s\n\n\n" "$xconf_firmware_config_ID" "$firmware_config_name" 
    printf "\n\nUpdating XCONF firmware config : %s with firmware filename : %s from device.conf\n\n" "$firmware_config_name" "$xconf_imagefile_to_upgrade"

    local payload_param_missing=0
    case "$platform_name" in
        RPI4)
            xconf_supported_model_ids=("RPI4" "RASPBERRY_PI4")
            ;;
        AH212) 
            xconf_supported_model_ids=("AH212" "AMLOGIC")
            ;;
        REALTEKHANK)
            xconf_supported_model_ids=("REALTEK" "RTD1325")
            ;;     
        *)
            printf '\n\nInvalid/Unidentified DUT model name [%s]\n\n\n' "$platform_name"
            xconf_supported_model_ids=()
            payload_param_missing=1
            ;;
    esac
    # Build supportedModelIds JSON array from bash array defined in device.conf
    # e.g. xconf_supported_model_ids=("AH212" "AMLOGIC")
    if [ ${#xconf_supported_model_ids[@]} -eq 0 ]; then
        local model_ids_json="[]"   
    else
        local model_ids_json
        model_ids_json=$(printf '"%s",' "${xconf_supported_model_ids[@]}")
        model_ids_json="[${model_ids_json%,}]"
    fi
    
    [ $payload_param_missing -eq 1 ] && { printf "\n\n[ERROR] supportedModelIds payload parameter empty/invalid for XCONF firmware config update operation\n\n\n"; return 1; }
    #xconf_restApi_firmware_config, xconf_imagefile_to_upgrade, xconf_imagefile_version, xconf_reboot_immediately are defined in device.conf file
    local xconf_firmware_config_payload
    xconf_firmware_config_payload=$(printf '{"id":"%s","firmwareFilename":"%s","firmwareVersion":"%s","rebootImmediately":%s,"description":"%s","supportedModelIds":%s}' \
        "$xconf_firmware_config_ID" \
        "$xconf_imagefile_to_upgrade" \
        "$xconf_imagefile_version" \
        "${xconf_reboot_immediately:-false}" \
        "$firmware_config_name" \
        "$model_ids_json")

    local xconf_response
    xconf_response=$(curl --silent --location \
        --connect-timeout 10 --max-time 20 \
        --request PUT "$xconf_restApi_firmware_config" \
        -H "X-API-KEY:$api_token" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        --data "$xconf_firmware_config_payload")

    if [ $? -eq 0 ] && [[ "$xconf_response" == *"firmware"* ]] && [[ "$xconf_response" == *"id"* ]]; then
        printf "\n\nXCONF firmware configuration updated successfully for DUT.\n\n\n"
        return 0
    else
        printf "\n\n[ERROR] Failed to update XCONF firmware configuration for DUT. No response received from server.\n\n\n"
        return 1
    fi

}




#Function Definition for xconf_verify_rules_response — Step 1: curl XCONF server with DUT MAC and verify firmware update response



xconf_verify_rules_response() {
    local step="$1"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Execute curl command to verify DUT is able to get the XCONF firmware update response\n\n\n" "$step"
    sleep 1
    get_iface_info "eth0" "mac"
    local get_iface_info_exit=$?
    if [ "$get_iface_info_exit" -ne 0 ]; then
        printf "\n\n[ERROR] Failed to retrieve DUT MAC address from eth0 interface\n\n\n"
        return 1
    fi
    local device_mac_id="$get_iface_result"
    local final_url="${xconf_config_check_url}${device_mac_id}"
    printf "\n\ncurl %s\n\n\n" "$final_url"
    local xconf_response=$(curl --silent --location --connect-timeout 10 "$final_url")
    printf "\n\nXCONF server response :\n%s\n\n\n" "$xconf_response"
    local resp_filename=$(get_XCONF_key_values "firmwareFilename" "$xconf_response")
    local resp_location=$(get_XCONF_key_values "firmwareLocation" "$xconf_response")
    local resp_version=$(get_XCONF_key_values "firmwareVersion" "$xconf_response")
    if [ -n "$resp_filename" ] && [ -n "$resp_location" ] && [ -n "$resp_version" ]; then
        printf "\n\nXCONF firmware update response received successfully for DUT MAC : %s\n\n" "$device_mac_id"
        printf "\nfirmwareFilename\t:\t%s\n" "$resp_filename"
        printf "\nfirmwareLocation\t:\t%s\n" "$resp_location"
        printf "\nfirmwareVersion\t\t:\t%s\n\n\n" "$resp_version"
        return 0
    else
        printf "\n\n[ERROR] XCONF server did not return a valid firmware update response for DUT MAC : %s\n\n\n" "$device_mac_id"
        return 1
    fi
}




#Function Definition for xconf_activate_system_plugin — Step 2: Activate org.rdk.System plugin via Controller.1.activate



xconf_activate_system_plugin() {
    local step="$1"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Execute curl command to activate org.rdk.System plugin via Controller.1.activate\n\n\n" "$step"
    local curl_activate="curl -X POST http://127.0.0.1:9998/jsonrpc -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"Controller.1.activate\",\"params\":{\"callsign\":\"org.rdk.System\"}}'"
    printf "\n%s\n\n\n" "$curl_activate"
    sleep 1
    local activate_response=$(curl --silent -X POST http://127.0.0.1:9998/jsonrpc \
        -d '{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.System"}}')
    printf "\n\norg.rdk.System plugin activation response :\n%s\n\n\n" "$activate_response"
    if echo "$activate_response" | grep -q '"result":null'; then
        printf "\n\norg.rdk.System plugin activated successfully\n\n\n"
        return 0
    else
        printf "\n\n[ERROR] Failed to activate org.rdk.System plugin. Response : %s\n\n\n" "$activate_response"
        return 1
    fi
}




#Function Definition for xconf_trigger_updateFirmware — Step 3: Trigger XCONF firmware upgrade via org.rdk.System.1.updateFirmware



xconf_trigger_updateFirmware() {
    local step="$1"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Execute curl command to trigger XCONF firmware upgrade via org.rdk.System.1.updateFirmware\n\n\n" "$step"
    local curl_updateFirmware="curl -X POST http://127.0.0.1:9998/jsonrpc -d '{\"jsonrpc\":\"2.0\",\"id\":\"3\",\"method\":\"org.rdk.System.1.updateFirmware\",\"params\":{}}'"
    printf "\n%s\n\n\n" "$curl_updateFirmware"
    sleep 1
    local update_response=$(curl --silent -X POST http://127.0.0.1:9998/jsonrpc \
        -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.updateFirmware","params":{}}')
    local update_success=$(get_JSON_KEY_values "success" "$update_response")
    printf "\n\norg.rdk.System.1.updateFirmware API response :\n%s\n\n\n" "$update_response"
    if [ "$update_success" = "true" ]; then
        printf "\n\nXCONF firmware upgrade triggered successfully. Firmware download initiated on DUT.\n\n\n"
        return 0
    else
        printf "\n\n[ERROR] Failed to trigger XCONF firmware upgrade. API returned : %s\n\n\n" "$update_success"
        return 1
    fi
}




#Function Definition for xconf_monitor_swupdate_log — Step 4: Monitor swupdate.log for firmware upgrade completion



xconf_monitor_swupdate_log() {
    local step="$1"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Monitor swupdate log for XCONF firmware upgrade completion\n\n\n" "$step"
    sleep 1
    local log_file="/opt/logs/swupdate.log"
    local success_pattern_1="doCDL success"
    local success_pattern_2="Image Flashing is success"
    local timeout=1200
    local elapsed=0
    local check_interval=15
    printf "\n\nCommand : tail -f %s\n\n" "$log_file"
    printf "\nMonitoring %s for firmware upgrade completion...\n" "$log_file"
    printf "\nExpected success strings : \"%s\" OR \"%s\"\n\n\n" "$success_pattern_1" "$success_pattern_2"
    while [ "$elapsed" -lt "$timeout" ]; do
        if grep -q "$success_pattern_1" "$log_file" 2>/dev/null || grep -q "$success_pattern_2" "$log_file" 2>/dev/null; then
            printf "\n\nXCONF firmware upgrade completed successfully. Success log detected in %s\n\n\n" "$log_file"
            printf "\n\nFirmware image is ready. Please reboot the DUT manually to activate the new firmware version : %s\n\n\n" "$xconf_imagefile_version"
            return 0
        fi
        printf "\rWaiting for firmware upgrade to complete... [%d/%d seconds elapsed]" "$elapsed" "$timeout"
        sleep "$check_interval"
        elapsed=$((elapsed + check_interval))
    done
    printf "\n\n[ERROR] Timeout : XCONF firmware upgrade did not complete within %d seconds. Check %s for details.\n\n\n" "$timeout" "$log_file"
    return 1
}




#Function defnition for testcase TC_XCONF_MANUAL_01



TC_XCONF_MANUAL_01() {

    local step_num="$1"
    if [ "$step_num" = "1" ]; then
        xconf_verify_rules_response "$step_num"
        local exit_code=$?
        [ "$exit_code" -eq 0 ] && return 0 || return 1

    elif [ "$step_num" = "2" ]; then
        xconf_activate_system_plugin "$step_num"
        local exit_code=$?
        [ "$exit_code" -eq 0 ] && return 0 || return 1

    elif [ "$step_num" = "3" ]; then
        xconf_trigger_updateFirmware "$step_num"
        local exit_code=$?
        [ "$exit_code" -eq 0 ] && return 0 || return 1

    elif [ "$step_num" = "4" ]; then
        xconf_monitor_swupdate_log "$step_num"
        local exit_code=$?
        [ "$exit_code" -eq 0 ] && return 0 || return 1

    else
        printf "\n\nDEBUG : Invalid step number for Testcase : TC_XCONF_MANUAL_01\n\n\n"
        return 1
    fi

}




#Function Definition for TestCase : tc_XCONF_MANUAL_testsuite



tc_XCONF_MANUAL_testsuite() {

  local TestcaseID="$2"
  local testcase_prefix="$1"
  test_step_status="PASS"

  #Precondition Check code block here xconf_server_url is passed to preCon_XCONF function from device.conf

  printf "\nPre-Conditon check\t\t: Checks whether DUT have a valid XCONF rules/Configuration and connected to network\n\n\n"
  preCon_XCONF "$xconf_server_url"
  local preCon_XCONF_fun_exit=$?
  
  if [ "$preCon_XCONF_fun_exit" -eq 0 ]; then
    printf '\n\nPre-condition check success. Starting Testcase execution!\n\n\n'


    #Step 1 code block for TC_XCONF_MANUAL_01

        if [[ "$TestcaseID" == "TC_XCONF_MANUAL_01" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_XCONF_MANUAL_01"
            sleep 1

    #Step 2 code block for TC_XCONF_MANUAL_01

            execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_XCONF_MANUAL_01"
            sleep 1

    #Step 3 code block for TC_XCONF_MANUAL_01

            execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_XCONF_MANUAL_01"
            sleep 1

    #Step 4 code block for TC_XCONF_MANUAL_01

            execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_XCONF_MANUAL_01"
            sleep 1
            dynamic_current_step_finder "$testcase_prefix" "TC_XCONF_MANUAL"
        fi

        #TestCase execution Result dynamic updating Function
        dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}"

        #Log generation and upload to server function
        log_generate_operations "$failed_step_num" "XCONF"

        printf "\n\nPost-condition: None\n\n"
  else
        printf "\n\nPre-condition check failure. Exiting XCONF Firmware Upgrade Automated Test!\n\n\n"
  fi

}















#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





while true; do
  printf "\n"
  printf "\n=============================================================================================================================================================\n\n";
  printf "                                                    ******* XCONF Firmware Upgrade Automated Test *******                                                                    ";
  printf "\n=============================================================================================================================================================\n\n\n";
  printf '01. Run TestCase : TC_XCONF_MANUAL_01        :\t[ Verify the XCONF Firmware upgrade beahviour using rdkservice API ] \n\n'
  printf '02. Run TestCase : TC_XCONF_MANUAL_02        :\t[ Verify the XCONF Firmware upgrade beahvior from another image to test image ] \n\n'
  printf '03. Run TestCase : TC_XCONF_MANUAL_03        :\t[ Verify the XCONF Firmware upgrade beahvior when DUT is connected to a Wifi network ] \n\n'
  printf '04. Run TestCase : TC_XCONF_MANUAL_04        :\t[ Verify the XCONF Firmware upgrade beahvior from test image to another image via RDK UI ] \n\n'
  printf "05. Run TestCase : TC_XCONF_MANUAL_05        :\t[ Verify the XCONF Firmware upgrade doesn't affect all user-specific settings, app data, and connections ] \n\n"
  printf '06. Show TestCase Execution Results\n\n'
  printf '07. Exit [ XCONF Firmware Upgrade Automated Test ]\n\n'
  printf "\n=============================================================================================================================================================\n\n\n";


  # ----- Main Testcaes Execution Menu -----

  
  read -p "Enter an Option to proceed : " menu_choice
  printf '\n\n\n'
  case "$menu_choice" in 
    1)
        exec_start "TC_XCONF_MANUAL_01"
        tc_XCONF_MANUAL_testsuite "tc1_step" "TC_XCONF_MANUAL_01"
        ;;
    2)
        exec_start "TC_XCONF_MANUAL_02"
        tc_XCONF_MANUAL_testsuite "tc2_step" "TC_XCONF_MANUAL_02"
        ;;
    3)
        exec_start "TC_XCONF_MANUAL_03"
        tc_XCONF_MANUAL_testsuite "tc3_step" "TC_XCONF_MANUAL_03"
        ;;
    4)
        exec_start "TC_XCONF_MANUAL_04"
        tc_XCONF_MANUAL_testsuite "tc4_step" "TC_XCONF_MANUAL_04"
        ;;
    5)
        exec_start "TC_XCONF_MANUAL_05"
        tc_XCONF_MANUAL_testsuite "tc5_step" "TC_XCONF_MANUAL_05"
        ;;                                 
    6)
        testcase_result_display_menu "TC_XCONF_MANUAL"  
        ;;       
    7)   
        printf '\nExited XCONF Automated Test\n\n\n' 
        break
        ;; 
    *)
        printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
        ;;      
  esac
done
