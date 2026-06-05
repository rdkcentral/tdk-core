## TestCase ID
RDKV_STABILITY_04
## TestCase Name
RDKV_CERT_RVS_URL_Redirect
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly setting URLs that trigger HTTP redirects in WebKitBrowser for url_redirect_max_count iterations, verifying the browser follows redirects correctly and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be in resumed state; Cobalt plugin must be deactivated; DeviceInfo plugin must be activated.|
|3|redirect_url and url_redirect_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, Cobalt, and DeviceInfo plugins. Set required states: WebKitBrowser=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Get current URL | Retrieve the current URL loaded in WebKitBrowser: `{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url"}` Save as initial URL. | Current URL should be retrieved successfully. |
| 4 | URL redirect loop (repeat for url_redirect_max_count iterations) | For each iteration: <br>Set the redirect URL in WebKitBrowser: `{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"value":"<redirect_url>"}}` <br>Wait for WebKitBrowser to follow the redirect (poll URL until it changes from redirect_url). <br>Verify the final URL after redirect is the expected destination URL. <br>Validate CPU load and memory usage via applicable API calls. | WebKitBrowser should follow the redirect successfully in each iteration. Final URL should match the expected redirect destination. CPU load and memory usage should remain within expected limits. |
| 5 | Restore initial URL | Set WebKitBrowser URL back to the original URL saved before the test. | Original URL should be restored. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 7 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the URL redirect stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 620

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
