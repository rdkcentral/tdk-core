## TestCase ID
RDKV_PERFORMANCE_60
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
To validate that the unified player application performs MP4 video play and pause operations without any crash while the WebInspect remote debugging port is open, verifying the WPEFramework log for crash indicators and confirming the application remains stable throughout the test duration.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Confirm required plugins are available | The DeviceInfo and org.rdk.PersistentStore plugins must be present and activatable on the device. | Both DeviceInfo and org.rdk.PersistentStore plugins should be available and capable of being activated. |
| 4 | Configure MP4 video URL in MediaValidationVariables | `video_src_url_mp4` must be set to a valid MP4 video stream URL in MediaValidationVariables. | The MP4 video URL should be configured and accessible from the device. |
| 5 | Configure LOGGING_METHOD in device config | `LOGGING_METHOD` must be configured in the device-specific config file as either `REST_API` or `WEB_INSPECT` to define how video playback events are logged. | The logging method should be correctly configured for test result monitoring. |
| 6 | Configure unified_player_app_download_url in MediaValidationVariables | `unified_player_app_download_url` must be set to the hosted bolt package URL for the lightning unified player application (e.g., `com.rdkcentral.lightning-unified-player+0.1.0.bolt`). | The app download URL should be configured and accessible. |
| 7 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific config file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure test parameters and build video player URL | Configure the test execution parameters including `execID`, `execDevId`, `resultId`, logging method (from `LOGGING_METHOD` device config), the MP4 video URL (`video_src_url_mp4`), test duration of 60 seconds, playback close operation, looptest option, and autotest flag. Build the complete video player test application URL with all arguments for the codec_mp4 player list from MediaValidationVariables. | All test URL arguments should be configured successfully and the complete video player URL should be built. |
| 2 | Verify and activate required plugins | Query the activation state of the DeviceInfo and org.rdk.PersistentStore plugins and activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PersistentStore"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | Both DeviceInfo and org.rdk.PersistentStore plugins should be in the activated state. |
| 3 | Set the video test URL in PersistentStore | Store the video player test application URL in the PersistentStore under the MVS namespace with the lightningURL key, so the unified player application reads and loads it upon launch. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.PersistentStore.setValue", "params": {"namespace": "MVS", "key": "lightningURL", "value": "<video_test_url>"}}` | The video test URL should be stored successfully in the PersistentStore. |
| 4 | Check if the unified player application is already installed | Query the installed packages list to determine whether the unified player application (com.rdkcentral.lightning-unified-player) is already present on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be returned successfully. |
| 5 | Download the application bundle | If the unified player application is not already installed, verify and activate the required AppManager plugins (org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager), then download the application bundle from the configured URL. This step is skipped if the application was found to be already installed. <br>Activate plugins: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<unified_player_app_download_url>"}}` | The application bundle should be downloaded successfully and a download ID should be returned. |
| 6 | Install the application bundle | Install the downloaded application bundle using the file locator path from `PACKAGEMANAGER_FILE_LOCATOR` device configuration. This step is skipped if the application was already installed. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully. |
| 7 | Verify application installation | Confirm that the unified player application appears in the installed packages list after installation. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The unified player application should appear in the installed packages list, confirming successful installation. |
| 8 | Launch the unified player application | Send a launch request for the installed application via the AppManager and wait 10 seconds to allow the application to reach a stable running state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.lightning-unified-player", "intent": "", "launchArgs": ""}}` | The application should launch successfully. |
| 9 | Verify the application is launched and running | Verify that the application instance is present and active in the loaded apps list on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | The unified player application should be listed among the loaded apps in APP_STATE_ACTIVE, confirming it is running. |
| 10 | Retrieve SSH access parameters | Retrieve the SSH connection parameters (method and credentials) required to execute commands on the device under test via the rdkservice_getSSHParams step. | SSH parameters should be retrieved successfully to allow remote command execution on the DUT. |
| 11 | Retrieve the WebInspect port from device log | Connect to the DUT via SSH and read the dacapp.log file to extract the WebInspect inspector port number assigned to the running application. <br>`cat /opt/logs/dacapp.log \| grep 'inspector port set to'` | The WebInspect inspector port number should be extracted successfully from the log. |
| 12 | Open the WebInspect URL in Chrome browser | Construct the WebInspect URL using the retrieved port and open it in a headless Chrome browser session to establish a WebSocket console connection for monitoring. URL format: `http://<deviceIP>:<webinspect_port>/Main.html?ws=<deviceIP>:<webinspect_port>/socket/1/1/WebPage`. Wait 20 seconds for the page to fully load. | The WebInspect page should load successfully in the Chrome browser and the WebSocket console connection to the application should be established. |
| 13 | Check for crash indicators in the WPEFramework log | Connect to the DUT via SSH and search the WPEFramework log for crash-related entries during the video playback session. <br>`cat /opt/logs/wpeframework.log \| grep -inr crash` <br>If a crash keyword is found in the output, additionally query the loaded apps list to determine whether the application is still running after the crash: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | No crash-related log entries should be found in the WPEFramework log. If the crash keyword is detected but the application is still listed as a loaded app (APP_STATE_ACTIVE), the crash is considered non-impactful and the test may still pass. If the application is no longer present in the loaded apps list, the crash is critical and the test should be marked as failure. |
| 14 | Monitor video play and pause events during playback | Monitor the playback event log via REST API (reading from the app log file) or via the WebInspect console socket, depending on the configured `LOGGING_METHOD`. Track expected and observed play and pause events until a TEST RESULT message is received or a timeout is reached. Tracked log entries include: `Expected Event: paused`, `Observed Event: paused`, `Expected Event: play`, `Observed Event: play`, and `TEST RESULT:`. | All expected play and pause events should be observed and the video player application should report a TEST RESULT. |
| 15 | Validate successful playback without crash | Confirm that the video playback completed successfully with no crash confirmed as critical. The test passes only if the TEST RESULT from the video player application is SUCCESS and no crash was validated as impactful (crash_Validation remains False). | The video player should report TEST RESULT: SUCCESS, confirming that the MP4 video play and pause operations completed without any impactful crash while the WebInspect port was open throughout the test. |
| 16 | Terminate the unified player application | Terminate the running application using the AppManager terminateApp API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.lightning-unified-player"}}` | The application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 2 mins

**Priority** : High

**Release Version** : M132<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
