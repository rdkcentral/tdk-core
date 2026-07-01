## TestCase ID
RDKV_Media_Validation_795
## TestCase Name
RDKV_CERT_MVS_Video_HTML_Mute_Unmute_AAC_H265_MP4
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test script to launch an HTML video player application via AppManager and perform mute and unmute operations on MP4 content with h265 and AAC codecs for a few minutes and then close the player.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | WPE Framework Running | Wpeframework process should be up and running in the device. | Ensure that Wpeframework process is active and running on the device. |
| 2 | Html Player BOLT App Available | HTML Player BOLT app package must be available for download via AppManager.<br>MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages<br>hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/).<br>MediaValidationVariables.html_player_app_download_url is derived from this base path and must<br>resolve to the BOLT app package (e.g.<br>http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.html-player+0.1.0.bolt). | Ensure that BOLT app package is available and accessible for download via AppManager. |
| 3 | AppManager App Installation Check | AppManager should check if the BOLT app is already installed using :<br>List packages: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}`<br>If it is not already installed then download and install the BOLT package.<br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/html-player-app"}}`<br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.html-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | BOLT app is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Mute audio (30s), unmute audio (30s).<br>Build the test URL with the video_src_url_aac_h265.<br>Store the constructed URL in PersistentStore for AppManager launch. | Ensure that playback operations are configured correctly: Mute audio (30s), unmute audio (30s).<br>Ensure the test URL is built with video_src_url_aac_h265. Ensure the URL is stored in<br>PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via RDKShell | Launch the WebKit instance with the HTML player test app using the video src URL, and perform<br>mute and unmute operations. | Ensure that Step executed successfully. |
| 3 | Perform Play Content and Validate Media Events | App performs the provided operations and validates each operation using media events ('Observed<br>Event: play') | Ensure that the app performs all configured operations and validates them using media events.<br>Operations should complete successfully without errors. |
| 4 | Update Test Result Based on Event Validation | If expected event ('Observed Event: play') is observed for each operation, app gives the<br>validation result as SUCCESS or else FAILURE. Update the test script result as SUCCESS/FAILURE<br>based on event validation result and proc check status (if applicable) | Ensure that the test result is updated as SUCCESS/FAILURE based on event validation result. |
| 5 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId:com.rdkcentral.html-player)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.html-player"}}'` | Ensure the test environment is restored successfully. Ensure that the app<br>(com.rdkcentral.html-player) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M143<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>