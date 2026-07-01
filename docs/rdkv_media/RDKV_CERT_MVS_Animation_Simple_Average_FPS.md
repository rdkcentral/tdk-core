## TestCase ID
RDKV_Media_Validation_68
## TestCase Name
RDKV_CERT_MVS_Animation_Simple_Average_FPS
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Animation application via AppManager to render combination of Rectangles and Texts and check whether the average FPS calculated for 60 sec duration value is as expected

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | WPE Framework Running | Wpeframework process should be up and running in the device. | Ensure that Wpeframework process is active and running on the device. |
| 2 | Object Animation BOLT App Available | Lightning Animation BOLT app package must be available for download via AppManager.<br>MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages<br>hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/).<br>MediaValidationVariables.object_animation_app_download_url is derived from this base path and<br>must resolve to the BOLT app package (e.g.<br>http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.object-animation-app+0.1.0.bolt). | Ensure that BOLT app package is available and accessible for download via AppManager. |
| 3 | Objects Count Configured | MediaValidationVariables.objects_count should be set to the number of animation objects for the<br>test. | Ensure that MediaValidationVariables.objects_count is configured with the required value. |
| 4 | Animation Duration Configured | MediaValidationVariables.animation_duration should be set to the desired animation duration (in<br>seconds). | Ensure that MediaValidationVariables.animation_duration is configured with the required value. |
| 5 | AppManager App Installation Check | AppManager should check if the BOLT app is already installed using :<br>List packages: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}`<br>If it is not already installed then download and install the BOLT package.<br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/object-animation-app"}}`<br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.object-animation-app", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | BOLT app is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Build the test URL for the Objects Animation app.<br>Store the constructed URL in PersistentStore for AppManager launch.<br>Sample URL:<br>`http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/objectanimations/build/index.html`<br>`?autotest=true` | Ensure that the URL is stored in PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.object-animation-app"}}'` | Ensure the app (com.rdkcentral.object-animation-app) is launched successfully and should be<br>listed in the loaded apps. |
| 3 | Perform Run Animation and Validate Media Events | App performs animation to render Rectangles and Texts for 60 seconds. | Ensure that animation to render rectangles and texts completes successfully without errors. |
| 4 | Execute Test Step | App gives average FPS value after 60 seconds | Ensure that Step executed successfully. |
| 5 | Execute Test Step | Get the average FPS value from the app and check whether FPS obtained is greater than or equal<br>to expected fps value. | Ensure that fps obtained is greater than or equal to expected fps value as expected. |
| 6 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId:com.rdkcentral.object-animation-app)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.object-animation-app"}}'` | Ensure the test environment is restored successfully. Ensure that the app<br>(com.rdkcentral.object-animation-app) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 3

**Priority** : High

**Release Version** : M87<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>