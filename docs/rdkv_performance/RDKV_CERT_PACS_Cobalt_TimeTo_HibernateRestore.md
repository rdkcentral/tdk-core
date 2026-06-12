## TestCase ID
RDKV_PERFORMANCE_148
## TestCase Name
RDKV_CERT_PACS_Cobalt_TimeTo_HibernateRestore
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to hibernate (suspend) and restore the Cobalt application is within the expected threshold limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin should be available in the build.|
|3|`COBALT_HIBERNATE_TIME_THRESHOLD_VALUE` and `COBALT_RESTORE_TIME_THRESHOLD_VALUE` must be configured in the device config file.|
|4|Time in Test Manager and DUT should be in sync with UTC.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Plugin state retrieved. |
| 3 | Set Cobalt to Resumed State | Ensure Cobalt is in the resumed state; restore from hibernated state if needed: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"resumed"}` | Cobalt is in resumed state. |
| 4 | Subscribe to onHibernated and onRestored Events | Register a WebSocket listener for both `onHibernated` and `onRestored` events from RDKShell: <br>`{"jsonrpc":"2.0","id":7,"method":"org.rdk.RDKShell.1.register","params":{"event":"onHibernated","id":"client.events.1"}}`<br>`{"jsonrpc":"2.0","id":8,"method":"org.rdk.RDKShell.1.register","params":{"event":"onRestored","id":"client.events.1"}}` | Event subscriptions established. |
| 5 | Hibernate Cobalt (Timed) | Save current system time and suspend Cobalt to initiate hibernation: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"suspended"}` | Suspend call sent; hibernate start time recorded. |
| 6 | Validate Hibernated State | Verify Cobalt transitions to hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `hibernated`. |
| 7 | Capture Hibernate Time | Retrieve the `onHibernated` event from the listener, extract its timestamp, and calculate time taken to hibernate by comparing to the hibernate start time. Validate against `COBALT_HIBERNATE_TIME_THRESHOLD_VALUE`. | Time taken to hibernate Cobalt is within the configured threshold. |
| 8 | Restore Cobalt (Timed) | Save current system time and restore Cobalt from hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"resumed"}` | Restore call sent; restore start time recorded. |
| 9 | Validate Cobalt Suspended State | Verify Cobalt transitions to suspended state after restore: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `suspended`. |
| 10 | Resume Cobalt (Timed) | Launch Cobalt to put it in the resumed state and record resume start time: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt is resumed. |
| 11 | Capture Restore Time | Retrieve the `onRestored` event from the listener and calculate restore time against `COBALT_RESTORE_TIME_THRESHOLD_VALUE`. | Time taken to restore Cobalt is within the configured threshold. |
| 12 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
