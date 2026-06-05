## TestCase ID
RDKV_STABILITY_72
## TestCase Name
RDKV_CERT_RVS_Cobalt_Hibernate_MultipleApps
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt hibernate memory management with multiple apps by measuring memory before and after hibernation for each app, ensuring memory is reduced during hibernate and within acceptable limits when restored.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list and must support hibernate functionality.|
|3|cobalt_test_url and a secondary YouTube TV app URL must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt and DeviceInfo plugins. Set required states: Cobalt=resumed, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Measure Cobalt memory before hibernate | Launch Cobalt via applicable API calls. Set video URL via deeplink. Get current memory usage for the Cobalt process via DeviceInfo.1.systeminfo. | Cobalt should launch successfully. Initial memory usage should be recorded. |
| 4 | Hibernate Cobalt | Hibernate Cobalt via `org.rdk.RDKShell.1.suspend`. Get memory usage after hibernation. | Cobalt should enter hibernated state. Memory usage should decrease after hibernation. |
| 5 | Restore Cobalt | Restore Cobalt from hibernate via `org.rdk.RDKShell.1.restoreApp`. Verify Cobalt is restored and memory is within acceptable limits. | Cobalt should restore successfully. Memory should return to expected levels. |
| 6 | Launch second app and measure memory | Launch a secondary Cobalt instance (YouTube TV app URL) via deeplink. Get memory usage before hibernation. | Second app should launch successfully. Memory usage should be recorded. |
| 7 | Hibernate second app | Hibernate the second app via `org.rdk.RDKShell.1.suspend`. Get memory usage after hibernation. | Second app should enter hibernated state. Memory should decrease after hibernation. |
| 8 | Restore second app | Restore second app from hibernate via `org.rdk.RDKShell.1.restoreApp`. Validate memory within expected limits. | Second app should restore successfully. Memory should return to acceptable levels. |
| 9 | Validate resource usage | Validate CPU load and memory usage via applicable API calls. | CPU load and memory usage should be within expected limits. |
| 10 | Save CPU/memory data | Save the collected memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all measurement data. |
| 11 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 12 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the hibernate multi-app test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M130<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
