## TestCase ID
RDKV_Media_Validation_03
## TestCase Name
RDKV_CERT_MVS_Animation_PlayPause_STRESS
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Animation application via AppManager and perform animation play and pause operation repeatedly for given number of times

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
|1| WPE Framework Running | Wpeframework process should be up and running in the device.| Wpeframework process is active and running on the device.|
|2| Animation BOLT App Available | Lightning Animation BOLT app package must be available for download via AppManager. MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/). MediaValidationVariables.animation_app_download_url is derived from this base path and must resolve to the BOLT app package (e.g. http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.animation-app+0.1.0.bolt).| BOLT app package is available and accessible for download via AppManager.|
|3| Pause Interval Stress Configured | MediaValidationVariables.pause_interval_stress should be set to the pause interval value for stress tests (in seconds).| MediaValidationVariables.pause_interval_stress is configured with the required value.|
|4| Play Interval Stress Configured | MediaValidationVariables.play_interval_stress should be set to the play interval value for stress tests (in seconds).| MediaValidationVariables.play_interval_stress is configured with the required value.|
|5| Repeat Count Stress Configured | MediaValidationVariables.repeat_count_stress should be set to the repeat count for stress tests.| MediaValidationVariables.repeat_count_stress is configured with the required value.|
|6| AppManager App Installation Check | AppManager should check if the BOLT app is already installed using `org.rdk.PackageManagerRDKEMS.1.listPackages`. If already present, proceed without download/install. If not present, download the BOLT app package via `org.rdk.DownloadManager.1.download` (params: `{"url":"<app_download_url>"}`) and install it via `org.rdk.PackageManagerRDKEMS.install` (params: `{"packageId":"<app_id>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator>"}`).| BOLT app is installed successfully on the device.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Pause, play, repeat. Build the test URL for the Animation app. Store the constructed URL in PersistentStore for AppManager launch. Sample URL:<br>`http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/animations/build/index.html?operations=pause,play,repeat&autotest=true` | Verify that playback operations are configured correctly: Pause, play, repeat. Confirm the URL is stored in PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.animation-app"}}'` | Ensure the app (com.rdkcentral.animation-app) is launched successfully and should be listed in the loaded apps. |
| 3 | Perform Pause / Play Content and Validate Media Events | App performs the pause and play operation repeatedly and validates using events | Verify that the pause and play operation repeatedly and validates using events completes successfully without errors. |
| 4 | Validate Event Result and Update Test Status | Monitor animation progress. Validates the 'pause, play, repeat' event (animation completes successfully) and retrieves the validation result with average CPU load value. Get the event validation result from the app and update the test script status | Confirm the 'pause, play, repeat' event is received and animation completes successfully. Verify that the validation result and average CPU load value are retrieved. |
| 5 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId: com.rdkcentral.animation-app)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.animation-app"}}'` | Ensure the test environment is restored successfully. Verify that the app (com.rdkcentral.animation-app) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>