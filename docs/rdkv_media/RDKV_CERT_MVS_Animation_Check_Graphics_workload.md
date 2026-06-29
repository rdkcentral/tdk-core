## TestCase ID
RDKV_Media_Validation_11
## TestCase Name
RDKV_CERT_MVS_Animation_Check_Graphics_workload
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to perform animation of multiple objects for multiple object counts one by one for the provided duration using lightning application and check how many objects can be rendered by the device with expected FPS value.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
|1| WPE Framework Running | Wpeframework process should be up and running in the device.| Wpeframework process is active and running on the device.|
|2| Multi Animation BOLT App Available | Lightning Multi Animation BOLT app package must be available for download via AppManager. MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/). MediaValidationVariables.multi_animation_app_download_url is derived from this base path and must resolve to the BOLT app package (e.g. http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.multi-animation-app+0.1.0.bolt).| BOLT app package is available and accessible for download via AppManager.|
|3| Animation Duration Configured | MediaValidationVariables.animation_duration should be set to the desired animation duration (in seconds).| MediaValidationVariables.animation_duration is configured with the required value.|
|4| AppManager App Installation Check | AppManager should check if the BOLT app is already installed using `org.rdk.PackageManagerRDKEMS.1.listPackages`. If already present, proceed without download/install. If not present, download the BOLT app package via `org.rdk.DownloadManager.1.download` (params: `{"url":"<app_download_url>"}`) and install it via `org.rdk.PackageManagerRDKEMS.install` (params: `{"packageId":"<app_id>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator>"}`).| BOLT app is installed successfully on the device.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Build the test URL for the Multianimation app. Store the constructed URL in PersistentStore for AppManager launch. Sample URL:<br>`http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/multianimations/build/index.html?autotest=true` | Confirm the URL is stored in PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.multi-animation-app"}}'` | Ensure the app (com.rdkcentral.multi-animation-app) is launched successfully and should be listed in the loaded apps. |
| 3 | Perform Run Animation and Validate Media Events | App performs animation of multiple objects for multiple object counts one by one for the provided duration. | Verify that animation of multiple objects for multiple object counts one by one for the provided duration completes successfully without errors. |
| 4 | Perform Run Animation and Validate Media Events | App starts with animation of single object for provided duration and collect the fps for every second, then find the average of collected fps. | Verify that with animation of single object for provided duration and collect the fps for every second, then find the average of collected fps completes successfully without errors. |
| 5 | Execute Test Step | If the average FPS obtained is greater than or equal to expected fps value, then app increases number of objects to | Step executed successfully. |
| 6 | Execute Test Step | Again average fps is calculated and checked, then app decides to proceed for further more number of objects or not. | Step executed successfully. |
| 7 | Execute Test Step | Average fps for single object animation should be as expected. If this condition is satisfied test result is set as SUCCESS or else FAILURE. | Average fps for single object animation should be as expected. |
| 8 | Execute Test Step | Test script finally gives the number of objects the device can animate with expected FPS | Step executed successfully. |
| 9 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId: com.rdkcentral.multi-animation-app)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.multi-animation-app"}}'` | Ensure the test environment is restored successfully. Verify that the app (com.rdkcentral.multi-animation-app) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>