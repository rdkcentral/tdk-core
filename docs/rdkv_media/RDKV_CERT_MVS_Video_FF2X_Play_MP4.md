## TestCase ID
RDKV_Media_Validation_354
## TestCase Name
RDKV_CERT_MVS_Video_FF2X_Play_MP4
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Video player application via AppManager and perform video fast forward operation in 2x speed for few seconds, continue video play of MP4 content and close the player

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | WPE Framework Running | Wpeframework process should be up and running in the device. | Ensure that Wpeframework process is active and running on the device. |
| 2 | Unified Player BOLT App Available | Lightning Player BOLT app package must be available for download via AppManager.<br>MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages<br>hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/).<br>MediaValidationVariables.unified_player_app_download_url is derived from this base path and<br>must resolve to the BOLT app package (e.g.<br>http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.lightning-unified-player+0.1.0.bolt<br>. | Ensure that BOLT app package is available and accessible for download via AppManager. |
| 3 | Fastfwd Check Interval Configured | MediaValidationVariables.fastfwd_check_interval should be set to the fast-forward check<br>interval (in seconds). | Ensure that MediaValidationVariables.fastfwd_check_interval is configured with the required<br>value. |
| 4 | AppManager App Installation Check | AppManager should check if the BOLT app is already installed using :<br>List packages: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}`<br>If it is not already installed then download and install the BOLT package.<br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/unified-player-app"}}`<br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | BOLT app is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Fast-forward at 2x speed (30s), resume playback (10s), close the<br>player (30s).<br>Build the test URL with the video_src_url_mp4 (MP4 stream).<br>Store the constructed URL in PersistentStore for AppManager launch.<br>Sample URL (sdk player):<br>`http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html`<br>`?player=sdk&url=http://<TM_IP>:<port>/TDK_Clear_Test_Streams_Sunrise/TDK_Asset_Sunrise_MP4.MP4`<br>`&operations=fastfwd2x(30),playnow(10),close(30)&autotest=true&type=MP4` | Ensure that playback operations are configured correctly: Fast-forward at 2x speed (30s),<br>resume playback (10s), close the player (30s). Ensure the test URL is built with<br>video_src_url_mp4. Ensure the URL is stored in PersistentStore (MVS/lightningURL)<br>successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the app (com.rdkcentral.lightning-unified-player) is launched successfully and should be<br>listed in the loaded apps. |
| 3 | Perform Configured Operations and Validate Events | App performs the provided operations and validates each operation using media events ('Observed<br>Event: ratechange') | Ensure that the app performs all configured operations and validates them using media events.<br>Operations should complete successfully without errors. |
| 4 | Validate Event Result and Update Test Status | If expected event ratechange occurs for fastforward and playnow operation, then app gives the<br>validation result as SUCCESS or else FAILURE | Ensure that expected event ratechange occurs for fastforward and playnow operation. Ensure that<br>the test result is updated as SUCCESS. |
| 5 | Update Test Result Based on Event Validation | Update the test script result as SUCCESS/FAILURE based on event validation result from the app<br>and proc check status (if applicable) | Ensure that the test result is updated as SUCCESS/FAILURE based on event validation result. |
| 6 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId:com.rdkcentral.lightning-unified-player)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the test environment is restored successfully. Ensure that the app<br>(com.rdkcentral.lightning-unified-player) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M120<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>