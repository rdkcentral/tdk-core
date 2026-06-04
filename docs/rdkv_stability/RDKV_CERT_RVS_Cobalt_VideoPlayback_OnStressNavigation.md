## TestCase ID
RDKV_STABILITY_57
## TestCase Name
RDKV_CERT_RVS_Cobalt_VideoPlayback_OnStressNavigation
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Cobalt can successfully play video after 99 stress navigation key operations, verifying the device remains stable under continuous key navigation stress.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list.|
|3|cobalt_test_url must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt | Launch Cobalt via using `org.rdk.RDKShell.1.launch`. | Cobalt should launch successfully. |
| 4 | Stress navigation loop (10 outer iterations × 10 key navigations) | For each of 10 outer iterations: <br>Send 10 navigation key events to Cobalt via `org.rdk.RDKShell.1.generateKey` (arrow keys and select). <br>Validate CPU load and memory usage via after each outer iteration. | Navigation key events should be delivered. CPU load and memory usage should remain within expected limits. |
| 5 | Final video playback validation (100th operation) | Send OK key to select and play a video: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":13,"modifiers":[],"client":"Cobalt"}}` <br>Validate video is playing via applicable API calls. | Video should start playing after the navigation stress. Video decoder proc entry should be present. |
| 6 | Destroy Cobalt | Destroy Cobalt via `org.rdk.RDKShell.1.destroy`. | Cobalt should be destroyed successfully. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 8 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 9 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 120

**Priority** : High

**Release Version** : M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
