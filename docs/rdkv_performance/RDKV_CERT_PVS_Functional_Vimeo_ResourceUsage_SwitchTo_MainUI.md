## TestCase ID
RDKV_PERFORMANCE_130
## TestCase Name
RDKV_CERT_PVS_Functional_Vimeo_ResourceUsage_SwitchTo_MainUI
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when switching from the Vimeo application back to the main UI.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|The application plugin used for Vimeo must be available in the build.|
|3|Main UI application must be available.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Launch Vimeo Application | Launch Vimeo and allow it to fully load. | Vimeo application active. |
| 3 | Capture Baseline Resource Usage | Record CPU and memory usage with Vimeo active. | Baseline recorded. |
| 4 | Switch to Main UI | Bring the main UI to front: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.moveToFront","params":{"client":"<main_ui_client>"}}` | Main UI brought to front. |
| 5 | Capture Resource Usage After Switch | Record CPU and memory usage after switching to main UI. | Resource data captured. |
| 6 | Validate Resource Usage | Verify CPU load and memory usage during the switch are within acceptable limits. | CPU load and memory usage when switching from Vimeo to main UI are within the expected limits. |
| 7 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M105<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
