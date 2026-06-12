## TestCase ID
RDKV_PERFORMANCE_32
## TestCase Name
RDKV_CERT_PVS_Apps_Cobalt_ResourceUsage_Onboot
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when Cobalt (YouTube) is launched immediately after a device reboot.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt, WebKitBrowser, and DeviceInfo plugins should be available in the build.|
|3|The device should be able to reboot and recover for testing.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Reboot Device | Reboot the device as part of the test using `rdkservice_rebootDevice` with `REBOOT_WAIT_TIME` from device config. | Device reboots and comes back online. |
| 3 | Validate Uptime | Query `DeviceInfo.1.systeminfo` and check the `uptime` field to confirm the device has just rebooted (uptime < 280 seconds). | Device uptime is below 280 seconds, confirming a fresh boot. |
| 4 | Check Plugin Status | Verify and set plugin status: deactivate WebKitBrowser and Cobalt, activate DeviceInfo: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Plugins confirmed in required state. |
| 5 | Launch Cobalt | Launch Cobalt via RDKShell immediately after reboot: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launches successfully. |
| 6 | Validate Resource Usage | Capture and validate CPU load and memory usage while Cobalt is running immediately after reboot. | CPU load and memory usage are within the expected acceptable limits. |
| 7 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
