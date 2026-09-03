#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
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
##########################################################################

# createTDKVTSPackage.sh - Rebuild VTS_Package_<timestamp>.tgz using a hardcoded
# module -> file mapping. No directory-structure guessing: for every module,
# each required file (binary + yamls) is searched for by name anywhere in
# the input tree, copied into that module's staging folder, and packed.
#
# Usage:
#   ./createTDKVTSPackage.sh <soc>
#
# Example:
#   sh createTDKVTSPackage.sh realtek
#
# Always reads from the current directory and writes
# VTS_Package_<soc>_<timestamp>.tgz into the current directory.
#
# Re-exec with bash if we weren't started with it (this script needs
# bash associative arrays, so plain 'sh'/'dash' won't work)
if [ -z "${BASH_VERSION:-}" ]; then
    exec bash "$0" "$@"
fi

set -eu
set -o pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <soc>" >&2
    echo "Supported SOCs: realtek, broadcom, amlogic, rpi4" >&2
    exit 1
fi

SOC="$1"

case "$SOC" in
    realtek|broadcom|amlogic|rpi4) ;;
    *)
        echo "Invalid SOC: $SOC" >&2
        echo "Supported SOCs: realtek, broadcom, amlogic, rpi4" >&2
        exit 1
        ;;
esac

INPUT="."
OUTDIR="."

WORK=$(mktemp -d)
TS=$(date +%d%m%Y_%H%M%S)
PKG_NAME="VTS_Package"
PKG_DIR="$WORK/$PKG_NAME"
mkdir -p "$PKG_DIR"

cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

# ---------------------------------------------------------------------------
# HARDCODED MAPPING: module name -> list of files that belong to it
# (binary + all yaml/yml files for that module)
# ---------------------------------------------------------------------------
declare -A MODULE_FILES
MODULE_FILES[deepsleep_manager]="hal_test_iarmmgrs-deepsleep-hal deepsleepmanagerWakeUpSources.yaml"
MODULE_FILES[device_settings]="hal_test_dshal Source_AudioSettings.yaml Source_VideoDevice.yaml Source_4K_VideoPort.yaml Source_4K_Display.yaml Source_HostSettings.yaml"
MODULE_FILES[hdmi_cec]="hal_test_RCECHal cec_responses.yml source_hdmiCEC.yml"
MODULE_FILES[power_manager]="hal_test_iarmmgrs-power-hal source_powerManager.yaml"
MODULE_FILES[rmf_audio_capture]="hal_test_rmfAudioCapture rmfAudioCaptureAuxNotSupported.yaml"

# Top-level files that go directly into VTS_Package/ (not inside a module tgz)
TOP_LEVEL_FILES="vts_version.txt libut_control.so"

# ---------------------------------------------------------------------------
# Step 1: get a working copy of the source tree
# ---------------------------------------------------------------------------
SRC="$WORK/src"
mkdir -p "$SRC"

if [ -d "$INPUT" ]; then
    cp -r "$INPUT"/. "$SRC"/
elif [[ "$INPUT" == *.tgz || "$INPUT" == *.tar.gz || "$INPUT" == *.tar ]]; then
    tar -xf "$INPUT" -C "$SRC"
else
    echo "Input must be a directory or a .tgz/.tar.gz/.tar file" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Step 2: for each module, find every required file anywhere in the tree
#         and copy it into that module's staging folder
# ---------------------------------------------------------------------------
STAGE="$WORK/stage"
mkdir -p "$STAGE"

for MODULE in "${!MODULE_FILES[@]}"; do
    MODULE_STAGE="$STAGE/$MODULE"

    MISSING=""
    created=false
    for FNAME in ${MODULE_FILES[$MODULE]}; do
        FOUND=$(find "$SRC" -type f -name "$FNAME" ! -path '*/lib/*' | head -n 1)
        if [ -n "$FOUND" ]; then
	    if ! $created; then
    	        mkdir -p "$MODULE_STAGE"
		created=true
	    fi
            cp "$FOUND" "$MODULE_STAGE/$FNAME"
        else
            MISSING="$MISSING $FNAME"
        fi
    done

    if [ -n "$MISSING" ]; then
        echo "WARNING: module '$MODULE' is missing:$MISSING" >&2
    fi

    # only tar the module if at least one file was actually found
    if [ -n "$(ls -A "$MODULE_STAGE" 2>/dev/null)" ]; then
	tar -czf "$PKG_DIR/${MODULE}_vts_bin.tgz" --mode=755 -C "$STAGE" "$MODULE"
        echo "Packed module: $MODULE"
    else
        echo "SKIPPED module: $MODULE (no files found at all)" >&2
    fi
done

# ---------------------------------------------------------------------------
# Step 3: top-level files (vts_version.txt, libut_control.so) go straight
#         into VTS_Package/ root
# ---------------------------------------------------------------------------
for FNAME in $TOP_LEVEL_FILES; do
    FOUND=$(find "$SRC" -maxdepth 2 -type f -name "$FNAME" ! -path '*/lib/*' | head -n 1)
    if [ -n "$FOUND" ]; then
        cp "$FOUND" "$PKG_DIR/$FNAME"
        echo "Carried over top-level file: $FNAME"
    fi
done

# ---------------------------------------------------------------------------
# Step 4: final package
# ---------------------------------------------------------------------------
OUT_TAR="$OUTDIR/VTS_Package_${SOC}_${TS}.tgz"
tar -czf "$OUT_TAR" -C "$WORK" "$PKG_NAME"

echo
echo "Created: $OUT_TAR"
echo
tar -tvf "$OUT_TAR"
