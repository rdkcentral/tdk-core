## TestCase ID
RDKV_PERFORMANCE_19
## TestCase Name
RDKV_CERT_PACS_Cobalt_ResourceUsage_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when the Cobalt application is launched.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt, WebKitBrowser, and DeviceInfo plugins should be available in the build.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of WebKitBrowser, Cobalt, and DeviceInfo plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@DeviceInfo"}` | Plugin states retrieved. |
| 3 | Set Plugin Pre-conditions | Activate DeviceInfo and deactivate Cobalt and WebKitBrowser to prepare a clean state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Plugins set to required state. |
| 4 | Launch Cobalt | Launch Cobalt via RDKShell and verify it is in the foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.getZOrder"}` | Cobalt is launched and in foreground. |
| 5 | Get CPU Load | Retrieve current CPU load percentage from the device. | CPU load value is retrieved. |
| 6 | Validate CPU Load | Verify that the CPU load is within the acceptable threshold (below 90%): <br>`rdkservice_validateCPULoad` with threshold 90.0 | CPU load is within expected range. |
| 7 | Get Memory Usage | Retrieve current memory usage percentage from the device. | Memory usage value is retrieved. |
| 8 | Validate Memory Usage | Verify that memory usage is within the acceptable threshold (below 90%): <br>`rdkservice_validateMemoryUsage` with threshold 90.0 | Memory usage is within expected range. |
| 9 | Deactivate Cobalt | Deactivate the Cobalt plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Cobalt deactivated successfully. |
| 10 | Revert Plugin Status | Restore the original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
