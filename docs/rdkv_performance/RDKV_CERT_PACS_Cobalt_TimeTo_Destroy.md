## TestCase ID
RDKV_PERFORMANCE_71
## TestCase Name
RDKV_CERT_PACS_Cobalt_TimeTo_Destroy
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to destroy the Cobalt plugin is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the build.|
|3|Time in Test Manager and DUT should be in sync with UTC.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt and WebKitBrowser plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states retrieved. |
| 3 | Set Plugin Pre-conditions | Deactivate Cobalt and WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Plugins deactivated. |
| 4 | Subscribe to onDestroyed Event | Register a WebSocket listener for the `onDestroyed` event from RDKShell: <br>`{"jsonrpc":"2.0","id":6,"method":"org.rdk.RDKShell.1.register","params":{"event":"onDestroyed","id":"client.events.1"}}` | Event subscription is established successfully. |
| 5 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt is launched and in resumed state. |
| 6 | Validate Cobalt Status | Verify Cobalt is in resumed state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `resumed`. |
| 7 | Destroy Cobalt (Timed) | Record current system time and destroy Cobalt plugin via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.destroy","params":{"callsign":"Cobalt"}}` | Destroy call is sent; destroy start time recorded. |
| 8 | Capture onDestroyed Event | Wait for and capture the `onDestroyed` event from the WebSocket listener. Extract the event timestamp from the event payload. | `onDestroyed` event is received for Cobalt with a valid timestamp. |
| 9 | Validate Destroy Time | Calculate the time taken to destroy Cobalt by comparing the destroy start time to the `onDestroyed` event timestamp. Validate against the configured `COBALT_DESTROY_TIME_THRESHOLD_VALUE` in the device config file. | Time taken to destroy Cobalt is within the expected threshold. |
| 10 | Revert Plugin Status | Restore the original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 2

**Priority** : High

**Release Version** : M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
