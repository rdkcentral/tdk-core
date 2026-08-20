#!/bin/bash

##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
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
##########################################################################

# Bolt Apps Bundle Generator
# Reads all app definitions from bundle-config.conf and generates signed bolt bundles.
# No external tools required beyond git and bash.

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Configuration
OUTPUT_DIR="generated-packages"
SIGNED_DIR="signed-packages"
BOLT_TOOLS_REPO_URL="https://github.com/rdkcentral/bolt-tools.git"
BOLT_TOOLS_CLONE_DIR="$PARENT_DIR/bolt-tools-cloned"
BOLT_CMD="$BOLT_TOOLS_CLONE_DIR/bolt/bin/bolt"
RALFPACK="$SCRIPT_DIR/ralfpack"
CERT_FILE="$SCRIPT_DIR/certs/$CERT_FILE"

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Generates signed bolt bundles for all apps defined in bundle-config.conf."
    echo "No external tools required beyond git and bash."
    echo ""
    echo "Options:"
    echo "  -c, --config <file>   Path to a custom .conf file (default: bundle-config.conf)"
    echo "  -a, --app <appId>     Generate bundle for a single app by its appId"
    echo "  -u, --base-url <url>  Override BASE_URL from config file"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Config file global settings:"
    echo "  BASE_URL=<url>          Base URL for hosted apps              (required)"
    echo "  VERSION=<version>       Default app version                   (required)"
    echo "  CERT_PASSPHRASE=<pass>  Certificate passphrase for signing    (required)"
    echo "  WPE_VERSION=<version>   WPE dependency version                (required)"
    echo "  DEV_MODE=true|false     Prepend --dev to all entry points     (optional, default: false)"
    echo ""
    echo "App entry format (one section per app):"
    echo "  [com.company.appid]"
    echo "  displayName=My App        Human-readable name                 (required)"
    echo "  appPath=myapp             Subfolder under BASE_URL            (optional)"
    echo "  entryFile=index.html      HTML filename, default: index.html  (optional)"
    echo "  entryPoint=https://...    Full URL override, ignores BASE_URL (optional)
  entryPoint=--dev https://... Full URL with --dev flag         (optional)
  devMode=true              Prepend --dev to the resolved URL  (optional)"
    echo ""
    echo "Entry point resolution (in order of precedence):"
    echo "  1. entryPoint set      -> used as-is"
    echo "  2. appPath + entryFile -> BASE_URL/appPath/entryFile"
    echo "  3. entryFile only      -> BASE_URL/entryFile"
    echo ""
    echo "Examples:"
    echo "  $0                                                       # all apps, default conf"
    echo "  $0 --app com.rdkcentral.webaudio                         # single app, default conf"
    echo "  $0 --config ./my-apps.conf                              # all apps, custom conf"
    echo "  $0 --config ./my-apps.conf --app com.rdkcentral.keytest # single app, custom conf"
    echo ""
    exit 1
}

# Clone and use bolt-tools from GitHub
ensure_bolt_tools() {
    echo "Cloning/updating bolt-tools from $BOLT_TOOLS_REPO_URL ..."

    if ! command -v git > /dev/null 2>&1; then
        echo "Error: git command is required to clone bolt-tools"
        exit 1
    fi

    if [ ! -d "$BOLT_TOOLS_CLONE_DIR/.git" ]; then
        echo "Cloning repository..."
        git clone "$BOLT_TOOLS_REPO_URL" "$BOLT_TOOLS_CLONE_DIR"
    else
        echo "Updating existing repository..."
        git -C "$BOLT_TOOLS_CLONE_DIR" pull --ff-only
    fi

    if [ ! -f "$BOLT_CMD" ]; then
        echo "Error: Cloned bolt-tools repository does not contain expected bolt binary"
        echo "Expected: $BOLT_CMD"
        exit 1
    fi

    if [ ! -f "$RALFPACK" ]; then
        echo "Error: ralfpack binary '$RALFPACK' not found"
        exit 1
    fi

    if [ ! -f "$CERT_FILE" ]; then
        echo "Error: Certificate file '$CERT_FILE' not found"
        exit 1
    fi

    echo "Resolved tooling:"
    echo "  bolt: $BOLT_CMD"
    echo "  ralfpack: $RALFPACK"
    echo "  cert: $CERT_FILE"
}

# Function to parse config file and process multiple apps
# Optional second argument: appId filter (process only that app)
# Optional third argument: BASE_URL override from command line
process_config_file() {
    local CONFIG_FILE="$1"
    local FILTER_APP_ID="${2:-}"
    local CMD_BASE_URL="${3:-}"
    local BASE_URL=""
    local CONFIG_VERSION="0.1.0"

    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Error: Config file '$CONFIG_FILE' not found"
        exit 1
    fi

    echo "Processing apps from config file: $CONFIG_FILE"
    echo ""

    # Read global settings
    local GLOBAL_DEV_MODE="false"
    while IFS='=' read -r key value || [ -n "$key" ]; do
        key="$(echo "$key" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
        value="$(echo "$value" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
        [[ "$key" =~ ^# ]] && continue
        [ "$key" = "BASE_URL" ]         && BASE_URL="$value"
        [ "$key" = "VERSION" ]          && CONFIG_VERSION="$value"
        [ "$key" = "CERT_PASSPHRASE" ]  && CERT_PASSPHRASE="$value"
        [ "$key" = "WPE_VERSION" ]      && WPE_VERSION="$value"
        [ "$key" = "DEV_MODE" ]         && GLOBAL_DEV_MODE="$value"
    done < "$CONFIG_FILE"

    # Command-line BASE_URL takes precedence over config file value
    if [ -n "$CMD_BASE_URL" ]; then
        BASE_URL="$CMD_BASE_URL"
    fi

    if [ -z "$BASE_URL" ]; then
        echo "Error: BASE_URL is required (set in config file or pass via --base-url)"
        exit 1
    fi
    if [[ ! "$BASE_URL" =~ ^https?:// ]]; then
        echo "Error: BASE_URL must be a valid HTTP/HTTPS URL"
        exit 1
    fi
    if [ -z "$CERT_PASSPHRASE" ]; then
        echo "Error: CERT_PASSPHRASE is required in config file"
        exit 1
    fi
    if [ -z "$WPE_VERSION" ]; then
        echo "Error: WPE_VERSION is required in config file"
        exit 1
    fi

    echo "Base URL: $BASE_URL"
    echo ""

    # Collect all app sections into arrays (keyed by app ID)
    declare -a APP_IDS=()
    declare -A APP_DISPLAY_NAMES=()
    declare -A APP_PATHS=()
    declare -A APP_ENTRY_FILES=()
    declare -A APP_ENTRY_POINTS=()
    declare -A APP_DEV_MODES=()
    declare -A APP_WEB_AUDIO=()

    local current_id=""
    while IFS= read -r line <&3 || [ -n "$line" ]; do
        line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
        [[ "$line" =~ ^# ]] && continue
        [ -z "$line" ] && continue

        if [[ "$line" =~ ^\[(.+)\]$ ]]; then
            current_id="${BASH_REMATCH[1]}"
            APP_IDS+=("$current_id")
        elif [ -n "$current_id" ] && [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            local k="${BASH_REMATCH[1]}" v="${BASH_REMATCH[2]}"
            k="$(echo "$k" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
            v="$(echo "$v" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
            [ "$k" = "displayName" ] && APP_DISPLAY_NAMES[$current_id]="$v"
            [ "$k" = "appPath" ]     && APP_PATHS[$current_id]="$v"
            [ "$k" = "entryFile" ]   && APP_ENTRY_FILES[$current_id]="$v"
            [ "$k" = "entryPoint" ]  && APP_ENTRY_POINTS[$current_id]="$v"
            [ "$k" = "devMode" ]     && APP_DEV_MODES[$current_id]="$v"
            [ "$k" = "webAudio" ]    && APP_WEB_AUDIO[$current_id]="$v"
        fi
    done 3< "$CONFIG_FILE"

    # Process each collected app
    local processed=0
    for APP_ID in "${APP_IDS[@]}"; do
        if [ -n "$FILTER_APP_ID" ] && [ "$APP_ID" != "$FILTER_APP_ID" ]; then
            continue
        fi

        local DISPLAY_NAME="${APP_DISPLAY_NAMES[$APP_ID]:-}"
        local APP_PATH="${APP_PATHS[$APP_ID]:-}"
        local ENTRY_FILE="${APP_ENTRY_FILES[$APP_ID]:-index.html}"
        local ENTRY_POINT_OVERRIDE="${APP_ENTRY_POINTS[$APP_ID]:-}"
        local DEV_MODE="${APP_DEV_MODES[$APP_ID]:-}"
        local WEB_AUDIO="${APP_WEB_AUDIO[$APP_ID]:-}"

        if [ -z "$DISPLAY_NAME" ]; then
            echo "Error: Missing displayName for app '$APP_ID'"
            exit 1
        fi

        if [ -n "$ENTRY_POINT_OVERRIDE" ]; then
            ENTRY_POINT="$ENTRY_POINT_OVERRIDE"
        elif [ -n "$APP_PATH" ]; then
            ENTRY_POINT="$BASE_URL/$APP_PATH/$ENTRY_FILE"
        else
            ENTRY_POINT="$BASE_URL/$ENTRY_FILE"
        fi

        # Prepend --dev if devMode=true (per-app) or DEV_MODE=true (global) and not already set
        if { [ "$DEV_MODE" = "true" ] || [ "$GLOBAL_DEV_MODE" = "true" ]; } && [[ ! "$ENTRY_POINT" =~ ^--dev ]]; then
            ENTRY_POINT="--dev $ENTRY_POINT"
        fi

        echo "=========================================="
        echo "Processing app: $DISPLAY_NAME"
        echo "  App ID: $APP_ID"
        echo "  Entry Point: $ENTRY_POINT"
        echo "  Version: $CONFIG_VERSION"
        echo "=========================================="
        echo ""

        process_single_app "$ENTRY_POINT" "$APP_ID" "$DISPLAY_NAME" "$CONFIG_VERSION" "$WEB_AUDIO"
        processed=$((processed + 1))
    done

    if [ "$processed" -eq 0 ]; then
        echo "Warning: No apps processed — app '$FILTER_APP_ID' not found in config"
        return
    fi

    # Sign all packages at once after all bolt files are built
    sign_package

    echo ""
    echo "=== All Apps Processed Successfully ==="
}

# Function to process a single app
process_single_app() {
    local ENTRY_POINT="$1"
    local APP_ID="$2"
    local APP_NAME="$3"
    local VERSION="$4"
    local WEB_AUDIO="${5:-}"

    # Validate inputs
    validate_inputs
    
    # Create the package
    create_app_archive
    generate_json_config
    create_bolt_package

    # Cleanup
    cleanup

    echo "✓ Bolt package created: $OUTPUT_DIR/${APP_ID}+${VERSION}.bolt"
    echo ""
}

# Function to validate inputs
validate_inputs() {
    # Validate entry point URL (optionally prefixed with --dev)
    if [[ ! "$ENTRY_POINT" =~ ^(--dev[[:space:]]+)?https?:// ]]; then
        echo "Error: Entry point must be a valid HTTP/HTTPS URL (optionally prefixed with --dev)"
        echo "Provided: $ENTRY_POINT"
        exit 1
    fi

    if [ ! -f "$BOLT_CMD" ]; then
        echo "Error: bolt executable '$BOLT_CMD' not found"
        exit 1
    fi

    if [ ! -f "$RALFPACK" ]; then
        echo "Error: ralfpack binary '$RALFPACK' not found"
        exit 1
    fi

    # Validate app ID format
    if [[ ! "$APP_ID" =~ ^[a-zA-Z0-9.-]+$ ]]; then
        echo "Error: App ID '$APP_ID' contains invalid characters"
        echo "Use only letters, numbers, dots, and hyphens"
        exit 1
    fi
}

# Function to create app archive
create_app_archive() {
    ARCHIVE_FILE="empty.tgz"
    if [ ! -f "$ARCHIVE_FILE" ]; then
        echo "Creating empty archive..."
        tar -czf "$ARCHIVE_FILE" -T /dev/null
    else
        echo "Reusing existing empty archive: $ARCHIVE_FILE"
    fi
}

# Function to generate JSON configuration
generate_json_config() {
    echo "Generating JSON configuration..."
    
    JSON_FILE="${APP_ID}.json"
    
    cat > "$JSON_FILE" << EOF
{
  "id": "$APP_ID",
  "version": "$VERSION",
  "versionName": "generated",
  "name": "$APP_NAME",
  "packageType": "application",
  "packageSpecifier": "html",
  "entryPoint": "$ENTRY_POINT",
  "dependencies": {
    "com.rdkcentral.wpe": "$WPE_VERSION"
  },
  "permissions": [
    "urn:rdk:permission:internet",
    "urn:rdk:permission:firebolt",
    "urn:rdk:permission:thunder",
    "urn:rdk:permission:rialto"
  ],
  "configuration": $([ "$WEB_AUDIO" = "true" ] && echo '{
    "urn:rdk:config:overrides": {
      "application": {
        "options": {
          "webAudio": true
        }
      }
    }
  }' || echo '{}')
}
EOF
    
    echo "JSON configuration created: $JSON_FILE"
    echo "Entry point: $ENTRY_POINT"
}

# Function to create bolt package
create_bolt_package() {
    echo "Creating bolt package..."
    
    mkdir -p "$OUTPUT_DIR"
    
    # Use the archive file we created
    "$BOLT_CMD" pack "$JSON_FILE" "$ARCHIVE_FILE"
    
    # Move the generated .bolt file to output directory
    BOLT_FILE="${APP_ID}+${VERSION}.bolt"
    if [ -f "$BOLT_FILE" ]; then
        mv "$BOLT_FILE" "$OUTPUT_DIR/"
        echo "Bolt package created: $OUTPUT_DIR/$BOLT_FILE"
    else
        echo "Error: Expected bolt package '$BOLT_FILE' was not created"
        exit 1
    fi
}

# Function to sign the package
sign_package() {
    echo "Signing the package..."

    mkdir -p "$SIGNED_DIR"

    local ABS_CERT_FILE
    ABS_CERT_FILE=$(cd "$(dirname "$CERT_FILE")" && pwd)/$(basename "$CERT_FILE")
    local ABS_OUTPUT_DIR="$(pwd)/$OUTPUT_DIR"
    local ABS_SIGNED_DIR="$(pwd)/$SIGNED_DIR"
    local ABS_RALFPACK
    ABS_RALFPACK=$(realpath "$RALFPACK")

    # Find all *.bolt packages in the output directory
    local PKGS=("$ABS_OUTPUT_DIR"/*.bolt)
    if [ ! -e "${PKGS[0]}" ]; then
        echo "Error: No *.bolt packages found in '$ABS_OUTPUT_DIR'"
        exit 1
    fi

    echo "Found ${#PKGS[@]} package(s) to sign"
    echo ""

    for pkg in "${PKGS[@]}"; do
        local pkg_name
        pkg_name=$(basename "$pkg")
        echo "Signing $pkg_name..."

        cp "$pkg" "$ABS_SIGNED_DIR/$pkg_name"

        (
            cd "$ABS_SIGNED_DIR"
            "$ABS_RALFPACK" sign --pkcs12="$ABS_CERT_FILE" --passphrase="$CERT_PASSPHRASE" "$pkg_name"
        )
        echo "Success..."
    done

    echo ""
    echo "All packages signed successfully!"
    echo "Package signed and available in: $SIGNED_DIR"
}

# Function to cleanup temporary files
cleanup() {
    echo "Cleaning up temporary files..."
    if [ -f "$JSON_FILE" ]; then
        rm "$JSON_FILE"
    fi
}

# Main script logic
main() {
    echo "=== Bolt Lightning Apps Bundle Generator ==="
    echo ""

    # Default config file path
    DEFAULT_CONFIG_FILE="$SCRIPT_DIR/bundle-config.conf"

    # Check for help
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        usage
    fi

    # Parse options
    local CONFIG_FILE="$DEFAULT_CONFIG_FILE"
    local FILTER_APP_ID=""
    local CMD_BASE_URL=""

    while [ $# -gt 0 ]; do
        case "$1" in
            --config|-c)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --app|-a)
                FILTER_APP_ID="$2"
                shift 2
                ;;
            --base-url|-u)
                CMD_BASE_URL="$2"
                shift 2
                ;;
            *)
                echo "Error: Unknown option '$1'"
                usage
                ;;
        esac
    done

    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Error: Config file '$CONFIG_FILE' not found"
        usage
    fi

    if [ -n "$FILTER_APP_ID" ]; then
        echo "Using config: $CONFIG_FILE"
        echo "Generating bundle for single app: $FILTER_APP_ID"
    else
        echo "Using config: $CONFIG_FILE"
    fi
    if [ -n "$CMD_BASE_URL" ]; then
        echo "BASE_URL override (cmd line): $CMD_BASE_URL"
    fi
    echo ""

    # Resolve bolt/signing tooling (clone from GitHub if needed)
    ensure_bolt_tools

    # Process apps (all or filtered by --app)
    process_config_file "$CONFIG_FILE" "$FILTER_APP_ID" "$CMD_BASE_URL"
}

# Run the main function
main "$@"
