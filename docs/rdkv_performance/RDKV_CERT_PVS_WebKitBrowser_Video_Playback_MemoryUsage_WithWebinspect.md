## TestCase ID
RDKV_PERFORMANCE_59
## TestCase Name
RDKV_CERT_PVS_WebKitBrowser_Video_Playback_MemoryUsage_WithWebinspect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the memory usage of the WebKitBrowser application remains within the configured threshold during MP4 video play and pause operations while keeping the WebInspect port open.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Confirm WebKitBrowser plugin is available | The WebKitBrowser plugin must be present and activatable. All other plugins should be disabled as a prerequisite. | The WebKitBrowser plugin should be available and enabled exclusively. |
| 4 | Configure video URL in MediaValidationVariables | `video_src_url_mp4` must be set to a valid MP4 video URL in MediaValidationVariables. | The video URL should be configured and accessible. |
| 5 | Configure LOGGING_METHOD in device config | `LOGGING_METHOD` must be configured in the device config file to define how test results are logged. | The logging method should be configured correctly. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure test parameters and build video player URL | Set up the test execution parameters including `execID`, `execDevId`, `resultId`, logging method, video URL, test duration (1800 seconds), and playback operations (close after duration). Build the complete video player test app URL with all arguments including the MP4 video source URL, looptest option, and autotest flag. | All test URL arguments should be configured successfully and the complete video player URL should be built. |
| 2 | Verify and activate the WebKitBrowser plugin | Query the WebKitBrowser plugin status and activate it if not already active, ensuring all other plugins are deactivated. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@WebKitBrowser"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "WebKitBrowser"}}` | The WebKitBrowser plugin should be in the activated state. |
| 3 | Open WebKitBrowser WebInspect port | Open the WebInspect remote debugging port on the WebKitBrowser instance to enable WebSocket-based console log monitoring during video playback. | The WebInspect port should be opened successfully and the WebSocket connection for console log monitoring should be established. |
| 4 | Load the video player URL in WebKitBrowser | Set the video player application URL in the WebKitBrowser. The URL includes the MP4 video source, loop test options, and autotest flag so playback starts automatically. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "WebKitBrowser.1.url", "params": {"url": "<video_player_test_url>"}}` | The video player URL should be loaded successfully in the WebKitBrowser. |
| 5 | Monitor memory usage during video playback | Once the video starts playing (indicated by a VIDEO STARTED PLAYING console log event), periodically capture the WebKitBrowser process memory usage via the WebInspect console socket. Collect memory usage samples during play and pause operations throughout the 1800-second test duration. | Memory usage samples should be collected successfully during video playback. The memory usage should remain within the configured threshold throughout the test duration. |
| 6 | Validate test completion without crash | Monitor the WebInspect console for a TEST RESULT: SUCCESS log entry indicating the video playback completed without a crash. | The video player should report TEST RESULT: SUCCESS, confirming MP4 video playback completed without any crash while the WebInspect port was open. Memory usage should be within the threshold throughout. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 360 mins

**Priority** : High

**Release Version** : M132<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
