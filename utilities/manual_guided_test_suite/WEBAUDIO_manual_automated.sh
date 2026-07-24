#!/bin/bash


source device.conf
source generic_functions.sh


#Author : aharil144@cable.comcast.com
#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





#Function to check the Pre-Condition before executing TC_WEBAUDIO_MANUAL TestSuite



preCon_Webaudio() {

  #webaudio_app_bundle , app_download_server , installed_app_ver these values are passed as parameter to function from device.conf file
  any_app_installer "Webaudio_manual" "$webaudio_app_bundle" "$app_download_server" "$installed_app_ver"
  local any_app_installer_exit=$?
  #installed_appID is the global variable which have appID value after any_app_installer function execution
  active_anyApp_instance_kill "Webaudio_manual" "$installed_appID"
  local active_anyApp_instance_kill_exit=$?

  if [ "$any_app_installer_exit" -eq 0 ] && [ "$active_anyApp_instance_kill_exit" -eq 0 ]; then
    return 0
  else
    return 1
  fi    

}




#Function definition for webaudio_step_des_selector to select step discription of each webAudio testcases 



webaudio_step_des_selector() {

    local test_ID="$1"
    local step_num="$2"
    local app_name="$3"
    case "$test_ID" in
        "tc1_step"|"tc2_step")
            if [ "$step_num" == "2" ]; then
                printf "\nStep %s\t\t: Select Testcase and navigate to click on [speak] button to speak text in textbox as audio\n\n\n" "$step_num"
            elif [ "$step_num" == "3" ]; then
                query_webaudio=$(printf "\n\nIs texts speaking audio heared when [speak] button is pressed on %s App [yes/no]: " "$app_name" )
                printf "\nStep %s\t\t: Verify whether text speak Audio is heared when [speak] button is pressed\n\n\n" "$step_num"
            else
                printf "\n\nDEBUG : Step description not avaialble for step - %s\n\n" "$step_num"   
            fi         
            ;;
        "tc3_step")
            if [ "$step_num" == "2" ]; then 
                printf "\nStep %s\t\t: Select Testcase and navigate to click on [speak with Random Voices] button to speak text in textbox with random languages audio\n\n\n" "$step_num"
            elif [ "$step_num" == "3" ]; then
                query_webaudio=$(printf "\n\nIs texts speaking with random voices audio heared when [speak with Random Voices] button is pressed on %s App [yes/no]: " "$app_name" )
                printf "\nStep %s\t\t: Verify whether text speak with random voices Audio is heared when [speak with Random Voices] button is pressed\n\n\n" "$step_num"
            else
                printf "\n\nDEBUG : Step description not avaialble for step - %s\n\n" "$step_num"   
            fi         
            ;;
        "tc9_step"|"tc10_step"|"tc11_step"|"tc12_step"|"tc13_step"|"tc14_step"|"tc15_step")
            if [ "$step_num" == "2" ]; then
                query_webaudio_html_launch=$(printf "\n\nIs Audio decoded information of codecs loaded on a html page of  %s App [yes/no]: " "$app_name" )
                printf "\nStep %s\t\t: Select Testcase and check whether Audio decoded information of codecs displayed on a html page\n\n\n" "$step_num"
            else
                printf "\n\nDEBUG : Step description not avaialble for step - %s\n\n" "$step_num"   
            fi      
            ;;
        "tc4_step")
            if [ "$step_num" == "2" ]; then
                query_webaudio_html_launch=$(printf "\n\nIs Audio context text message loaded on a html page of %s App [yes/no]: " "$app_name" )
                printf "\nStep %s\t\t: Select Testcase and check whether Audio context text message loaded on html page\n\n\n" "$step_num"
            else
                printf "\n\nDEBUG : Step description not avaialble for step - %s\n\n" "$step_num"   
            fi
            ;; 
        "tc5_step")   
            if [ "$step_num" == "2" ]; then
                query_webaudio_html_launch=$(printf "\n\nIs the text message 'This test passes if it does not crash' displayed on a html page of %s App [yes/no]: " "$app_name" )
                printf "\nStep %s\t\t: Select Testcase and check whether Audiocontext_creation_destruction message loaded on a html page\n\n\n" "$step_num"
            else
                printf "\n\nDEBUG : Step description not avaialble for step - %s\n\n" "$step_num"   
            fi
            ;;
        "tc6_step")
            if [ "$step_num" == "2" ]; then 
                printf "\nStep %s\t\t: Select Testcase and navigate to click on play button to start audio playback\n\n\n" "$step_num"
            elif [ "$step_num" == "3" ]; then
                query_webaudio=$(printf "\n\nIs an (alarm sound) Audio heared when play button is pressed on %s App [yes/no]: " "$app_name" )
                printf "\nStep %s\t\t: Verify proper Audio heared when play button is pressed\n\n\n" "$step_num"
            else
                printf "\n\nDEBUG : Step description not avaialble for step - %s\n\n" "$step_num"   
            fi         
            ;;
        "tc7_step")
            if [ "$step_num" == "2" ]; then 
                printf "\nStep %s\t\t: Select Testcase and navigate to click on [start synthesis] button\n\n\n" "$step_num"
            elif [ "$step_num" == "3" ]; then
                query_webaudio=$(printf "\n\nIs an (Buzzor/warning sound) Audio heared when [start synthesis] button is pressed on %s App [yes/no]: " "$app_name" )
                printf "\nStep %s\t\t: Verify proper Audio heared when [start synthesis] button is pressed\n\n\n" "$step_num"
            else
                printf "\n\nDEBUG : Step description not avaialble for step - %s\n\n" "$step_num"   
            fi         
            ;;
        "tc8_step")
            if [ "$step_num" == "2" ]; then 
                printf "\nStep %s\t\t: Select Testcase and navigate to click on [start Video] [Play audio] [Start speech synthesis] buttons to start Multi Media Playback\n\n\n" "$step_num"
            elif [ "$step_num" == "3" ]; then
                query_webaudio=$(printf "\n\nIs Multimedia playback started when corresponding buttons are pressed on %s App [yes/no]: " "$app_name" )
                printf "\nStep %s\t\t: Verify proper Multimedia playback heppens when [start Video] [Play audio] [Start speech synthesis] buttons are pressed\n\n\n" "$step_num"
            else
                printf "\n\nDEBUG : Step description not avaialble for step - %s\n\n" "$step_num"   
            fi         
            ;;
        *)
            printf "\n\n\nDEBUG : Invalid TestCase ID -> %s\n\n" "$test_ID"  
    esac                

}



#Function to check the WebAudio testcases in tc_WEBAUDIO_MANUAL TestSuite



TC_WEBAUDIO_MANUAL_test() {

  local step_num="$1"
  local app_name="$2"
  local testcase_id="$3" 
  printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"

  case "$testcase_id" in
    "tc1_step"|"tc2_step"|"tc3_step"|"tc6_step"|"tc7_step"|"tc8_step")
        case "$step_num" in 
            "1")
                printf "\nStep %s\t\t: Launch %s App via AppManager.1.launchApp API\n\n\n" "$step_num" "$app_name"
                anyApp_launch "$installed_appID" "$app_name"
                local anyApp_launch_exit=$?

                if [ "$anyApp_launch_exit" -eq 0 ]; then
                    return 0
                else
                    return 1
                fi
                ;;
            "2")
                webaudio_step_des_selector "$testcase_id" "$step_num" "$app_name" 
                dynamic_inApp_loader "$installed_appID" "$testcase_id" "$app_name"
                local dynamic_inApp_loader_exit=$?

                if [ "$dynamic_inApp_loader_exit" -eq 0 ]; then
                    return 0
                else
                    return 1
                fi
                ;;
            "3")
                local user_choice_webaudio="user_choice_webaudio"
                webaudio_step_des_selector "$testcase_id" "$step_num" "$app_name"
                user_confirmation "$user_choice_webaudio" "$query_webaudio"
                local user_confirmation_fun_exit=$?

                if [ "$user_confirmation_fun_exit" -eq 0 ]; then
                    return 0
                else
                    return 1
                fi
                ;;
            "4")    
                printf "\nStep %s\t\t: Close the %s App Using Home key press or AppManager.terminateApp API\n\n\n" "$step_num" "$app_name"     
                terminate_app "$app_name" "$installed_appID"
                local terminate_app_exit=$?

                if [ "$terminate_app_exit" -eq 0 ]; then
                    return 0
                else
                    return 1
                fi
                ;;
            *)
                printf "\n\n\nInvalid Step number for testcase_ID : %s\n\n" "$testcase_id"
                return 1
                ;;
        esac
        ;;
    "tc4_step"|"tc5_step"|"tc9_step"|"tc10_step"|"tc11_step"|"tc12_step"|"tc13_step"|"tc14_step"|"tc15_step") 
        case "$step_num" in 
            "1")
                printf "\nStep %s\t\t: Launch %s App via AppManager.1.launchApp API\n\n\n" "$step_num" "$app_name"
                anyApp_launch "$installed_appID" "$app_name"
                local anyApp_launch_exit=$?

                if [ "$anyApp_launch_exit" -eq 0 ]; then
                    return 0
                else
                    return 1
                fi
                ;;
            "2")
                local user_choice_webaudio_test="user_choice_webaudio_test"
                webaudio_step_des_selector "$testcase_id" "$step_num" "$app_name"
                dynamic_inApp_loader "$installed_appID" "$testcase_id" "$app_name"
                local dynamic_inApp_loader_exit=$?

                user_confirmation "$user_choice_webaudio_test" "$query_webaudio_html_launch"
                local user_confirmation_fun_exit_1=$?

                if [ "$dynamic_inApp_loader_exit" -eq 0 ] && [ "$user_confirmation_fun_exit_1" -eq 0 ]; then
                    return 0
                else
                    return 1
                fi
                ;;
            "3")    
                printf "\nStep %s\t\t: Close the %s App Using Home key press or AppManager.terminateApp API\n\n\n" "$step_num" "$app_name"     
                terminate_app "$app_name" "$installed_appID"
                local terminate_app_exit=$?

                if [ "$terminate_app_exit" -eq 0 ]; then
                    return 0
                else
                    return 1
                fi
                ;;
            *)
                printf "\n\n\nInvalid Step number for testcase_ID : %s\n\n" "$testcase_id"
                return 1
                ;;
        esac
        ;;    
    *)
        printf "\n\n\nInvalid testcase_ID : %s for Webaudio test\n\n" "$testcase_id"
        return 1
        ;; 
  esac             

}



#Function definition for webaudio_inner_step_execute_1 for steps execute in inner functions



webaudio_inner_step_execute_1() {

   local test_prefix="$1"
   local webaudio_test_fun="$2"
   local app_name="$3"
   local testCase_name="$4"

   #Step 1 code block for TC_WEBAUDIO_MANUAL_test_1,2,3 SPEACH_SYNTHESIS_1,2,3,6,7,8

   execute_stepStatusUpdate_steps "1" "$test_prefix" "$webaudio_test_fun" "$app_name"
   sleep 1

   #Step 2 code block for TC_WEBAUDIO_MANUAL_test_1,2,3 SPEACH_SYNTHESIS_1,2,3,6,7,8

   execute_stepStatusUpdate_steps "2" "$test_prefix" "$webaudio_test_fun" "$app_name"
   sleep 1

   #Step 3 code block for TC_WEBAUDIO_MANUAL_test_1,2,3 SPEACH_SYNTHESIS_1,2,3,6,7,8

   execute_stepStatusUpdate_steps "3" "$test_prefix" "$webaudio_test_fun" "$app_name"
   sleep 1

   #Step 4 code block for TC_WEBAUDIO_MANUAL_test_1,2,3 SPEACH_SYNTHESIS_1,2,3,6,7,8

   execute_stepStatusUpdate_steps "4" "$test_prefix" "$webaudio_test_fun" "$app_name"
   sleep 1
   dynamic_current_step_finder "$test_prefix" "$testCase_name"

}



#Function definition for webaudio_inner_step_execute_2 for steps execute in inner functions



webaudio_inner_step_execute_2() {

   local test_prefix="$1"
   local webaudio_test_fun="$2"
   local app_name="$3"
   local testCase_name="$4"

   #Step 1 code block for TC_WEBAUDIO_MANUAL_test_4,5,9,10,11,12,13,14,15

   execute_stepStatusUpdate_steps "1" "$test_prefix" "$webaudio_test_fun" "$app_name"
   sleep 1

   #Step 2 code block for TC_WEBAUDIO_MANUAL_test_4,5,9,10,11,12,13,14,15

   execute_stepStatusUpdate_steps "2" "$test_prefix" "$webaudio_test_fun" "$app_name"
   sleep 1

   #Step 3 code block for TC_WEBAUDIO_MANUAL_test_4,5,9,10,11,12,13,14,15 

   execute_stepStatusUpdate_steps "3" "$test_prefix" "$webaudio_test_fun" "$app_name"
   sleep 1
   dynamic_current_step_finder "$test_prefix" "$testCase_name"

}



#Function Definition for TestCase : tc_WEBAUDIO_MANUAL_testsuite



tc_WEBAUDIO_MANUAL_testsuite() {

  local TestcaseID="$2"
  local testcase_prefix="$1"
  test_step_status="PASS"

  #Precondition Check code block

  printf "\n\nPre-Conditon check\t\t: Check whether WebAudio App installeded or not. If not install the App\n\n\n"
  preCon_Webaudio
  local preCon_Webaudio_exit=$?
  
  if [ "$preCon_Webaudio_exit" -eq 0 ]; then
    printf '\n\nPre-condition check success. Starting Testcase execution!\n\n\n'    

    case "$TestcaseID" in
        "TC_WEBAUDIO_MANUAL_01"|"TC_WEBAUDIO_MANUAL_02"|"TC_WEBAUDIO_MANUAL_03"|"TC_WEBAUDIO_MANUAL_06"|"TC_WEBAUDIO_MANUAL_07"|"TC_WEBAUDIO_MANUAL_08")
            webaudio_inner_step_execute_1 "$testcase_prefix" "TC_WEBAUDIO_MANUAL_test" "webaudio_manual" "TC_WEBAUDIO_MANUAL"
            ;;
        "TC_WEBAUDIO_MANUAL_04"|"TC_WEBAUDIO_MANUAL_05"|"TC_WEBAUDIO_MANUAL_09"|"TC_WEBAUDIO_MANUAL_10"|"TC_WEBAUDIO_MANUAL_11"|"TC_WEBAUDIO_MANUAL_12"|"TC_WEBAUDIO_MANUAL_13"|"TC_WEBAUDIO_MANUAL_14"|"TC_WEBAUDIO_MANUAL_15")
            webaudio_inner_step_execute_2 "$testcase_prefix" "TC_WEBAUDIO_MANUAL_test" "webaudio_manual" "TC_WEBAUDIO_MANUAL"
            ;;
    esac
    
    #TestCase execution Result dynamic updating Function     
    dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}" 

    #Log generation and upload to server function
    log_generate_operations "$failed_step_num" "webaudio"

    #Postcondition code block    
    printf '\nExecuting Post-condition Steps for Testcase : %s\n\n\n' "$TestcaseID"
    sleep 1
    postCondition_Execution_webaudio "$TestcaseID" 
    postCondition_Execution_webaudio_exit=$?

    if [ "$postCondition_Execution_webaudio_exit" -eq 0 ]; then
        printf '\nPost-condition Execution Success. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
    else
        printf '\nPost-condition Execution failed. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
    fi
  else
    printf '\n\nPre-condition check failure. Exiting WEBAUDIO Automated Test!\n\n\n' 
  fi

}




#Function Definition for postcondition image formats postCondition_Execution_webaudio


postCondition_Execution_webaudio() {

  dynamic_appInstanceId=""
  kill_app "webaudio_manual" "$isAppInstalled_appid"  
  local kill_app_exit=$?
  if [ "$kill_app_exit" -eq 0 ]; then
    post_cond_UI_focus_set "refui"
    post_cond_UI_focus_set_exit=$?

    if [ "$post_cond_UI_focus_set_exit" -eq 0 ]; then
        return 0
    else
        return 1
    fi    
  else
    post_cond_UI_focus_set "refui"
    post_cond_UI_focus_set_exit=$?

    if [ "$post_cond_UI_focus_set_exit" -eq 0 ]; then
        return 0
    else
        return 1
    fi     
  fi    

}








#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





while true; do
  printf "\n"
  printf "\n=============================================================================================================================================================\n\n";
  printf "                                                      ******* WEBAUDIO Manual Automated Test *******                                                                    ";
  printf "\n=============================================================================================================================================================\n\n\n";
  printf '01. Run TestCase : TC_WEBAUDIO_MANUAL_01        :\t[ Verify the speech_synthesis_test_1 via Webaudio App ] \n\n'
  printf '02. Run TestCase : TC_WEBAUDIO_MANUAL_02        :\t[ Verify the speech_synthesis_test_2 (supported audio languages) via Webaudio App ] \n\n'
  printf '03. Run TestCase : TC_WEBAUDIO_MANUAL_03        :\t[ Verify the speech_synthesis_test_3 (3 different audio languages continously) via Webaudio App ] \n\n'
  printf '04. Run TestCase : TC_WEBAUDIO_MANUAL_04        :\t[ Verify the creation of an AudioContext object via Webaudio App ] \n\n'
  printf '05. Run TestCase : TC_WEBAUDIO_MANUAL_05        :\t[ Verify the creation of an Audiocontext_creation_destruction object via Webaudio App ] \n\n'
  printf '06. Run TestCase : TC_WEBAUDIO_MANUAL_06        :\t[ Verify the Audio_Playback using webaudio API via Webaudio App ] \n\n'
  printf '07. Run TestCase : TC_WEBAUDIO_MANUAL_07        :\t[ Verify the Generated_Sound_FM playback using webaudio API via Webaudio App ] \n\n'
  printf '08. Run TestCase : TC_WEBAUDIO_MANUAL_08        :\t[ Verify the Multi_media_playback via Webaudio App ] \n\n'
  printf '09. Run TestCase : TC_WEBAUDIO_MANUAL_09        :\t[ Verify the Audio decoding of aac -> vbr-128kbps-44khz via Webaudio App ] \n\n'
  printf '10. Run TestCase : TC_WEBAUDIO_MANUAL_10        :\t[ Verify the Audio decoding of mp3 -> 128kbps-44khz via Webaudio App ] \n\n'
  printf '11. Run TestCase : TC_WEBAUDIO_MANUAL_11        :\t[ Verify the Audio decoding of vorbis -> vbr-70kbps-44khz via Webaudio App ] \n\n'
  printf '12. Run TestCase : TC_WEBAUDIO_MANUAL_12        :\t[ Verify the Audio decoding of vorbis -> vbr-96kbps-44khz via Webaudio App ] \n\n'
  printf '13. Run TestCase : TC_WEBAUDIO_MANUAL_13        :\t[ Verify the Audio decoding of vorbis -> vbr-128kbps-44khz via Webaudio App ] \n\n'
  printf '14. Run TestCase : TC_WEBAUDIO_MANUAL_14        :\t[ Verify the Audio decoding of wav -> 24bit-22khz-resample via Webaudio App ] \n\n'
  printf '15. Run TestCase : TC_WEBAUDIO_MANUAL_15        :\t[ Verify the Audio decoding of wav -> 24bit-44khz via Webaudio App ] \n\n'
  printf '16. Show TestCase Execution Results\n\n'
  printf '17. Exit [ WebAudio Automated Test ]\n\n'
  printf "\n=============================================================================================================================================================\n\n\n";


  # ----- Main Testcaes Execution Menu -----

  
  read -p "Enter an Option to proceed : " menu_choice
  printf '\n\n\n'
  case "$menu_choice" in 
    1)
        exec_start "TC_WEBAUDIO_MANUAL_01"
        tc_WEBAUDIO_MANUAL_testsuite "tc1_step" "TC_WEBAUDIO_MANUAL_01"
        ;;
    2)
        exec_start "TC_WEBAUDIO_MANUAL_02"
        tc_WEBAUDIO_MANUAL_testsuite "tc2_step" "TC_WEBAUDIO_MANUAL_02"
        ;;
    3)
        exec_start "TC_WEBAUDIO_MANUAL_03"
        tc_WEBAUDIO_MANUAL_testsuite "tc3_step" "TC_WEBAUDIO_MANUAL_03"
        ;;
    4)
        exec_start "TC_WEBAUDIO_MANUAL_04"
        tc_WEBAUDIO_MANUAL_testsuite "tc4_step" "TC_WEBAUDIO_MANUAL_04"
        ;;
    5)
        exec_start "TC_WEBAUDIO_MANUAL_05"
        tc_WEBAUDIO_MANUAL_testsuite "tc5_step" "TC_WEBAUDIO_MANUAL_05"
        ;;
    6)
        exec_start "TC_WEBAUDIO_MANUAL_06"
        tc_WEBAUDIO_MANUAL_testsuite "tc6_step" "TC_WEBAUDIO_MANUAL_06"
        ;;    
    7)
        exec_start "TC_WEBAUDIO_MANUAL_07"
        tc_WEBAUDIO_MANUAL_testsuite "tc7_step" "TC_WEBAUDIO_MANUAL_07"
        ;;
    8)
        exec_start "TC_WEBAUDIO_MANUAL_08"
        tc_WEBAUDIO_MANUAL_testsuite "tc8_step" "TC_WEBAUDIO_MANUAL_08"
        ;;        
    9)
        exec_start "TC_WEBAUDIO_MANUAL_09"
        tc_WEBAUDIO_MANUAL_testsuite "tc9_step" "TC_WEBAUDIO_MANUAL_09"
        ;;
    10)
        exec_start "TC_WEBAUDIO_MANUAL_10"
        tc_WEBAUDIO_MANUAL_testsuite "tc10_step" "TC_WEBAUDIO_MANUAL_10"
        ;; 
    11)
        exec_start "TC_WEBAUDIO_MANUAL_11"
        tc_WEBAUDIO_MANUAL_testsuite "tc11_step" "TC_WEBAUDIO_MANUAL_11"
        ;;   
    12)
        exec_start "TC_WEBAUDIO_MANUAL_12"
        tc_WEBAUDIO_MANUAL_testsuite "tc12_step" "TC_WEBAUDIO_MANUAL_12"
        ;;
    13)
        exec_start "TC_WEBAUDIO_MANUAL_13"
        tc_WEBAUDIO_MANUAL_testsuite "tc13_step" "TC_WEBAUDIO_MANUAL_13"
        ;; 
    14)
        exec_start "TC_WEBAUDIO_MANUAL_14"
        tc_WEBAUDIO_MANUAL_testsuite "tc14_step" "TC_WEBAUDIO_MANUAL_14"
        ;; 
    15)
        exec_start "TC_WEBAUDIO_MANUAL_15"
        tc_WEBAUDIO_MANUAL_testsuite "tc15_step" "TC_WEBAUDIO_MANUAL_15"
        ;;                  
    16)
        testcase_result_display_menu "TC_WEBAUDIO_MANUAL"  
        ;;       
    17)   
        printf '\nExited WEBAUDIO Automated Test\n\n\n' 
        break
        ;; 
    *)
        printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
        ;;      
  esac
done  





#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
