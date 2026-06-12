## TestCase ID
RDKV_PERFORMANCE_95
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_ChangeSystemMode
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to change the system mode (e.g., normal mode, EAS mode, etc.) is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.System` plugin should be available for system mode control.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Start Time | Record UTC timestamp before sending the system mode change request. | Start time recorded. |
| 3 | Change System Mode | Send system mode change request: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setMode","params":{"modeInfo":{"mode":"<mode>","duration":<duration>}}}` | Mode change request sent. |
| 4 | Record End Time | Record UTC timestamp after system mode change completes. | End time recorded. |
| 5 | Validate Time | Calculate time to change system mode = end timestamp - start timestamp. Compare against threshold. | Time to change system mode is within the expected threshold. |
| 6 | Revert System Mode | Restore the original system mode. | System mode reverted. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 3

**Priority** : High

**Release Version** : M96<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
