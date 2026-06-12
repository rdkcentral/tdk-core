## TestCase ID
RDKV_PERFORMANCE_150
## TestCase Name
RDKV_CERT_PACS_Cobalt_Hibernate_memory_usage_4K_Video_PlayPause
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that memory usage decreases significantly (to less than 1/10th of active state usage) when Cobalt is hibernated during 4K video playback, and that video playback resumes correctly after restoration.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and DeviceInfo plugins should be available in the build.|
|3|`video4K_test_url` must be configured in `PerformanceTestVariables`.|
|4|SSH access parameters must be configured in the device config file for proc/log validation.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt, WebKitBrowser, and DeviceInfo plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states retrieved successfully. |
| 3 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launches and is in the foreground. |
| 4 | Set 4K Video URL | Load the 4K video URL into Cobalt using the deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<video4K_test_url>"}` | Deeplink call returns success. |
| 5 | Start Video Playback | Press the Enter key to begin video playback: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key press sent successfully. |
| 6 | Validate Video Playing | Verify that the 4K video is playing using proc entry validation via SSH. | Video playback is confirmed as active through decoder proc entries. |
| 7 | Capture Memory Usage (Active) | Capture the current process memory usage for Cobalt (CobaltImplementation) before hibernation using the memcr library. | Memory usage value (in MB) is captured for the active state. |
| 8 | Hibernate Cobalt | Suspend Cobalt to transition it to the hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"suspended"}` | Cobalt transitions to hibernated state. |
| 9 | Validate Hibernated State | Verify Cobalt is hibernated: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `hibernated`. |
| 10 | Capture Memory Usage (Hibernated) | Capture Cobalt process memory usage in the hibernated state using the memcr library and compare to active-state usage. | Memory usage in hibernated state is less than 1/10th of the active state memory usage. |
| 11 | Restore Cobalt | Restore Cobalt from the hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"resumed"}` | Cobalt state returns from hibernated to suspended. |
| 12 | Validate Playback Resumed | Verify that video playback has resumed after restoration by checking wpeframework logs via SSH. | Wpeframework log confirms video playback is active again. |
| 13 | Deactivate Cobalt | Deactivate the Cobalt plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Cobalt is deactivated. |
| 14 | Revert Plugin Status | Restore the original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M130<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
