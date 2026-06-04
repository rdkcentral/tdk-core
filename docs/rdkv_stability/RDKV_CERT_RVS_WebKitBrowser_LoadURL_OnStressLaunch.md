## TestCase ID
RDKV_STABILITY_50
## TestCase Name
RDKV_CERT_RVS_WebKitBrowser_LoadURL_OnStressLaunch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that WebKitBrowser can successfully load a URL after 99 continuous launch-and-destroy stress cycles, verifying CPU and memory usage remains within expected limits and URL loading functions correctly after extended stress.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be available in the supported plugins list.|
|3|webkit_url must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, Cobalt, and DeviceInfo plugins. Set required states: WebKitBrowser=deactivated, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Stress launch-and-destroy loop (99 iterations) | For each of 99 iterations: <br>Launch WebKitBrowser via : launch via `org.rdk.RDKShell.1.launch` → verify activated → destroy via `org.rdk.RDKShell.1.destroy` → verify deactivated. <br>Validate CPU load and memory usage via applicable API calls. | WebKitBrowser should launch and be destroyed successfully in each of 99 iterations. CPU load and memory usage should remain within expected limits. |
| 4 | Final URL load validation (100th iteration) | On the 100th iteration: <br>Launch WebKitBrowser via `org.rdk.RDKShell.1.launch`. <br>Set webkit_url: `{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"value":"<webkit_url>"}}` <br>Verify URL is set correctly by getting the current URL. <br>Destroy WebKitBrowser via `org.rdk.RDKShell.1.destroy`. | WebKitBrowser should successfully load URL after 99 stress cycles. URL should be set and verified correctly. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 120

**Priority** : High

**Release Version** : M93<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
