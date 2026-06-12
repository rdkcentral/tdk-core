## TestCase ID
RDKV_PERFORMANCE_12
## TestCase Name
RDKV_CERT_PACS_Cobalt_PlayNext
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Cobalt can navigate through YouTube videos and play the next video successfully by sending key events.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the build.|
|3|SSH access parameters (method, credentials, video validation script) must be configured in the device config file.|
|4|TV must be connected to the DUT.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of WebKitBrowser and Cobalt plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Plugin states retrieved successfully. |
| 3 | Set Plugin Pre-conditions | Deactivate WebKitBrowser and Cobalt if not already deactivated: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"WebKitBrowser"}}` | Plugins set to required deactivated state. |
| 4 | Launch Cobalt | Launch Cobalt via RDKShell and verify it is in the foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.getZOrder"}` | Cobalt is launched and present in foreground. |
| 5 | Navigate to Next Video | Send Down Arrow key followed by Right Arrow key to navigate to the next video: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":40,"modifiers":[],"delay":1.0},{"keyCode":39,"modifiers":[],"delay":1.0}]}}` | Navigation key presses sent successfully. |
| 6 | Select Video (Press OK) | Press the Enter key (OK) to select and play the highlighted video: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | OK key press sent successfully. |
| 7 | Validate Video Playback | Verify video playback of the selected next video using proc entries via SSH. | Decoder proc entries confirm video is playing. |
| 8 | Revert Plugin Status | Restore original plugin states as captured before the test. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
