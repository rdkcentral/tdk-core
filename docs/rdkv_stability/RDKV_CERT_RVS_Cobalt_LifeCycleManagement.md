## TestCase ID
RDKV_STABILITY_40
## TestCase Name
RDKV_CERT_RVS_Cobalt_LifeCycleManagement
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt plugin stability by executing a complete lifecycle management sequence (launch, set URL, suspend, resume, moveToBack, moveToFront, destroy) for lifecycle_max_count iterations, verifying CPU and memory usage remains within expected limits throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list.|
|3|cobalt_test_url and lifecycle_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=deactivated, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Lifecycle management loop (repeat for lifecycle_max_count iterations) | For each iteration, execute `rdkservice_executeLifeCycle` for Cobalt with operations including the Cobalt deeplink URL: <br>Launch Cobalt via `org.rdk.RDKShell.1.launch`. <br>Set video URL via deeplink: `{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_test_url>"}}` <br>Verify video is playing via `rdkservice_validateProcEntry`. <br>Suspend Cobalt via `org.rdk.RDKShell.1.suspend` and verify status is "suspended". <br>Resume Cobalt via `org.rdk.RDKShell.1.launch` and verify status is "resumed". <br>Move Cobalt to back via `org.rdk.RDKShell.1.moveToBack`. <br>Move Cobalt to front via `org.rdk.RDKShell.1.moveToFront`. <br>Destroy Cobalt via `org.rdk.RDKShell.1.destroy`. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | All lifecycle transitions should succeed. Video should play after each launch and after resume. CPU load and memory usage should remain within expected limits. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the lifecycle stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 5000

**Priority** : High

**Release Version** : M90<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
