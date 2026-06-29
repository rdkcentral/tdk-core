## TestCase ID
RDKV_CERT_RVS_6
## TestCase Name
RDKV_CERT_RVS_LongDuration_VideoPlayback_4K_HLS

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability and resource usage during long-duration 4K HLS video playback using the configured webkit or LightningApp browser instance for a minimum of 10 hours, confirming that CPU and memory usage remain within acceptable limits throughout the playback session.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure video_src_url_4k_hls in MediaValidationVariables | `video_src_url_4k_hls` must be set to a valid 4K HLS video stream URL of at least 10 hours duration in MediaValidationVariables. | The video URL variable should point to a reachable 4K HLS stream. |
| 4 | Configure webkit_instance in StabilityTestVariables | `webkit_instance` must be set to the browser plugin instance to use for playback (e.g., WebKitBrowser or LightningApp) in StabilityTestVariables. | The webkit_instance variable should be configured with a valid browser plugin name. |
| 5 | Configure webinspect_port or lightning_app_webinspect_port in StabilityTestVariables | The appropriate WebInspect port must be configured in StabilityTestVariables based on the selected webkit_instance. | The webinspect port variable should be set to the correct port for the selected browser instance. |
| 6 | Configure LOGGING_METHOD in device config | `LOGGING_METHOD` must be configured in the device-specific config file as either `REST_API` or `WEB_INSPECT`. | The LOGGING_METHOD key should be set to a valid value in the device config file. |
| 7 | Configure codec_hls_h264 player list in MediaValidationVariables | `codec_hls_h264` must contain the player instance name(s) to be used for playback (comma-separated). | The player list should contain at least one valid player name. |
| 8 | Confirm required browser plugin and DeviceInfo are available | The configured webkit browser plugin instance, Cobalt, and DeviceInfo plugins must be present in the build. They must be listed in `SUPPORTED_PLUGINS` in the device config. | All required plugins should be available in the build. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration key. If set to "Yes", the device is rebooted via the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully if reboot was configured. |
| 2 | Validate device resource usage before test | Check device state and resource usage before starting the long-duration test via DeviceInfo.1.systeminfo. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Verify and activate required plugins | Read `SUPPORTED_PLUGINS` from device config and check the activation state of Cobalt, DeviceInfo, and the configured webkit_instance. Set the required states: webkit_instance to resumed, Cobalt to deactivated, DeviceInfo to activated. Original states are saved for revert. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@Cobalt"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<webkit_instance>"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<webkit_instance>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.deactivate", "params": {"callsign": "Cobalt"}}` | webkit_instance should be in resumed state, Cobalt should be deactivated, and DeviceInfo should be activated. |
| 4 | Retrieve current URL from browser instance | Get the current URL loaded in the webkit browser instance before setting the test URL. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "<webkit_instance>.1.url"}` | Current URL should be retrieved successfully from the browser plugin. |
| 5 | Set 4K HLS video test URL in browser instance | Set the 4K HLS video test application URL (constructed from video_src_url_4k_hls and URL arguments) into the webkit browser instance. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "<webkit_instance>.1.url", "params": {"value": "<video_test_url>"}}` | The video test URL should be set successfully in the browser instance. |
| 6 | Validate URL is set in browser instance | Verify that the URL was successfully set by querying the browser plugin URL property. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "<webkit_instance>.1.url"}` | The retrieved URL should match the configured video test URL. |
| 7 | Monitor 4K HLS video playback and validate resource usage | Monitor the long-duration 4K HLS video playback session for the configured test duration (36000 seconds / 10 hours). Depending on the logging method (REST_API or WEB_INSPECT), resource usage is periodically measured and logged. CPU load and memory usage are recorded per measurement interval. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | 4K HLS video playback should continue without crash throughout the entire test duration. CPU and memory usage should remain within acceptable thresholds. |
| 8 | Revert browser URL to original value | After the long-duration playback completes or on failure, revert the browser URL back to the original value recorded in Step 4. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "<webkit_instance>.1.url", "params": {"value": "<original_url>"}}` | Browser URL should be successfully restored to the original value. |
| 9 | Revert plugin statuses | Revert all plugins back to their original states recorded before Step 3. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "Cobalt"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.deactivate", "params": {"callsign": "<webkit_instance>"}}` | Plugin states should be restored to their pre-test values. |
| 10 | Validate device resource usage after test | Check device state and resource usage after the long-duration test completes to confirm the device remains healthy. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range after the long-duration test completes. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 1000 mins

**Priority** : High

**Release Version** : M103<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
