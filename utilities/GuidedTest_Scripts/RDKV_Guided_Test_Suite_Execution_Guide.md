# RDKV Guided Test Suite — Execution Guide

> **Version**: 1.0 | **Platform**: RDK-V (Video Accelerator, RPI-Client) | **Execution Environment**: DUT Serial/SSH Console | **Execution Model**: Guided (Partially Automated)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Repository Structure](#2-repository-structure)
3. [Prerequisites](#3-prerequisites)
4. [Deploying Files to the DUT](#4-deploying-files-to-the-dut)
5. [Configuring device.conf](#5-configuring-deviceconf)
   - [5.1 Common Parameters — All Modules](#51-common-parameters--all-modules)
   - [5.2 Module-Specific Parameters](#52-module-specific-parameters)
6. [Running a Test Script — Step-by-Step](#6-running-a-test-script--step-by-step)
7. [Test Module Reference](#7-test-module-reference)
   - [7.1 BT Audio (External Audio)](#71-bt-audio-external-audio)
   - [7.2 HDCP Compliance](#72-hdcp-compliance)
   - [7.3 Image Formats](#73-image-formats)
   - [7.4 IPv6](#74-ipv6)
   - [7.5 MEMCR](#75-memcr)
   - [7.6 Power Management](#76-power-management)
   - [7.7 System](#77-system)
   - [7.8 WebAudio](#78-webaudio)
   - [7.9 XCONF Image Upgrade](#79-xconf-image-upgrade) *(v1: 1 TC — additional TCs planned)*
8. [Test Results and Logs](#8-test-results-and-logs)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Overview

The **RDKV Guided Test Suite** is a collection of interactive shell scripts designed to validate RDK-V platform capabilities across multiple feature modules. Each script provides a numbered menu allowing the tester to select and execute individual test cases against a live RDK-V DUT (Device Under Test).

### Execution Model — Guided (Partially Automated)

These scripts are **not fully automated** and are **not fully manual** — they follow a **Guided Test** execution model, which is a form of partial automation. Understanding this distinction is important before running any script.

| Step Type | Description | Tester Action Required? |
|-----------|-------------|-------------------------|
| **Automated** | The script executes device-side API calls (JSON-RPC/curl), parses the response, and validates the result entirely on its own — no tester involvement needed. | No — script proceeds automatically |
| **Guided (Prompted)** | The script reaches a checkpoint where the outcome cannot be verified programmatically (e.g., audio is audible, video is rendering, a visual element is visible on the TV display). The script **pauses and displays a `[yes/no]` prompt**. The tester must observe the DUT/display, then type `yes` or `no` and press Enter to continue. | **Yes — tester must respond** |
| **Visual / Auditory Only** | Some test cases are entirely observation-based (e.g., confirming BT audio is heard, verifying image rendering on screen). These steps are driven by the tester's real-time observation of the connected TV/display or audio output. | **Yes — tester must observe and confirm** |

> **In summary**: The script handles all device interactions and API calls automatically. The tester is involved **only** at specific checkpoints where human observation is the only way to verify the outcome — for example, confirming that audio is heard from a Bluetooth speaker, or that an image renders correctly on the display.

**Total test modules**: 9  
**Total test cases across all modules**: 56 *(v1 — XCONF additional TCs planned)*

| Module | Script | Test Cases |
|--------|--------|-----------|
| BT Audio | `BT_AUDIO_AUTOMATED.sh` | 7 |
| HDCP Compliance | `HDCP_COMPLIANCE_AUTOMATED.sh` | 7 |
| Image Formats | `Image_formats.sh` | 4 |
| IPv6 | `IPv6_Automated.sh` | 8 |
| MEMCR | `MEMCR_AUTOMATED.sh` | 10 |
| Power Management | `POWER_MGMT_Automated.sh` | 1 |
| System | `System_Automated.sh` | 3 |
| WebAudio | `WEBAUDIO_manual_automated.sh` | 15 |
| XCONF Image Upgrade | `XCONF_imageUpgrade_Automated.sh` | 1 |

---

## 2. Repository Structure

The following files make up the Guided Test Suite. All files are located in the `Guided Test scripts/` folder of this repository.

```
Guided Test scripts/
├── device.conf                       # Configuration file — must be updated per test environment
├── generic_functions.sh              # Shared helper library — required by all scripts
├── BT_AUDIO_AUTOMATED.sh             # BT Audio test module (7 TCs)
├── HDCP_COMPLIANCE_AUTOMATED.sh      # HDCP Compliance test module (7 TCs)
├── Image_formats.sh                  # Image Formats test module (4 TCs)
├── IPv6_Automated.sh                 # IPv6 test module (8 TCs)
├── MEMCR_AUTOMATED.sh                # MEMCR test module (10 TCs)
├── POWER_MGMT_Automated.sh           # Power Management test module (1 TC)
├── System_Automated.sh               # System test module (3 TCs)
├── WEBAUDIO_manual_automated.sh      # WebAudio test module (15 TCs)
└── XCONF_imageUpgrade_Automated.sh   # XCONF Image Upgrade test module (5 TCs)
```

> **Important**: `device.conf` and `generic_functions.sh` are shared dependencies. **Every test script sources both files at startup.** They must always be present in the same working directory as the test script on the DUT.

### Push to Git Repository — Recommended Approach

Push all files as **individual files** (do not zip). Reasons:
- Each file has independent version history and can be updated separately.
- A tester cloning the repo gets the full suite ready to use without any extraction step.
- GitHub renders shell scripts with syntax highlighting when viewed individually.
- Individual file diffs are clean and reviewable in pull requests.

**Recommended branch strategy**:
```
feature/guided-test-scripts → Pull Request → develop → main
```

---

## 3. Prerequisites

Before running any test script, ensure the following conditions are met on both the host machine and the DUT.

### Host Machine Requirements

| Requirement | Details |
|-------------|---------|
| SSH client | PuTTY, OpenSSH, or equivalent |
| Serial terminal (optional) | Minicom, TeraTerm, or equivalent — required if SSH is unavailable |
| SCP or SFTP client | For transferring files to the DUT |
| Network access | Host and DUT must be on the same network |

### DUT Requirements

| Requirement | Details |
|-------------|---------|
| RDK-V firmware | Must be a valid RDK build (verified via `/version.txt`) |
| WPEFramework (Thunder) running | All scripts call Thunder JSON-RPC APIs at `http://127.0.0.1:9998/jsonrpc` |
| Root access via SSH/serial | Scripts must be executed with root permissions |
| Ethernet or Wi-Fi connectivity | Required for API calls, app downloads, and internet access tests |
| HDMI display connected | Required for all tests that validate visual output |
| Bluetooth remote paired | Required for RDK UI navigation tests |
| Sufficient disk space | Results and logs are written to `/home/root/` by default |

### Module-Specific Hardware Requirements

| Module | Additional Hardware Required |
|--------|------------------------------|
| BT Audio | External Bluetooth A2DP device (headset or soundbar) in pairing mode |
| HDCP Compliance | HDMI display with HDCP support |
| Image Formats | Network access to the configured `app_download_server` |
| WebAudio | Network access to the configured `app_download_server` |
| XCONF Image Upgrade | Valid XCONF server configuration and firmware image available |

---

## 4. Deploying Files to the DUT

**Three files are always required** for any test module:

1. The module test script (e.g., `BT_AUDIO_AUTOMATED.sh`)
2. `device.conf` — must be configured with the correct values for your test environment before transfer
3. `generic_functions.sh` — shared helper library, unchanged across executions

### Step 1 — Update device.conf on the Host

Before transferring files to the DUT, open `device.conf` on the host and update all parameters relevant to your test module. Refer to [Section 5](#5-configuring-deviceconf) for the complete parameter reference.

### Step 2 — Transfer Files to the DUT

Use SCP to copy the required files to the DUT's working directory:

```bash
# Transfer files for a specific module (example: BT Audio)
scp BT_AUDIO_AUTOMATED.sh device.conf generic_functions.sh root@<DUT_IP>:/home/root/

# Transfer all scripts at once (for full suite deployment)
scp *.sh device.conf root@<DUT_IP>:/home/root/
```

### Step 3 — SSH into the DUT

```bash
ssh root@<DUT_IP>
```

### Step 4 — Navigate to the Working Directory

```bash
cd /home/root/
```

### Step 5 — Set Execute Permissions

```bash
chmod +x BT_AUDIO_AUTOMATED.sh
# Or for all scripts at once:
chmod +x *.sh
```

---

## 5. Configuring device.conf

`device.conf` is the central configuration file that controls all test environment parameters. It must be updated with values specific to your DUT and test environment **before running any test**.

> **Security Notice**: `device.conf` contains sensitive data including server URLs, API tokens, and credentials. Do **not** commit actual credential values to a public repository. Use placeholder values in the repository copy and configure the actual values on the DUT directly before test execution.

### 5.1 Common Parameters — All Modules

These parameters apply to all test modules.

| Parameter | Description | Default Value | Update Required? |
|-----------|-------------|---------------|-----------------|
| `result_directory` | Directory on DUT where test execution results are written | `/home/root/test_Execution_results` | Optional — change if needed |
| `issue_logs_directory` | Directory on DUT where failure logs are stored | `/home/root/test_Execution_results/logs` | Optional — change if needed |

### 5.2 Module-Specific Parameters

---

#### BT Audio — `BT_AUDIO_AUTOMATED.sh`

| Parameter | Description | Example Value | Update Required? |
|-----------|-------------|---------------|-----------------|
| `EXT_BT_devices` | Exact name of the external Bluetooth audio device to pair and connect | `"Creative Stage"` | **Yes** — set to your device's BT name |
| `sleep_timer` | Seconds to wait before retrieving the discovered device list after scanning | `25` | Adjust if scan is slow |
| `max_scan_retries` | Maximum retries to locate the target BT device in the discovered list | `3` | Adjust for unstable BT environments |
| `max_scan_discovered_devices` | Maximum retries to retrieve the discovered devices list after scanning | `3` | Adjust if needed |
| `max_reconnect_check` | Maximum retries to verify BT auto-reconnection after a device reboot | `5` | Adjust based on device reboot speed |
| `yt_URL` | YouTube video ID for AV playback deeplink | `"v=zQGQLEE1nQs"` | **Yes** — ensure the video is accessible |
| `amz_URL` | Amazon Prime Video ASIN deeplink for AV playback | `"asinlist=B00OVLYY6A&refMarker=ref_marker_value"` | **Yes** — ensure content is available |
| `default_volume_level` | Default volume level for BT volume control tests (range: 0–255) | `122` | Adjust as needed |
| `increase_volume` | Array of volume levels for incremental increase test | `(152 188 224)` | Adjust as needed |
| `decrease_volume` | Array of volume levels for incremental decrease test | `(108 72 36)` | Adjust as needed |

---

#### HDCP Compliance — `HDCP_COMPLIANCE_AUTOMATED.sh`

| Parameter | Description | Default Value | Update Required? |
|-----------|-------------|---------------|-----------------|
| `hdcp_logs_path` | Path to the HDCP/UI manager log file on the DUT where HDCP status events are logged | `/opt/logs/uimgr_log.txt` | Optional — update only if your build uses a different log path |

---

#### Image Formats — `Image_formats.sh`

| Parameter | Description | Example Value | Update Required? |
|-----------|-------------|---------------|-----------------|
| `browser_test_app_bundle` | Bundle name of the Browser Test application to download and install | `"com.rdkcentral.browser_test+0.3.1.bolt"` | **Yes** — confirm the bundle name for your firmware version |
| `app_download_server` | Base URL of the server hosting the app bundles for download | `"https://tdktest.rdkcentral.com:8443/images"` | **Yes** — confirm server accessibility from DUT |
| `installed_app_ver` | Expected installed version of the app (used for verification) | `"0.3.1"` | **Yes** — must match the bundle version |
| `app_Operations_logs_path` | Path to WPEFramework log file for app install/launch operation logging | `/opt/logs/wpeframework.log` | Optional |

---

#### IPv6 — `IPv6_Automated.sh`

| Parameter | Description | Example Value | Update Required? |
|-----------|-------------|---------------|-----------------|
| `ipv6_conf_SSID` | Name of the IPv6-supported Wi-Fi SSID — used in the precondition check to verify DUT is connected to the correct SSID | `""` (empty = skip check) | **Yes** — set to your IPv6-capable SSID name |
| `yt_URL` | YouTube video ID for AV playback deeplink | `"v=zQGQLEE1nQs"` | **Yes** — ensure accessibility |

---

#### MEMCR — `MEMCR_AUTOMATED.sh`

| Parameter | Description | Example Value | Update Required? |
|-----------|-------------|---------------|-----------------|
| `memcr_test_apps` | Array of application names to test for MEMCR state management | `("Cobalt" "Amazon" "YouTubeTV")` | Optional — update if testing different apps |
| `app_launch_type` | Method used to launch apps — either via RDK service APIs or generateKey UI navigation | `"RDK_service_API"` | Optional — `"RDK_service_API"` is the recommended default |
| `yt_URL` | YouTube video ID for AV playback deeplink | `"v=zQGQLEE1nQs"` | **Yes** |
| `amz_URL` | Amazon Prime Video ASIN deeplink | `"asinlist=B00OVLYY6A&refMarker=ref_marker_value"` | **Yes** |

---

#### Power Management — `POWER_MGMT_Automated.sh`

| Parameter | Description | Example Value | Update Required? |
|-----------|-------------|---------------|-----------------|
| `yt_URL` | YouTube video ID for AV playback deeplink — used to verify DUT wakeup and playback functionality | `"v=zQGQLEE1nQs"` | **Yes** |

---

#### System — `System_Automated.sh`

No module-specific parameters. Only the common `result_directory` and `issue_logs_directory` apply. Ensure the DUT has Ethernet connected and a valid IP address assigned (verified in the precondition step of TC_SYSTEM_MANUAL_01).

---

#### WebAudio — `WEBAUDIO_manual_automated.sh`

| Parameter | Description | Example Value | Update Required? |
|-----------|-------------|---------------|-----------------|
| `webaudio_app_bundle` | Bundle name of the WebAudio manual test application to download and install | `"com.rdkcentral.webaudio_manual+0.3.1.bolt"` | **Yes** — confirm bundle name for your firmware version |
| `app_download_server` | Base URL of the server hosting the app bundles | `"https://tdktest.rdkcentral.com:8443/images"` | **Yes** — confirm DUT can reach this server |
| `installed_app_ver` | Expected installed version of the WebAudio app (used for verification) | `"0.3.1"` | **Yes** — must match the bundle version |

---

#### XCONF Image Upgrade — `XCONF_imageUpgrade_Automated.sh`

> **Security Notice**: This module requires an XCONF API authentication token (`xconf_API_key_token`). This is a sensitive credential. **Never commit the actual token value to a public repository.** Configure it directly on the DUT in the `device.conf` file after deployment.

| Parameter | Description | Update Required? |
|-----------|-------------|-----------------|
| `xconf_server_url` | Base URL of the XCONF server | **Yes** |
| `xconf_config_check_url` | XCONF configuration check endpoint URL (appended with DUT MAC address) | **Yes** |
| `xconf_imagefile_to_upgrade` | Filename of the firmware image to upgrade to | **Yes** — set to your target firmware image filename |
| `xconf_imagefile_version` | Expected firmware version string after upgrade (used for post-upgrade verification) | **Yes** — must match `xconf_imagefile_to_upgrade` |
| `xconf_reboot_immediately` | Whether the DUT reboots immediately after firmware download | Optional — default `"true"` |
| `xconf_firmware_dwld_location` | Server URL from which the firmware image is downloaded | **Yes** |
| `xconf_firmwareConfig_name` | Name of the XCONF firmware configuration entry | **Yes** |
| `xconf_API_key_token` | Authentication token for XCONF REST API calls | **Yes — sensitive credential, configure on DUT only** |
| `xconf_restApi_firmware_config` | XCONF REST API endpoint for reading firmware configurations | **Yes** |
| `xconf_firmwareConfig_query_url` | XCONF REST API endpoint for querying firmware entries | **Yes** |

---

## 6. Running a Test Script — Step-by-Step

All test scripts follow the same interactive execution pattern.

### Complete Execution Flow

```bash
# Step 1: SSH into the DUT
ssh root@<DUT_IP>

# Step 2: Navigate to the working directory where the scripts were deployed
cd /home/root/

# Step 3: Ensure execute permission is set
chmod +x BT_AUDIO_AUTOMATED.sh

# Step 4: Run the script
bash BT_AUDIO_AUTOMATED.sh
```

### Step 5: Select a Test Case from the Menu

When the script starts, it displays a numbered menu of all available test cases for that module. Example (BT Audio):

```
1. Run TestCase : TC_EXTERNALAUDIO_MANUAL_01  : [ Pair and connect an external BT Device ]
2. Run TestCase : TC_EXTERNALAUDIO_MANUAL_02  : [ Start Audio streaming in external BT Device ]
3. Run TestCase : TC_EXTERNALAUDIO_MANUAL_03  : [ Unpair and Disconnect external BT Device ]
4. Run TestCase : TC_EXTERNALAUDIO_MANUAL_04  : [ Reboot External BT device while Audio streaming ]
5. Run TestCase : TC_EXTERNALAUDIO_MANUAL_05  : [ Volume Control (Mute/Unmute) while Audio streaming ]
6. Run TestCase : TC_EXTERNALAUDIO_MANUAL_06  : [ Volume Control (Increase/Decrease) while Audio streaming ]
7. Run TestCase : TC_EXTERNALAUDIO_MANUAL_07  : [ DeviceInfo verification of connected external BT Device ]

Enter an Option to proceed :
```

Enter the number corresponding to the test case you want to run and press **Enter**.

### Step 6: Respond to Guided Prompts (Partial Automation Checkpoints)

During execution, the script may pause at a **guided checkpoint** — a point where the result can only be verified by human observation (e.g., audio is heard, video is rendered on the display, a UI element is visible). The script displays a prompt in this format:

```
Is <observation description> [yes/no]:
```

Observe the DUT or connected display/audio output, then type `yes` if the expected behaviour is confirmed or `no` if it is not, and press **Enter**. The script records your response and proceeds to the next step.

> These `[yes/no]` prompts are the **guided** part of the partial automation model. All other steps before and after these prompts are fully automated by the script.

### Step 7: Test Completion

When a test case completes, the script prints a PASS or FAIL result and writes the detailed result to the `result_directory` configured in `device.conf`.

---

## 7. Test Module Reference

---

### 7.1 BT Audio (External Audio)

**Script**: `BT_AUDIO_AUTOMATED.sh`  
**TC ID Prefix**: `TC_EXTERNALAUDIO_MANUAL_`  
**Supported Models**: Video Accelerator only

**Module Prerequisites**:
- External Bluetooth A2DP audio device (headset or soundbar) powered on and in pairing/discoverable mode.
- YouTube or Amazon Prime Video installed on the DUT and signed in with valid credentials.
- `EXT_BT_devices` in `device.conf` must match the **exact Bluetooth broadcast name** of your device.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_EXTERNALAUDIO_MANUAL_01` | Pair and connect an external BT device |
| 2 | `TC_EXTERNALAUDIO_MANUAL_02` | Start audio streaming from the external BT device |
| 3 | `TC_EXTERNALAUDIO_MANUAL_03` | Unpair and disconnect the external BT device |
| 4 | `TC_EXTERNALAUDIO_MANUAL_04` | Reboot external BT device while audio streaming is active |
| 5 | `TC_EXTERNALAUDIO_MANUAL_05` | Volume control — Mute and Unmute while audio streaming |
| 6 | `TC_EXTERNALAUDIO_MANUAL_06` | Volume control — Increase and Decrease while audio streaming |
| 7 | `TC_EXTERNALAUDIO_MANUAL_07` | Device info verification of the connected external BT device |

**device.conf Parameters**: `EXT_BT_devices`, `sleep_timer`, `max_scan_retries`, `max_scan_discovered_devices`, `max_reconnect_check`, `yt_URL`, `amz_URL`, `default_volume_level`, `increase_volume`, `decrease_volume`, `result_directory`, `issue_logs_directory`

---

### 7.2 HDCP Compliance

**Script**: `HDCP_COMPLIANCE_AUTOMATED.sh`  
**TC ID Prefix**: `TC_HDCPCOMPLIANCE_MANUAL_`  
**Supported Models**: Video Accelerator only

**Module Prerequisites**:
- HDMI display with HDCP support connected to the DUT.
- DUT must be actively displaying content over HDMI.
- `hdcp_logs_path` must point to the correct log file path on your build.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_HDCPCOMPLIANCE_MANUAL_01` | Verify the HDMI cable connected status |
| 2 | `TC_HDCPCOMPLIANCE_MANUAL_02` | Verify the HDCP authentication initiated status |
| 3 | `TC_HDCPCOMPLIANCE_MANUAL_03` | Verify the HDCP authenticated status |
| 4 | `TC_HDCPCOMPLIANCE_MANUAL_04` | Verify the HDCP protocol support |
| 5 | `TC_HDCPCOMPLIANCE_MANUAL_05` | Verify the HDCP enabled status |
| 6 | `TC_HDCPCOMPLIANCE_MANUAL_06` | Verify the device-supported, received, and current HDCP version |
| 7 | `TC_HDCPCOMPLIANCE_MANUAL_07` | Verify the HDCP compliant enabled status |

**device.conf Parameters**: `hdcp_logs_path`, `result_directory`, `issue_logs_directory`

---

### 7.3 Image Formats

**Script**: `Image_formats.sh`  
**TC ID Prefix**: `TC_IMAGEFORMATS_MANUAL_`  
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- DUT must have network access to the `app_download_server` to download and install the Browser Test application.
- `browser_test_app_bundle` and `installed_app_ver` must match the bundle available on your test server.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_IMAGEFORMATS_MANUAL_01` | Verify PNG image format rendering via Browser Test App |
| 2 | `TC_IMAGEFORMATS_MANUAL_02` | Verify JPEG image format rendering via Browser Test App |
| 3 | `TC_IMAGEFORMATS_MANUAL_03` | Verify SVG image format rendering via Browser Test App |
| 4 | `TC_IMAGEFORMATS_MANUAL_04` | Verify WebP image format rendering via Browser Test App |

**device.conf Parameters**: `browser_test_app_bundle`, `app_download_server`, `installed_app_ver`, `app_Operations_logs_path`, `result_directory`, `issue_logs_directory`

---

### 7.4 IPv6

**Script**: `IPv6_Automated.sh`  
**TC ID Prefix**: `TC_IPv6_MANUAL_`  
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- DUT must be connected to an IPv6-supported Wi-Fi SSID.
- For Ethernet-involved test cases, Ethernet must be connected with a valid IP address.
- Set `ipv6_conf_SSID` to the name of the IPv6-capable SSID in your environment.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_IPv6_MANUAL_01` | Verify IP settings when connected to an IPv6-supported SSID |
| 2 | `TC_IPv6_MANUAL_02` | Verify the public IPv6 IP when connected to an IPv6 SSID with Ethernet connected |
| 3 | `TC_IPv6_MANUAL_03` | Verify the public IPv6 IP when connected to an IPv6 SSID with Ethernet disconnected |
| 4 | `TC_IPv6_MANUAL_04` | Verify internet accessibility when connected to an IPv6 SSID with Ethernet connected |
| 5 | `TC_IPv6_MANUAL_05` | Verify internet accessibility when connected to an IPv6 SSID with Ethernet disconnected |
| 6 | `TC_IPv6_MANUAL_06` | Verify the Trace API when connected to an IPv6 SSID with Ethernet disconnected |
| 7 | `TC_IPv6_MANUAL_07` | Verify the Ping API when connected to an IPv6 SSID with Ethernet disconnected |
| 8 | `TC_IPv6_MANUAL_08` | Verify the getPublicIP API response when connected to an IPv6 SSID with Ethernet connected |

**device.conf Parameters**: `ipv6_conf_SSID`, `yt_URL`, `result_directory`, `issue_logs_directory`

---

### 7.5 MEMCR

**Script**: `MEMCR_AUTOMATED.sh`  
**TC ID Prefix**: `TC_MEMCR_MANUAL_`  
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- YouTube, YouTubeTV, and Amazon Prime Video must be installed on the DUT.
- All three apps must be signed in with valid user credentials.
- The `memcr` daemon must be running on the DUT (`systemctl status memcr`).

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_MEMCR_MANUAL_01` | Check the MEMCR service status |
| 2 | `TC_MEMCR_MANUAL_02` | Verify the state of the YouTube app after pressing the Home button post-launch |
| 3 | `TC_MEMCR_MANUAL_03` | Verify that memory usage decreases after pressing the Home button from the YouTube app |
| 4 | `TC_MEMCR_MANUAL_04` | Verify YouTube state serialization after Hibernate and Resume |
| 5 | `TC_MEMCR_MANUAL_05` | Verify the state of the YouTubeTV app after pressing the Home button post-launch |
| 6 | `TC_MEMCR_MANUAL_06` | Verify that memory usage decreases after pressing the Home button from the YouTubeTV app |
| 7 | `TC_MEMCR_MANUAL_07` | Verify YouTubeTV state serialization after Hibernate and Resume |
| 8 | `TC_MEMCR_MANUAL_08` | Verify the state of the Amazon app after pressing the Home button post-launch |
| 9 | `TC_MEMCR_MANUAL_09` | Verify that memory usage decreases after pressing the Home button from the Amazon app |
| 10 | `TC_MEMCR_MANUAL_10` | Verify Amazon state serialization after Hibernate and Resume |

**device.conf Parameters**: `memcr_test_apps`, `app_launch_type`, `yt_URL`, `amz_URL`, `result_directory`, `issue_logs_directory`

---

### 7.6 Power Management

**Script**: `POWER_MGMT_Automated.sh`  
**TC ID Prefix**: `TC_POWER_MANUAL_`  
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- Energy Saver must be set to **OFF** in Settings → Other Settings → Energy Saver on the DUT before running the test. The script will prompt you to confirm this.
- YouTube must be installed and signed in on the DUT.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_POWER_MANUAL_01` | Verify the DUT can be set to LIGHT SLEEP and then wake up using RDK service APIs |

**device.conf Parameters**: `yt_URL`, `result_directory`, `issue_logs_directory`

---

### 7.7 System

**Script**: `System_Automated.sh`  
**TC ID Prefix**: `TC_SYSTEM_MANUAL_`  
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- DUT must have a valid Ethernet IP address (verified automatically in the precondition of TC_SYSTEM_MANUAL_01).
- No module-specific `device.conf` parameters need to be updated beyond the common ones.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_SYSTEM_MANUAL_01` | Verify the SSH Dropbear service status and confirm it is active |
| 2 | `TC_SYSTEM_MANUAL_02` | Verify the running status of WPEFramework processes |
| 3 | `TC_SYSTEM_MANUAL_03` | Verify the log rollover RDK functionality |

**device.conf Parameters**: `result_directory`, `issue_logs_directory`

---

### 7.8 WebAudio

**Script**: `WEBAUDIO_manual_automated.sh`  
**TC ID Prefix**: `TC_WEBAUDIO_MANUAL_`  
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- DUT must have network access to the `app_download_server` to download and install the WebAudio manual test application.
- `webaudio_app_bundle` and `installed_app_ver` must match the bundle available on your test server.
- The test relies on auditory confirmation — ensure a speaker or headset is connected to the DUT to hear audio output during tests.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_WEBAUDIO_MANUAL_01` | Verify Speech Synthesis Test 1 via WebAudio app |
| 2 | `TC_WEBAUDIO_MANUAL_02` | Verify Speech Synthesis Test 2 — supported audio languages |
| 3 | `TC_WEBAUDIO_MANUAL_03` | Verify Speech Synthesis Test 3 — 3 different audio languages continuously |
| 4 | `TC_WEBAUDIO_MANUAL_04` | Verify AudioContext object creation via WebAudio app |
| 5 | `TC_WEBAUDIO_MANUAL_05` | Verify AudioContext creation and destruction via WebAudio app |
| 6 | `TC_WEBAUDIO_MANUAL_06` | Verify audio playback using WebAudio API via WebAudio app |
| 7 | `TC_WEBAUDIO_MANUAL_07` | Verify FM sound synthesis (Generated Sound FM) via WebAudio app |
| 8 | `TC_WEBAUDIO_MANUAL_08` | Verify multimedia playback via WebAudio app |
| 9 | `TC_WEBAUDIO_MANUAL_09` | Verify AAC audio decoding — VBR 128 kbps / 44 kHz |
| 10 | `TC_WEBAUDIO_MANUAL_10` | Verify MP3 audio decoding — 128 kbps / 44 kHz |
| 11 | `TC_WEBAUDIO_MANUAL_11` | Verify Vorbis audio decoding — VBR 70 kbps / 44 kHz |
| 12 | `TC_WEBAUDIO_MANUAL_12` | Verify Vorbis audio decoding — VBR 96 kbps / 44 kHz |
| 13 | `TC_WEBAUDIO_MANUAL_13` | Verify Vorbis audio decoding — VBR 128 kbps / 44 kHz |
| 14 | `TC_WEBAUDIO_MANUAL_14` | Verify WAV audio decoding — 24-bit / 22 kHz resample |
| 15 | `TC_WEBAUDIO_MANUAL_15` | Verify WAV audio decoding — 24-bit / 44 kHz |

**device.conf Parameters**: `webaudio_app_bundle`, `app_download_server`, `installed_app_ver`, `result_directory`, `issue_logs_directory`

---

### 7.9 XCONF Image Upgrade

**Script**: `XCONF_imageUpgrade_Automated.sh`  
**TC ID Prefix**: `TC_XCONF_MANUAL_`  
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- All XCONF server parameters in `device.conf` must be configured with valid values before running.
- The target firmware image must be available at the configured `xconf_firmware_dwld_location`.
- The DUT must have network access to the XCONF server.
- `xconf_API_key_token` must be set to a valid XCONF REST API authentication token.

> **Warning**: XCONF upgrade test cases will modify the DUT firmware. Ensure you have a recovery plan (e.g., serial console access) before executing these tests.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_XCONF_MANUAL_01` | Verify XCONF firmware upgrade behaviour using RDK service API |

> **Note**: Additional XCONF test cases (TC_XCONF_MANUAL_02 through TC_XCONF_MANUAL_05) are planned and will be added in a future documentation revision.

**device.conf Parameters**: `xconf_server_url`, `xconf_config_check_url`, `xconf_imagefile_to_upgrade`, `xconf_imagefile_version`, `xconf_reboot_immediately`, `xconf_firmware_dwld_location`, `xconf_firmwareConfig_name`, `xconf_API_key_token`, `xconf_restApi_firmware_config`, `xconf_firmwareConfig_query_url`, `result_directory`, `issue_logs_directory`

---

## 8. Test Results and Logs

After each test case execution, the script writes the result to the DUT at the path configured in `result_directory`.

### Result Directory Structure

```
/home/root/test_Execution_results/
├── TC_EXTERNALAUDIO_MANUAL_01_result.txt   # PASS/FAIL result for each TC
├── TC_EXTERNALAUDIO_MANUAL_02_result.txt
├── ...
└── logs/
    ├── TC_EXTERNALAUDIO_MANUAL_01_issue.log  # Detailed failure logs (only on FAIL)
    └── ...
```

### Retrieving Results from the DUT

After test execution, retrieve the results directory from the DUT to the host machine:

```bash
# Retrieve all results at once
scp -r root@<DUT_IP>:/home/root/test_Execution_results/ ./test_results_$(date +%Y%m%d)/

# List result files on the DUT
ssh root@<DUT_IP> "ls -la /home/root/test_Execution_results/"

# View a specific result file
ssh root@<DUT_IP> "cat /home/root/test_Execution_results/TC_EXTERNALAUDIO_MANUAL_01_result.txt"
```

---

## 9. Troubleshooting

| Issue | Likely Cause | Resolution |
|-------|-------------|-----------|
| Script exits immediately with `source: not found` | `device.conf` or `generic_functions.sh` not in the same directory as the script | Transfer all three files (`script.sh`, `device.conf`, `generic_functions.sh`) to the same working directory on the DUT |
| `curl: (7) Failed to connect` | WPEFramework (Thunder) is not running on port 9998 | Verify Thunder is running: `systemctl status wpeframework` |
| `Ethernet is not connected to DUT` | Precondition check failed — no valid IPv4 on eth0 | Connect the Ethernet cable and verify IP: `ip -4 addr show eth0` |
| BT device not found during scan | BT device name in `device.conf` does not match broadcast name, or device is not in pairing mode | Put the BT device in pairing mode; verify the exact name using `hciconfig` or another BT scanner |
| App bundle download fails | DUT cannot reach `app_download_server` | Verify network connectivity from DUT: `curl -I https://tdktest.rdkcentral.com:8443/` |
| XCONF upgrade does not trigger | XCONF configuration not set up correctly, or API token is invalid | Verify all `xconf_*` parameters in `device.conf`; confirm the firmware config exists on the XCONF server |
| Test result directory missing | `result_directory` path does not exist on the DUT | Create it manually: `mkdir -p /home/root/test_Execution_results/logs` |

---

*For questions or issues, contact the test suite author: aharil144@cable.comcast.com*
