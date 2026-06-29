## TestCase ID
RDKV_PERFORMANCE_224
## TestCase Name
RDKV_CERT_PVS_WebKitBrowser_Video_Playback_Without_Crash_WithWebinspect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the WebKitBrowser application can perform MP4 video play and pause operations without any crash while the WebInspect remote debugging port is open throughout the test duration.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Confirm WebKitBrowser plugin is available | The WebKitBrowser plugin must be present and activatable. All other plugins should be disabled as a prerequisite. | The WebKitBrowser plugin should be available and enabled exclusively. |
| 4 | Configure video URL in MediaValidationVariables | `video_src_url_mp4` must be set to a valid MP4 video URL in MediaValidationVariables. | The video URL should be configured and accessible. |
| 5 | Configure LOGGING_METHOD in device config | `LOGGING_METHOD` must be configured in the device config file. | The logging method should be configured correctly. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure test parameters and build video player URL | Set up the test execution parameters including `execID`, `execDevId`, `resultId`, logging method, video URL, test duration (1800 seconds), and playback operations. Build the complete video player test app URL with all arguments including the MP4 video source URL, looptest option, and autotest flag. | All test URL arguments should be configured successfully and the complete video player URL should be built. |
| 2 | Verify and activate the WebKitBrowser plugin | Query the WebKitBrowser plugin status and activate it if not already active, with all other plugins deactivated. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@WebKitBrowser"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "WebKitBrowser"}}` | The WebKitBrowser plugin should be in the activated state. |
| 3 | Open WebKitBrowser WebInspect port | Open the WebInspect remote debugging port on the WebKitBrowser instance to enable console log monitoring during video playback. | The WebInspect port should be opened successfully and the WebSocket console connection should be established. |
| 4 | Load the video player URL in WebKitBrowser | Set the video player application URL in the WebKitBrowser. The URL includes the MP4 video source, loop test options, and autotest flag. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "WebKitBrowser.1.url", "params": {"url": "<video_player_test_url>"}}` | The video player URL should be loaded successfully in the WebKitBrowser. |
| 5 | Monitor for crash indicators during video playback | Once the video starts playing (VIDEO STARTED PLAYING console event), monitor the WebInspect console socket throughout the test duration for any crash-related log events or connection refused errors. Wait for the TEST RESULT event from the application. | No crashes or connection refused errors should be observed during the MP4 video play and pause operations. The WebKitBrowser process should remain stable throughout the test duration. |
| 6 | Validate successful playback completion without crash | Monitor the WebInspect console for a TEST RESULT: SUCCESS log entry indicating the video playback completed without a crash. If TEST RESULT: FAILURE or a crash-related event is observed, report failure. | The video player should report TEST RESULT: SUCCESS, confirming MP4 video playback with play and pause operations completed successfully without any crash while the WebInspect port was open. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 100 mins

**Priority** : High

**Release Version** : M132<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
