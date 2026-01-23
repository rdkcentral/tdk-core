#!/bin/sh

# Configuration
BASE_DIR="/"
INSTALLER="InstallVTSPackage.sh"
TARGET_FOLDER="VTS_Package"
PACKAGE_PATH=$(ls ${BASE_DIR}VTS_Package*.tgz 2>/dev/null | head -n 1)

printf "\n\nStarting Workflow: checking the package files and installer file\n\n"
sleep 1

# 1. Check if the installer and package exist in /
if [ -f "$BASE_DIR/$INSTALLER" ] && [ -f "$PACKAGE_PATH" ]; then
    printf "\n\nVTS_package_installer\t:\t%s\n\nVTS_Package\t:\t%s\n\nBoth are available in %s directory. Package Installation started.....\n\n\n" "$INSTALLER" "$PACKAGE_PATH" "$BASE_DIR"
    
    cd "$BASE_DIR"
    chmod +x "$INSTALLER"
    sh "$INSTALLER"
    
    # Capture the exit code of the installer
    install_RC=$?

    if [ "$install_RC" -eq 0 ]; then
        printf "\n\n%s script execution finished and success\n\n" "$INSTALLER"
        if [ -d "$BASE_DIR/$TARGET_FOLDER" ]; then
            if [ "$(ls -A $BASE_DIR/$TARGET_FOLDER)" ]; then
                printf "\n\n'%s' directory exists and contains files! %s installation successfull\n\n\n" "$TARGET_FOLDER" "$PACKAGE_PATH"
                exit 0
            else
                printf "\n\nERROR : '%s' directory exists but it is EMPTY\n\n\n" "$TARGET_FOLDER"
                exit 1
            fi
        else
            printf "\n\nERROR : '%s' directory doesn't exist %s installation failed\n\n\n" "$TARGET_FOLDER" "$PACKAGE_PATH"
            exit 1
        fi        
    else
        printf "\n\nERROR : %s script execution failed with exit code %s\n\n" "$INSTALLER" "$install_RC"
        exit 1
    fi  
else
    printf "\n\nERROR: Missing installer or package in %s directory to proceed package installation\n\n\n" "$BASE_DIR"
    printf "\nChecked installer: %s\n\n" "${BASE_DIR}${INSTALLER}"
    printf "\nChecked package  : %s\n\n" "${PACKAGE_PATH:-<none found>}"
    exit 1
fi
