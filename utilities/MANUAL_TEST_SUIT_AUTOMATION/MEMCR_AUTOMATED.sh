#!/bin/bash

#Author : aharil144@cable.comcast.com

source device.conf
source generic_functions.sh

test_step_status="PASS"


#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




#Function to display the status of each App for memcr test



display_app_status() {

   local app_name="$1"
   if [[ "$app_name" == "Cobalt" ]]; then
      app_name="Youtube"
      printf '\n%s App availble in DUT for memcr test\n\n' "$app_name"
   else
      printf '\n%s App availble in DUT for memcr test\n\n' "$app_name"
   fi
}



#Function Definition for Launching YouTube Apps from RDK UI



rdk_ui_youtube_launch() {

   local app="$1"
   local is_relaunch_flag="$2"
   sleep 1
   memcr_app_status "$app"
   local memcr_app_status_exit=$?

   if [ "$memcr_app_status_exit" -eq 0 ]; then
      platform_keycode_count_finder "$app"
      local platform_keycode_count_finder_exit=$?

      if [ "$platform_keycode_count_finder_exit" -ne 0 ]; then
         printf "\n\n\nDEBUG : platform_keycode_count_finder function failed with error code : %s\n\n" "$platform_keycode_count_finder_exit"
         return $platform_keycode_count_finder_exit
      else   
         generateKey_applaunch_operation ${#yt_nav_keys[@]} ${#yt_key_counts[@]} "${yt_nav_keys[@]}" "${yt_key_counts[@]}"
         local generateKey_applaunch_operation_exit=$?

         if [[ "$generateKey_applaunch_operation_exit" -ne 0 ]]; then
            printf "\n\n\nDEBUG : generateKey_applaunch_operation function failed with error code : %s\n\n" "$generateKey_applaunch_operation_exit"
            return $generateKey_applaunch_operation_exit
         else
            if [[ "$is_relaunch_flag" -eq 1 ]]; then
               return 0
            else      
               sleep 5
               youtube_deeplink_launch
               local youtube_deeplink_launch_func_exit=$?
               sleep 3
               if [ "$youtube_deeplink_launch_func_exit" -eq 0 ]; then
                  generateKey_RDKUI_navigation "13"
                  local generate_key_exit_2=$?
                  sleep 10
                  user_choice_3="user_choice_3"
                  printf '\n\n\n' 
                  local Query_3="Is YouTube App launched and able to see AV playback? [yes/no]: "
                  user_confirmation "$user_choice_3" "$Query_3"
                  local user_confirmation_fun_exit=$?

                  if [ "$generate_key_exit_2" -ne 0 ]; then
                     printf "\n\ngenerateKey "enter" key RDK UI navigation failed\n\n"
                     printf "\n\n\nDEBUG : generateKey_RDKUI_navigation function failed with error code : %s\n\n" "$generate_key_exit_2"
                     return "$generate_key_exit_2"
                  elif [ "$user_confirmation_fun_exit" -ne 0 ]; then
                     printf "\n\n\nDEBUG : user_confirmation function failed with error code : %s\n\n" "$user_confirmation_fun_exit"
                     return "$user_confirmation_fun_exit"
                  else
                     return 0
                  fi
               else
                  printf '\n\nUnable to start AV playback on %s using deeplink\n\n\n' "$app"
                  printf "\n\n\nDEBUG : youtube_deeplink_launch function failed with error code : %s\n\n" "$youtube_deeplink_launch_func_exit"     
                  return $youtube_deeplink_launch_func_exit
               fi   
            fi   
         fi
      fi       
   else
      printf '\n\n%s App not available in RDKUI to launch\n\n\n' "$app"
      printf "\n\n\nDEBUG : memcr_app_status function failed with error code : %s\n\n" "$memcr_app_status_exit" 
      return 1   
   fi       

}


#Function Definition for Launching YouTube Apps from RDK UI



rdk_ui_youtube_TV_launch() {

   local app="$1"
   sleep 1
   memcr_app_status "$app"
   local memcr_app_status_exit=$?

   if [ "$memcr_app_status_exit" -eq 0 ]; then
      platform_keycode_count_finder "$app"
      local platform_keycode_count_finder_exit=$?

      if [ "$platform_keycode_count_finder_exit" -eq 0 ]; then
         generateKey_applaunch_operation ${#yttv_nav_keys[@]} ${#yttv_key_counts[@]} "${yttv_nav_keys[@]}" "${yttv_key_counts[@]}"
         local generateKey_applaunch_operation_exit=$?

         if [ "$generateKey_applaunch_operation_exit" -eq 0 ]; then
            sleep 5
            user_choice_4="user_choice_4" 
            printf '\n\n\n'
            local Query_4="Is YouTubeTV App launched and able to see in RDK UI? [yes/no]: "
            user_confirmation "$user_choice_4" "$Query_4"
            local user_confirmation_fun_exit=$?

            if [ "$user_confirmation_fun_exit" -eq 0 ]; then
               printf '\n\n%s App launched successfully in RDK UI\n\n\n' "$app"
               return 0
            else
               printf "\n\n%s App didn't launch in RDK UI\n\n\n" "$app"
               return 1
            fi
         else
            printf "\n\n\nDEBUG : generateKey_applaunch_operation function failed with error code : %s\n\n" "$generateKey_applaunch_operation_exit"
            return $generateKey_applaunch_operation_exit
         fi 
      else
         printf "\n\n\nDEBUG : platform_keycode_count_finder function failed with error code : %s\n\n" "$platform_keycode_count_finder_exit"
         return $platform_keycode_count_finder_exit
      fi      
   else
      printf '\n\n%s App not available in RDKUI to launch\n\n\n' "$app"
      printf "\n\n\nDEBUG : memcr_app_status function failed with error code : %s\n\n" "$memcr_app_status_exit"
      return 1   
   fi

} 



#Function Definition for Launching Aamazon App from RDK UI



rdk_ui_amazon_launch() {

   local app="$1"
   local is_relaunch_flag="$2"
   sleep 1
   memcr_app_status "$app"
   local memcr_app_status_exit=$?

   if [ "$memcr_app_status_exit" -eq 0 ]; then
      platform_keycode_count_finder "$app"
      local platform_keycode_count_finder_exit=$?

      if [ "$platform_keycode_count_finder_exit" -eq 0 ]; then
         generateKey_applaunch_operation ${#amz_nav_keys[@]} ${#amz_key_counts[@]} "${amz_nav_keys[@]}" "${amz_key_counts[@]}"
         local generateKey_applaunch_operation_exit=$?
         sleep 3

         if [ "$generateKey_applaunch_operation_exit" -eq 0 ]; then
            if [[ "$is_relaunch_flag" -eq 1 ]]; then
               return 0
            else
               sleep 5
               amazon_deeplink_launch
               amazon_deeplink_launch_exit=$?
               sleep 3
               if [ "$amazon_deeplink_launch_exit" -eq 0 ]; then
                  generateKey_RDKUI_navigation "13"
                  local generate_key_exit_2=$?
                  sleep 2 
                  local user_choice_5="user_choice_5"
                  printf '\n\n\n' 
                  local Query_5="Is Amazon App launched and able to see AV playback? [yes/no]: "
                  user_confirmation "$user_choice_5" "$Query_5"
                  local user_confirmation_fun_exit=$?

                  if [ "$generate_key_exit_2" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
                     printf '\n\n%s App launched and AV playback started successfully\n\n\n' "$app"
                     return 0
                  else  
                     printf "\n\ngenerateKey "enter" key RDK UI navigation failed\n\n"
                     printf "\n\n\nDEBUG : generateKey_RDKUI_navigation function failed with error code : %s\n\n" "$generate_key_exit_2"
                     return $generate_key_exit_2
                  fi
               else
                  printf '\n\nUnable to start AV playback on %s using deeplink\n\n\n' "$app"
                  printf "\n\n\nDEBUG : amazon_deeplink_launch function failed with error code : %s\n\n" "$amazon_deeplink_launch_exit"     
                  return 1     
               fi
            fi   
         else
            printf "\n\n\nDEBUG : generateKey_applaunch_operation function failed with error code : %s\n\n" "$generateKey_applaunch_operation_exit"
            return $generateKey_applaunch_operation_exit
         fi
      else
         printf "\n\n\nDEBUG : platform_keycode_count_finder function failed with error code : %s\n\n" "$platform_keycode_count_finder_exit"
         return $platform_keycode_count_finder_exit
      fi    
   else
      printf '\n\n%s App not available in RDKUI to launch\n\n\n' "$app"
      printf "\n\n\nDEBUG : memcr_app_status function failed with error code : %s\n\n" "$memcr_app_status_exit"
      return 1    
   fi        

}



#Function to check the Pre-Condition before executing TC_MEMCR_MANUAL TestSuite



pre_Check_App_Exist() {

   for app in "${memcr_test_apps[@]}"; do
      memcr_app_status "$app"
      memcr_app_status_exit=$? 

      if [ "$memcr_app_status_exit" -eq 0 ]; then
         if [[ "$app" == "Cobalt" ]]; then
            app_available_flag1=0
         fi
         if [[ "$app" == "Amazon" ]]; then
            app_available_flag2=0
         fi
         if [[ "$app" == "YouTubeTV" ]]; then
            app_available_flag3=0
         fi
         display_app_status "$app"
      else
         if [[ "$app" == "Cobalt" ]]; then
            app="Youtube"
            app_available_flag1=1
         fi
         if [[ "$app" == "Amazon" ]]; then
            app_available_flag2=1
         fi
         if [[ "$app" == "YouTubeTV" ]]; then
            app_available_flag3=1
         fi
         printf '%s App not available in device for MEMCR test\n\n\n' "$app"
      fi
   done

#Checking whether Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.AppHibernate.Enable datamodel is true or not
   sleep 1
   apphibernate_status 
   local apphibernate_status_exit=$?

   if [ "$apphibernate_status_exit" -eq 0 ]; then
      local app_hibernate_status=0
   else
      local app_hibernate_status=1
   fi

   if [[ "$app_available_flag1" == 1 && "$app_available_flag2" == 1 && "$app_available_flag3" == 1 ]]; then
      printf '\n\nNo PremiumApps are available in Device for proceeding memcr test\n\n\n'
      return 1
   elif [[ "$app_available_flag1" == 0 && "$app_available_flag2" == 0 && "$app_available_flag3" == 0 && "$app_hibernate_status" == 0 ]]; then
      printf '\n\nAll PremiumApps are available in Device and apphibernate DataModel status is true for proceeding memcr test\n\n\n'
      return 0   
   else
      if [[ "$app_hibernate_status" == 0 ]]; then
         printf '\n\nOne or more PremiumApp available in Device and apphibernate DataModel status is true for proceeding memcr test\n\n\n'
         return 0
      else
         printf '\n\nOne or more PremiumApp available in Device but apphibernate DataModel status is false. Failed to proceed memcr test\n\n\n'
         return 1
      fi   
   fi

} 



#Function Definition for TC_MEMCR_MANUAL_01  



TC_MEMCR_MANUAL_01() {

   local step_num="$1"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "\nStep %s\t\t: Execute systemctl command to check the status of memcr\n\n\n" "$step_num"
   printf "\n\nsystemctl status memcr\n\n\n"
   memcr_status_result=$(systemctl status memcr | awk '/Active:/ {print $2}')
   if [[ "$memcr_status_result" == "active" ]]; then
      printf "\nMemcr Status is Up and returns state  : %s\n\n\n" "$memcr_status_result"
      return 0
   else
      printf "\nMemcr Status is down and returns state  : %s\n\n\n" "$memcr_status_result"
      return 1
   fi 

}



#Function Definition for TC_MEMCR_MANUAL_02 STEP 1 also used in TC_MEMCR_MANUAL_03 STEP 1



TC_MEMCR_MANUAL_02_step1() {
 
   local step_num="$1"
   local app_name="$2"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "\nStep %s\t\t: Validate the launch of the %s application and subsequent initiation of AV playback.\n\n\n" "$step_num" "$app_name"
   sleep 2

   launch_premium_apps "$app_name"
   local launch_premium_apps_exit1=$?
      
   if [ "$launch_premium_apps_exit1" -eq 0 ]; then
      return 0
   else
      printf '\n\nDEBUG : launch_premium_apps function failed with error code %s\n\n\n' "$launch_premium_apps_exit1"
      return $launch_premium_apps_exit1
   fi

}



#Function Definition for TC_MEMCR_MANUAL_03 STEP 2 



TC_MEMCR_MANUAL_03_step2(){

   local step_num="$1"
   local app_name="$2"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "\nStep %s\t\t: Execute the command to extract the PID of %s App\n\n\n" "$step_num" "$app_name"
   case "$app_name" in
      "YouTube") printf "\n\nps -aux | grep YouTube\n\n\n" ;;
      "YouTubeTV") printf "\n\nps -aux | grep YouTubeTV\n\n\n" ;;
      "Amazon") printf "\n\nps -aux | grep Amazon\n\n\n" ;; 
      *) printf "\n\nInvalid/Unidentified App -> %s\n\n\n" "$app_name" ;;
   esac             
   sleep 2

   premiumApp_PID_extract "$app_name"
   local premiumApp_PID_exit=$?

   if [ "$premiumApp_PID_exit" -eq 0 ]; then
      return 0
   else
      printf '\n\nDEBUG : premiumApp_PID_extract function failed with error code %s\n\n\n' "$premiumApp_PID_exit"
      return $premiumApp_PID_exit
   fi

}



#Function Definition for TC_MEMCR_MANUAL_03 STEP 4 



TC_MEMCR_MANUAL_03_step4() {

   local step_num="$1"
   local proc_ID="$2"
   local app_name="$3"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "\nStep %s\t\t: Execute command to get the memory consumption of /proc/<PID> of %s App\n\n\n" "$step_num" "$app_name"
   printf "\n\ngrep -i 'VmRSS' status | awk '{print \$2\$3}'\n\n\n"
   sleep 2

   memcr_apps_memoryUsage "$proc_ID"
   local memcr_apps_memoryUsage_exit=$?

   if [ "$memcr_apps_memoryUsage_exit" -eq 0 ]; then
      printf "\n\n\nTotal Memory consumed by %s App  :  %sKB\n\n\n" "$app_name" "$memory_used"
      if [[ "$step_num" =~ ^[0-9]+$ ]]; then
         eval "memory_used_${step_num}='$memory_used'"
         return 0
      else
         echo "Invalid step number: $step_num"
         return 1
      fi
   else
      printf '\n\nDEBUG : memcr_apps_memoryUsage function failed with error code %s\n\n\n' "$memcr_apps_memoryUsage_exit"
      return $memcr_apps_memoryUsage_exit
   fi

}



#Function Definition for TC_MEMCR_MANUAL_03 STEP 6 



TC_MEMCR_MANUAL_03_step6() {

   local step_num="$1"
   local proc_ID="$2"
   local app_name="$3"
   sleep 1

   TC_MEMCR_MANUAL_03_step4 "$step_num" "$proc_ID" "$app_name"
   local TC_MEMCR_MANUAL_03_step4_exit=$?
   sleep 1
   memory_usage_comparison "$memory_used_4" "$memory_used_6"
   local memory_usage_comparison_exit=$?
   sleep 1

   if [[ "$TC_MEMCR_MANUAL_03_step4_exit" -eq 0 ]] && [[ "$memory_usage_comparison_exit" -eq 0 ]]; then
      printf "\n\n\nMemory Consumption of %s after homekey press is less than 1/10 of before homekey press \n\n\n\n=> Current Memory Usage : %sKB\n\n=> previous Memory Usage : %sKB\n\n\n\n" "$app_name" "$memory_used_6" "$memory_used_4"
      return 0
   else
      printf "\n\n\nMemory Consumption of %s after homekey press is greater than 1/10 of before homekey press \n\n\n\n=> Current Memory Usage : %sKB\n\n=> previous Memory Usage : %sKB\n\n\n\n" "$app_name" "$memory_used_6" "$memory_used_4" 
      printf '\n\nDEBUG : memory_usage_comparison function returns failure error code : %s\n\n\n' "$memory_usage_comparison_exit" 
      return $memory_usage_comparison_exit
   fi

}


#Function Definition for TC_MEMCR_MANUAL_04 STEP 2 and TC_MEMCR_MANUAL_04 STEP 4



TC_MEMCR_MANUAL_04_step2() {

   local step_num="$1"
   local app="$2"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "\nStep %s\t\t: Execute command to Change directory to /media/apps/memcr/ and list the contents\n\n\n" "$step_num"
   printf "\n\ncd /media/apps/memcr/\n\n\n"
   sleep 1
   platform_type_finder
   sleep 1
   memcr_directory_navigation "$platform_model"
   memcr_directory_navigation_exit1=$?
   sleep 1
   
   if [[ "$memcr_directory_navigation_exit1" -eq 0 ]]; then 
      return 0
   elif [[ "$memcr_directory_navigation_exit1" -eq 10 && "$file_found" == "true" ]]; then
      printf "\n\nSerialized file with .img extension created while %s App went to hibernated state\n\n\n" "$app"
      return 5
   else   
      printf '\n\nDEBUG : memcr_directory_navigation function failed with error code %s\n\n\n' "$memcr_directory_navigation_exit1"
      return "$memcr_directory_navigation_exit1"  
   fi

}



#Function Definition for TC_MEMCR_MANUAL_04 STEP 3



TC_MEMCR_MANUAL_04_step3() {

   local step_num="$1"
   local appname="$2"
   local playbackPos_fun="$3"
   if [[ "$appname" == "YouTube" ]]; then   
      printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
      printf "\nStep %s\t\t: Observe the time position in video and Press Home key to move %s App to background\n\n\n" "$step_num" "$appname"
      sleep 1
   fi   
   memcr_app_homekey_close "$step_num" "$appname" "$playbackPos_fun" 
   local memcr_app_homekey_close_exit=$?
   sleep 1

   if [ "$memcr_app_homekey_close_exit" -eq 0 ]; then
      return 0
   else   
      printf '\n\nDEBUG : memcr_app_homekey_close function failed with error code %s\n\n\n' "$memcr_app_homekey_close_exit"
      return $memcr_app_homekey_close_exit
   fi    

}



#Function Definition for TC_MEMCR_MANUAL_04 STEP 5 to launch YouTube again from hibernated state and check the resumed playback position



TC_MEMCR_MANUAL_04_step5() {

   local step_num="$1"
   local appname="$2"
   local playback_pos_value="$3"
   is_relaunch=1
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   if [[ "$appname" != "YouTube" ]]; then
      printf "\nStep %s\t\t: Launch %s App from Hibernate state and verify App Homepage is loaded\n\n\n" "$step_num" "$appname"
   else
      printf "\nStep %s\t\t: Launch %s App from Hibernate state and verify whether video resumed from last playback Position -> %s\n\n\n" "$step_num" "$appname" "$playback_pos_value"
   fi   
   sleep 1
   case "$appname" in
      "YouTube") rdk_ui_youtube_launch "$appname" "$is_relaunch" ;;
      "YouTubeTV") rdk_ui_youtube_TV_launch "$appname" ;;
      "Amazon") rdk_ui_amazon_launch "$appname" "$is_relaunch" ;; 
      *) printf "\n\nInvalid/Unidentified App -> %s\n\n\n" "$appname" ;;
   esac
   local rdkui_app_launch_exit=$?
   local user_choice_7="user_choice_7"
   printf '\n\n\n'
   if [[ "$appname" != "YouTube" ]]; then
      local Query_7=$(printf "Is %s App launched and Homepage is loaded? [yes/no]: " "$appname" )
   else   
      local Query_7=$(printf "Is %s App launched and AV playback resumed from last playback position -> [ %s ] ? [yes/no]: " "$appname" "$playback_pos_value" )
   fi   
   user_confirmation "$user_choice_7" "$Query_7"
   local user_confirmation_fun_exit=$?

   if [ "$rdkui_app_launch_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
      if [[ "$appname" != "YouTube" ]]; then
         printf "\n\n%s App launched and Homepage is loaded successfully\n\n\n" "$appname"
      else   
         printf "\n\n%s App launched and AV playback resumed from last playback position [ %s ]\n\n\n" "$appname" "$playback_pos_value"
      fi   
      return 0
   else
      if [[ "$appname" != "YouTube" ]]; then
         printf "\n\n%s App launch failed or Homepage is not loaded properly\n\n\n" "$appname"  
      else
         printf "\n\n%s App launch failed or AV playback didn't resumed from last playback position [ %s ]\n\n\n" "$appname" "$playback_pos_value"  
      fi
      printf "\n\n\nDEBUG : generateKey_RDKUI_navigation function failed with error code : %s\n\n" "$generate_key_exit"    
      return 1
   fi

}



#Function Definition for TC_MEMCR_MANUAL_03 STEP 3 



TC_MEMCR_MANUAL_03_step3() {

   local step_num="$1"
   local proc_ID="$2"
   local app_name="$3"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "\nStep %s\t\t: Execute command to Change directory to /proc/<PID> of %s App\n\n\n" "$step_num" "$app_name"
   printf "\n\ncd /proc/<pid>\n\n\n"
   sleep 1

   proc_ID_navigation "$proc_ID"
   local proc_ID_navigation_exit=$?

   if [ "$proc_ID_navigation_exit" -eq 0 ]; then
      printf "\n\n\nCurrent Working directory Changed to %s\n\n\n" "$(pwd)" 
      return 0
   else
      printf '\n\nDEBUG : proc_ID_navigation function failed with error code %s\n\n\n' "$proc_ID_navigation_exit"
      return $proc_ID_navigation_exit
   fi

}



#Function Definition for memory usage comparison function used in TC_MEMCR_MANUAL_03 STEP 6



memory_usage_comparison() {

   local memoryUsage_before_homeKey_press="$1"
   local memoryUsage_after_homeKey_press="$2"

   local threshold_point=$((memoryUsage_before_homeKey_press / 10))
   if [[ "$memoryUsage_after_homeKey_press" -lt "$threshold_point" ]]; then
      return 0
   else
      return 128
   fi 
     
}



#Function Definition for changing directory to procID directory



proc_ID_navigation() {

   local proc_id="$1"
   if [ -d "/proc/$proc_id" ]; then
      if cd "/proc/$proc_id"; then
         return 0
      else
         printf "\n\n\nFailed to change directory to /proc/%s\n\n\n" "$proc_id"
         return 119
      fi
   else
      printf "\n\n\nProcess : %s not found in /proc directory\n\n\n" "$proc_id"
      return 118
   fi 

}



#Function Definition for changing directory to memcr directory



memcr_directory_navigation() {

   local device_pltform="$1"
   if [[ "$invalid_platform" == "true" ]]; then
      printf '\n\ndirectory change operation failed\n\n\n'
      return 1
   elif [[ "$device_pltform" == "AH212" ]]; then
      if [ -d "/tmp/data/memcr" ]; then
         if cd "/tmp/data/memcr"; then
            if [ -z "$(ls -A)" ]; then
               printf "\n\n\n/tmp/data/memcr directory is Empty!!\n\n\n"
               return 0
            else
               printf "\n\n\n/tmp/data/memcr directory is not Empty : %s\n\n\n" "$(ls)"
               file_found="true"
               return 10  
            fi   
         else
            printf "\n\n\nFailed to change directory to /tmp/data/memcr\n\n\n"
            return 139
         fi
      else
         printf "\n\n\n/tmp/data/memcr directory not available in %s device\n\n\n" "$device_pltform"
         return 138
      fi
   else
      if [ -d "/media/apps/memcr" ]; then
         if cd "/media/apps/memcr"; then
            if [ -z "$(ls -A)" ]; then
               printf "\n\n\n/media/apps/memcr directory is Empty!!\n\n\n"
               return 0
            else
               printf "\n\n\n/media/apps/memcr directory is not Empty : %s\n\n\n" "$(ls)"
               file_found="true"
               return 10  
            fi   
         else
            printf "\n\n\nFailed to change directory to /media/apps/memcr\n\n\n"
            return 139
         fi
      else
         printf "\n\n\n/media/apps/memcr/ directory not available in %s\n\n\n" "$device_pltform"
         return 138
      fi
   fi   

}


#Function Definition for memecr_App Avplayback_Position fetching before home key press close and confirming. Function used for  TC_MEMCR_MANUAL_03_step5 



getCurrentPlaybackPosition() {

   local app="$1"
   sleep 2
   while true; do
      printf "\n\nEnter the current exact playback position of %s App (format:- HH:MM:SS): " "$app"
      read -r playbackPos
      printf "\n\n"
      playbackPos=$(echo "$playbackPos" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      if [[ "$playbackPos" =~ ^([0-9]{1,2}):([0-5][0-9]):([0-5][0-9])$ ]]; then
        printf "\nCurrent Playback Position : %s\n\n\n" "$playbackPos"
        break
      else
        printf "\n\nInvalid playback position format. Try again!! [Note] : Please enter time in HH:MM:SS format (e.g., 12:02:30)\n\n\n"
      fi
   done

}



#Function Definition for memecr_App home key press close and confirming. Function used for  TC_MEMCR_MANUAL_02_step3 



memcr_app_homekey_close() {

   local step_num="$1"
   local app_name="$2"
   local playbackPosition_func="$3"
   if (( "$playbackPosition_func" == 1 )); then
      getCurrentPlaybackPosition
   else      
      printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
      printf "\nStep %s\t\t: Press Home button and check the behavior of %s\n\n\n" "$step_num" "$app_name"
      sleep 1   
   fi   
   generateKey_RDKUI_navigation "36"
   local generatekey_nav_exit=$?
   sleep 5
   local user_choice_6="user_choice_6" 
   local Query_6="Is $app_name moved to background and the RDK UI visible on TV? [yes/no]: "
   user_confirmation "$user_choice_6" "$Query_6"
   local user_confirmation_fun_exit=$?

   if [ "$generatekey_nav_exit" -eq 0 ] && [ "$user_confirmation_fun_exit" -eq 0 ]; then
      printf "\nConfirmed: %s moved to background and the RDK UI visible on TV\n\n\n" "$app_name"
      return 0
   else
      printf "\nFailed to move %s to background and RDK UI is not visible on TV\n\n\n" "$app_name"
      return 1
   fi      

}



#Function Definition for premiumApplaunch and step update for TC_MEMCR_MANUAL_02_step1  TC_MEMCR_MANUAL_04_step1 TC_MEMCR_MANUAL_03_step1



memcr_applaunch_common_teststep(){

   local _testcase_prefix_="$1"
   local appName="$2"
   local is_app_available="$3"
   sleep 2
   if [[ "$test_step_status" != "FAIL" ]]; then
      if [[ "$is_app_available" == 0 ]]; then
         app_state_check_and_destroy "$appName"
         local app_state_check_and_destroy_exit1=$? 

         if [ "$app_state_check_and_destroy_exit1" -ne 0 ]; then
            printf "\n\nSkipping Step 1, as the step preCondition check had failed\n\n"
            printf "\n\n\nUnable to proceed testcase : %s\n\n\n" "$TestcaseID"
            update_test_status "${_testcase_prefix_}1" "NT"
            test_step_status="FAIL"
         else
            printf "\n\n%s App is available in DUT. Proceeding Testcase : %s\n\n" "$appName" "$TestcaseID"
            declare "${_testcase_prefix_}_num_1=1"
            memcr_dynamic_var_name_0="${_testcase_prefix_}_num_1"
            TC_MEMCR_MANUAL_02_step1 "${!memcr_dynamic_var_name_0}" "$appName"
            local memcr_fun_exit_status=$?

            if [ "$memcr_fun_exit_status" -eq 0 ]; then
               printf "\nStep 1 status\t:  PASS\n\n\n"
               update_test_status "${_testcase_prefix_}1" "PASSED"
            else
               printf "Step 1 status\t:  FAIL\n\n\n"
               update_test_status "${_testcase_prefix_}1" "FAILED"
               test_step_status="FAIL" 
            fi
         fi   
      else
         printf '\n\n%s App not available in DUT\n\n\n' "$appName"
         printf "Step 1 status\t:  FAIL\n\n\n"
         update_test_status "${_testcase_prefix_}1" "FAILED"
         test_step_status="FAIL"
      fi          
   else
      printf "\n\nSkipping Step 1, as the previous step failed\n\n"
      update_test_status "${_testcase_prefix_}1" "NT"   
   fi

}



#Function Definition for TC_MEMCR_MANUAL_02_step2 function used in TC_MEMCR_MANUAL_02_step2



TC_MEMCR_MANUAL_02_step2() {

   local step_heading="$1"
   local test_app="$2"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "$step_heading"
   printf "\n\ncurl --data-binary '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.getState", "params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc \n\n\n"
   sleep 1
   get_Premium_App_state "$test_app"
   local get_Premium_App_state_fun_exit=$?
   sleep 1

   if [ "$get_Premium_App_state_fun_exit" -eq 0 ]; then
      printf "\n%s App current state during playback : %s\n\n\n" "$test_app" "$app_state" 
      return 0
   else
      printf "\n%s App current state during playback : %s\n\n\n" "$test_app" "$app_state"
      return 1
   fi   

}



#Function Definition for TC_MEMCR_MANUAL_02_step4 function used in TC_MEMCR_MANUAL_02_step4



TC_MEMCR_MANUAL_02_step4() {

   local step_heading="$1"
   local test_app="$2"
   printf "\n_________________________________________________________________________________________________________________________________________________________\n\n"
   printf "$step_heading"
   printf "\n\ncurl --data-binary '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.RDKShell.1.getState", "params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc \n\n\n"
   sleep 1
   get_Premium_App_state "$test_app"
   local get_Premium_App_state_fun_exit_1=$?
   sleep 1
   
   if [ "$get_Premium_App_state_fun_exit_1" -eq 0 ]; then
      printf "\n%s App current state after Home key Press : %s\n\n\n" "$test_app" "$app_state"
      return 1
   else
      if [[ "$hibernated_app_state" == 1 ]]; then
         printf "\n%s App current state after Home key Press : %s\n\n\n" "$test_app" "$app_state"
         return 0
      else
         printf "\n%s App current state after Home key Press : %s\n\n\n" "$test_app" "$app_state"
         return 1  
      fi
   fi        

}




#Function Definition for TestCase : TC_MEMCR_MANUAL_testsuite



tc_MEMCR_MANUAL_testsuite() {

   local TestcaseID="$2"
   local testcase_prefix="$1"
   test_step_status="PASS"
   is_relaunch_flag=0

   #Precondition Check code block

   printf "\n"
   printf "Pre-Conditon check\t\t:  Checks whether DUT have Youtube App | Youtube Tv App | Amazon Prime Video App for MEMCR test\n\n\n"
   pre_Check_App_Exist
   pre_Check_App_fun_exit=$?
   
   if [ "$pre_Check_App_fun_exit" -eq 0 ]; then
      printf '\n\nPre-condition check success. Starting Testcase execution!\n\n\n'


#Step 1 code block for TC_MEMCR_MANUAL_01


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_01" ]]; then
         execute_stepStatusUpdate_steps "1" "$testcase_prefix" "TC_MEMCR_MANUAL_01" 
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL" 
      fi  


#Step 1 code block for TC_MEMCR_MANUAL_02


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_02" ]]; then
         memcr_applaunch_common_teststep "$testcase_prefix" "YouTube" "$app_available_flag1"
         sleep 1


#Step 2 code block for TC_MEMCR_MANUAL_02         
         

         local step2_message="\nStep 2\t\t: Execute curl command to get the state of Youtube App after AV Playback\n\n\n"
         execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_MEMCR_MANUAL_02_step2" "YouTube" "$step2_message"
         sleep 1
         

#Step 3 code block for TC_MEMCR_MANUAL_02         
         
         
         playbackPos_fun=0
         execute_stepStatusUpdate_steps "3" "$testcase_prefix" "memcr_app_homekey_close" "YouTube" "" "$playbackPos_fun"
         sleep 1         


#Step 4 code block for TC_MEMCR_MANUAL_02        
         

         local step4_message="\nStep 4\t\t: Execute curl command to get the state of Youtube App after pressing Home key\n\n\n"
         execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_MEMCR_MANUAL_02_step4" "YouTube" "$step4_message"
         sleep 1
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL" 
      fi
      

#Step 1 code block for TC_MEMCR_MANUAL_03


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_03" ]]; then
         memcr_applaunch_common_teststep "$testcase_prefix" "YouTube" "$app_available_flag1"
         sleep 1              


#Step 2 code block for TC_MEMCR_MANUAL_03         
         

         execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step2" "YouTube"
         sleep 1                       


#Step 3 code block for TC_MEMCR_MANUAL_03         
         

         execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step3" "YouTube" "" "" "$premiumApp_PID"
         sleep 1
                               

#Step 4 code block for TC_MEMCR_MANUAL_03         
         

         execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step4" "YouTube" "" "" "$premiumApp_PID"
         sleep 1
                                       

#Step 5 code block for TC_MEMCR_MANUAL_03         
         

         playbackPos_fun=0
         execute_stepStatusUpdate_steps "5" "$testcase_prefix" "memcr_app_homekey_close" "YouTube" "" "$playbackPos_fun"
         sleep 1
                                       

#Step 6 code block for TC_MEMCR_MANUAL_03         
         

         execute_stepStatusUpdate_steps "6" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step6" "YouTube" "" "" "$premiumApp_PID"
         sleep 1
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL"
      fi   
     

#Step 1 code block for TC_MEMCR_MANUAL_04


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_04" ]]; then
         memcr_applaunch_common_teststep "$testcase_prefix" "YouTube" "$app_available_flag1"
    

#Step 2 code block for TC_MEMCR_MANUAL_04

        
         execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step2" "YouTube"
         sleep 1
        

#Step 3 code block for TC_MEMCR_MANUAL_04


         playbackPos_fun=1
         execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step3" "YouTube" "" "$playbackPos_fun"
         sleep 1
                  

#Step 4 code block for TC_MEMCR_MANUAL_04


         execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step2" "YouTube"
         sleep 1
                          

#Step 5 code block for TC_MEMCR_MANUAL_04


         execute_stepStatusUpdate_steps "5" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step5" "YouTube"
         sleep 1
                         

#Step 6 code block for TC_MEMCR_MANUAL_04


         execute_stepStatusUpdate_steps "6" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step2" "YouTube"
         sleep 1
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL"
      fi 


#Step 1 code block for TC_MEMCR_MANUAL_05


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_05" ]]; then
         memcr_applaunch_common_teststep "$testcase_prefix" "YouTubeTV" "$app_available_flag3"
         sleep 1


#Step 2 code block for TC_MEMCR_MANUAL_05         
         

         local step2_message="\nStep 2\t\t: Execute curl command to get the state of YoutubeTV App after AV Playback\n\n\n"
         execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_MEMCR_MANUAL_02_step2" "YouTubeTV" "$step2_message"
         sleep 1
         

#Step 3 code block for TC_MEMCR_MANUAL_05         
         
         
         playbackPos_fun=0
         execute_stepStatusUpdate_steps "3" "$testcase_prefix" "memcr_app_homekey_close" "YouTubeTV" "" "$playbackPos_fun"
         sleep 1         


#Step 4 code block for TC_MEMCR_MANUAL_05        
         

         local step4_message="\nStep 4\t\t: Execute curl command to get the state of YoutubeTV App after pressing Home key\n\n\n"
         execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_MEMCR_MANUAL_02_step4" "YouTubeTV" "$step4_message"
         sleep 1
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL" 
      fi  


#Step 1 code block for TC_MEMCR_MANUAL_06


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_06" ]]; then
         memcr_applaunch_common_teststep "$testcase_prefix" "YouTubeTV" "$app_available_flag3"
         sleep 1              


#Step 2 code block for TC_MEMCR_MANUAL_06         
         

         execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step2" "YouTubeTV"
         sleep 1                       


#Step 3 code block for TC_MEMCR_MANUAL_06         
         

         execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step3" "YouTubeTV" "" "" "$premiumApp_PID"
         sleep 1
                               

#Step 4 code block for TC_MEMCR_MANUAL_06         
         

         execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step4" "YouTubeTV" "" "" "$premiumApp_PID"
         sleep 1
                                       

#Step 5 code block for TC_MEMCR_MANUAL_06        
         

         playbackPos_fun=0
         execute_stepStatusUpdate_steps "5" "$testcase_prefix" "memcr_app_homekey_close" "YouTubeTV" "" "$playbackPos_fun"
         sleep 1
                                       

#Step 6 code block for TC_MEMCR_MANUAL_06        
         

         execute_stepStatusUpdate_steps "6" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step6" "YouTubeTV" "" "" "$premiumApp_PID"
         sleep 1
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL"
      fi   
     

#Step 1 code block for TC_MEMCR_MANUAL_07


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_07" ]]; then
         memcr_applaunch_common_teststep "$testcase_prefix" "YouTubeTV" "$app_available_flag3"
    

#Step 2 code block for TC_MEMCR_MANUAL_07

        
         execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step2" "YouTubeTV"
         sleep 1
        

#Step 3 code block for TC_MEMCR_MANUAL_07


         playbackPos_fun=0
         execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step3" "YouTubeTV" "" "$playbackPos_fun"
         sleep 1
                  

#Step 4 code block for TC_MEMCR_MANUAL_07


         execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step2" "YouTubeTV"
         sleep 1
                          

#Step 5 code block for TC_MEMCR_MANUAL_07


         execute_stepStatusUpdate_steps "5" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step5" "YouTubeTV"
         sleep 1
                         

#Step 6 code block for TC_MEMCR_MANUAL_07


         execute_stepStatusUpdate_steps "6" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step2" "YouTubeTV"
         sleep 1
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL"
      fi


#Step 1 code block for TC_MEMCR_MANUAL_08


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_08" ]]; then
         memcr_applaunch_common_teststep "$testcase_prefix" "Amazon" "$app_available_flag2"
         sleep 1


#Step 2 code block for TC_MEMCR_MANUAL_08         
         

         local step2_message="\nStep 2\t\t: Execute curl command to get the state of Amazon App after AV Playback\n\n\n"
         execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_MEMCR_MANUAL_02_step2" "Amazon" "$step2_message"
         sleep 1
         

#Step 3 code block for TC_MEMCR_MANUAL_08         
         
         
         playbackPos_fun=0
         execute_stepStatusUpdate_steps "3" "$testcase_prefix" "memcr_app_homekey_close" "Amazon" "" "$playbackPos_fun"
         sleep 1         


#Step 4 code block for TC_MEMCR_MANUAL_08        
         

         local step4_message="\nStep 4\t\t: Execute curl command to get the state of Amazon App after pressing Home key\n\n\n"
         execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_MEMCR_MANUAL_02_step4" "Amazon" "$step4_message"
         sleep 1
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL" 
      fi  


#Step 1 code block for TC_MEMCR_MANUAL_09


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_09" ]]; then
         memcr_applaunch_common_teststep "$testcase_prefix" "Amazon" "$app_available_flag2"
         sleep 1              


#Step 2 code block for TC_MEMCR_MANUAL_09         
         

         execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step2" "Amazon"
         sleep 1                       


#Step 3 code block for TC_MEMCR_MANUAL_09         
         

         execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step3" "Amazon" "" "" "$premiumApp_PID"
         sleep 1
                               

#Step 4 code block for TC_MEMCR_MANUAL_09         
         

         execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step4" "Amazon" "" "" "$premiumApp_PID"
         sleep 1
                                       

#Step 5 code block for TC_MEMCR_MANUAL_09        
         

         playbackPos_fun=0
         execute_stepStatusUpdate_steps "5" "$testcase_prefix" "memcr_app_homekey_close" "Amazon" "" "$playbackPos_fun"
         sleep 1
                                       

#Step 6 code block for TC_MEMCR_MANUAL_09        
         

         execute_stepStatusUpdate_steps "6" "$testcase_prefix" "TC_MEMCR_MANUAL_03_step6" "Amazon" "" "" "$premiumApp_PID"
         sleep 1
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL"
      fi   
     

#Step 1 code block for TC_MEMCR_MANUAL_10


      if [[ "$TestcaseID" == "TC_MEMCR_MANUAL_10" ]]; then
         memcr_applaunch_common_teststep "$testcase_prefix" "Amazon" "$app_available_flag3"
    

#Step 2 code block for TC_MEMCR_MANUAL_10

        
         execute_stepStatusUpdate_steps "2" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step2" "Amazon"
         sleep 1
        

#Step 3 code block for TC_MEMCR_MANUAL_10


         playbackPos_fun=0
         execute_stepStatusUpdate_steps "3" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step3" "Amazon" "" "$playbackPos_fun"
         sleep 1
                  

#Step 4 code block for TC_MEMCR_MANUAL_10


         execute_stepStatusUpdate_steps "4" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step2" "Amazon"
         sleep 1
                          

#Step 5 code block for TC_MEMCR_MANUAL_10


         execute_stepStatusUpdate_steps "5" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step5" "Amazon"
         sleep 1
                         

#Step 6 code block for TC_MEMCR_MANUAL_10


         execute_stepStatusUpdate_steps "6" "$testcase_prefix" "TC_MEMCR_MANUAL_04_step2" "Amazon"
         sleep 1
         dynamic_current_step_finder "$testcase_prefix" "TC_MEMCR_MANUAL"
      fi

      #TestCase execution Result dynamic updating Function     
      dynamic_test_result_update "$current_step_num" "$TestcaseID" "${testcase_prefix}"

#Postcondition code block    

      printf '\nExecuting Post-condition Steps for Testcase : %s\n\n\n' "$TestcaseID"
      sleep 1
      postCondition_Execution_memcr "$TestcaseID" 
      postCondition_Execution_memcr_exit=$?

      if [ "$postCondition_Execution_memcr_exit" -eq 0 ]; then
         printf '\nPost-condition Execution Success. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
      else
         printf '\nPost-condition Execution failed. Exiting Test Case : %s\n\n\n\n' "$TestcaseID"
      fi      

   else
      printf '\n\nPremium Apps are unavailable, Pre-condition check failed. Exiting MEMCR test Execution!\n\n\n' 
   fi

}



#Function Definition for precondition checking of premium app hibernate or active state and destroy it



app_state_check_and_destroy() {

   local app_name="$1"
   printf "\n\n\nStep precondition check for hibernate or active %s App state\n\n\n" "$app_name"
   get_Premium_App_state "$app_name"
   local get_Premium_App_exit=$?

   if [[ "$get_Premium_App_exit" -eq 0 ]] || [[ "$hibernated_app_state" == 1 ]]; then
      destroy_app "$app_name"
      local destroy_app_exit=$?
      
      if [ "$destroy_app_exit" -eq 0 ]; then
         return 0
      else
         printf "\n\n\nDEBUG : destroy_app function failed with error code : %s\n\n" "$destroy_app_exit"
         return 1         
      fi
   else
      return 0
   fi

}



#Function Definition for postCondition checking of Memcr 


postCondition_Execution_memcr() {

   local testcaseID="$1"
   if [[ "$testcaseID" == "TC_MEMCR_MANUAL_02" ]]; then 
      destroy_app "YouTube"
      local destroy_app_exit=$?
      if [ "$destroy_app_exit" -eq 0 ]; then
         return 0
      else
         return 1
      fi
   fi
   if [[ "$testcaseID" == "TC_MEMCR_MANUAL_05" ]]; then 
      destroy_app "YouTubeTV"
      local destroy_app_exit=$?
      if [ "$destroy_app_exit" -eq 0 ]; then
         return 0
      else
         return 1
      fi
   fi
   if [[ "$testcaseID" == "TC_MEMCR_MANUAL_08" ]]; then 
      destroy_app "Amazon"
      local destroy_app_exit=$?
      if [ "$destroy_app_exit" -eq 0 ]; then
         return 0
      else
         return 1
      fi
   fi   
   if [[ "$testcaseID" == "TC_MEMCR_MANUAL_03" ]] || [[ "$testcaseID" == "TC_MEMCR_MANUAL_04" ]]; then
      destroy_app "YouTube"
      local destroy_app_exit_1=$?
      if [ "$destroy_app_exit_1" -eq 0 ] && cd /home/root; then
         printf "\n\n\nCurrent Working directory Changed to %s\n\n\n" "$(pwd)" 
         return 0
      else
         return 1
      fi
   elif [[ "$testcaseID" == "TC_MEMCR_MANUAL_06" ]] || [[ "$testcaseID" == "TC_MEMCR_MANUAL_07" ]]; then
       destroy_app "YouTubeTV"
      local destroy_app_exit_1=$?
      if [ "$destroy_app_exit_1" -eq 0 ] && cd /home/root; then
         printf "\n\n\nCurrent Working directory Changed to %s\n\n\n" "$(pwd)" 
         return 0
      else
         return 1
      fi
   elif [[ "$testcaseID" == "TC_MEMCR_MANUAL_09" ]] || [[ "$testcaseID" == "TC_MEMCR_MANUAL_10" ]]; then
       destroy_app "Amazon"
      local destroy_app_exit_1=$?
      if [ "$destroy_app_exit_1" -eq 0 ] && cd /home/root; then
         printf "\n\n\nCurrent Working directory Changed to %s\n\n\n" "$(pwd)" 
         return 0
      else
         return 1
      fi            
   else
      return 0
   fi

}




#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________




while true; do
   echo " "
   printf "\n=============================================================================================================================================================\n\n";
   echo "                                                      ******* MEMCR Automated Test *******                                                                    ";
   printf "=============================================================================================================================================================\n\n\n";
   printf '01. Run TestCase : TC_MEMCR_MANUAL_01        :\t[ Check the memcr status ] \n\n'
   printf '02. Run TestCase : TC_MEMCR_MANUAL_02        :\t[ Check the state of YouTube app after pressing the Home button post-launch ] \n\n'
   printf '03. Run TestCase : TC_MEMCR_MANUAL_03        :\t[ Verify whether memory usage decreases after pressing the Home button from YouTube App ] \n\n'
   printf '04. Run TestCase : TC_MEMCR_MANUAL_04        :\t[ Verify YouTube State Serialization after Hibernate and Resume ] \n\n'
   printf '05. Run TestCase : TC_MEMCR_MANUAL_05        :\t[ Check the state of YouTubeTV app after pressing the Home button post-launch ] \n\n'
   printf '06. Run TestCase : TC_MEMCR_MANUAL_06        :\t[ Verify whether memory usage decreases after pressing the Home button from YouTubeTV App ] \n\n'
   printf '07. Run TestCase : TC_MEMCR_MANUAL_07        :\t[ Verify YouTubeTV State Serialization after Hibernate and Resume ] \n\n'
   printf '08. Run TestCase : TC_MEMCR_MANUAL_08        :\t[ Check the state of Amazon app after pressing the Home button post-launch ] \n\n'
   printf '09. Run TestCase : TC_MEMCR_MANUAL_09        :\t[ Verify whether memory usage decreases after pressing the Home button from Amazon App ] \n\n'
   printf '10. Run TestCase : TC_MEMCR_MANUAL_10        :\t[ Verify Amazon State Serialization after Hibernate and Resume ] \n\n'
   printf '11. Show TestCase Execution Results\n\n'
   printf '12. Exit\n\n'
   printf "\n=============================================================================================================================================================\n\n\n";


   # ----- Main Testcaes Execution Menu -----

   
   read -p "Enter an Option to proceed : " menu_choice
   printf '\n\n\n'
   case "$menu_choice" in 
      1)
         exec_start "TC_MEMCR_MANUAL_01"
         tc_MEMCR_MANUAL_testsuite "tc1_step" "TC_MEMCR_MANUAL_01"
         ;;
      2)
         exec_start "TC_MEMCR_MANUAL_02"
         tc_MEMCR_MANUAL_testsuite "tc2_step" "TC_MEMCR_MANUAL_02"
         ;;
      3)
         exec_start "TC_MEMCR_MANUAL_03"
         tc_MEMCR_MANUAL_testsuite "tc3_step" "TC_MEMCR_MANUAL_03"
         ;;
      4)
         exec_start "TC_MEMCR_MANUAL_04"
         tc_MEMCR_MANUAL_testsuite "tc4_step" "TC_MEMCR_MANUAL_04"
         ;;
      5)
         exec_start "TC_MEMCR_MANUAL_05"
         tc_MEMCR_MANUAL_testsuite "tc5_step" "TC_MEMCR_MANUAL_05"
         ;;
      6)
         exec_start "TC_MEMCR_MANUAL_06"
         tc_MEMCR_MANUAL_testsuite "tc6_step" "TC_MEMCR_MANUAL_06"
         ;;
      7)
         exec_start "TC_MEMCR_MANUAL_07"
         tc_MEMCR_MANUAL_testsuite "tc7_step" "TC_MEMCR_MANUAL_07"
         ;;
      8)
         exec_start "TC_MEMCR_MANUAL_08"
         tc_MEMCR_MANUAL_testsuite "tc8_step" "TC_MEMCR_MANUAL_08"
         ;;
      9)
         exec_start "TC_MEMCR_MANUAL_09"
         tc_MEMCR_MANUAL_testsuite "tc9_step" "TC_MEMCR_MANUAL_09"
         ;;
      10)
         exec_start "TC_MEMCR_MANUAL_10"
         tc_MEMCR_MANUAL_testsuite "tc10_step" "TC_MEMCR_MANUAL_10"
         ;;                       
      11)
         testcase_result_display_menu "TC_MEMCR_MANUAL"  
         ;;       
      12)   
         printf '\nExiting MEMCR Automated Test\n\n\n' 
         break
         ;; 
      *)
         printf '\nInvalid option selected. Please Try Again !!!\n\n\n'
         ;;      
   esac
done  







#______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________





