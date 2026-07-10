## TestCase ID
RDKV_MANUAL_MEMCR_08
## TestCase Name
RDKV_CERT_MANUAL_MEMCR_PRIME_HIBERNATE_ON_HOMEKEY_PRESS

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Amazon Prime Video application transitions to the APP_STATE_HIBERNATED state when the Home key is pressed while Amazon Prime Video is active.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned. |
| 3 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 4 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT. |
| 5 | Verify MEMCR App on home screen | Verify that the MEMCR App is available in the My Apps section/row of the RDK UI Home screen. If the MEMCR App is already present, skip the remaining installation steps. | The MEMCR App should be visible in the My Apps section of the RDK UI Home screen or be available for installation. |
| 6 | Install MEMCR App | Select the MEMCR App tile on the Recommended Apps row and press Enter/OK on the remote. Verify that a loading indicator appears on the tile. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The MEMCR App should be installed successfully on the DUT. |
| 7 | Verify MEMCR App listed on home screen | Verify that the installed MEMCR App is listed under the My Apps section/row of the RDK UI Home screen, ready to launch. | The MEMCR App should be visible in the My Apps section of the RDK UI Home screen and ready to launch. |
| 8 | Verify MEMCR App package in /opt/CDL/ | Verify that the MEMCR App package is downloaded and available in the /opt/CDL/ directory of the DUT.<br>Command: `ls -lh /opt/CDL/` | The MEMCR App package should be listed in the /opt/CDL/ directory of the DUT. |
| 9 | Sign in to apps and verify A/V playback | After installing and launching the YouTube or Amazon Prime application, sign in with valid user credentials and verify A/V playback is functional prior to the Memcr test execution. | Sign-in should succeed and A/V playback should be functional in the installed application. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch Amazon Prime Video app | Select the Amazon Prime Video App tile from the My Apps / Recommended Apps section and press Enter/OK on the remote. | The Amazon Prime Video App should launch successfully (cold launch or hot launch based on the app's previous state). |
| 2 | Select content and initiate Amazon Prime playback | Select any video content and initiate playback on Amazon Prime Video. | A/V playback on Amazon Prime Video should start successfully. |
| 3 | Query app state via API | Execute the following curl command in the DUT serial console or SSH terminal to query the current app state.<br>Command: `curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 6, "method": "org.rdk.AppManager.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | The Amazon Prime Video App state returned by getLoadedApps should be APP_STATE_ACTIVE. |
| 4 | Press Home key on remote | Press the Home key on the remote. | The RDK UI Home screen should be displayed. |
| 5 | Query app state after Home key press | Execute the following curl command in the DUT serial console or SSH terminal to query the current app state.<br>Command: `curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 6, "method": "org.rdk.AppManager.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | The Amazon Prime Video App state returned by getLoadedApps should be APP_STATE_HIBERNATED. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
