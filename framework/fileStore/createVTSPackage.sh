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

platform=$1
platform="${platform,,}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VTSVARS="${SCRIPT_DIR}/VTSTestVariables.py"

if [[ "$platform" == "realtek" ]];then
     platform_repo="https://code.rdkcentral.com/r/collaboration/soc/realtek/rdk/tdk-video"
elif [[ "$platform" == "amlogic" ]];then
     platform_repo="https://code.rdkcentral.com/r/collaboration/soc/amlogic/rdk/tdk-video"
elif [[ "$platform" == "broadcom" ]];then
     platform_repo="https://code.rdkcentral.com/r/collaboration/soc/broadcom/rdk/tdk-video"
elif [[ "$platform" == "rpi4" ]];then
     platform_repo="https://github.com/rdkcentral/tdk-video-raspberrypi"
else
     echo "ERROR : Unable to obtain platform repo for this vendor"
     exit
fi

# ---------------------------------------------------------------------------
# run_compile: invoke vts_compile.sh with the current platform so a fresh
# generic package is built immediately after configure_vts.txt is synced.
# ---------------------------------------------------------------------------
run_compile() {
    local compile_script="${SCRIPT_DIR}/vtsPackageUtilities/vts_compile.sh"
    if [ ! -f "$compile_script" ]; then
        echo "WARNING: vts_compile.sh not found at $compile_script — skipping auto-compile"
        return 0
    fi
    echo -e "\n#--- Launching vts_compile.sh $platform ---#"
    cd "${SCRIPT_DIR}/vtsPackageUtilities"
    bash vts_compile.sh "$platform"
    local rc=$?
    cd "$SCRIPT_DIR"
    if [ $rc -ne 0 ]; then
        echo "ERROR: vts_compile.sh failed (exit $rc)"
        # Find the latest log file and print the last 30 lines so the exact
        # error is visible without having to open the log manually.
        local latest_log
        latest_log=$(ls -t "${SCRIPT_DIR}/vtsPackageUtilities/logs/"*.log 2>/dev/null | head -n1)
        if [ -n "$latest_log" ]; then
            echo -e "\n--- Last 30 lines of $latest_log ---"
            tail -n 30 "$latest_log"
            echo "--- End of log ---"
        fi
        exit $rc
    fi
    echo -e "#--- vts_compile.sh completed successfully ---#\n"
}

# ---------------------------------------------------------------------------
# Version verification: cross-check vts_version.txt inside the generic package
# against HPK_VERSION and any per-module overrides in VTSTestVariables.py.
# ---------------------------------------------------------------------------

# Read a value from vts_version.txt content ("key = value" format).
_pkg_ver() { printf '%s' "$1" | grep -m1 "^${2} =" | awk -F' = ' '{print $2}' | tr -d ' \r'; }

# Read a Python string variable from VTSTestVariables.py.
_py_var() {
    python3 - "$1" "$2" 2>/dev/null <<'PYEOF'
import re, sys
path, var = sys.argv[1], sys.argv[2]
with open(path) as f:
    for line in f:
        m = re.match(r'^' + re.escape(var) + r'\s*=\s*["\']?(.*?)["\']?\s*$', line.strip())
        if m:
            val = m.group(1).strip().strip('"').strip("'")
            print(val)
            break
PYEOF
}

# ---------------------------------------------------------------------------
# sync_configure_vts: propagate HPK_VERSION and all *_OVERRIDE values from
# VTSTestVariables.py into vtsPackageUtilities/configure_vts.txt so the next
# vts_compile.sh run uses the same versions.
# ---------------------------------------------------------------------------
sync_configure_vts() {
    local vtsvars="$1"
    local cfg="${SCRIPT_DIR}/vtsPackageUtilities/configure_vts.txt"

    if [ ! -f "$vtsvars" ] || [ ! -f "$cfg" ]; then
        echo "WARNING: Cannot sync configure_vts.txt — file(s) missing"
        return 0
    fi

    echo -e "\n#--- Syncing configure_vts.txt from VTSTestVariables.py ---#"

    # HPK_VERSION (always present, no comment toggle needed)
    local hpk
    hpk=$(_py_var "$vtsvars" "HPK_VERSION")
    if [ -n "$hpk" ]; then
        sed -i "s|^HPK_VERSION=.*|HPK_VERSION=${hpk}|" "$cfg"
        echo "  SET  : HPK_VERSION = $hpk"
    fi

    # DEVICE_TYPE (always present, no comment toggle needed)
    local device_type
    device_type=$(_py_var "$vtsvars" "DEVICE_TYPE")
    if [ -n "$device_type" ]; then
        sed -i "s|^DEVICE_TYPE=.*|DEVICE_TYPE=${device_type}|" "$cfg"
        echo "  SET  : DEVICE_TYPE = $device_type"
    fi

    # Per-module test version overrides
    for entry in \
        "DS_HAL_TEST_VERSION_OVERRIDE" \
        "DEEPSLEEP_HAL_TEST_VERSION_OVERRIDE" \
        "POWER_HAL_TEST_VERSION_OVERRIDE" \
        "HDMICEC_HAL_TEST_VERSION_OVERRIDE" \
        "RMF_AUDIO_CAPTURE_HAL_TEST_VERSION_OVERRIDE"
    do
        local val
        val=$(_py_var "$vtsvars" "$entry")
        if [ -n "$val" ]; then
            sed -i "s|^#*${entry}=.*|${entry}=${val}|" "$cfg"
            echo "  SET  : $entry = $val"
        else
            sed -i "s|^${entry}=.*|#${entry}=|" "$cfg"
            echo "  CLEAR: $entry (empty — HPK-derived)"
        fi
    done

    # Per-module header version overrides
    for entry in \
        "DS_HAL_HEADER_VERSION_OVERRIDE" \
        "DEEPSLEEP_HAL_HEADER_VERSION_OVERRIDE" \
        "POWER_HAL_HEADER_VERSION_OVERRIDE" \
        "HDMICEC_HAL_HEADER_VERSION_OVERRIDE" \
        "RMF_AUDIO_CAPTURE_HAL_HEADER_VERSION_OVERRIDE"
    do
        local val
        val=$(_py_var "$vtsvars" "$entry")
        if [ -n "$val" ]; then
            sed -i "s|^#*${entry}=.*|${entry}=${val}|" "$cfg"
            echo "  SET  : $entry = $val"
        else
            sed -i "s|^${entry}=.*|#${entry}=|" "$cfg"
            echo "  CLEAR: $entry (empty — HPK-derived)"
        fi
    done

    echo -e "#--- configure_vts.txt updated ---#\n"
}

verify_versions() {
    local pkg_path="$1"
    local vtsvars="$2"

    echo -e "\n#--- Verifying package versions against VTSTestVariables.py ---#"

    if [ ! -f "$vtsvars" ]; then
        echo "WARNING: VTSTestVariables.py not found at $vtsvars — skipping version check"
        return 0
    fi

    local vts_ver
    vts_ver=$(tar -xOf "$pkg_path" VTS_Package/vts_version.txt 2>/dev/null) || {
        echo "WARNING: vts_version.txt not found in package — skipping version check"
        return 0
    }

    local errors=0

    # Always check HPK version
    local cfg_hpk pkg_hpk
    cfg_hpk=$(_py_var "$vtsvars" "HPK_VERSION")
    pkg_hpk=$(_pkg_ver "$vts_ver" "HPK_version")
    if [ "$cfg_hpk" = "$pkg_hpk" ]; then
        echo "  OK   : HPK_version = $pkg_hpk"
    else
        echo "  ERROR: HPK_version mismatch — VTSTestVariables.py: '$cfg_hpk', package: '$pkg_hpk'"
        errors=$((errors+1))
    fi

    # Per-module test version overrides — only verified when a non-empty override is configured
    local override pkg_val var_name pkg_key
    for entry in \
        "DS_HAL_TEST_VERSION_OVERRIDE:rdk-halif-test-device_settings" \
        "DEEPSLEEP_HAL_TEST_VERSION_OVERRIDE:rdk-halif-test-deepsleep_manager" \
        "POWER_HAL_TEST_VERSION_OVERRIDE:rdk-halif-test-power_manager" \
        "HDMICEC_HAL_TEST_VERSION_OVERRIDE:rdk-halif-test-hdmi_cec" \
        "RMF_AUDIO_CAPTURE_HAL_TEST_VERSION_OVERRIDE:rdk-halif-test-rmf_audio_capture"
    do
        var_name="${entry%%:*}"
        pkg_key="${entry##*:}"
        override=$(_py_var "$vtsvars" "$var_name")
        pkg_val=$(_pkg_ver "$vts_ver" "$pkg_key")
        if [ -z "$override" ]; then
            echo "  INFO : $pkg_key — no override configured, package has: $pkg_val"
        elif [ "$override" = "$pkg_val" ]; then
            echo "  OK   : $pkg_key = $pkg_val (override matches)"
        else
            echo "  ERROR: $pkg_key mismatch — override: '$override', package: '$pkg_val'"
            echo "MISMATCH - $pkg_key"
            errors=$((errors+1))
        fi
    done

    # Per-module HAL header version overrides — only verified when a non-empty override is configured
    for entry in \
        "DS_HAL_HEADER_VERSION_OVERRIDE:rdk-halif-device_settings" \
        "DEEPSLEEP_HAL_HEADER_VERSION_OVERRIDE:rdk-halif-deepsleep_manager" \
        "POWER_HAL_HEADER_VERSION_OVERRIDE:rdk-halif-power_manager" \
        "HDMICEC_HAL_HEADER_VERSION_OVERRIDE:rdk-halif-hdmi_cec" \
        "RMF_AUDIO_CAPTURE_HAL_HEADER_VERSION_OVERRIDE:rdk-halif-rmf_audio_capture"
    do
        var_name="${entry%%:*}"
        pkg_key="${entry##*:}"
        override=$(_py_var "$vtsvars" "$var_name")
        pkg_val=$(_pkg_ver "$vts_ver" "$pkg_key")
        if [ -z "$override" ]; then
            echo "  INFO : $pkg_key (header) — no override configured, package has: $pkg_val"
        elif [ "$override" = "$pkg_val" ]; then
            echo "  OK   : $pkg_key (header) = $pkg_val (override matches)"
        else
            echo "  ERROR: $pkg_key (header) mismatch — override: '$override', package: '$pkg_val'"
            echo "MISMATCH - $pkg_key (header)"
            errors=$((errors+1))
        fi
    done

    if [ "$errors" -gt 0 ]; then
        echo -e "\nERROR: $errors version mismatch(es) found. Rebuild the VTS package with matching versions."
        sync_configure_vts "$vtsvars"
        run_compile
        exit 1
    fi
    echo -e "#--- Version verification PASSED ---#\n"
}

#Check if Generic VTS Package is present
GENERIC_PACKAGE=$(ls -t vts_packages/Generic_VTS_Package*.tgz 2>/dev/null | head -n1)
if [ -z "$GENERIC_PACKAGE" ];then
    echo "Generic VTS Package not present in fileStore"
    # Check if SDK install script is present before attempting to build
    SDK_INSTALL_SCRIPT=$(grep -m1 "^SDK_INSTALL_SCRIPT=" "${SCRIPT_DIR}/vtsPackageUtilities/configure_vts.txt" 2>/dev/null | cut -d'=' -f2 | tr -d ' \r')
    if [ -n "$SDK_INSTALL_SCRIPT" ] && [ -f "${SCRIPT_DIR}/vtsPackageUtilities/${SDK_INSTALL_SCRIPT}" ]; then
        echo "SDK install script found: ${SCRIPT_DIR}/${SDK_INSTALL_SCRIPT}"
        echo "Attempting to create new VTS package..."
        echo "Updating configure_vts.txt with versions from VTSTestVariables.py for next compile run..."
        sync_configure_vts "$VTSVARS"
        run_compile
    else
        echo "ERROR: Generic VTS Package not found in fileStore. Please upload the Generic VTS Package and retry."
        exit 1
    fi
    exit
fi
GENERIC_PACKAGE_PATH="$GENERIC_PACKAGE"
GENERIC_PACKAGE=$(basename "$GENERIC_PACKAGE")
echo "Creating package using $GENERIC_PACKAGE"

verify_versions "$GENERIC_PACKAGE_PATH" "$VTSVARS"

system_date=$(date)
formatted_date=$(echo "$system_date" | awk '{ printf "%02d%02d%04d_%02d%02d%02d\n", $3, (index("JanFebMarAprMayJunJulAugSepOctNovDec", $2)+2)/3, $6, substr($4,1,2), substr($4,4,2), substr($4,7,2) }')

# If DEVICE_TYPE is SINK, skip platform repo clone and all binary extraction.
# Just deliver the generic package directly under vts_packages/$platform/.
DEVICE_TYPE=$(_py_var "$VTSVARS" "DEVICE_TYPE")
if [ "${DEVICE_TYPE}" = "SINK" ]; then
    echo "DEVICE_TYPE=SINK: skipping platform repo clone — copying generic package directly"
    mkdir -p "vts_packages/${platform}"
    sink_pkg="vts_packages/${platform}/VTS_Package_${platform}_Sink_${formatted_date}.tgz"
    cp "$GENERIC_PACKAGE_PATH" "$sink_pkg"
    echo "Created ${sink_pkg} successfully"
    exit 0
fi

#Create temp directory
cd vts_packages
mkdir -p $platform
cd $platform
temp_dir="${platform}_${formatted_date}"
echo "Creating package in $temp_dir"
mkdir $temp_dir
cd $temp_dir

if [[ ! -d "../tdk_${platform}_repo" ]];then
    # ── Clone the platform repo ───────────────────────────────────────────
    # Credentials (if the repo is private) are expected to be provided via
    # the user's ~/.netrc file. Add entries such as:
    #     machine github.com          login <user> password <token>
    #     machine code.rdkcentral.com login <user> password <password>
    # then run: chmod 600 ~/.netrc
    echo "Cloning $platform_repo ..."
    git clone "$platform_repo" "tdk_${platform}_repo" >/dev/null 2>&1

    # ── Check clone result ────────────────────────────────────────────────
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to clone the repository: $platform_repo"
        echo "       If this is a private repository, ensure your credentials"
        echo "       are configured in ~/.netrc, for example:"
        if [[ "$platform_repo" == *"code.rdkcentral.com"* ]]; then
            echo "         machine code.rdkcentral.com login <user> password <password>"
        elif [[ "$platform_repo" == *"github.com"* ]]; then
            echo "         machine github.com login <user> password <token>"
        fi
        echo "       then run: chmod 600 ~/.netrc"
        cd ..
        rm -rf "$temp_dir"
        exit 1
    fi
    echo -e "\nCloned platform repo: $platform_repo"
else
    cp -r "../tdk_${platform}_repo" .
    echo -e "\nCopied platform repo"
fi

echo `pwd`
ls

#Creating Vendor specific TDK package
#Copy generic package into $temp_dir
cp ../../$GENERIC_PACKAGE .
tar -xvf $GENERIC_PACKAGE >/dev/null 2>&1
cd VTS_Package
for file in *vts_bin.tgz*; do
    tar -xvf "$file" >/dev/null 2>&1
done
rm -rf *vts_bin.tgz
for dir in */; do
    if [[ "$dir" != "tdk_${platform}_repo/" ]];then
	 echo -e "\nProcessing $dir"
	 if [ -d "../tdk_${platform}_repo/VTS_profiles/RDK9/$dir" ];then
	      echo -e "Copying VTS_profiles/RDK9/$dir yaml files"
	      cp ../tdk_${platform}_repo/VTS_profiles/RDK9/$dir/* $dir/
	      rm -rf $dir/libraries.txt
	      rm -rf $dir/lib/
	      if [ ! -f "libut_control.so" ];then
		     echo "Copying libut_control.so"
		     cp $dir/libut_control.so .
	      fi
	      rm $dir/lib*.so
	 fi
    fi
done
tar -cvzf device_settings_vts_bin.tgz device_settings >/dev/null 2>&1
tar -cvzf deepsleep_manager_vts_bin.tgz deepsleep_manager >/dev/null 2>&1
tar -cvzf power_manager_vts_bin.tgz power_manager >/dev/null 2>&1
tar -cvzf rmf_audio_capture_vts_bin.tgz rmf_audio_capture >/dev/null 2>&1
tar -cvzf hdmi_cec_vts_bin.tgz hdmi_cec >/dev/null 2>&1
for dir in */; do
    if [ -d "$dir" ]; then
	 rm -rf $dir
    fi
done
cd ..
rm -rf tdk_${platform}_repo $GENERIC_PACKAGE
tar -cvzf VTS_Package_${platform}_${formatted_date}.tgz * >/dev/null 2>&1
cd ..
cp $temp_dir/VTS_Package_${platform}_${formatted_date}.tgz .
echo "Created VTS_Package_${platform}_${formatted_date}.tgz successfully"


#Cleanup
rm -r $temp_dir
