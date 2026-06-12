## TestCase ID
RDKV_PERFORMANCE_22
## TestCase Name
RDKV_CERT_PACS_Cobalt_TimeTo_SuspendResume
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to suspend and resume the Cobalt plugin is within the expected threshold limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin should be available in the build.|
|3|`COBALT_SUSPEND_TIME_THRESHOLD_VALUE`, `COBALT_RESUME_TIME_THRESHOLD_VALUE`, and `THRESHOLD_OFFSET` must be configured in the device config file.|
|4|Time in Test Manager and DUT should be in sync with UTC.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt plugin and ensure it is in resumed state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt plugin state retrieved. |
| 3 | Set Cobalt to Resumed State | Activate Cobalt to ensure it is in the resumed state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt is in resumed state. |
| 4 | Subscribe to onSuspended and onLaunched Events | Register WebSocket listener for both `onSuspended` and `onLaunched` events from RDKShell: <br>`{"jsonrpc":"2.0","id":5,"method":"org.rdk.RDKShell.1.register","params":{"event":"onSuspended","id":"client.events.1"}}`<br>`{"jsonrpc":"2.0","id":6,"method":"org.rdk.RDKShell.1.register","params":{"event":"onLaunched","id":"client.events.1"}}` | Event subscriptions established. |
| 5 | Suspend Cobalt (Timed) | Save current system time and suspend Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"suspended"}` | Suspend call sent; start time recorded. |
| 6 | Validate Cobalt Suspended | Verify Cobalt is in the suspended state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `suspended`. |
| 7 | Resume Cobalt (Timed) | Save current system time and resume Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Launch call sent; resume start time recorded. |
| 8 | Validate Cobalt Resumed | Confirm Cobalt is back in resumed state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `resumed`. |
| 9 | Capture and Validate Suspend/Resume Times | Retrieve `onSuspended` and `onLaunched` events from the listener buffer. Calculate: <br>- Suspend time = `onSuspended` event timestamp - suspend start time. Validate against `COBALT_SUSPEND_TIME_THRESHOLD_VALUE`. <br>- Resume time = `onLaunched` event timestamp - resume start time. Validate against `COBALT_RESUME_TIME_THRESHOLD_VALUE`. | Both suspend time and resume time are within their respective configured threshold values. |
| 10 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 8

**Priority** : High

**Release Version** : M85<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
