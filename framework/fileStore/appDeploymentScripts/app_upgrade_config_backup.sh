#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's LICENSE
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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

# Default backup directory
default_backup_dir="/mnt/TM_BACKUP"
# Use the provided argument if given, otherwise use the default
backup_dir="${1:-$default_backup_dir}"

log_dir="${2:-$backup_dir/configBackupLogs}"

backup_dir="$backup_dir/tdkservice/fileStore"
# Create the log directory if it doesn't exist
mkdir -p "$log_dir"

# Log file path
log_file="/$log_dir/config_backup_$(date +%Y%m%d_%H%M%S).log"
echo "Starting script execution at $(date)" | tee -a "$log_file"

# ...existing code...
source_file_video="/opt/tomcat/webapps/tdkservice/fileStore/tdkvRDKServiceConfig/Video_Accelerator.config"
backup_dir_video="$backup_dir/tdkvRDKServiceConfig"
destination_dir_video="/opt/tomcat/webapps/tdkservice/fileStore/tdkvRDKServiceConfig/"
source_file_device="/opt/tomcat/webapps/tdkservice/fileStore/tdkvDeviceConfig/sampleDevice.config"
backup_dir_device="$backup_dir/tdkvDeviceConfig"
destination_dir_device="/opt/tomcat/webapps/tdkservice/fileStore/tdkvDeviceConfig/"
source_file_device_capabilities="/opt/tomcat/webapps/tdkservice/fileStore/tdkvDeviceCapabilities/Video_Accelerator_deviceCapability.ini"
backup_dir_device_capabilities="$backup_dir/tdkvDeviceCapabilities"
destination_dir_device_capabilities="/opt/tomcat/webapps/tdkservice/fileStore/tdkvDeviceCapabilities/"
backup_file_browser_validation="$backup_dir/BrowserPerformanceVariables.py"
source_file_browser_validation="/opt/tomcat/webapps/tdkservice/fileStore/BrowserPerformanceVariables.py"
destination_dir_browser_validation="/opt/tomcat/webapps/tdkservice/fileStore/"
backup_file_media_validation="$backup_dir/MediaValidationVariables.py"
source_file_media_validation="/opt/tomcat/webapps/tdkservice/fileStore/MediaValidationVariables.py"
destination_dir_media_validation="/opt/tomcat/webapps/tdkservice/fileStore/"
backup_file_performance_validation="$backup_dir/PerformanceTestVariables.py"
source_file_performance_validation="/opt/tomcat/webapps/tdkservice/fileStore/PerformanceTestVariables.py"
destination_dir_performance_validation="/opt/tomcat/webapps/tdkservice/fileStore/"
backup_file_stability_validation="$backup_dir/StabilityTestVariables.py"
source_file_stability_validation="/opt/tomcat/webapps/tdkservice/fileStore/StabilityTestVariables.py"
destination_dir_stability_validation="/opt/tomcat/webapps/tdkservice/fileStore/"
backup_file_vts_validation="$backup_dir/VTSTestVariables.py"
source_file_vts_validation="/opt/tomcat/webapps/tdkservice/fileStore/VTSTestVariables.py"
destination_dir_vts_validation="/opt/tomcat/webapps/tdkservice/fileStore/"

process_and_compare_backup_files() {
    local backup_file=$1
    local source_file=$2
    local destination_dir=$3
    echo "Processing backup file: $backup_file" | tee -a "$log_file"
    echo "Using source file: $source_file" | tee -a "$log_file"
    echo "Destination directory: $destination_dir" | tee -a "$log_file"
    if [ ! -f "$backup_file" ]; then
        echo "Warning: Backup file not found: $backup_file" | tee -a "$log_file"
        return
    fi
    declare -A backup_values
    declare -A section_map
    current_section=""
    # Read the backup file and store values in a map
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue  # Skip empty lines
        if [[ "$line" =~ ^\[.*\]$ ]]; then
            current_section="$line"  # Store section header
            section_map["$current_section"]="$current_section"
        elif [[ $line != \#* ]]; then
            key=$(echo "$line" | cut -d '=' -f 1 | xargs)
            value=$(echo "$line" | cut -d '=' -f 2- | xargs)
            if [[ -n "$key" ]]; then
                backup_values["$current_section|$key"]="$value"
            fi
        fi
    done < "$backup_file"
    local tmp_file=$(mktemp)
    current_section=""
    # Process source file and update backup file
    while IFS= read -r line; do
        if [[ -z "$line" ]]; then
            echo "" >> "$tmp_file"
            continue
        fi
        if [[ "$line" =~ ^\[.*\]$ ]]; then
            current_section="$line"  # Capture current section
            echo "$current_section" >> "$tmp_file"
        elif [[ $line != \#* ]]; then
            key=$(echo "$line" | cut -d '=' -f 1 | xargs)
            value=$(echo "$line" | cut -d '=' -f 2- | xargs)
            if [[ -n "${backup_values[$current_section|$key]}" ]]; then
                value="${backup_values[$current_section|$key]}"
                echo "$key = $value" >> "$tmp_file"
            else
                echo "$key = $value" >> "$tmp_file"
            fi
        else
            echo "$line" >> "$tmp_file"
        fi
    done < "$source_file"
    mv "$tmp_file" "$backup_file"
    cp "$backup_file" "$destination_dir"
    echo "Updated backup file: $backup_file" | tee -a "$log_file"
    echo "Copied to destination: $destination_dir" | tee -a "$log_file"
}


process_and_compare_backup_python_files() {
    local backup_file=$1
    local source_file=$2
    local destination_dir=$3

    echo "Processing backup file: $backup_file" | tee -a "$log_file"
    echo "Using source file: $source_file" | tee -a "$log_file"
    echo "Destination directory: $destination_dir" | tee -a "$log_file"

    if [ ! -f "$backup_file" ]; then
        echo "Warning: Backup file not found: $backup_file" | tee -a "$log_file"
        return
    fi

    # Collect source keys so backup-only keys can be inserted at their backup position.
    declare -A source_keys
    while IFS= read -r line || [[ -n $line ]]; do
        if [[ "$line" =~ ^[[:space:]]*([a-zA-Z_][a-zA-Z0-9_]*)[[:space:]]*= ]]; then
            source_keys["${BASH_REMATCH[1]}"]=1
        fi
    done < "$source_file"

    # Read complete values from the backup, including multiline lists.
    declare -A backup_values
    declare -A backup_keys
    backup_key_order=()
    active_key=""
    active_value=""
    active_closing_character=""
    while IFS= read -r line || [[ -n $line ]]; do
        if [[ -n "$active_key" ]]; then
            active_value+=$'\n'"$line"
            if [[ "$line" =~ ^[[:space:]]*"$active_closing_character"[[:space:]]*,?[[:space:]]*$ ]]; then
                backup_values["$active_key"]="$active_value"
                active_key=""
                active_value=""
                active_closing_character=""
            fi
            continue
        fi

        if [[ "$line" =~ ^[[:space:]]*([a-zA-Z_][a-zA-Z0-9_]*)[[:space:]]*=(.*)$ ]]; then
            key="${BASH_REMATCH[1]}"
            value="${BASH_REMATCH[2]}"
            value="${value#"${value%%[![:space:]]*}"}"
            value="${value%"${value##*[![:space:]]}"}"
            backup_values["$key"]="$value"

            if [[ -z "${backup_keys[$key]+x}" ]]; then
                backup_keys["$key"]=1
                backup_key_order+=("$key")
            fi

            case "${value:0:1}" in
                '[') active_closing_character=']' ;;
                '{') active_closing_character='}' ;;
                '(') active_closing_character=')' ;;
                *) active_closing_character="" ;;
            esac
            if [[ -n "$active_closing_character" && ! "$value" =~ "$active_closing_character"[[:space:]]*,?[[:space:]]*$ ]]; then
                active_key="$key"
                active_value="$value"
            fi
        fi
    done < "$backup_file"

    # Group backup-only keys after the nearest preceding key shared by both files.
    # Keys before the first shared key are emitted before the first source assignment.
    declare -A backup_only_after
    backup_only_before=""
    previous_shared_key=""
    for key in "${backup_key_order[@]}"; do
        if [[ -n "${source_keys[$key]+x}" ]]; then
            previous_shared_key="$key"
        elif [[ -n "$previous_shared_key" ]]; then
            backup_only_after["$previous_shared_key"]+="$key"$'\n'
        else
            backup_only_before+="$key"$'\n'
        fi
    done

    write_backup_only_keys() {
        local keys=$1
        local backup_only_key
        while IFS= read -r backup_only_key; do
            [[ -z "$backup_only_key" ]] && continue
            printf '%s = %s\n' "$backup_only_key" "${backup_values[$backup_only_key]}" >> "$tmp_file"
        done <<< "$keys"
    }

    # Prepare the temporary file for the updated content
    local tmp_file=$(mktemp)
    local first_source_assignment=true

    # Process the deployed source file and apply values from the backup.
    active_key=""
    active_source_block=""
    active_closing_character=""
    while IFS= read -r line || [[ -n $line ]]; do
        if [[ -n "$active_key" ]]; then
            active_source_block+=$'\n'"$line"
            if [[ "$line" =~ ^[[:space:]]*"$active_closing_character"[[:space:]]*,?[[:space:]]*$ ]]; then
                # Multi-line source blocks are never empty, so the source (upgrade default) always wins.
                printf '%s\n' "$active_source_block" >> "$tmp_file"
                write_backup_only_keys "${backup_only_after[$active_key]-}"
                active_key=""
                active_source_block=""
                active_closing_character=""
            fi
        elif [[ -z "$line" ]]; then
            echo "" >> "$tmp_file"  # Preserve blank lines
        elif [[ $line == \#* ]]; then
            echo "$line" >> "$tmp_file"  # Preserve comments
        elif [[ "$line" =~ ^[[:space:]]*([a-zA-Z_][a-zA-Z0-9_]*)[[:space:]]*=(.*)$ ]]; then
            key="${BASH_REMATCH[1]}"
            value="${BASH_REMATCH[2]}"
            if [[ "$first_source_assignment" == true ]]; then
                write_backup_only_keys "$backup_only_before"
                first_source_assignment=false
            fi
            case "${value#"${value%%[![:space:]]*}"}" in
                '['*) active_closing_character=']' ;;
                '{'*) active_closing_character='}' ;;
                '('*) active_closing_character=')' ;;
                *) active_closing_character="" ;;
            esac
            if [[ -n "$active_closing_character" && ! "$value" =~ "$active_closing_character"[[:space:]]*,?[[:space:]]*$ ]]; then
                active_key="$key"
                active_source_block="$line"
            else
                # Source (upgrade default) wins; use backup only when the source value is empty.
                trimmed_value="${value#"${value%%[![:space:]]*}"}"
                trimmed_value="${trimmed_value%"${trimmed_value##*[![:space:]]}"}"
                # Blank values and empty literals ("", '', [], {}, ()) count as empty.
                case "$trimmed_value" in
                    ""|'""'|"''"|"[]"|"{}"|"()") source_value_empty=true ;;
                    *) source_value_empty=false ;;
                esac
                if [[ "$source_value_empty" == true && -n "${backup_values[$key]+x}" ]]; then
                    printf '%s = %s\n' "$key" "${backup_values[$key]}" >> "$tmp_file"
                else
                    printf '%s\n' "$line" >> "$tmp_file"
                fi
            fi
            if [[ -z "$active_key" ]]; then
                write_backup_only_keys "${backup_only_after[$key]-}"
            fi
        else
            echo "$line" >> "$tmp_file"
        fi
    done < "$source_file"

    # If the source has no assignments, retain backup-only keys after its content.
    if [[ "$first_source_assignment" == true ]]; then
        write_backup_only_keys "$backup_only_before"
    fi

    # Restore the merged content without modifying the backup archive.
    cp "$tmp_file" "$destination_dir/$(basename "$backup_file")"
    rm -f "$tmp_file"

    echo "Preserved backup file: $backup_file" | tee -a "$log_file"
    echo "Restored file to: $destination_dir" | tee -a "$log_file"
}

process_all_pythons() {
    local backup_file=$1
    local source_file=$2
    local destination_dir=$3

    process_and_compare_backup_python_files "$backup_file" "$source_file" "$destination_dir"
}

# Excluded files
exclude_files=("sample_CI_Exec.config" "VA_SampleHP.config" "VA_SampleLP.config" "sample_deviceCapability.ini" "sampleThunderEnabled.config")
process_all_configs() {
    local backup_dir=$1
    local source_file=$2
    local destination_dir=$3
    local suffix=$4

    # Iterate over backup files in the directory
    for backup_file in "$backup_dir"/*"$suffix"; do
        # Extract the base name of the backup file
        base_name=$(basename "$backup_file")

        # Check if the file is in the exclude list
        if [[ " ${exclude_files[@]} " =~ " $base_name " ]]; then
            echo "Skipping excluded file: $base_name" | tee -a "$log_file"
            continue
        fi

        process_and_compare_backup_files "$backup_file" "$source_file" "$destination_dir"
    done
}


# Run config file processing in parallel
process_all_configs "$backup_dir_video" "$source_file_video" "$destination_dir_video" ".config" &
process_all_configs "$backup_dir_device" "$source_file_device" "$destination_dir_device" ".config" &
process_all_configs "$backup_dir_device_capabilities" "$source_file_device_capabilities" "$destination_dir_device_capabilities" "_deviceCapability.ini" &

# Run Python file processing in parallel
process_all_pythons "$backup_file_browser_validation" "$source_file_browser_validation" "$destination_dir_browser_validation" &
process_all_pythons "$backup_file_media_validation" "$source_file_media_validation" "$destination_dir_media_validation" &
process_all_pythons "$backup_file_performance_validation" "$source_file_performance_validation" "$destination_dir_performance_validation" &
process_all_pythons "$backup_file_stability_validation" "$source_file_stability_validation" "$destination_dir_stability_validation" &
process_all_pythons "$backup_file_vts_validation" "$source_file_vts_validation" "$destination_dir_vts_validation" &

# Wait for all background processes to complete
wait

# Copy logs folder from backup directory to fileStore location
backup_logs_dir="$backup_dir/logs"
destination_logs_dir="/opt/tomcat/webapps/tdkservice/fileStore/logs"

if [ -d "$backup_logs_dir" ]; then
    echo "Copying logs folder from backup directory to fileStore..." | tee -a "$log_file"
    echo "Source: $backup_logs_dir" | tee -a "$log_file"
    echo "Destination: $destination_logs_dir" | tee -a "$log_file"
    
    # Create destination directory if it doesn't exist
    mkdir -p "$destination_logs_dir"
    
    # Copy the logs folder contents
    cp -r "$backup_logs_dir"/* "$destination_logs_dir/" 2>/dev/null || {
        echo "Warning: No files found in logs directory or copy failed" | tee -a "$log_file"
    }
    
    echo "Logs folder copy completed successfully." | tee -a "$log_file"
else
    echo "Warning: Backup logs directory not found: $backup_logs_dir" | tee -a "$log_file"
fi

echo "All tasks completed."