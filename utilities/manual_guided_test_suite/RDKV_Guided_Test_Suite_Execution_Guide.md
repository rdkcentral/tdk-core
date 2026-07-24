# RDKV Guided Test Suite — Execution Guide

> **Version**: 1.0 | **Platform**: RDK-V (Video Accelerator, RPI-Client) | **Execution Environment**: DUT Serial/SSH Console | **Execution Model**: Guided (Partially Automated)

> **Intended Audience**: Test engineers and QA testers responsible for executing RDK-V certification test cases on a live DUT. This guide covers cloning the repository, configuring the test environment, deploying scripts to the DUT, and executing test cases.

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-24 | TDKV Test Team | Initial release — 9 modules, 56 test cases (v1) |

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
10. [Known Limitations](#10-known-limitations)

---

## 1. Overview

The **RDKV Guided Test Suite** is a collection of interactive shell scripts that validate RDK-V platform capabilities across multiple feature modules. Each script presents a numbered menu so you can select and execute individual test cases against a live RDK-V DUT (Device Under Test).

### Execution Model — Guided (Partially Automated)

These scripts are **not fully automated** and are **not fully manual** — they follow a **Guided Test** execution model, which is a form of partial automation. Understanding this distinction is important before running any script.

| Step Type | Description | Tester Action Required? |
|-----------|-------------|-------------------------|
| **Automated** | The script executes device-side API calls (JSON-RPC/curl), parses the response, and validates the result entirely without any interaction. | No — the script proceeds automatically. |
| **Guided (Prompted)** | The script reaches a checkpoint where the outcome cannot be verified programmatically (for example, audio is audible or a visual element is visible on the TV display). The script **pauses and displays a `[yes/no]` prompt**. You must observe the DUT or display, then type `yes` or `no` and press Enter to continue. | **Yes — you must respond.** |
| **Visual / Auditory Only** | Certain test cases are entirely observation-based — for example, confirming that Bluetooth audio is heard or that an image renders correctly on screen. | **Yes — you must observe and confirm.** |

> **In summary**: The script handles all device interactions and API calls automatically. You are involved **only** at specific checkpoints where human observation is the only way to verify the outcome.

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

### Cloning the Repository

> **Note**: Replace the placeholder URL below with the actual repository URL before use.

```bash
# Clone the repository
git clone https://github.com/<your-org>/<your-repo>.git

# Navigate to the manual_guided_test_suite folder
cd "<your-repo>/utilities/manual_guided_test_suite/"
```

> **Branch**: All test scripts are maintained in the `develop` branch. Switch to the correct branch after cloning:
>
> ```bash
> git checkout develop
> ```

### Getting the Latest Scripts

To pull the latest updates after the initial clone:

```bash
git pull origin develop
```

> Pull before each test execution cycle to ensure you are running the latest version of the scripts.

### Repository File Tree

The following files make up the Guided Test Suite. All files are located in the `utilities/manual_guided_test_suite/` folder of this repository.

```text
utilities/manual_guided_test_suite/
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
└── XCONF_imageUpgrade_Automated.sh   # XCONF Image Upgrade test module (1 TC — v1)
```

> **Important**: `device.conf` and `generic_functions.sh` are shared dependencies. Every test script sources both files at startup. They must always be present in the same working directory as the test script on the DUT.

---

## 3. Prerequisites

Verify the following conditions on both the host machine and the DUT before running any test script.

### Host Machine Requirements

| Requirement | Details |
|-------------|---------|
| SSH client | PuTTY, OpenSSH, or equivalent. |
| Serial terminal (optional) | Minicom, TeraTerm, or equivalent — required only if SSH is unavailable. |
| SCP or SFTP client | Required for transferring scripts to the DUT. |
| Network access | The host machine and the DUT must be on the same network. |

### DUT Requirements

| Requirement | Details |
|-------------|---------|
| RDK-V firmware | Must be a valid RDK build, verifiable via `/version.txt`. |
| WPEFramework (Thunder) running | All scripts call Thunder JSON-RPC APIs at `http://127.0.0.1:9998/jsonrpc`. |
| Root access via SSH/serial | Scripts must be executed with root permissions. |
| Ethernet or Wi-Fi connectivity | Required for API calls, app downloads, and internet access tests. |
| HDMI display connected | Required for all tests that validate visual output on the connected display. |
| Sufficient disk space | Results and logs are written to `/home/root/test_Execution_results/`. Ensure at least 50 MB of free space on the DUT. |

### Module-Specific Hardware Requirements

| Module | Additional Hardware Required |
|--------|------------------------------|
| BT Audio | External Bluetooth A2DP device (headset or soundbar) in pairing/discoverable mode. |
| HDCP Compliance | HDMI display with HDCP support. |
| Image Formats | Network access from the DUT to the configured `app_download_server`. |
| WebAudio | Network access from the DUT to the configured `app_download_server`. |
| XCONF Image Upgrade | Valid XCONF server configuration and firmware image available at the configured download location. |

---

## 4. Deploying Files to the DUT

Three files are always required for any test module:

1. The module test script (for example, `BT_AUDIO_AUTOMATED.sh`).
2. `device.conf` — configure this file with the correct values for your test environment before transfer. Refer to [Section 5](#5-configuring-deviceconf).
3. `generic_functions.sh` — shared helper library; no modification required.

### Step 1 — Update `device.conf` on the Host

Open `device.conf` on your host machine and update all parameters relevant to the test module you plan to run. Refer to [Section 5](#5-configuring-deviceconf) for the complete parameter reference.

### Step 2 — Transfer Files to the DUT

Use SCP to copy the required files to the DUT's working directory.

```bash
# Transfer files for a specific module (example: BT Audio)
scp BT_AUDIO_AUTOMATED.sh device.conf generic_functions.sh root@<DUT_IP>:/home/root/

# Transfer all scripts at once (for full suite deployment)
# Note: *.sh includes generic_functions.sh — no separate transfer needed.
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

## 5. Configuring `device.conf`

`device.conf` is the central configuration file that controls all test environment parameters. Update it with values specific to your DUT and test environment **before running any test**.

> **Security Notice**: `device.conf` contains sensitive parameters including API tokens and credentials. Configure sensitive values directly on the DUT after deployment.

### 5.1 Common Parameters — All Modules

These parameters apply to all test modules.

| Parameter | Description | Example Value / Default Value | Update Required? |
|-----------|-------------|-------------------------------|-----------------|
| `result_directory` | Directory on the DUT where test execution results are written. | `/home/root/test_Execution_results` | Optional — change only if a different path is required. |
| `issue_logs_directory` | Directory on the DUT where failure logs are stored. | `/home/root/test_Execution_results/logs` | Optional — change only if a different path is required. |

### 5.2 Module-Specific Parameters

---

#### BT Audio — `BT_AUDIO_AUTOMATED.sh`

| Parameter | Description | Example Value / Default Value | Update Required? |
|-----------|-------------|-------------------------------|-----------------|
| `EXT_BT_devices` | Exact Bluetooth broadcast name of the external audio device to pair and connect. | `<External_BT_device_Name>` | **Yes** — set to your device's exact Bluetooth name. |
| `sleep_timer` | Seconds to wait before retrieving the discovered device list after scanning. | `25` | Optional — increase if the BT scan is slow. |
| `max_scan_retries` | Maximum retries to locate the target Bluetooth device in the discovered device list. | `3` | Optional — increase for unstable Bluetooth environments. |
| `max_scan_discovered_devices` | Maximum retries to retrieve the discovered devices list after scanning starts. | `3` | Optional — adjust if needed. |
| `max_reconnect_check` | Maximum retries to verify Bluetooth auto-reconnection after a device reboot. | `5` | Optional — adjust based on device reboot speed. |
| `yt_URL` | YouTube video ID for AV playback deeplink. | `<yt_video_id>` | **Yes** — ensure the video is accessible from the DUT. |
| `amz_URL` | Amazon Prime Video ASIN deeplink for AV playback. | `<amz_content_asin>` | **Yes** — ensure the content is available and accessible. |
| `default_volume_level` | Default volume level for Bluetooth volume control tests (range: 0–255). | `122` | Optional — adjust as needed. |
| `increase_volume` | Array of volume levels for the incremental volume increase test. | `(152 188 224)` | Optional — adjust as needed. |
| `decrease_volume` | Array of volume levels for the incremental volume decrease test. | `(108 72 36)` | Optional — adjust as needed. |

---

#### HDCP Compliance — `HDCP_COMPLIANCE_AUTOMATED.sh`

| Parameter | Description | Example Value / Default Value | Update Required? |
|-----------|-------------|-------------------------------|-----------------|
| `hdcp_logs_path` | Path to the HDCP/UI manager log file on the DUT where HDCP status events are recorded. | `/opt/logs/uimgr_log.txt` | Optional — update only if your firmware build uses a different log file path. |

---

#### Image Formats — `Image_formats.sh`

| Parameter | Description | Example Value / Default Value | Update Required? |
|-----------|-------------|-------------------------------|-----------------|
| `browser_test_app_bundle` | Bundle name of the Browser Test application to download and install on the DUT. | `"com.rdkcentral.browser_test+0.3.1.bolt"` | **Yes** — confirm the bundle name for your firmware version. |
| `app_download_server` | Base URL of the server hosting the application bundle for download. | `<app_download_server_url>` | **Yes** — confirm the DUT can reach this server. |
| `installed_app_ver` | Expected installed version of the Browser Test app (used for post-install verification). | `<app_version>` | **Yes** — must match the version of the downloaded bundle. |
| `app_Operations_logs_path` | Path to the WPEFramework log file used for app install and launch operation logging. | `/opt/logs/wpeframework.log` | Optional — update only if your build uses a different log path. |

---

#### IPv6 — `IPv6_Automated.sh`

| Parameter | Description | Example Value / Default Value | Update Required? |
|-----------|-------------|-------------------------------|-----------------|
| `ipv6_conf_SSID` | Name of the IPv6-supported Wi-Fi SSID. The script uses this value in the precondition check to verify the DUT is connected to the correct IPv6-capable network before test execution. | `<IPv6_supported_SSID_name>` | **Mandatory** — must be set to the exact name of your IPv6-capable SSID. Leaving this empty or incorrect will cause the precondition check to fail and the test to abort. |
| `yt_URL` | YouTube video ID for AV playback deeplink. | `<yt_video_id>` | **Yes** — ensure the video is accessible from the DUT. |

---

#### MEMCR — `MEMCR_AUTOMATED.sh`

| Parameter | Description | Example Value / Default Value | Update Required? |
|-----------|-------------|-------------------------------|-----------------|
| `memcr_test_apps` | Array of application names to test for MEMCR state management. The MEMCR test module is designed to test these three specific applications and requires all three to be present. | `("YouTube" "Amazon" "YouTubeTV")` | **Mandatory** — all three applications must be installed and signed in on the DUT before running the test. |
| `app_launch_type` | Method used to launch apps — either via RDK service APIs or via `generateKey` UI navigation. | `"RDK_service_API"` | Optional — `"RDK_service_API"` is the recommended default. |
| `yt_URL` | YouTube video ID for AV playback deeplink. | `<yt_video_id>` | **Yes** — ensure the video is accessible from the DUT. |
| `amz_URL` | Amazon Prime Video ASIN deeplink for AV playback. | `<amz_content_asin>` | **Yes** — ensure the content is available and accessible. |

---

#### Power Management — `POWER_MGMT_Automated.sh`

| Parameter | Description | Example Value / Default Value | Update Required? |
|-----------|-------------|-------------------------------|-----------------|
| `yt_URL` | YouTube video ID for AV playback deeplink — used to verify DUT wakeup and playback functionality after LIGHT SLEEP. | `<yt_video_id>` | **Yes** — ensure the video is accessible from the DUT. |

---

#### System — `System_Automated.sh`

No module-specific parameters. Only the common `result_directory` and `issue_logs_directory` parameters apply. Ensure the DUT has Ethernet connected and a valid IP address assigned before running (verified automatically in the precondition of `TC_SYSTEM_MANUAL_01`).

---

#### WebAudio — `WEBAUDIO_manual_automated.sh`

| Parameter | Description | Example Value / Default Value | Update Required? |
|-----------|-------------|-------------------------------|-----------------|
| `webaudio_app_bundle` | Bundle name of the WebAudio manual test application to download and install on the DUT. | `"com.rdkcentral.webaudio_manual+0.3.1.bolt"` | **Yes** — confirm the bundle name for your firmware version. |
| `app_download_server` | Base URL of the server hosting the application bundle for download. | `<app_download_server_url>` | **Yes** — confirm the DUT can reach this server. |
| `installed_app_ver` | Expected installed version of the WebAudio app (used for post-install verification). | `<app_version>` | **Yes** — must match the version of the downloaded bundle. |

---

#### XCONF Image Upgrade — `XCONF_imageUpgrade_Automated.sh`

> **Security Notice**: `xconf_API_key_token` is a sensitive credential. Configure it directly on the DUT in `device.conf` after deployment.

| Parameter | Description | Example Value / Default Value | Update Required? |
|-----------|-------------|-------------------------------|-----------------|
| `xconf_server_url` | Base URL of the XCONF server. | `https://xconf.rdkcentral.com` | **Yes** |
| `xconf_config_check_url` | XCONF configuration check endpoint URL — the DUT MAC address is appended at runtime. | `https://xconf.rdkcentral.com/xconf/swu/stb?eStbMac=` | **Yes** |
| `xconf_imagefile_to_upgrade` | Filename of the target firmware image to upgrade to. | `<firmware-image-filename>.img` | **Yes** — set to your target firmware image filename. |
| `xconf_imagefile_version` | Expected firmware version string after the upgrade, used for post-upgrade verification. | `<firmware-version-string>` | **Yes** — must match the version encoded in `xconf_imagefile_to_upgrade`. |
| `xconf_reboot_immediately` | Controls whether the DUT reboots immediately after the firmware download completes. Accepts `"true"` or `"false"`. | `"true"` | Optional — default is `"true"`. |
| `xconf_firmware_dwld_location` | Base URL of the server from which the firmware image is downloaded. | `https://<server>:<port>/images/` | **Yes** |
| `xconf_firmwareConfig_name` | Name of the XCONF firmware configuration entry used for this upgrade. | `<config-name>` | **Yes** |
| `xconf_API_key_token` | Authentication token for XCONF REST API calls. | `<sensitive_API_token>` | **Yes — sensitive credential. Configure on the DUT only.** |
| `xconf_restApi_firmware_config` | XCONF REST API endpoint for reading firmware configurations. | `https://xconf.rdkcentral.com/xconfAdminService/updates/firmwares?applicationType=stb` | **Yes** |
| `xconf_firmwareConfig_query_url` | XCONF REST API endpoint for querying firmware entries. | `https://xconf.rdkcentral.com/xconfAdminService/queries/firmwares` | **Yes** |

---

## 6. Running a Test Script — Step-by-Step

All test scripts follow the same interactive execution pattern. Follow all 7 steps in order.

### Step 1 — SSH into the DUT

```bash
ssh root@<DUT_IP>
```

### Step 2 — Navigate to the Working Directory

```bash
cd /home/root/
```

### Step 3 — Set Execute Permissions

```bash
chmod +x BT_AUDIO_AUTOMATED.sh
# Or for all scripts at once:
chmod +x *.sh
```

### Step 4 — Run the Script

```bash
bash BT_AUDIO_AUTOMATED.sh
```

### Step 5 — Select a Test Case from the Menu

When the script starts, it displays a numbered menu of all available test cases for that module. Example (BT Audio):

```text
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

### Step 6 — Respond to Guided Prompts (Partial Automation Checkpoints)

During execution, the script may pause at a **guided checkpoint** — a point where the result can only be verified by human observation (for example, audio is heard, video is rendered on the display, or a UI element is visible). The script displays a prompt in this format:

```text
Is <observation description> [yes/no]:
```

Observe the DUT or connected display/audio output, then type `yes` if the expected behaviour is confirmed or `no` if it is not, and press **Enter**. The script records your response and proceeds to the next step.

> **Note**: These `[yes/no]` prompts are the **guided** part of the partial automation model. All other steps before and after these prompts are fully automated by the script.

> **If you respond `no`**: The script records a **FAIL** result for that step. Depending on the step criticality, the script either continues to the next step or terminates the test case. The result file will contain the failed step details for investigation.

### Step 7 — Verify Test Completion

When a test case completes, the script prints a PASS or FAIL result on the console and writes the detailed result to the `result_directory` configured in `device.conf`.

**Example console output on PASS:**

```text
Testcase Execution Result : TC_EXTERNALAUDIO_MANUAL_01 : PASS
```

**Example console output on FAIL:**

```text
Testcase Execution Result : TC_EXTERNALAUDIO_MANUAL_01 : FAIL
```

Refer to [Section 8](#8-test-results-and-logs) for instructions on retrieving the detailed result files from the DUT.

---

## 7. Test Module Reference

---

### 7.1 BT Audio (External Audio)

**Script**: `BT_AUDIO_AUTOMATED.sh`
**TC ID Prefix**: `TC_EXTERNALAUDIO_MANUAL_`
**Supported Models**: Video Accelerator only

**Module Prerequisites**:
- Power on the external Bluetooth A2DP audio device (headset or soundbar) and place it in pairing/discoverable mode before running the script.
- Install YouTube or Amazon Prime Video on the DUT and sign in with valid user credentials.
- Set `EXT_BT_devices` in `device.conf` to match the **exact Bluetooth broadcast name** of your audio device.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_EXTERNALAUDIO_MANUAL_01` | Pair and connect an external Bluetooth audio device. |
| 2 | `TC_EXTERNALAUDIO_MANUAL_02` | Start audio streaming from the connected external Bluetooth device. |
| 3 | `TC_EXTERNALAUDIO_MANUAL_03` | Unpair and disconnect the external Bluetooth audio device. |
| 4 | `TC_EXTERNALAUDIO_MANUAL_04` | Reboot the external Bluetooth device while audio streaming is active and verify auto-reconnection. |
| 5 | `TC_EXTERNALAUDIO_MANUAL_05` | Mute and unmute audio streaming via the Bluetooth volume management API. |
| 6 | `TC_EXTERNALAUDIO_MANUAL_06` | Increase and decrease audio streaming volume via the Bluetooth volume management API. |
| 7 | `TC_EXTERNALAUDIO_MANUAL_07` | Verify device information (name, MAC address, manufacturer ID, device type) for the connected Bluetooth device. |

**device.conf Parameters**: `EXT_BT_devices`, `sleep_timer`, `max_scan_retries`, `max_scan_discovered_devices`, `max_reconnect_check`, `yt_URL`, `amz_URL`, `default_volume_level`, `increase_volume`, `decrease_volume`, `result_directory`, `issue_logs_directory`

---

### 7.2 HDCP Compliance

**Script**: `HDCP_COMPLIANCE_AUTOMATED.sh`
**TC ID Prefix**: `TC_HDCPCOMPLIANCE_MANUAL_`
**Supported Models**: Video Accelerator only

**Module Prerequisites**:
- Connect an HDMI display with HDCP support to the DUT.
- Ensure the DUT is actively outputting content over HDMI before running the script.
- Confirm `hdcp_logs_path` in `device.conf` points to the correct log file path for your firmware build.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_HDCPCOMPLIANCE_MANUAL_01` | Verify the HDMI cable connected status. |
| 2 | `TC_HDCPCOMPLIANCE_MANUAL_02` | Verify the HDCP authentication initiated status. |
| 3 | `TC_HDCPCOMPLIANCE_MANUAL_03` | Verify the HDCP authenticated status. |
| 4 | `TC_HDCPCOMPLIANCE_MANUAL_04` | Verify the HDCP protocol support. |
| 5 | `TC_HDCPCOMPLIANCE_MANUAL_05` | Verify the HDCP enabled status. |
| 6 | `TC_HDCPCOMPLIANCE_MANUAL_06` | Verify the device-supported, received, and current HDCP version. |
| 7 | `TC_HDCPCOMPLIANCE_MANUAL_07` | Verify the HDCP compliant enabled status. |

**device.conf Parameters**: `hdcp_logs_path`, `result_directory`, `issue_logs_directory`

---

### 7.3 Image Formats

**Script**: `Image_formats.sh`
**TC ID Prefix**: `TC_IMAGEFORMATS_MANUAL_`
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- Ensure the DUT has network access to the `app_download_server` to download and install the Browser Test application.
- Confirm `browser_test_app_bundle` and `installed_app_ver` in `device.conf` match the bundle available on your test server.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_IMAGEFORMATS_MANUAL_01` | Verify PNG image format rendering via the Browser Test application. |
| 2 | `TC_IMAGEFORMATS_MANUAL_02` | Verify JPEG image format rendering via the Browser Test application. |
| 3 | `TC_IMAGEFORMATS_MANUAL_03` | Verify SVG image format rendering via the Browser Test application. |
| 4 | `TC_IMAGEFORMATS_MANUAL_04` | Verify WebP image format rendering via the Browser Test application. |

**device.conf Parameters**: `browser_test_app_bundle`, `app_download_server`, `installed_app_ver`, `app_Operations_logs_path`, `result_directory`, `issue_logs_directory`

---

### 7.4 IPv6

**Script**: `IPv6_Automated.sh`
**TC ID Prefix**: `TC_IPv6_MANUAL_`
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- Connect the DUT to an IPv6-supported Wi-Fi SSID before running the script.
- For test cases that require Ethernet, ensure Ethernet is connected with a valid IP address.
- Set `ipv6_conf_SSID` in `device.conf` to the name of the IPv6-capable SSID in your test environment.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_IPv6_MANUAL_01` | Verify IP settings when connected to an IPv6-supported SSID. |
| 2 | `TC_IPv6_MANUAL_02` | Verify the public IPv6 IP address when connected to an IPv6 SSID with Ethernet connected. |
| 3 | `TC_IPv6_MANUAL_03` | Verify the public IPv6 IP address when connected to an IPv6 SSID with Ethernet disconnected. |
| 4 | `TC_IPv6_MANUAL_04` | Verify internet accessibility when connected to an IPv6 SSID with Ethernet connected. |
| 5 | `TC_IPv6_MANUAL_05` | Verify internet accessibility when connected to an IPv6 SSID with Ethernet disconnected. |
| 6 | `TC_IPv6_MANUAL_06` | Verify the Trace API when connected to an IPv6 SSID with Ethernet disconnected. |
| 7 | `TC_IPv6_MANUAL_07` | Verify the Ping API when connected to an IPv6 SSID with Ethernet disconnected. |
| 8 | `TC_IPv6_MANUAL_08` | Verify the getPublicIP API response when connected to an IPv6 SSID with Ethernet connected. |

**device.conf Parameters**: `ipv6_conf_SSID`, `yt_URL`, `result_directory`, `issue_logs_directory`

---

### 7.5 MEMCR

**Script**: `MEMCR_AUTOMATED.sh`
**TC ID Prefix**: `TC_MEMCR_MANUAL_`
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- Install YouTube, YouTubeTV, and Amazon Prime Video on the DUT before running the script.
- Sign in to all three applications with valid user credentials.
- Confirm the `memcr` daemon is running on the DUT: `systemctl status memcr`.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_MEMCR_MANUAL_01` | Verify the MEMCR service status. |
| 2 | `TC_MEMCR_MANUAL_02` | Verify the state of the YouTube app after pressing the Home button post-launch. |
| 3 | `TC_MEMCR_MANUAL_03` | Verify that memory usage decreases after pressing the Home button from the YouTube app. |
| 4 | `TC_MEMCR_MANUAL_04` | Verify YouTube state serialization after Hibernate and Resume. |
| 5 | `TC_MEMCR_MANUAL_05` | Verify the state of the YouTubeTV app after pressing the Home button post-launch. |
| 6 | `TC_MEMCR_MANUAL_06` | Verify that memory usage decreases after pressing the Home button from the YouTubeTV app. |
| 7 | `TC_MEMCR_MANUAL_07` | Verify YouTubeTV state serialization after Hibernate and Resume. |
| 8 | `TC_MEMCR_MANUAL_08` | Verify the state of the Amazon app after pressing the Home button post-launch. |
| 9 | `TC_MEMCR_MANUAL_09` | Verify that memory usage decreases after pressing the Home button from the Amazon app. |
| 10 | `TC_MEMCR_MANUAL_10` | Verify Amazon state serialization after Hibernate and Resume. |

**device.conf Parameters**: `memcr_test_apps`, `app_launch_type`, `yt_URL`, `amz_URL`, `result_directory`, `issue_logs_directory`

---

### 7.6 Power Management

**Script**: `POWER_MGMT_Automated.sh`
**TC ID Prefix**: `TC_POWER_MANUAL_`
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- Set Energy Saver to **OFF** in **Settings → Other Settings → Energy Saver** on the DUT before running the script. The script will prompt you to confirm this setting.
- Install YouTube on the DUT and sign in with valid user credentials.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_POWER_MANUAL_01` | Verify the DUT can enter LIGHT SLEEP state and wake up using RDK service APIs. |

**device.conf Parameters**: `yt_URL`, `result_directory`, `issue_logs_directory`

---

### 7.7 System

**Script**: `System_Automated.sh`
**TC ID Prefix**: `TC_SYSTEM_MANUAL_`
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- Ensure the DUT has Ethernet connected with a valid IP address (the precondition of `TC_SYSTEM_MANUAL_01` verifies this automatically).
- No module-specific `device.conf` parameters need to be updated beyond the common ones.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_SYSTEM_MANUAL_01` | Verify the SSH Dropbear service is active and the device firmware is identified as a valid RDK build. |
| 2 | `TC_SYSTEM_MANUAL_02` | Verify the running status of WPEFramework processes. |
| 3 | `TC_SYSTEM_MANUAL_03` | Verify the log rollover RDK functionality. |

**device.conf Parameters**: `result_directory`, `issue_logs_directory`

---

### 7.8 WebAudio

**Script**: `WEBAUDIO_manual_automated.sh`
**TC ID Prefix**: `TC_WEBAUDIO_MANUAL_`
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- Ensure the DUT has network access to the `app_download_server` to download and install the WebAudio manual test application.
- Confirm `webaudio_app_bundle` and `installed_app_ver` in `device.conf` match the bundle available on your test server.
- Connect a speaker or headset to the DUT — these tests require auditory confirmation of audio output.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_WEBAUDIO_MANUAL_01` | Verify Speech Synthesis Test 1 via the WebAudio application. |
| 2 | `TC_WEBAUDIO_MANUAL_02` | Verify Speech Synthesis Test 2 — supported audio languages. |
| 3 | `TC_WEBAUDIO_MANUAL_03` | Verify Speech Synthesis Test 3 — 3 different audio languages played continuously. |
| 4 | `TC_WEBAUDIO_MANUAL_04` | Verify AudioContext object creation via the WebAudio application. |
| 5 | `TC_WEBAUDIO_MANUAL_05` | Verify AudioContext creation and destruction via the WebAudio application. |
| 6 | `TC_WEBAUDIO_MANUAL_06` | Verify audio playback using the WebAudio API via the WebAudio application. |
| 7 | `TC_WEBAUDIO_MANUAL_07` | Verify FM sound synthesis (Generated Sound FM) via the WebAudio application. |
| 8 | `TC_WEBAUDIO_MANUAL_08` | Verify multimedia playback via the WebAudio application. |
| 9 | `TC_WEBAUDIO_MANUAL_09` | Verify AAC audio decoding — VBR 128 kbps / 44 kHz. |
| 10 | `TC_WEBAUDIO_MANUAL_10` | Verify MP3 audio decoding — 128 kbps / 44 kHz. |
| 11 | `TC_WEBAUDIO_MANUAL_11` | Verify Vorbis audio decoding — VBR 70 kbps / 44 kHz. |
| 12 | `TC_WEBAUDIO_MANUAL_12` | Verify Vorbis audio decoding — VBR 96 kbps / 44 kHz. |
| 13 | `TC_WEBAUDIO_MANUAL_13` | Verify Vorbis audio decoding — VBR 128 kbps / 44 kHz. |
| 14 | `TC_WEBAUDIO_MANUAL_14` | Verify WAV audio decoding — 24-bit / 22 kHz resample. |
| 15 | `TC_WEBAUDIO_MANUAL_15` | Verify WAV audio decoding — 24-bit / 44 kHz. |

**device.conf Parameters**: `webaudio_app_bundle`, `app_download_server`, `installed_app_ver`, `result_directory`, `issue_logs_directory`

---

### 7.9 XCONF Image Upgrade

**Script**: `XCONF_imageUpgrade_Automated.sh`
**TC ID Prefix**: `TC_XCONF_MANUAL_`
**Supported Models**: RPI-Client, Video Accelerator

**Module Prerequisites**:
- Configure all `xconf_*` parameters in `device.conf` with valid values before running the script.
- Ensure the target firmware image is available at the configured `xconf_firmware_dwld_location`.
- Ensure the DUT has network access to the XCONF server.
- Set `xconf_API_key_token` to a valid XCONF REST API authentication token directly on the DUT.

> **Warning**: XCONF upgrade test cases modify the DUT firmware. These are destructive operations. Ensure you have a recovery plan — for example, serial console access and a recovery firmware image — before executing these tests.

**Test Cases**:

| # | TC ID | Description |
|---|-------|-------------|
| 1 | `TC_XCONF_MANUAL_01` | Verify XCONF firmware upgrade behaviour using the RDK service API. |

> **Note**: Additional XCONF test cases (`TC_XCONF_MANUAL_02` through `TC_XCONF_MANUAL_05`) are planned and will be documented in a future revision.

**device.conf Parameters**: `xconf_server_url`, `xconf_config_check_url`, `xconf_imagefile_to_upgrade`, `xconf_imagefile_version`, `xconf_reboot_immediately`, `xconf_firmware_dwld_location`, `xconf_firmwareConfig_name`, `xconf_API_key_token`, `xconf_restApi_firmware_config`, `xconf_firmwareConfig_query_url`, `result_directory`, `issue_logs_directory`

---

## 8. Test Results and Logs

After each test case execution, the script writes the result to the path configured in `result_directory` on the DUT.

### Result Directory Structure

```text
/home/root/test_Execution_results/
├── TC_EXTERNALAUDIO_MANUAL_01_result.txt   # PASS/FAIL result for each TC
├── TC_EXTERNALAUDIO_MANUAL_02_result.txt
├── ...
└── logs/
    ├── TC_EXTERNALAUDIO_MANUAL_01_issue.log  # Detailed failure logs (written only on FAIL)
    └── ...
```

### Retrieving Results from the DUT

After test execution, retrieve the results directory from the DUT to your host machine:

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
| `./device.conf: No such file or directory` or `source: not found` | `device.conf` or `generic_functions.sh` is not in the same directory as the script on the DUT. | Transfer all three files (`script.sh`, `device.conf`, `generic_functions.sh`) to the same working directory on the DUT. |
| `curl: (7) Failed to connect to 127.0.0.1 port 9998` | WPEFramework (Thunder) is not running on the DUT. | Verify Thunder is running: `systemctl status wpeframework`. |
| `Ethernet is not connected to DUT` | The System module precondition check failed — no valid IPv4 address found on `eth0`. | Connect the Ethernet cable and verify the IP address: `ip -4 addr show eth0`. |
| Bluetooth device not found during scan | The device name in `EXT_BT_devices` does not match the device's Bluetooth broadcast name, or the device is not in pairing mode. | Place the Bluetooth device in pairing/discoverable mode. Verify the exact broadcast name using `hciconfig` or a Bluetooth scanning tool. |
| App bundle download fails | The DUT cannot reach the `app_download_server`. | Verify the value of `app_download_server` in `device.conf` and confirm the DUT has network connectivity to that server. |
| XCONF firmware upgrade does not trigger | The XCONF configuration is incorrect, or the API token is invalid. | Verify all `xconf_*` parameters in `device.conf`. Confirm the firmware configuration entry exists on the XCONF server. |
| Test result directory is missing | The `result_directory` path does not exist on the DUT. | Create it manually: `mkdir -p /home/root/test_Execution_results/logs`. |

---

## 10. Known Limitations

| # | Limitation |
|---|------------|
| 1 | **Scripts must run directly on the DUT.** Remote execution from a host machine is not supported. SSH into the DUT first, then run the script from the DUT shell. |
| 2 | **No parallel test execution.** Scripts are designed for sequential, single-instance execution. Running multiple scripts simultaneously on the same DUT is not supported and may produce unreliable results. |
| 3 | **XCONF tests modify DUT firmware.** `TC_XCONF_MANUAL_01` through `TC_XCONF_MANUAL_05` trigger a firmware upgrade on the DUT. These are destructive operations. Ensure a recovery plan — serial console access and a recovery firmware image — is in place before executing. |
| 4 | **Guided prompts require tester presence.** Scripts cannot run unattended. You must be present to observe the DUT and respond to `[yes/no]` prompts during execution. |
| 5 | **BT Audio and HDCP Compliance tests are Video Accelerator only.** `BT_AUDIO_AUTOMATED.sh` and `HDCP_COMPLIANCE_AUTOMATED.sh` do not support RPI-Client hardware. |
| 6 | **IPv6 tests require an IPv6-capable network environment.** An IPv6-supported Wi-Fi SSID must be available in the test environment. These tests cannot run on IPv4-only networks. |
| 7 | **Image Formats and WebAudio tests require internet access for app download.** The DUT must be able to reach the `app_download_server` configured in `device.conf` during test setup. |