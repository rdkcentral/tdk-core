#!/bin/bash


source device.conf
source generic_functions.sh


#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




#Function to check the Pre-Condition before executing TC_IMAGEFORMATS_MANUAL TestSuite



preCon_IMAGEFORMATS() {

  browserInstance_deactivate "WebKitBrowser"
  local browserInstance_deactivate_status=$?

  rdkshell_suspend_operation "ResidentApp"
  local rdkshell_suspend_exit=$?
  
  if [ "$browserInstance_deactivate_status" -eq 0 ] && [ "$rdkshell_suspend_exit" -eq 0 ]; then
    return 0
  else
    return 1
  fi    

}




#Function to check the Pre-Condition before executing TC_IMAGEFORMATS_MANUAL TestSuite



TC_IMAGEFORMATS_MANUAL_test() {

  local step_num="$1"
  local img_url="$2"
  local image_format="$3"
  local user_choice_img_format="user_choice_img_format"
  local query_img_format=$(printf "\n\nIs %s image format loaded in WebKitBrowser and Visible on TV [yes/no]: " "$image_format" )
  printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
  printf "\nStep %s\t\t: Execute curl command to launch .%s image format via WebKitBrowser\n\n\n" "$step_num" "$img_format"    
  printf "\n\ncurl --data-binary '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "WebKitBrowser", "type":"WebKitBrowser", "uri":%s, "x":0, "y":0, "w":1920, "h":1080}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc \n\n" "$img_url"
  sleep 1
  check_file_on_serve "$img_url"
  local check_file_on_server_exit=$?
    
  if [ "$check_file_on_server_exit" -eq 0 ]; then
    printf "\n\n\n[ .%s ] Image format file is available in server and accessible via URL : %s\n\n\n" "$image_format" "$img_url"
    sleep 1
    rdkshell_URL_launch "$img_url" "WebKitBrowser"
    local rdkshell_URL_launch_exit=$?

    user_confirmation "$user_choice_img_format" "$query_img_format"
    local user_confirmation_fun_exit=$?

    if [ "$rdkshell_URL_launch_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
      printf "\n\n[ .%s ] image format loaded in WebKitBrowser via RDKShell and visible on TV\n\n\n" "$image_format"
      return 0
    else
      printf "\n\nUnable to load [ .%s ] image format in WebKitBrowser via RDKShell and Not visible on TV\n\n\n" "$image_format"
      return 1
    fi
  else
    printf "\n\n\nDEBUG : Configured [ .%s ] Image format file is not available in server.Returns %s error code from server\n\n\n" "$image_format" "$check_file_on_server_exit"
    return $check_file_on_server_exit 
  fi  

}




#Function Definition for TestCase : tc_IMAGEFORMATS_MANUAL_testsuite



tc_IMAGEFORMATS_MANUAL_testsuite() {

  local TestcaseID="$2"
  local testcase_prefix="$1"
  test_step_status="PASS"

  #Precondition Check code block

  printf "\n"
  printf "Pre-Conditon check\t\t: Suspending ResidentApp and Deactivating Active Instance of WebkitBrowser\n\n\n"
  preCon_IMAGEFORMATS
  local preCon_IMAGEFORMATS_fun_exit=$?
  
  if [ "$preCon_IMAGEFORMATS_fun_exit" -eq 0 ]; then
    printf '\n\nPre-condition check success. Starting Testcase execution!\n\n\n'
    

#Step 1 code block for TC_IMAGEFORMATS_MANUAL_test 1 [ .jpg image format ]


    if [[ "$TestcaseID" == "TC_IMAGEFORMATS_MANUAL_01" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL_test" "" "" "" "" "jpg"
      dynamic_current_step_finder "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL" 
    fi  


#Step 1 code block for TC_IMAGEFORMATS_MANUAL_test 2 [ .png image format ]    


    if [[ "$TestcaseID" == "TC_IMAGEFORMATS_MANUAL_02" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL_test" "" "" "" "" "png"
      dynamic_current_step_finder "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL" 
    fi
     
   
#Step 1 code block for TC_IMAGEFORMATS_MANUAL_test 3 [ .svg image format ]


    if [[ "$TestcaseID" == "TC_IMAGEFORMATS_MANUAL_03" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL_test" "" "" "" "" "svg"
      dynamic_current_step_finder "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL" 
    fi  


#Step 1 code block for TC_IMAGEFORMATS_MANUAL_test 4 [ .webp image format ]    


    if [[ "$TestcaseID" == "TC_IMAGEFORMATS_MANUAL_04" ]]; then
      execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL_test" "" "" "" "" "webp"
      dynamic_current_step_finder "$testcase_prefix" "TC_IMAGEFORMATS_MANUAL" 
    fi

    #TestCase execution Result dynamic updating Function     
    dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}" 

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

  rdkshell_suspend_operation "WebKitBrowser"
  local rdkshell_suspend_exit=$?

  rdkshell_launch_operation "ResidentApp"
  local rdkshell_launch_exit=$?

  if [ "$rdkshell_suspend_exit" -eq 0 ] && [ "$rdkshell_launch_exit" -eq 0 ]; then
    printf "\n\nWebkitBrowser instance suspended and RDK UI loaded on TV\n\n\n"
    return 0
  else
    printf "\n\nFailed to suspended WebkitBrowser instance and load RDK UI on TV\n\n\n"
    return 1
  fi    

}




#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





while true; do
  printf "\n"
  printf "\n=============================================================================================================================================================\n\n";
  printf "                                                      ******* Image Format Automated Test *******                                                                    ";
  printf "\n=============================================================================================================================================================\n\n\n";
  printf '01. Run TestCase : TC_IMAGEFORMATS_MANUAL_01        :\t[ Verify the Jpeg image format launch via WebkitBrowser] \n\n'
  printf '02. Run TestCase : TC_IMAGEFORMATS_MANUAL_02        :\t[ Verify the png image format launch via WebkitBrowser ] \n\n'
  printf '03. Run TestCase : TC_IMAGEFORMATS_MANUAL_03        :\t[ Verify the svg image format launch via WebkitBrowser ] \n\n'
  printf '04. Run TestCase : TC_IMAGEFORMATS_MANUAL_04        :\t[ Verify the webp image format launch via WebkitBrowser ] \n\n'
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
