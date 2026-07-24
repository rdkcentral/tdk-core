#!/bin/bash


source device.conf
source generic_functions.sh

#Author : aharil144@cable.comcast.com
#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________






#Function Definition to check the Pre-Condition before executing TC_SYSTEM_MANUAL TestSuite



preCon_SYSTEM() {

    local testcaseID="$1"
    if [[ "$testcaseID" == "TC_SYSTEM_MANUAL_01" ]]; then
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nPre-Condition\t\t: Execute command to verify whether device have a valid IP address and network Connection\n\n\n"
        local cmd_ip_address="ip -4 addr show eth0 | awk '/inet / {split($2,a,\"/\"); print a[1]}'"
        printf "\n$cmd_ip_address\n\n\n"   
        sleep 1
        local extracted_ipv4_addr=$(ip -4 addr show eth0 | awk '/inet / {split($2,a,"/"); print a[1]}')
        if [ -z "$extracted_ipv4_addr" ]; then
            printf "\n\nEthernet is not connected to DUT. Unable to fetch IPV4 address : %s\n\n\n" "$extracted_ipv4_addr"
            return 1
        else
            printf "\n\nEthernet is Connected IPv4 address is [ %s ]\n\n\n" "$extracted_ipv4_addr" 
            return 0
        fi     
    else
        return 0
    fi    

}



#Function Definition to check the build details of the device 



build_details_check() {

    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Execute Command to check the Build version of device\n\n\n" "$step"
    printf "\n\ngrep -i \"imagename\" /version.txt | cut -d: -f2- | xargs\n\n\n" 
    sleep 1
    local build_name=$(grep -i "imagename" /version.txt | cut -d: -f2- | xargs)
    if [[ "$build_name" == *"rdk"* ]]; then
        printf "\n\nCurrent build version : %s\n\n\n" "$build_name"
        return 0
    else
        printf "\n\nUnable to detect the build information\n\n\n"
        return 1
    fi    

}
    


#Function Definition to check the ssh dropbear service status



ssh_dropbear_check() {
    
    local active_state=$(systemctl show -p ActiveState --value dropbear)
    local sub_state=$(systemctl show -p SubState --value dropbear)

    if [ "$active_state" = "active" ] && [ "$sub_state" = "running" ]; then
        printf "\n\nDropbear service is %s and substate : %s\n\n\n" "$active_state" "$sub_state"
        return 0
    else
        printf "\n\nDropbear service is %s and substate : %s\n\n\n" "$active_state" "$sub_state"
        return 1
    fi

}



#Function defnition for testcase TC_SYSTEM_MANUAL_01



TC_SYSTEM_MANUAL_01() {

    local step="$1"
    if [ "$step" = "1" ]; then
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute Command to verify SSH dropbear service\n\n\n" "$step" 
        sleep 1
        ssh_dropbear_check "$step"
        local ssh_dropbear_check_fun_exit=$?

        if [ "$ssh_dropbear_check_fun_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step" = "2" ]; then
        build_details_check "$step"
        local build_details_check_exit=$?

        if [ "$build_details_check_exit" -eq 0 ]; then
            return 0
        else
            return 1
        fi
    else
        printf "\n\nDEBUG : Invalid step number for Testcase : TC_SYSTEM_MANUAL_01\n\n\n"
        return 1
    fi        

}



#Function defnition for testcase TC_SYSTEM_MANUAL_02



TC_SYSTEM_MANUAL_02() {

    local step="$1"
    printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
    printf "\nStep %s\t\t: Execute Command to verify the running status of Wpe framework processes\n\n\n" "$step"
    printf '\n\npgrep -l '^WPE'\n\n\n'  
    sleep 1        
    if pgrep -l '^WPE' >/dev/null; then
        printf "\n\nWPE framework Processes found :\n\n\n"
        pgrep -l '^WPE'
        printf "\n\n"
        return 0
    else
        printf "\n\nUnable to detect WPE framework Processes\n\n\n"
        return 1
    fi

}



#Function defnition for testcase TC_SYSTEM_MANUAL_03



TC_SYSTEM_MANUAL_03() {

    local step="$1"
    local log_dir="/opt/logs/PreviousLogs"
    if [ "$step" = "1" ]; then
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute Command to navigate and check opt/logs/ folder\n\n\n" "$step"
        printf '\ncd /opt/logs. check PreviousLogs directory available or not\n\n\n'
        sleep 1
        cd /opt/logs/ 
        pwd
        if [ -d "/opt/logs/PreviousLogs" ]; then
            return 0
        else
            return 1
        fi
    elif [ "$step" = "2" ]; then  
        printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
        printf "\nStep %s\t\t: Execute commands to check whether .log files are available in PreviousLogs directory\n\n\n" "$step"
        printf '\n\n[ -d "/opt/logs/PreviousLogs" ] && [ "$(ls -A "/opt/logs/PreviousLogs")" ]\n\n\n\n'
        sleep 1 
        cd /opt/logs/PreviousLogs 
        if [ -d "$log_dir" ] && [ "$(ls -A "$log_dir")" ]; then
            printf "\n\n%s directory exists and not empty\n\n\n" "$log_dir"
            valid_files=$(find "$log_dir" -maxdepth 1 -name "*.log" -type f -size +0c | head -n 1)

            if [ -n "$valid_files" ]; then
                printf "\n\nPrevious log file Eg : %s found\n\n\n" "$valid_files" 
                return 0
            else
                printf "\n\nPrevious log file found on %s are empty\n\n\n" "$log_dir"
                return 1
            fi
        else
           printf "\n\n%s directory doesn't exists or it's empty\n\n\n" "$log_dir"    
           return 1
        fi
    else
        printf "\n\nDEBUG : Invalid step number for Testcase : TC_SYSTEM_MANUAL_03\n\n\n"
        return 1
    fi              

}








#Function Definition for TestCase : tc_SYSTEM_MANUAL_testsuite



tc_SYSTEM_MANUAL_testsuite() {

    local TestcaseID="$2"
    local testcase_prefix="$1"
    test_step_status="PASS"
    
    #Precondition Check code block
    
    printf "\n"
    preCon_SYSTEM "$TestcaseID" 
    local preCon_SYSTEM_fun_exit=$?
    
    if [ "$preCon_SYSTEM_fun_exit" -eq 0 ]; then
        sleep 1
        printf "\n\nPre-condition check success. Starting Testcase execution!\n\n\n"


    #Step 1 code block for TC_SYSTEM_MANUAL_01

        if [[ "$TestcaseID" == "TC_SYSTEM_MANUAL_01" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_SYSTEM_MANUAL_01"
            sleep 1
           
    #Step 2 code block for TC_SYSTEM_MANUAL_01

            execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_SYSTEM_MANUAL_01"
            sleep 1 
            dynamic_current_step_finder "$testcase_prefix" "TC_SYSTEM_MANUAL"
        fi


    #Step 1 code block for TC_SYSTEM_MANUAL_02

        if [[ "$TestcaseID" == "TC_SYSTEM_MANUAL_02" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_SYSTEM_MANUAL_02"
            sleep 1
            dynamic_current_step_finder "$testcase_prefix" "TC_SYSTEM_MANUAL"
        fi


    #Step 1 code block for TC_SYSTEM_MANUAL_03

        if [[ "$TestcaseID" == "TC_SYSTEM_MANUAL_03" ]]; then
            execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_SYSTEM_MANUAL_03"
            sleep 1
           
    #Step 2 code block for TC_SYSTEM_MANUAL_03

            execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_SYSTEM_MANUAL_03"
            sleep 1 
            dynamic_current_step_finder "$testcase_prefix" "TC_SYSTEM_MANUAL"
        fi

        #TestCase execution Result dynamic updating Function     
        dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}"
        
        printf "\n\nPost-condition: None\n\n" 
    else
        printf "\n\nPre-condition check failure. Exiting SYSTEM Automated Test!\n\n\n" 
    fi    

}





#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





while true; do

  printf "\n"
  printf "\n=============================================================================================================================================================\n\n";
  printf "                                                      ******* SYSTEM Automated Test *******                                                                    \n";
  printf "\n=============================================================================================================================================================\n\n\n";
  printf '01. Run TestCase : TC_SYSTEM_MANUAL_01        :\t[ Verify SSH dropbear service and status ] \n\n'
  printf '02. Run TestCase : TC_SYSTEM_MANUAL_02        :\t[ Verify the running status of Wpe framework processes ] \n\n'
  printf '03. Run TestCase : TC_SYSTEM_MANUAL_03        :\t[ Verify the log rollover RDK functionality ] \n\n'
  printf '04. Show TestCase Execution Results\n\n'
  printf '05. Exit [ POWER MANAGEMENT Automated Test ]\n\n'
  printf "\n=============================================================================================================================================================\n\n\n";


  # ----- Main Testcaes Execution Menu -----

  
  read -p "Enter an Option to proceed : " menu_choice
  printf '\n\n\n'
  case "$menu_choice" in 
    1)
        exec_start "TC_SYSTEM_MANUAL_01"
        tc_SYSTEM_MANUAL_testsuite "tc1_step" "TC_SYSTEM_MANUAL_01"
        ;;
    2)
        exec_start "TC_SYSTEM_MANUAL_02"
        tc_SYSTEM_MANUAL_testsuite "tc2_step" "TC_SYSTEM_MANUAL_02"
        ;;
    3)
        exec_start "TC_SYSTEM_MANUAL_03"
        tc_SYSTEM_MANUAL_testsuite "tc3_step" "TC_SYSTEM_MANUAL_03"
        ;;        
    4)              
        testcase_result_display_menu "TC_SYSTEM_MANUAL"  
        ;;       
    5)   
        printf '\nExited SYSTEM Automated Test\n\n\n' 
        break
        ;; 
    *)
        printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
        ;;      
  esac
done
