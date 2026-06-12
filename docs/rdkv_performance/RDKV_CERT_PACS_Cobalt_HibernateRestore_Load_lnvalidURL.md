## TestCase ID
RDKV_PERFORMANCE_153
## TestCase Name
RDKV_CERT_PACS_Cobalt_HibernateRestore_Load_lnvalidURL
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that no crash is observed when Cobalt is resumed from a hibernated state and loaded with an invalid URL via the deeplink method.

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
| 4 | Hibernate Cobalt | Suspend (hibernate) the Cobalt plugin by setting its state to suspended: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"suspended"}` | Cobalt state changes to suspended/hibernated. |
| 5 | Validate Hibernated State | Verify Cobalt is in the hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is reported as `hibernated`. |
| 6 | Restore Cobalt | Restore Cobalt from hibernated state by setting its state to resumed: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"resumed"}` | Cobalt state changes to suspended (restored from hibernate). |
| 7 | Validate Restored State | Verify Cobalt state after restore: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt is in the suspended/resumed state after restore. |
| 8 | Resume Cobalt with Invalid URL | Use the deeplink method to resume Cobalt with an invalid URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<invalid_url>"}` | Deeplink call is sent. Cobalt handles the invalid URL without crashing. |
| 9 | Check for Crash | Verify no crash is observed by checking wpeframework logs via SSH for crash indicators. | No crash log entries are present; device remains stable. |
| 10 | Revert Plugin Status | Restore original plugin states as captured before the test. | Plugins reverted to original state successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M130<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
