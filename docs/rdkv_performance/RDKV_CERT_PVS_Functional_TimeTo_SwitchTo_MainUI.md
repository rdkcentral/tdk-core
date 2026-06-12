## TestCase ID
RDKV_PERFORMANCE_30
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_SwitchTo_MainUI
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to switch from a running application back to the main UI is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Main UI application and at least one other application must be available.|
|3|`SWITCH_TO_MAIN_UI_THRESHOLD` must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Launch Secondary App | Activate a secondary application. | Secondary app active. |
| 3 | Record Switch Start Time | Record UTC timestamp before switching to main UI. | Start time recorded. |
| 4 | Switch to Main UI | Set the main UI as the front application: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.moveToFront","params":{"client":"<main_ui_client>"}}` | Main UI brought to front. |
| 5 | Record Main UI Active Time | Record UTC timestamp when main UI is active. | End time recorded. |
| 6 | Validate Time | Calculate switch time = end timestamp - start timestamp. Compare against threshold. | Time to switch to main UI is within the expected threshold. |
| 7 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
