#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2024 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################

#Directory to migrate
DIRECTORY=""

#method to replace "((" to "(" in print statements
remove_extra_parenth()
{
temp_file="temp_file.py"
search_string="print(("
replace_string="print("

while IFS= read -r line; do
    # Check if the line contains the search string
    if [ -n "$(echo "$line" | grep "$search_string")" ]; then
        # Replace the search string with the replace string
        modified_line="${line//$search_string/$replace_string}"

        # Remove the last ");" from the modified line
        modified_line=$(echo "$modified_line" | sed 's/;$//')
        modified_line=$(echo "$modified_line" | sed 's/)$//')

        # Append the modified line to the temporary file
        echo "$modified_line" >> "$temp_file"
    else
        # If the line doesn't contain the search string, keep it unchanged
        echo "$line" >> "$temp_file"
    fi
done < "$file"

# Replace the original file with the temporary file
mv "$temp_file" "$file"

echo "Deleted all extra parenthesis in print statements."
}

FAILED_FILES=()

#To migrate a file given as commandline argument
if [ -n "$1" ]; then
    file=$1
    IFS=$'\n'
    if ! echo "$file" | grep -i -q ".py\>" ; then
        echo "Skipping $file ....."
        exit 1
    fi
    echo "Converting file: $file to python3..."
    echo "Commenting the java code.."
    sed -i "s/ip = <ipaddress>/#ip = <ipaddress>/" "$file"
    sed -i "s/port = <port>/#port = <port>/" "$file"
    echo "Running 2to3 tool...."
    RESPONSE=$('2to3' -w "$file")
    if [[ "$RESPONSE" =~ "Can't parse" ]]; then
        echo "Failed to parse the file: $file"
        echo "$RESPONSE"
        FAILED_FILES+=("$file")
    else
        remove_extra_parenth  
    fi
    echo "Reidenting the code for python3"
    reindent "$file"
    echo "Uncommenting the java code.."
    sed -i "s/#ip = <ipaddress>/ip = <ipaddress>/" "$file"
    sed -i "s/#port = <port>/port = <port>/" "$file"
      if [[ ${#FAILED_FILES[@]} -gt 0 ]]; then
          echo "Failed to parse below files:"
          printf '%s\n' "${FAILED_FILES[@]}"
      else
          expand -i -t 4 "$file" > /tmp/e && mv /tmp/e "$file"
          echo "Successfully Converted all the given files to python3"
      fi
else
    #Migrate all the files in the confugired directory
    if [ -d "$DIRECTORY" ]; then
      cd "$DIRECTORY" || exit 1
      IFS=$'\n'
      FILES=($(ls))
      for file in "${FILES[@]}"
          do
              if ! echo "$file" | grep -i -q ".py\>" ; then
                echo "Skipping $file ....."
                continue
              fi
              echo "Migrating file: $file to python3..."
              echo "Commenting the java code.."
              sed -i "s/ip = <ipaddress>/#ip = <ipaddress>/" "$file"
              sed -i "s/port = <port>/#port = <port>/" "$file"
              echo "Running 2to3 tool...."
              RESPONSE=$('2to3' -w "$file")
              if [[ "$RESPONSE" =~ "Can't parse" ]]; then
                echo "Failed to parse the file: $file"
                echo "$RESPONSE"
                FAILED_FILES+=("$file")
	      else
		  remove_extra_parenth
              fi
              echo "Reidenting the code for python3"
              reindent "$file"
              echo "Uncommenting the java code.."
              sed -i "s/#ip = <ipaddress>/ip = <ipaddress>/" "$file"
              sed -i "s/#port = <port>/port = <port>/" "$file"
        done
    if [[ ${#FAILED_FILES[@]} -gt 0 ]]; then
       echo "Failed to parse below files:"
       printf '%s\n' "${FAILED_FILES[@]}"
    else
       expand -i -t 4 "$file" > /tmp/e && mv /tmp/e "$file"
       echo "Successfully Converted all the given files to python3"
    fi
    unset IFS
  else
    echo "Please provide the correct directory"
  fi
fi


