## TestCase ID
RDKV_Media_Validation_362
## TestCase Name
RDKV_CERT_MVS_Video_Seek_Pos_4K_HLS
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Video player application through AppManager and perform video seek to position operation of 4K HLS video content

<a name="head.Precondition"></a>
## Preconditions
|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | Ensure that WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.unified_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.seekpos_check_interval should be set to the seek-position check interval (in seconds). | Ensure that the required configuration value is set correctly. |
| 5 | Verify that the required configuration is set correctly. | MediaValidationVariables.seekfwd_position should be set to the seek-forward target position (in seconds). | Ensure that MediaValidationVariables.seekfwd_position should be configured with the required value. |
| 6 | Verify that the required configuration is set correctly. | MediaValidationVariables.seekbwd_position should be set to the seek-backward target position (in seconds). | Ensure that MediaValidationVariables.seekbwd_position should be configured with the required value. |
| 7 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 8 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 9 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Run playback operations and validate media events. | Start playback of the content and close the player after 30s (close_interval). | Ensure that expected media events are observed for the configured operations. |
| 2 | Store the launch URL in PersistentStore. | Build the test URL with the video_src_url_4k_hls (HLS stream). Store the constructed URL in PersistentStore for AppManager launch. Sample URL (hlsjs player):<br><code>http://&lt;TM_IP&gt;:&lt;port&gt;/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html<br>?player=sdk<br>&url=http://&lt;TM_IP&gt;:&lt;port&gt;/TDK_Clear_Test_Streams_Sunrise/HLS_HEVC_AAC/master.m3u8<br>&operations=close(30)<br>&autotest=true<br>&type=HLS</code>. | Ensure that the launch URL is stored in PersistentStore. |
| 3 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 4 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps by sending the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.lightning-unified-player is present in the loaded apps list. |
| 5 | Execute operations and validate media events. | App performs seek to position operations and validates using seeking, seeked events and with position. | Ensure that expected media events are observed for the configured operations. |
| 6 | Execute operations and validate media events. | If expected event ('Observed Event: ') is observed for each operation, the app reports SUCCESS; otherwise, it reports FAILURE. Update the test script result as SUCCESS/FAILURE based on event validation result from the app and proc check status (if applicable). | Ensure that expected media events are observed for the configured operations. |
| 7 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |
<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: Video_Accelerator

**Estimated duration**: 5

**Priority**: High

**Release Version**: M122<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
