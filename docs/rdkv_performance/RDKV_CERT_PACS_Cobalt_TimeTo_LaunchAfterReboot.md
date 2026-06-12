## TestCase ID
RDKV_PERFORMANCE_63
## TestCase Name
RDKV_CERT_PACS_Cobalt_TimeTo_LaunchAfterReboot
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch the Cobalt plugin immediately after a device reboot is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt, WebKitBrowser, and DeviceInfo plugins should be available in the build.|
|3|`COBALT_LAUNCH_AFTER_BOOT_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be configured in the device config file.|
|4|Time in Test Manager and DUT should be in sync.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of WebKitBrowser, Cobalt, and DeviceInfo plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@DeviceInfo"}` | Plugin states retrieved. |
| 3 | Reboot Device | Reboot the DUT using the WPEFramework harakiri method and wait for device to come back online: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.harakiri"}` | Device reboots successfully and comes back online within 160 seconds. |
| 4 | Get Device Uptime | Retrieve device uptime to confirm fresh reboot: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"DeviceInfo.1.systeminfo","params":{"reqValue":"uptime"}}` | Device uptime is less than 240 seconds, confirming fresh reboot. |
| 5 | Set Plugin Pre-conditions | After reboot, activate DeviceInfo and deactivate Cobalt and WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}` | Plugins set to required state. |
| 6 | Subscribe to onLaunched Event | Register a WebSocket listener for the `onLaunched` event from RDKShell: <br>`{"jsonrpc":"2.0","id":6,"method":"org.rdk.RDKShell.1.register","params":{"event":"onLaunched","id":"client.events.1"}}` | Event subscription established. |
| 7 | Launch Cobalt (Timed) | Record current system time and launch Cobalt immediately after reboot: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launch initiated; start time recorded. |
| 8 | Validate Cobalt Resumed | Confirm Cobalt is in the resumed state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `resumed`. |
| 9 | Capture onLaunched Event | Wait for and capture the `onLaunched` event for Cobalt from the listener. Extract the event timestamp. | `onLaunched` event received for Cobalt with a valid timestamp. |
| 10 | Validate Launch Time After Reboot | Calculate the time taken to launch Cobalt after reboot by comparing launch start time to the `onLaunched` event timestamp. Validate against `COBALT_LAUNCH_AFTER_BOOT_THRESHOLD_VALUE` + `THRESHOLD_OFFSET`. | Time taken to launch Cobalt after reboot is within the expected threshold. |
| 11 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 8

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
