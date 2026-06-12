## TestCase ID
RDKV_PERFORMANCE_36
## TestCase Name
RDKV_CERT_PACS_Cobalt_TimeTo_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch the Cobalt plugin is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the build.|
|3|`COBALT_LAUNCH_TIME_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be configured in the device config file.|
|4|Time in Test Manager and DUT should be in sync with UTC.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt and WebKitBrowser plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states retrieved. |
| 3 | Set Plugin Pre-conditions | Deactivate Cobalt and WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Plugins deactivated. |
| 4 | Subscribe to onLaunched Event | Register a WebSocket listener for the `onLaunched` event from RDKShell: <br>`{"jsonrpc":"2.0","id":6,"method":"org.rdk.RDKShell.1.register","params":{"event":"onLaunched","id":"client.events.1"}}` | Event subscription established. |
| 5 | Launch Cobalt (Timed) | Record current system time and launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Launch call sent; launch start time recorded. |
| 6 | Validate Cobalt Resumed | Verify Cobalt is in the resumed state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `resumed`. |
| 7 | Capture onLaunched Event | Wait for and capture the `onLaunched` event from the WebSocket listener. Extract the event timestamp. | `onLaunched` event is received for Cobalt with a valid timestamp. |
| 8 | Validate Launch Time | Calculate time taken to launch Cobalt by comparing the launch start time to the `onLaunched` event timestamp. Validate against the configured `COBALT_LAUNCH_TIME_THRESHOLD_VALUE` + `THRESHOLD_OFFSET`. | Time taken to launch Cobalt is within the expected threshold. |
| 9 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M88<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
