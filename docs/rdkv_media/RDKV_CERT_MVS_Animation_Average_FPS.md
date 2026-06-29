## TestCase ID
RDKV_Media_Validation_04
## TestCase Name
RDKV_CERT_MVS_Animation_Average_FPS
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Animation application via AppManager and check whether the average FPS calculated for 60 sec duration value is as expected

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
|1| WPE Framework Running | Wpeframework process should be up and running in the device.| Wpeframework process is active and running on the device.|
|2| Animation BOLT App Available | Lightning Animation BOLT app package must be available for download via AppManager. MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/). MediaValidationVariables.animation_app_download_url is derived from this base path and must resolve to the BOLT app package (e.g. http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.animation-app+0.1.0.bolt).| BOLT app package is available and accessible for download via AppManager.|
|3| AppManager App Installation Check | AppManager should check if the BOLT app is already installed using `org.rdk.PackageManagerRDKEMS.1.listPackages`. If already present, proceed without download/install. If not present, download the BOLT app package via `org.rdk.DownloadManager.1.download` (params: `{"url":"<app_download_url>"}`) and install it via `org.rdk.PackageManagerRDKEMS.install` (params: `{"packageId":"<app_id>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator>"}`).| BOLT app is installed successfully on the device.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Stop (60s). Build the test URL for the Animation app. Store the constructed URL in PersistentStore for AppManager launch. Sample URL:<br>`http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/animations/build/index.html?operations=stop(60)&autotest=true` | Verify that playback operations are configured correctly: Stop (60s). Confirm the URL is stored in PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.animation-app"}}'` | Ensure the app (com.rdkcentral.animation-app) is launched successfully and should be listed in the loaded apps. |
| 3 | Perform Run Animation and Validate Media Events | App performs animation for 60 sec and stops after that. | Verify that animation completes successfully without errors. |
| 4 | Validate Event Result and Update Test Status | Monitor animation progress. Validates the 'stop' event (animation completes successfully) and retrieves the validation result with average CPU load value. It also gives average FPS value | Confirm the 'stop' event is received and animation completes successfully. Verify that the validation result and average CPU load value are retrieved. |
| 5 | Monitor and Validate Media Events | Get the event validation result and average FPS value from the app and check whether FPS obtained is greater than or equal to expected fps value. | Verify that fps obtained is greater than or equal to expected fps value as expected. |
| 6 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId: com.rdkcentral.animation-app)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.animation-app"}}'` | Ensure the test environment is restored successfully. Verify that the app (com.rdkcentral.animation-app) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 3

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>