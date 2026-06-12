## TestCase ID
RDKV_PERFORMANCE_81
## TestCase Name
RDKV_CERT_PACS_Cobalt_ToggleInterface_onVideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that video playback in Cobalt continues without interruption even after the network interface is toggled between WiFi and Ethernet.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|The DUT should be connected and configured with WiFi IP, or a WiFi Access Point with the same IP range must be available.|
|3|A Lightning application for IP-change detection should be hosted and `ip_change_app_url` configured in `PerformanceTestVariables`.|
|4|`cobalt_test_url` must be configured in `PerformanceTestVariables`.|
|5|`tm_username` and `tm_password` must be configured.|
|6|SSH access parameters must be configured in device config.|
|7|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt, WebKitBrowser, and org.rdk.NetworkManager plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@org.rdk.NetworkManager"}` | Plugin states retrieved. |
| 3 | Set Plugin Pre-conditions | Activate NetworkManager and deactivate Cobalt and WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"org.rdk.NetworkManager"}}` | Plugins set to required state. |
| 4 | Check Current Network Interface | Determine the currently active network interface (eth0 or wlan0) using the IP-change detection utility. | Current network interface is identified. |
| 5 | Launch Cobalt | Launch Cobalt via RDKShell and verify it is in the foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launched and in foreground. |
| 6 | Set Video URL | Load the video URL into Cobalt using the deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<cobalt_test_url>"}` | Deeplink returns success. |
| 7 | Start Video Playback | Press Enter key twice (once to play, once to skip ad) to start video playback: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key presses sent. |
| 8 | Validate Video Playing Before Toggle | Verify video playback is active via proc entry validation or wpeframework log via SSH. | Video playback is confirmed as active. |
| 9 | Toggle Network Interface | Toggle the active network interface to the alternate interface (e.g., from eth0 to wlan0) using `org.rdk.Network.1.setInterfaceEnabled`. | Network interface toggle is completed. |
| 10 | Validate Video Playing After Toggle | Verify video playback is still active after the network interface toggle via proc entry validation or wpeframework log. | Video playback continues after network interface toggle. |
| 11 | Revert Network Interface | Restore the original network interface. | Network interface reverted. |
| 12 | Deactivate Cobalt | Deactivate the Cobalt plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Cobalt deactivated. |
| 13 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
