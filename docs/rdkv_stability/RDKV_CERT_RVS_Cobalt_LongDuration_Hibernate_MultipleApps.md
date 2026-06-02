## TestCase ID
RDKV_STABILITY_73
## TestCase Name
RDKV_CERT_RVS_Cobalt_LongDuration_Hibernate_MultipleApps
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt hibernate memory management with multiple apps over a long duration by measuring memory before and after long-duration hibernation for each app, ensuring memory is properly managed during and after restore.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list and must support hibernate functionality.|
|3|hibernate_wait_duration and cobalt_test_url (plus secondary app URL) must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt and DeviceInfo plugins. Set required states: Cobalt=resumed, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Measure and hibernate first Cobalt app | Launch Cobalt. Set video URL via deeplink. Get memory usage. Hibernate Cobalt via `org.rdk.RDKShell.1.suspend`. Wait for hibernate_wait_duration seconds. Get memory usage during long hibernate. | Cobalt should hibernate and memory should decrease during hibernation. |
| 4 | Restore first Cobalt app | Restore Cobalt from hibernate via `org.rdk.RDKShell.1.restoreApp`. Resume Cobalt. Verify memory is within acceptable limits after restore. | Cobalt should restore successfully after long-duration hibernation. Memory should return to acceptable levels. |
| 5 | Measure and hibernate second app | Launch a secondary Cobalt instance via deeplink. Get memory usage. Hibernate via `org.rdk.RDKShell.1.suspend`. Wait for hibernate_wait_duration seconds. Get memory during long hibernate. | Second app should hibernate. Memory should decrease during hibernation. |
| 6 | Restore second app | Restore second app from hibernate via `org.rdk.RDKShell.1.restoreApp`. Resume. Validate memory within expected limits. | Second app should restore successfully. Memory should return to acceptable levels. |
| 7 | Validate resource usage | Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | CPU load and memory usage should be within expected limits. |
| 8 | Save CPU/memory data | Save the collected memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all measurement data. |
| 9 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 10 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the long-duration hibernate multi-app test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 185

**Priority** : High

**Release Version** : M130<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
