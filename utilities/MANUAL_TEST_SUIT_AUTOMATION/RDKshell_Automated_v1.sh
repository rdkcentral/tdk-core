#!/bin/bash


source device.conf
source generic_functions.sh

#Author : aharil144@cable.comcast.com
#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




#Function Definition to check the Pre-Condition before executing TC_RDKshell_MANUAL TestSuite



preCon_RDKshell() {

  browserInstance_deactivate "WebKitBrowser"
  local browserInstance_deactivate_status=$?

  browserInstance_deactivate "HtmlApp"
  local browserInstance_deactivate_status_1=$?

  rdkshell_suspend_operation "ResidentApp"
  local rdkshell_suspend_exit=$?
  
  if [ "$browserInstance_deactivate_status" -eq 0 ] && [ "$browserInstance_deactivate_status_1" -eq 0 ] && [ "$rdkshell_suspend_exit" -eq 0 ]; then
    return 0
  else
    printf "\n\n\nDEBUG : browserInstance_deactivate | rdkshell_suspend_operation function failed with error code : %s | %s | %s\n\n" "$browserInstance_deactivate_status" "$browserInstance_deactivate_status_1" "$rdkshell_suspend_exit"
    return 1
  fi    

}




#Function defnition for WebkitBrowser Default URL launch via RDKShell used in multiple testcases



rdkshell_wktBrw_defURL_launch() {
    local step="$1"
    local def_URL="$2"
    local user_choice="user_choice_url"
    local query_wkt_behaviour=$(printf "\n\nIs default webpage URL : %s loaded in WebKitBrowser via RDKshell and Visible on TV [yes/no]: " "$def_URL")
    sleep 1
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Execute curl command to launch Default preset URL : %s in WebKitBrowser via RDKShell\n\n\n" "$step" "$def_URL"    
    printf "\n\ncurl --data-binary '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "WebKitBrowser", "type":"WebKitBrowser", "uri":%s, "x":0, "y":0, "w":1920, "h":1080}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc \n\n" "$def_URL"
    check_file_on_serve "$def_URL"
    local check_file_on_server_exit=$?
    
    if [ "$check_file_on_server_exit" -eq 0 ]; then
        printf "\n\n\nConfigured default webpage : [ %s ] is accessible and available via URL\n\n\n" "$def_URL"
        sleep 1
        rdkshell_URL_launch "$def_URL" "WebKitBrowser"
        local rdkshell_URL_launch_exit=$?
    
        user_confirmation "$user_choice" "$query_wkt_behaviour"
        local user_confirmation_fun_exit=$?

        if [ "$rdkshell_URL_launch_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
            printf "\n\nDefault webpage URL : [ %s ] loaded in WebKitBrowser via RDKshell and visible on TV\n\n\n" "$def_URL"
            return 0
        else
            printf "\n\nUnable to load default webpage URL : [ %s ] in WebKitBrowser via RDKshell and Not visible on TV\n\n\n" "$def_URL"
            return 1
        fi
    else
        printf "\n\n\nDEBUG : Configured default webpage URL : [ %s ] is not available.Returns %s error code from Webpage\n\n\n" "$def_URL" "$check_file_on_server_exit"
        return $check_file_on_server_exit 
    fi 

}




#Function defnition for WebkitBrowser|HtmlApp deactivate used for multiple testcases



wktInstance_deactivate_step() {

    local step_no="$1"
    local instance_name="$2" 
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Execute curl command to deactivate the active %s instance\n\n\n" "$step_num" "$instance_name" 
    local curl_to_deactivate="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\": \"2.0\",\"id\": 1234567890,\"method\": \"Controller.1.deactivate\",\"params\": {\"callsign\": \"%s\"}}' http://127.0.0.1:9998/jsonrpc \n\n"
    printf "\n$curl_to_deactivate\n\n\n" "$instance_name" 
    sleep 1
    browserInstance_deactivate "$instance_name"
    local browserInstance_deactivate_exit=$?

    if [ "$browserInstance_deactivate_exit" -eq 0 ]; then
        printf "\n\nActive %s Instance deactivated successfully\n\n\n" "$instance_name"
        return 0
    else
        printf "\n\nDeactivating Active %s Instance failed\n\n\n" "$instance_name"
        return $browserInstance_deactivate_exit
    fi        
}



#Function defnition for testcase TC_RDKSHELL_MANUAL_01 



TC_RDKSHELL_MANUAL_01() {

  local step_num="$1"
  local wktbrw_url="$2"
  local user_choice_url="user_choice_url"
  local query_URL_load=$(printf "\n\nIs Html preset URL : %s loaded in WebKitBrowser and Visible on TV [yes/no]: " "$wktbrw_url")
  if [ "$step_num" = "6" ]; then
    wktInstance_deactivate_step "$step_num" "WebKitBrowser"  
    local wktInstance_deactivate_step_exit=$?

    if [ "$wktInstance_deactivate_step_exit" -eq 0 ]; then
        return 0
    else
        return $wktInstance_deactivate_step_exit
    fi 
  else
    rdkshell_wktBrw_defURL_launch "$step_num" "$wktbrw_url"
    local rdkshell_wktBrw_defURL_launch_exit=$?

    if [ "$rdkshell_wktBrw_defURL_launch_exit" -eq 0 ]; then
      return 0
    else
      return $rdkshell_wktBrw_defURL_launch_exit
    fi
  fi    

}




#Function defnition for testcase TC_RDKSHELL_MANUAL_02 



TC_RDKSHELL_MANUAL_02() {

    local step_num="$1"
    local htmlApp_url="$2"
    local user_choice_url="user_choice_url"
    local query_URL_load=$(printf "\n\nIs preset URL : %s loaded in HtmlApp instance and Visible on TV [yes/no]: " "$htmlApp_url")
    if [ "$step_num" = "4" ]; then
       wktInstance_deactivate_step "$step_num" "HtmlApp"  
       local wktInstance_deactivate_step_exit=$?

       if [ "$wktInstance_deactivate_step_exit" -eq 0 ]; then
         return 0
       else
         return $wktInstance_deactivate_step_exit
       fi        
    else
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to launch preset URL : %s via HtmlApp instance with RDKShell\n\n\n" "$step_num" "$htmlApp_url"    
        printf "\n\ncurl --data-binary '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "HtmlApp", "type":"HtmlApp", "uri":"%s", "x":0, "y":0, "w":1920, "h":1080}}'  -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc \n\n" "$htmlApp_url"
        sleep 1
        check_file_on_serve "$htmlApp_url"
        local check_file_on_server_exit=$?
        
        if [ "$check_file_on_server_exit" -eq 0 ]; then
            printf "\n\n\nConfigured preset URL : [ %s ] is available in server and accessible via URL\n\n\n" "$htmlApp_url"
            sleep 1
            rdkshell_URL_launch "$htmlApp_url" "HtmlApp"
            local rdkshell_URL_launch_exit=$?

            user_confirmation "$user_choice_url" "$query_URL_load"
            local user_confirmation_fun_exit=$?

            if [ "$rdkshell_URL_launch_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
                printf "\n\nPreset URL : [ %s ] loaded in HtmlApp via RDKShell and visible on TV\n\n\n" "$htmlApp_url"
                return 0
            else
                printf "\n\nUnable to load preset URL : [ %s ] in HtmlApp via RDKShell and Not visible on TV\n\n\n" "$htmlApp_url"
                return 1
            fi
        else
            printf "\n\n\nDEBUG : Configured preset URL : [ %s ] is not available in server.Returns %s error code from server\n\n\n" "$htmlApp_url" "$check_file_on_server_exit"
            return $check_file_on_server_exit 
        fi
    fi
}




#Function defnition for testcase TC_RDKSHELL_MANUAL_03 



TC_RDKSHELL_MANUAL_03() {

    local step_num="$1"
    local wktBrw_Default_URL="$3"
    local opacity_val="$2"
    local user_choice="user_choice"
    local query_opacity=$(printf "\n\nIs Opacity behaviour of WebKitBrowser working as expected for value : %s and Visible on TV [yes/no]: " "$opacity_val")
    if [ "$step_num" = "1" ]; then
        rdkshell_wktBrw_defURL_launch "$step_num" "$wktBrw_Default_URL"
        local rdkshell_wktBrw_defURL_launch_exit=$?

        if [ "$rdkshell_wktBrw_defURL_launch_exit" -eq 0 ]; then
            return 0
        else
            return $rdkshell_wktBrw_defURL_launch_exit
        fi
    elif [ "$step_num" = "5" ]; then
        wktInstance_deactivate_step "$step_num" "WebKitBrowser"  
        local wktInstance_deactivate_step_exit=$?

        if [ "$wktInstance_deactivate_step_exit" -eq 0 ]; then
            return 0
        else
            return $wktInstance_deactivate_step_exit
        fi
    else
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to verify Opacity behavior in WebKitBrowser via RDKShell\n\n\n" "$step_num"    
        local curl_to_execute="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"org.rdk.RDKShell.1.setOpacity\", \"params\":{ \"client\": \"WebKitBrowser\", \"opacity\": %s}}' http://127.0.0.1:7778/jsonrpc"
        printf "\n$curl_to_execute\n\n\n" "$opacity_val"
        sleep 1    
        local json_payload_opacity=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.setOpacity", "params":{ "client": "WebKitBrowser", "opacity": %s}}' "$opacity_val")
        local json_Res_opacity=$(curl -# --data-binary "$json_payload_opacity" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
        local opacity_status=$(echo "$json_Res_opacity" | sed -n 's/.*"success":[[:space:]]*\([^,}]*\).*/\1/p')
        sleep 1
        
        user_confirmation "$user_choice" "$query_opacity"
        local user_confirmation_fun_exit=$?

        if [ "$opacity_status" = "true" ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
           return 0
        else
            if [ "$opacity_status" != "true" ]; then
                #235 error code return specific for opacity value setting error
                return 235
            else
                printf "\n\nUnable to verify setOpacity behaviour of WebkitBrowser from TV screen\n\n\n"
                return $user_confirmation_fun_exit
            fi       
        fi
    fi        

}




#Function defnition for testcase TC_RDKSHELL_MANUAL_04 



TC_RDKSHELL_MANUAL_04() {

    local step_num="$1"
    local wktBrw_Default_URL="$2"
    local user_choice="user_choice"
    local query_scale=$(printf "\n\nIs WebKitBrowser setScale behaviour working as expected and is Visible on TV [yes/no]: ")
    if [ "$step_num" = "1" ]; then
        rdkshell_wktBrw_defURL_launch "$step_num" "$wktBrw_Default_URL"
        local rdkshell_wktBrw_defURL_launch_exit=$?

        if [ "$rdkshell_wktBrw_defURL_launch_exit" -eq 0 ]; then
            return 0
        else
            return $rdkshell_wktBrw_defURL_launch_exit
        fi
    elif [ "$step_num" = "3" ]; then
        wktInstance_deactivate_step "$step_num" "WebKitBrowser"  
        local wktInstance_deactivate_step_exit=$?

        if [ "$wktInstance_deactivate_step_exit" -eq 0 ]; then
            return 0
        else
            return $wktInstance_deactivate_step_exit
        fi
    else
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to verify setScale behavior in WebKitBrowser via RDKShell\n\n\n" "$step_num" 
        local curl_to_setScale="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"org.rdk.RDKShell.1.setScale\", \"params\":{\"client\": \"WebKitBrowser\", \"sx\":1.5, \"sy\":1.5}}' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_setScale\n\n\n"   
        sleep 1    
        local json_payload_setScale=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.setScale", "params":{"client": "WebKitBrowser", "sx":1.5, "sy":1.5}}')
        local json_Res_setScale=$(curl -# --data-binary "$json_payload_setScale" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
        local setScale_status=$(echo "$json_Res_setScale" | sed -n 's/.*"success":[[:space:]]*\([^,}]*\).*/\1/p')
        sleep 1
        
        user_confirmation "$user_choice" "$query_scale"
        local user_confirmation_fun_exit=$?

        if [ "$setScale_status" = "true" ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
           return 0
        else
            if [ "$setScale_status" != "true" ]; then
                #231 error code return specific for opacity value setting error
                return 231
            else
                printf "\n\nUnable to verify setScale behaviour of WebkitBrowser from TV screen\n\n\n"
                return $user_confirmation_fun_exit
            fi       
        fi
    fi        

}




#Function defnition for testcase TC_RDKSHELL_MANUAL_05 



TC_RDKSHELL_MANUAL_05() {

    local step_num="$1"
    local wktBrw_Default_URL="$2"
    local user_choice="user_choice"
    local query_setBounds=$(printf "\n\nIs WebKitBrowser Bounds behaviour of WebkitBrowser working as expected and is Visible on TV [yes/no]: ")
    if [ "$step_num" = "1" ]; then
        rdkshell_wktBrw_defURL_launch "$step_num" "$wktBrw_Default_URL"
        local rdkshell_wktBrw_defURL_launch_exit=$?

        if [ "$rdkshell_wktBrw_defURL_launch_exit" -eq 0 ]; then
            return 0
        else
            return $rdkshell_wktBrw_defURL_launch_exit
        fi
    elif [ "$step_num" = "3" ]; then
        wktInstance_deactivate_step "$step_num" "WebKitBrowser"  
        local wktInstance_deactivate_step_exit=$?

        if [ "$wktInstance_deactivate_step_exit" -eq 0 ]; then
            return 0
        else
            return $wktInstance_deactivate_step_exit
        fi
    else
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to verify setBounds behavior in WebKitBrowser via RDKShell\n\n\n" "$step_num" 
        local curl_to_setBounds="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"org.rdk.RDKShell.1.setBounds\", \"params\":{\"client\": \"WebKitBrowser\",\"x\": 100,\"y\": 100,\"w\": 600,\"h\": 400}}' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_setBounds\n\n\n"   
        sleep 1    
        local json_payload_setBounds=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.setBounds", "params":{"client": "WebKitBrowser","x": 100,"y": 100,"w": 600,"h": 400}}')
        local json_Res_setBounds=$(curl -# --data-binary "$json_payload_setBounds" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
        local setBounds_status=$(echo "$json_Res_setBounds" | sed -n 's/.*"success":[[:space:]]*\([^,}]*\).*/\1/p')
        sleep 1
        
        user_confirmation "$user_choice" "$query_setBounds"
        local user_confirmation_fun_exit=$?

        if [ "$setBounds_status" = "true" ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
           return 0
        else
            if [ "$setBounds_status" != "true" ]; then
                #232 error code return specific for opacity value setting error
                return 232
            else
                printf "\n\nUnable to verify setBounds bahaviour of WebkitBrowser from TV screen\n\n\n"
                return $user_confirmation_fun_exit
            fi       
        fi
    fi        

}




#Function defnition for testcase TC_RDKSHELL_MANUAL_06 



TC_RDKSHELL_MANUAL_06() {

    local step_num="$1"
    local wktBrw_Default_URL="$2"
    local user_choice="user_choice"
    local query_addAnimation=$(printf "\n\nIs WebKitBrowser Animation behaviour working as expected and is Visible on TV [yes/no]: ")
    if [ "$step_num" = "1" ]; then
        rdkshell_wktBrw_defURL_launch "$step_num" "$wktBrw_Default_URL"
        local rdkshell_wktBrw_defURL_launch_exit=$?

        if [ "$rdkshell_wktBrw_defURL_launch_exit" -eq 0 ]; then
            return 0
        else
            return $rdkshell_wktBrw_defURL_launch_exit
        fi
    elif [ "$step_num" = "3" ]; then
        wktInstance_deactivate_step "$step_num" "WebKitBrowser"  
        local wktInstance_deactivate_step_exit=$?

        if [ "$wktInstance_deactivate_step_exit" -eq 0 ]; then
            return 0
        else
            return $wktInstance_deactivate_step_exit
        fi
    else
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to verify addAnimation behavior in WebKitBrowser via RDKShell\n\n\n" "$step_num" 
        local curl_to_addAnimation="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"org.rdk.RDKShell.1.addAnimation\", \"params\":{\"animations\": [{ \"client\": \"ResidentApp\", \"x\":0, \"y\":0, \"w\":1920, \"h\":1080, \"duration\":\"10\"}, {\"client\": \"WebKitBrowser\",\"x\":0, \"y\":0, \"w\":20,\"h\":30, \"sx\":0.5, \"sy\":0.5, \"duration\":\"10\" }]}}' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_addAnimation\n\n\n"   
        sleep 1    
        local json_payload_addAnimation=$(printf '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.addAnimation", "params":{"animations": [{ "client": "ResidentApp", "x":0, "y":0, "w":1920, "h":1080, "duration":"10"}, {"client": "WebKitBrowser","x":0, "y":0, "w":20,"h":30, "sx":0.5, "sy":0.5, "duration":"10" }]}}')
        local json_Res_addAnimation=$(curl -# --data-binary "$json_payload_addAnimation" -H "Content-Type: application/json" http://127.0.0.1:9998/jsonrpc)
        local addAnimation_status=$(echo "$json_Res_addAnimation" | sed -n 's/.*"success":[[:space:]]*\([^,}]*\).*/\1/p')
        sleep 1
        
        user_confirmation "$user_choice" "$query_addAnimation"
        local user_confirmation_fun_exit=$?

        if [ "$addAnimation_status" = "true" ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
           return 0
        else
            if [ "$setBounds_status" != "true" ]; then
                #236 error code return specific for opacity value setting error
                return 236
            else
                printf "\n\nUnable to verify Animation behaviour of WebkitBrowser from TV screen\n\n\n"
                return $user_confirmation_fun_exit
            fi       
        fi
    fi        

}




#Function defnition for rdkshell_setScreenResolution sub function to setscreen Resolution 



sub_fun_setScreenResolution() {

    local width="$1"
    local height="$2"
    local user_choice="user_choice"
    local query_setScreenResolution=$(printf "\n\nIs setScreenResolution behaviour in org.rdk.RDKShell plugin working as expected and reflected the same on TV [yes/no]: ")
    rdkshell_setScreenResolution "$width" "$height"
    local rdkshell_setScreenResolution_exit=$?

    user_confirmation "$user_choice" "$query_setScreenResolution"
    local user_confirmation_fun_exit=$? 

    if [ "$rdkshell_setScreenResolution_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
        sleep 1
        rdkshell_getScreenResolution
        local rdkshell_getScreenResolution_exit=$?

        if [ "$rdkshell_getScreenResolution_exit" -eq 0 ] && [ "$getScreenRes_width" -eq "$width" ] && [ "$getScreenRes_height" -eq "$height" ]; then
            return 0
        else
            printf "\n\nCurrent ScreenResolution width after Setting ScreenResolution : %s\n\nCurrent ScreenResolution height after Setting ScreenResolution : %s\n\n\n" "$getScreenRes_width" "$getScreenRes_height"
            printf "\nDEBUG : ScreenResolution set after setscreenResolution is not reflected while getScreenResolution\n\n\n"
            return 1
        fi    
    else
        return $rdkshell_setScreenResolution_exit
    fi

}




#Function defnition for testcase TC_RDKSHELL_MANUAL_07 



TC_RDKSHELL_MANUAL_07() {

    local step_num="$1"
    local wktBrw_Default_URL="$2"
    if [ "$step_num" = "1" ]; then
        rdkshell_wktBrw_defURL_launch "$step_num" "$wktBrw_Default_URL"
        local rdkshell_wktBrw_defURL_launch_exit=$?

        if [ "$rdkshell_wktBrw_defURL_launch_exit" -eq 0 ]; then
            return 0
        else
            return $rdkshell_wktBrw_defURL_launch_exit
        fi
    elif [ "$step_num" = "4" ]; then
        wktInstance_deactivate_step "$step_num" "WebKitBrowser"  
        local wktInstance_deactivate_step_exit=$?

        if [ "$wktInstance_deactivate_step_exit" -eq 0 ]; then
            return 0
        else
            return $wktInstance_deactivate_step_exit
        fi
    elif [ "$step_num" = "2" ]; then
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to Get the current screen resolution in box via RDKShell\n\n\n" "$step_num" 
        local curl_to_getScreenResolution="curl --data-binary '{\"jsonrpc\": \"2.0\", \"id\": 2, \"method\": \"org.rdk.RDKShell.1.getScreenResolution\"}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_getScreenResolution\n\n\n"   
        sleep 1
        rdkshell_getScreenResolution
        local rdkshell_getScreenResolution_exit=$?   
        
        if [ "$rdkshell_getScreenResolution_exit" -eq 0 ]; then
            original_width="$getScreenRes_width"
            original_height="$getScreenRes_height"
            return 0
        else
            return $rdkshell_getScreenResolution_exit
        fi
    elif [ "$step_num" = "3" ]; then 
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to Set the screen resolution in box via RDKShell\n\n\n" "$step_num" 
        local curl_to_setScreenResolution="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"org.rdk.RDKShell.1.setScreenResolution\", \"params\":{ \"w\": <width>, \"h\": <height> }}' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_setScreenResolution\n\n\n"   
        sleep 1 
        if [ "$getScreenRes_width" -eq 720 ] && [ "$getScreenRes_height" -eq 480 ]; then  
            sub_fun_setScreenResolution "1280" "720"
            local sub_fun_setScreenResolution_exit=$?

            if [ "$sub_fun_setScreenResolution_exit" -eq 0 ]; then
                return 0
            else
                return $sub_fun_setScreenResolution_exit
            fi
        else
            sub_fun_setScreenResolution "720" "480"
            local sub_fun_setScreenResolution_exit=$? 

            if [ "$sub_fun_setScreenResolution_exit" -eq 0 ]; then
                return 0
            else
                return $sub_fun_setScreenResolution_exit
            fi
        fi          
    elif [ "$step_num" = "5" ]; then    
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to launch and Set the focus to ResidentApp in box via RDKShell\n\n\n" "$step_num" 
        local curl_to_setFocus="curl --data-binary '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"org.rdk.RDKShell.1.setFocus\", \"params\":{ \"client\": \"ResidentApp\" }}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_setFocus\n\n\n"   
        sleep 1       
        rdkshell_launch_operation "ResidentApp"
        local rdkshell_launch_fun_exit=$?

        if [ "$rdkshell_launch_fun_exit" -eq 0 ]; then
            printf "\n\nResidentApp launched and RDK UI loaded on TV\n\n\n"
            return 0
        else
            printf "\n\nFailed to launch ResidentApp and load RDK UI on TV\n\n\n"
            return 1
        fi
    else
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute curl command to Set the screen resolution to previous Value via RDKShell\n\n\n" "$step_num" 
        local curl_to_setScreenResolution="curl --header \"Content-Type: application/json\" --request POST --data '{\"jsonrpc\":\"2.0\", \"id\":3, \"method\":\"org.rdk.RDKShell.1.setScreenResolution\", \"params\":{ \"w\": <width>, \"h\": <height> }}' http://127.0.0.1:9998/jsonrpc"
        printf "\n$curl_to_setScreenResolution\n\n\n"   
        sleep 1
        sub_fun_setScreenResolution "$original_width" "$original_height"
        local sub_fun_setScreenResolution_exit=$?

        if [ "$sub_fun_setScreenResolution_exit" -eq 0 ]; then
            return 0
        else
            return $sub_fun_setScreenResolution_exit
        fi
    fi 

}




#Function Definition for TestCase : tc_RDKSHELL_MANUAL_testsuite



tc_RDKSHELL_MANUAL_testsuite() {

  local TestcaseID="$2"
  local testcase_prefix="$1"
  test_step_status="PASS"

  #Precondition Check code block

  printf "\n"
  printf "Pre-Conditon check\t\t: Suspending ResidentApp and Deactivating Active Instance of WebkitBrowser and HtmlApp\n\n\n"
  preCon_RDKshell
  local preCon_RDKshell_fun_exit=$?
  
  if [ "$preCon_RDKshell_fun_exit" -eq 0 ]; then
    printf '\n\nPre-condition check success. Starting Testcase execution!\n\n\n'
       

#Step 1 code block for TC_RDKSHELL_MANUAL_01 


    if [[ "$TestcaseID" == "TC_RDKSHELL_MANUAL_01" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_RDKSHELL_MANUAL_01"
      sleep 1


#Step 2 code block for TC_RDKSHELL_MANUAL_01         


      execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_RDKSHELL_MANUAL_01"
      sleep 1
      

#Step 3 code block for TC_RDKSHELL_MANUAL_01         


      execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_RDKSHELL_MANUAL_01"
      sleep 1
      

#Step 4 code block for TC_RDKSHELL_MANUAL_01         


      execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_RDKSHELL_MANUAL_01"
      sleep 1


#Step 5 code block for TC_RDKSHELL_MANUAL_01         


      execute_stepStatusUpdate_steps "5" "$testcase_prefix" "TC_RDKSHELL_MANUAL_01"
      sleep 1
      

#Step 6 code block for TC_RDKSHELL_MANUAL_01         


      execute_stepStatusUpdate_steps "6" "$testcase_prefix" "TC_RDKSHELL_MANUAL_01" 
      sleep 1      
      dynamic_current_step_finder "$testcase_prefix" "TC_RDKSHELL_MANUAL" 
    fi 
      

#Step 1 code block for TC_RDKSHELL_MANUAL_02 


    if [[ "$TestcaseID" == "TC_RDKSHELL_MANUAL_02" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_RDKSHELL_MANUAL_02"
      sleep 1


#Step 2 code block for TC_RDKSHELL_MANUAL_02  

     
      execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_RDKSHELL_MANUAL_02"
      sleep 1
      

#Step 3 code block for TC_RDKSHELL_MANUAL_02 


      execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_RDKSHELL_MANUAL_02"
      sleep 1


#Step 4 code block for TC_RDKSHELL_MANUAL_02 

     
      execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_RDKSHELL_MANUAL_02"
      sleep 1
      dynamic_current_step_finder "$testcase_prefix" "TC_RDKSHELL_MANUAL" 
    fi


#Step 1 code block for TC_RDKSHELL_MANUAL_03 


    if [[ "$TestcaseID" == "TC_RDKSHELL_MANUAL_03" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_RDKSHELL_MANUAL_03"
      sleep 1


#Step 2 code block for TC_RDKSHELL_MANUAL_03  

     
      execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_RDKSHELL_MANUAL_03"
      sleep 1
      

#Step 3 code block for TC_RDKSHELL_MANUAL_03 


      execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_RDKSHELL_MANUAL_03"
      sleep 1


#Step 4 code block for TC_RDKSHELL_MANUAL_03 

     
      execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_RDKSHELL_MANUAL_03"
      sleep 1
      

#Step 5 code block for TC_RDKSHELL_MANUAL_03 

     
      execute_stepStatusUpdate_steps "5" "$testcase_prefix" "TC_RDKSHELL_MANUAL_03"
      sleep 1
      dynamic_current_step_finder "$testcase_prefix" "TC_RDKSHELL_MANUAL" 
    fi
     

#Step 1 code block for TC_RDKSHELL_MANUAL_04 


    if [[ "$TestcaseID" == "TC_RDKSHELL_MANUAL_04" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_RDKSHELL_MANUAL_04"
      sleep 1


#Step 2 code block for TC_RDKSHELL_MANUAL_04  

     
      execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_RDKSHELL_MANUAL_04"
      sleep 1
      

#Step 3 code block for TC_RDKSHELL_MANUAL_04 


      execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_RDKSHELL_MANUAL_04"
      sleep 1
      dynamic_current_step_finder "$testcase_prefix" "TC_RDKSHELL_MANUAL" 
    fi
    

#Step 1 code block for TC_RDKSHELL_MANUAL_05 


    if [[ "$TestcaseID" == "TC_RDKSHELL_MANUAL_05" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_RDKSHELL_MANUAL_05"
      sleep 1


#Step 2 code block for TC_RDKSHELL_MANUAL_05  

     
      execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_RDKSHELL_MANUAL_05"
      sleep 1
      

#Step 3 code block for TC_RDKSHELL_MANUAL_05


      execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_RDKSHELL_MANUAL_05"
      sleep 1
      dynamic_current_step_finder "$testcase_prefix" "TC_RDKSHELL_MANUAL" 
    fi
  

#Step 1 code block for TC_RDKSHELL_MANUAL_06 


    if [[ "$TestcaseID" == "TC_RDKSHELL_MANUAL_06" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_RDKSHELL_MANUAL_06"
      sleep 1


#Step 2 code block for TC_RDKSHELL_MANUAL_06  

     
      execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_RDKSHELL_MANUAL_06"
      sleep 1
      

#Step 3 code block for TC_RDKSHELL_MANUAL_06


      execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_RDKSHELL_MANUAL_06"
      sleep 1
      dynamic_current_step_finder "$testcase_prefix" "TC_RDKSHELL_MANUAL" 
    fi
 

#Step 1 code block for TC_RDKSHELL_MANUAL_07 


    if [[ "$TestcaseID" == "TC_RDKSHELL_MANUAL_07" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_RDKSHELL_MANUAL_07"
      sleep 1


#Step 2 code block for TC_RDKSHELL_MANUAL_07  

     
      execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_RDKSHELL_MANUAL_07"
      sleep 1
      

#Step 3 code block for TC_RDKSHELL_MANUAL_07


      execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_RDKSHELL_MANUAL_07"
      sleep 1
     

#Step 4 code block for TC_RDKSHELL_MANUAL_07


      execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_RDKSHELL_MANUAL_07"
      sleep 1
     

#Step 5 code block for TC_RDKSHELL_MANUAL_07


      execute_stepStatusUpdate_steps "5" "$testcase_prefix" "TC_RDKSHELL_MANUAL_07"
      sleep 1
     

#Step 6 code block for TC_RDKSHELL_MANUAL_07


      execute_stepStatusUpdate_steps "6" "$testcase_prefix" "TC_RDKSHELL_MANUAL_07"
      sleep 1                  
      dynamic_current_step_finder "$testcase_prefix" "TC_RDKSHELL_MANUAL" 
    fi    

    #TestCase execution Result dynamic updating Function     
    dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}" 


    #Postcondition code block    
    printf '\nExecuting Post-condition Steps for Testcase : %s\n\n\n' "$TestcaseID"
    sleep 1
    postCondition_Execution_WebKitInst "$TestcaseID" 
    local postCondition_Execution_WebKitInst_exit=$?

    if [ "$postCondition_Execution_WebKitInst_exit" -eq 0 ]; then
        printf '\nPost-condition Execution Success. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
    else
        printf '\nPost-condition Execution failed. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
    fi

  else
    printf '\n\nPre-condition check failure. Exiting RDKSHELL Automated Test!\n\n\n' 
  fi

} 




#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





while true; do
  printf "\n"
  printf "\n=============================================================================================================================================================\n\n";
  printf "                                                      ******* RDKSHELL Automated Test *******                                                                    ";
  printf "\n=============================================================================================================================================================\n\n\n";
  printf '01. Run TestCase : TC_RDKSHELL_MANUAL_01        :\t[ Verify the HTML preset Url launch via WebkitBrowser with RDKShell ] \n\n'
  printf '02. Run TestCase : TC_RDKSHELL_MANUAL_02        :\t[ Verify HtmlApp launch with RDKShell and Load Url multiple times ] \n\n'
  printf '03. Run TestCase : TC_RDKSHELL_MANUAL_03        :\t[ Verify the Opacity behavior in WebKitBrowser ] \n\n'
  printf '04. Run TestCase : TC_RDKSHELL_MANUAL_04        :\t[ Verify the Scale behavior in WebKitBrowser ] \n\n'
  printf '05. Run TestCase : TC_RDKSHELL_MANUAL_05        :\t[ Verify the Bounds behavior in WebKitBrowser ] \n\n'
  printf '06. Run TestCase : TC_RDKSHELL_MANUAL_06        :\t[ Verify the Animation behavior in WebKitBrowser ] \n\n'
  printf '07. Run TestCase : TC_RDKSHELL_MANUAL_07        :\t[ Verify the setScreenResolution behaviour in RDKShell plugin using curl command ] \n\n'
  printf '08. Show TestCase Execution Results\n\n'
  printf '09. Exit [ RDKSHELL Automated Test ]\n\n'
  printf "\n=============================================================================================================================================================\n\n\n";


  # ----- Main Testcaes Execution Menu -----

  
  read -p "Enter an Option to proceed : " menu_choice
  printf '\n\n\n'
  case "$menu_choice" in 
    1)
        exec_start "TC_RDKSHELL_MANUAL_01"
        tc_RDKSHELL_MANUAL_testsuite "tc1_step" "TC_RDKSHELL_MANUAL_01"
        ;;
    2)
        exec_start "TC_RDKSHELL_MANUAL_02"
        tc_RDKSHELL_MANUAL_testsuite "tc2_step" "TC_RDKSHELL_MANUAL_02"
        ;;
    3)
        exec_start "TC_RDKSHELL_MANUAL_03"
        tc_RDKSHELL_MANUAL_testsuite "tc3_step" "TC_RDKSHELL_MANUAL_03"
        ;;
    4)
        exec_start "TC_RDKSHELL_MANUAL_04"
        tc_RDKSHELL_MANUAL_testsuite "tc4_step" "TC_RDKSHELL_MANUAL_04"
        ;;
    5)
        exec_start "TC_RDKSHELL_MANUAL_05"
        tc_RDKSHELL_MANUAL_testsuite "tc5_step" "TC_RDKSHELL_MANUAL_05"
        ;;
    6)
        exec_start "TC_RDKSHELL_MANUAL_06"
        tc_RDKSHELL_MANUAL_testsuite "tc6_step" "TC_RDKSHELL_MANUAL_06"
        ;; 
    7)
        exec_start "TC_RDKSHELL_MANUAL_07"
        tc_RDKSHELL_MANUAL_testsuite "tc7_step" "TC_RDKSHELL_MANUAL_07"
        ;;                                 
    8)
        testcase_result_display_menu "TC_RDKSHELL_MANUAL"  
        ;;       
    9)   
        printf '\nExited RDKSHELL Automated Test\n\n\n' 
        break
        ;; 
    *)
        printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
        ;;      
  esac
done


