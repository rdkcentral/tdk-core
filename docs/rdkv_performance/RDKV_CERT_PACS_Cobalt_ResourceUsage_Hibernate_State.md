## TestCase ID
RDKV_PERFORMANCE_146
## TestCase Name
RDKV_CERT_PACS_Cobalt_ResourceUsage_Hibernate_State
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when the Cobalt application is placed in the hibernated state.

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
| 2 | Check Plugin Status | Check the current state of Cobalt, WebKitBrowser, and DeviceInfo plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@DeviceInfo"}` | Plugin states retrieved. |
| 3 | Set Plugin Pre-conditions | Activate DeviceInfo and deactivate Cobalt and WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"WebKitBrowser"}}` | Plugins set to required state. |
| 4 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt is launched and in foreground. |
| 5 | Validate Cobalt Resumed State | Verify Cobalt is in resumed state after launch: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `resumed`. |
| 6 | Get Cobalt Process ID | Get the process ID of CobaltImplementation for memory tracking using memcr library. | Process ID retrieved successfully. |
| 7 | Capture Memory Before Hibernate | Capture the memory usage of CobaltImplementation process before hibernation via memcr library. | Memory usage captured in MB. |
| 8 | Hibernate Cobalt | Suspend Cobalt to transition it to hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"suspended"}` | Cobalt transitions to hibernated state. |
| 9 | Validate Hibernated State | Confirm Cobalt state is hibernated: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `hibernated`. |
| 10 | Capture Memory After Hibernate | Capture CobaltImplementation process memory usage in hibernated state using memcr library and compare. | Memory usage in hibernated state is reduced compared to active state and within expected limits. |
| 11 | Validate Resource Usage | Verify overall system CPU load and memory usage are within acceptable thresholds. | CPU and memory usage are within expected limits. |
| 12 | Revert Plugin Status | Restore the original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
