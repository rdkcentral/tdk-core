#!/bin/bash


source device.conf
source generic_functions.sh


#Author : aharil144@cable.comcast.com
#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




#Function to check the Pre-Condition before executing TC_IMAGEFORMATS_MANUAL TestSuite



preCon_IMAGEFORMATS() {

  #browser_test_app_bundle , app_download_server , installed_app_ver these values are passed as parameter to function from device.conf file
  any_app_installer "Browser_test" "$browser_test_app_bundle" "$app_download_server" "$installed_app_ver"
  local any_app_installer_exit=$?
  #installed_appID is the global variable which have appID value after any_app_installer function execution
  active_anyApp_instance_kill "Browser_test" "$installed_appID"
  local active_anyApp_instance_kill_exit=$?

  if [ "$any_app_installer_exit" -eq 0 ] && [ "$active_anyApp_instance_kill_exit" -eq 0 ]; then
    return 0
  else
    return 1
  fi    

}




#Function to check the image formats in TC_IMAGEFORMATS_MANUAL TestSuite



TC_IMAGEFORMATS_MANUAL_test() {

  local step_num="$1"
  local image_format="$2"
  local app_name="$3"
  local testcase_id="$4" 
  local user_choice_img_format="user_choice_img_format"
  local query_img_format=$(printf "\n\nIs %s image format loaded in %s App and Visible on TV [yes/no]: " "$image_format" "$app_name" )
  printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
  printf "\nStep %s\t\t: Launch %s App and load %s image fromat\n\n\n" "$step_num" "$app_name" "$image_format" 
  
  anyApp_launch "$installed_appID" "$app_name"
  local anyApp_launch_exit=$?

  if [ "$anyApp_launch_exit" -eq 0 ]; then
    dynamic_inApp_loader "$installed_appID" "$testcase_id" "$app_name"
    local dynamic_inApp_loader_exit=$?

    user_confirmation "$user_choice_img_format" "$query_img_format"
    local user_confirmation_fun_exit=$?

    if [ "$dynamic_inApp_loader_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
      printf "\n\n[ .%s ] image format loaded in %s App and visible on TV\n\n\n" "$image_format" "$app_name"
      return 0
    else
      printf "\n\n\nUnable to load [ .%s ] image format via %s App and Not visible on TV\n\n\n" "$image_format" "$app_name"
      return 1
    fi
  else
    printf "\n\n\nDEBUG : Unable to launch %s App with appID - %s\n\n" "$app_name" "$installed_appID"
    return 1
  fi  

}




#Function Definition for TestCase : tc_IMAGEFORMATS_MANUAL_testsuite



tc_IMAGEFORMATS_MANUAL_testsuite() {

  local TestcaseID="$2"
  local testcase_prefix="$1"
  test_step_status="PASS"

  #Precondition Check code block

  printf "\n\nPre-Conditon check\t\t: Check whether Browser_test App installeded or not. If not install the App\n\n\n"
  preCon_IMAGEFORMATS
  local preCon_IMAGEFORMATS_fun_exit=$?
  
  if [ "$preCon_IMAGEFORMATS_fun_exit" -eq 0 ]; then
    printf '\n\nPre-condition check success. Starting Testcase execution!\n\n\n'
    

#Step 1 code block for TC_IMAGEFORMATS_MANUAL_test 1 [ .jpg image format ]


    if [[ "$TestcaseID" == "TC_IMAGEFORMATS_MANUAL_01" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL_test" "Browser_test" "" "" "" "png"
      dynamic_current_step_finder "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL" 
    fi  


#Step 1 code block for TC_IMAGEFORMATS_MANUAL_test 2 [ .png image format ]    


    if [[ "$TestcaseID" == "TC_IMAGEFORMATS_MANUAL_02" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL_test" "Browser_test" "" "" "" "jpg"
      dynamic_current_step_finder "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL" 
    fi
     
   
#Step 1 code block for TC_IMAGEFORMATS_MANUAL_test 3 [ .svg image format ]


    if [[ "$TestcaseID" == "TC_IMAGEFORMATS_MANUAL_03" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL_test" "Browser_test" "" "" "" "svg"
      dynamic_current_step_finder "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL" 
    fi  


#Step 1 code block for TC_IMAGEFORMATS_MANUAL_test 4 [ .webp image format ]    


    if [[ "$TestcaseID" == "TC_IMAGEFORMATS_MANUAL_04" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL_test" "Browser_test" "" "" "" "webp"
      dynamic_current_step_finder "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL" 
    fi

    #TestCase execution Result dynamic updating Function     
    dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}" 

    #Log generation and upload to server function
    log_generate_operations "$failed_step_num" "Image_format"

    #Postcondition code block    
    printf '\nExecuting Post-condition Steps for Testcase : %s\n\n\n' "$TestcaseID"
    sleep 1
    postCondition_Execution_IMAGEFORMATS "$TestcaseID" 
    postCondition_Execution_IMAGEFORMATS_exit=$?

    if [ "$postCondition_Execution_IMAGEFORMATS_exit" -eq 0 ]; then
        printf '\nPost-condition Execution Success. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
    else
        printf '\nPost-condition Execution failed. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
    fi
  else
    printf '\n\nPre-condition check failure. Exiting IMAGEFORMATS Automated Test!\n\n\n' 
  fi

}




#Function Definition for postcondition image formats postCondition_Execution_IMAGEFORMATS


postCondition_Execution_IMAGEFORMATS() {

  dynamic_appInstanceId=""
  kill_app "Browser_test" "$isAppInstalled_appid"  
  local kill_app_exit=$?
  if [ "$kill_app_exit" -eq 0 ]; then
      isAppInstalled "refui"
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
  else
      return 1    
  fi    

}




#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





while true; do
  printf "\n"
  printf "\n=============================================================================================================================================================\n\n";
  printf "                                                      ******* Image Format Automated Test *******                                                                    ";
  printf "\n=============================================================================================================================================================\n\n\n";
  printf '01. Run TestCase : TC_IMAGEFORMATS_MANUAL_01        :\t[ Verify the png image format launch via Browser_test App ] \n\n'
  printf '02. Run TestCase : TC_IMAGEFORMATS_MANUAL_02        :\t[ Verify the jpeg image format launch via Browser_test App ] \n\n'
  printf '03. Run TestCase : TC_IMAGEFORMATS_MANUAL_03        :\t[ Verify the svg image format launch via Browser_test App ] \n\n'
  printf '04. Run TestCase : TC_IMAGEFORMATS_MANUAL_04        :\t[ Verify the webp image format launch via Browser_test App ] \n\n'
  printf '05. Show TestCase Execution Results\n\n'
  printf '06. Exit [ Image Format Automated Test ]\n\n'
  printf "\n=============================================================================================================================================================\n\n\n";


  # ----- Main Testcaes Execution Menu -----

  
  read -p "Enter an Option to proceed : " menu_choice
  printf '\n\n\n'
  case "$menu_choice" in 
    1)
        exec_start "TC_IMAGEFORMATS_MANUAL_01"
        tc_IMAGEFORMATS_MANUAL_testsuite "tc1_step" "TC_IMAGEFORMATS_MANUAL_01"
        ;;
    2)
        exec_start "TC_IMAGEFORMATS_MANUAL_02"
        tc_IMAGEFORMATS_MANUAL_testsuite "tc2_step" "TC_IMAGEFORMATS_MANUAL_02"
        ;;
    3)
        exec_start "TC_IMAGEFORMATS_MANUAL_03"
        tc_IMAGEFORMATS_MANUAL_testsuite "tc3_step" "TC_IMAGEFORMATS_MANUAL_03"
        ;;
    4)
        exec_start "TC_IMAGEFORMATS_MANUAL_04"
        tc_IMAGEFORMATS_MANUAL_testsuite "tc4_step" "TC_IMAGEFORMATS_MANUAL_04"
        ;;                      
    5)
        testcase_result_display_menu "TC_IMAGEFORMATS_MANUAL"  
        ;;       
    6)   
        printf '\nExited Image Format Automated Test\n\n\n' 
        break
        ;; 
    *)
        printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
        ;;      
  esac
done  





#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
