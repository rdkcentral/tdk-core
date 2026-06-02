## TestCase ID
RDKV_STABILITY_33
## TestCase Name
RDKV_CERT_RVS_Cobalt_Video_SearchAndPlay
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly navigating to the Cobalt search feature, entering search keywords, playing search results, and returning to home for cobalt_search_max_count iterations, verifying CPU and memory usage remains within expected limits throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list.|
|3|cobalt_search_max_count and cobalt_search_keyword must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt | Launch Cobalt via `launch_plugin` using `org.rdk.RDKShell.1.launch`. | Cobalt should launch successfully. |
| 4 | Search and play loop (repeat for cobalt_search_max_count iterations) | For each iteration: <br>Navigate to the search field using arrow keys via `org.rdk.RDKShell.1.generateKey`. <br>Send individual character key codes for the search keyword using `org.rdk.RDKShell.1.generateKey`. <br>Press OK to confirm search: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":13,"modifiers":[],"client":"Cobalt"}}` <br>Navigate to first search result and press OK to play. <br>Validate video is playing via `rdkservice_validateProcEntry`. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. <br>Press Home key to navigate back to the home screen. | Search and playback should succeed in each iteration. Video decoder proc entry should be present during playback. CPU load and memory usage should remain within expected limits. |
| 5 | Destroy Cobalt | Destroy Cobalt via `org.rdk.RDKShell.1.destroy`. | Cobalt should be destroyed successfully. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 7 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the search and play stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 4000

**Priority** : High

**Release Version** : M88<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
