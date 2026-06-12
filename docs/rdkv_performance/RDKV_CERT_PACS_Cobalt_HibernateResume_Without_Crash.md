## TestCase ID
RDKV_PERFORMANCE_152
## TestCase Name
RDKV_CERT_PACS_Cobalt_HibernateResume_Without_Crash
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that no crash is observed during the hibernate and restore process of the Cobalt application.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin should be available in the build.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online within the expected time. |
| 2 | Check Plugin Status | Check the current state of Cobalt and WebKitBrowser plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states are retrieved successfully. |
| 3 | Launch Cobalt | Launch Cobalt via RDKShell and verify it is in the foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launches successfully and is in foreground. |
| 4 | Hibernate Cobalt | Suspend Cobalt to transition it to hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"suspended"}` | Cobalt state changes to suspended/hibernated. |
| 5 | Validate Hibernated State | Verify Cobalt is in the hibernated state and check for crashes via SSH wpeframework log inspection: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `hibernated`; no crash is observed. |
| 6 | Restore Cobalt | Restore Cobalt from hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"resumed"}` | Cobalt state transitions from hibernated to suspended/resumed successfully. |
| 7 | Validate Restored State | Verify Cobalt state after restore and check for any crash via wpeframework log via SSH. | Cobalt is in the suspended state; no crash is observed. |
| 8 | Resume Cobalt | Resume Cobalt application to the active state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt is in the resumed state. |
| 9 | Check for Crash After Resume | Verify no crash is observed after resuming Cobalt by inspecting wpeframework logs via SSH. | No crash log entries are present; device and Cobalt remain stable. |
| 10 | Revert Plugin Status | Restore original plugin states as captured before the test. | Plugins reverted to original state successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M130<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
