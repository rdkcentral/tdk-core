## TestCase ID
RDKV_PERFORMANCE_82
## TestCase Name
RDKV_CERT_PVS_Browser_Strike_720_resolution
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the browser performance score obtained from the Strike benchmark tool at 720p (1280x720) resolution using WebKitBrowser and confirm the score meets the configured threshold value.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify WPEFramework status | WPEFramework process must be up and running on the device before test execution begins. | WPEFramework process should be active and accessible on the device. |
| 2 | Configure pre-requisite reboot | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | Device should be in a clean state prior to performance test execution. |
| 3 | Configure Strike tool URL and webinspect port | `strike_tool_url` must be set in BrowserPerformanceVariables and `webinspect_port` must be configured in PerformanceTestVariables with the correct port for the WebKit inspector. | The Strike tool URL must be reachable from the device and the webinspect port must be valid. |
| 4 | Configure threshold value in device config | `STRIKE_THRESHOLD_VALUE` must be configured in the device-specific configuration file with the expected minimum score for the Strike benchmark. | Threshold value should be available and non-empty for score validation. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot device as pre-requisite | If `PRE_REQ_REBOOT_PVS` is configured as Yes, reboot the device by issuing the harakiri command and wait 150 seconds for reboot to complete: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should reboot successfully and come back online within the wait period. |
| 2 | Check WebKitBrowser and Cobalt plugin status | Query the current status of WebKitBrowser and Cobalt plugins to determine whether pre-requisites are satisfied: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@WebKitBrowser"}`<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@Cobalt"}` | WebKitBrowser must be in resumed state and Cobalt must be in deactivated, suspended, or not-present state. |
| 3 | Set pre-requisites if not already met | If pre-requisites are not satisfied, deactivate Cobalt and launch WebKitBrowser using RDKShell: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.deactivate", "params": {"callsign": "Cobalt"}}`<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.RDKShell.1.launch", "params": {"callsign": "WebKitBrowser", "type": "", "uri": ""}}` | Cobalt should be deactivated and WebKitBrowser should be in resumed state after the setup. |
| 4 | Get current screen resolution | Retrieve the current screen resolution from RDKShell to enable revert after the test: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.RDKShell.1.getScreenResolution"}` | Current screen resolution should be successfully retrieved. |
| 5 | Set screen resolution to 720p | Set the screen resolution to 1280x720 (720p) using RDKShell: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.RDKShell.1.setScreenResolution", "params": {"w": 1280, "h": 720}}` | Screen resolution should be set to 1280x720 successfully. |
| 6 | Validate screen resolution is set to 720p | Confirm that the screen resolution was applied correctly: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.RDKShell.1.getScreenResolution"}` | Screen resolution returned should match the target resolution of 1280x720. |
| 7 | Get current URL from WebKitBrowser | Retrieve the current URL loaded in WebKitBrowser to enable URL revert at the end of the test: `{"jsonrpc": "2.0", "id": 1234567890, "method": "WebKitBrowser.1.url"}` | Current URL should be successfully retrieved from WebKitBrowser. |
| 8 | Set Strike tool URL in WebKitBrowser | Load the Strike benchmark tool URL into WebKitBrowser: `{"jsonrpc": "2.0", "id": 1234567890, "method": "WebKitBrowser.1.url", "params": "<strike_tool_url>"}` | Strike tool URL should be set successfully on WebKitBrowser. |
| 9 | Validate Strike tool URL is loaded | Retrieve the current URL from WebKitBrowser and verify it matches the Strike tool URL: `{"jsonrpc": "2.0", "id": 1234567890, "method": "WebKitBrowser.1.url"}` | URL retrieved must match the configured Strike tool URL, confirming successful page load. |
| 10 | Trigger Strike benchmark via key press | Send an Enter key press to WebKitBrowser to initiate the Strike benchmark test: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.RDKShell.1.generateKey", "params": {"keys": [{"keyCode": 13, "modifiers": [], "delay": 1.0, "callsign": "WebKitBrowser", "client": "WebKitBrowser"}]}}` | The key event should be delivered to WebKitBrowser and the Strike benchmark should begin execution. |
| 11 | Retrieve Strike benchmark score from device log | Wait 360 seconds for the Strike benchmark to complete, then retrieve the score by reading the log entry containing "Score" from the device via SSH: `cat /opt/logs/wpeframework.log \| grep -inr 'Score' \| tail -1`. Validate that the score timestamp is later than the benchmark start time. | A valid numeric Score value should be present in the wpeframework.log after the benchmark execution time, with a timestamp later than the test start time. |
| 12 | Validate Strike benchmark score against threshold | Compare the retrieved Strike score against `STRIKE_THRESHOLD_VALUE` from the device configuration file. | The Strike benchmark score should be greater than the configured `STRIKE_THRESHOLD_VALUE`. |
| 13 | Revert WebKitBrowser URL to original | Restore the WebKitBrowser URL to the value saved before the test began: `{"jsonrpc": "2.0", "id": 1234567890, "method": "WebKitBrowser.1.url", "params": "<original_url>"}` | WebKitBrowser URL should be successfully reverted to the original URL. |
| 14 | Revert screen resolution to original | Restore the screen resolution to the original value retrieved before the test: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.RDKShell.1.setScreenResolution", "params": {"w": <original_w>, "h": <original_h>}}` | Screen resolution should be successfully restored to its original value. |
| 15 | Revert plugin states | If plugin states were changed during pre-requisite setup, restore WebKitBrowser and Cobalt to their original states as appropriate. | Plugin states should be restored to their original configuration. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M97<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
