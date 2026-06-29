## TestCase ID
RDKV_Media_Validation_147
## TestCase Name
RDKV_CERT_MVS_Video_Seek_FF_EC3
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Video player application via AppManager and perform video medium trick play operations like seek and FF of ec3 content

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
|1| WPE Framework Running | Wpeframework process should be up and running in the device.| Wpeframework process is active and running on the device.|
|2| Unified Player BOLT App Available | Lightning Player BOLT app package must be available for download via AppManager. MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/). MediaValidationVariables.unified_player_app_download_url is derived from this base path and must resolve to the BOLT app package (e.g. http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.lightning-unified-player+0.1.0.bolt).| BOLT app package is available and accessible for download via AppManager.|
|3| Fastfwd Check Interval Configured | MediaValidationVariables.fastfwd_check_interval should be set to the fast-forward check interval (in seconds).| MediaValidationVariables.fastfwd_check_interval is configured with the required value.|
|4| Ec3 URL Type Configured | MediaValidationVariables.ec3_url_type should be set to the EC3 stream type value.| MediaValidationVariables.ec3_url_type is configured with the required value.|
|5| AppManager App Installation Check | AppManager should check if the BOLT app is already installed using `org.rdk.PackageManagerRDKEMS.1.listPackages`. If already present, proceed without download/install. If not present, download the BOLT app package via `org.rdk.DownloadManager.1.download` (params: `{"url":"<app_download_url>"}`) and install it via `org.rdk.PackageManagerRDKEMS.install` (params: `{"packageId":"<app_id>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator>"}`).| BOLT app is installed successfully on the device.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch App as Pre-Requisite via RDKShell | As pre requisite, install and launch the test app via AppManager (setMediaTestPreRequisites), open websocket connection to webinspect page | Ensure the app is launched successfully and should be listed in the loaded apps. |
| 2 | Configure Playback Operations and Test URL | Set playback operations: Seek forward (30s), fast-forward (20s), resume playback (30s). Build the test URL with the video_src_url_ec3. Store the constructed URL in PersistentStore for AppManager launch. Sample URL (dashjs player):<br>`http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/unifiedplayer/build/index.html?player=sdk&url=http://<TM_IP>:<port>/TDK_Clear_Test_Streams_Sunrise/DASH_H264_EC3/atfms_291_dash_tdk_avc_eac3_fmp4.mpd&operations=seekfwd(30),fastfwd(20),playnow(30)&autotest=true` | Verify that playback operations are configured correctly: Seek forward (30s), fast-forward (20s), resume playback (30s). Confirm the test URL is built with video_src_url_ec3. Confirm the URL is stored in PersistentStore (MVS/lightningURL) successfully. |
| 3 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the app (com.rdkcentral.lightning-unified-player) is launched successfully and should be listed in the loaded apps. |
| 4 | Perform Seek and Validate Media Events | App performs the provided operations and validates each operation using media events ('Observed Event: ') and with position and rate value for seek and fast-forward operations | Verify that the app performs all configured operations and validates them using media events. Operations should complete successfully without errors. |
| 5 | Update Test Result Based on Event Validation | If expected event ('Observed Event: ') is observed for each operation, app gives the validation result as SUCCESS or else FAILURE. Update the test script result as SUCCESS/FAILURE based on event validation result from the app and proc check status (if applicable) | Check that the test result is updated as SUCCESS/FAILURE based on event validation result. |
| 6 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId: com.rdkcentral.lightning-unified-player)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the test environment is restored successfully. Verify that the app (com.rdkcentral.lightning-unified-player) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>