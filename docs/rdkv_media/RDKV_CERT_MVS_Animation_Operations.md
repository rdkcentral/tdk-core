## TestCase ID
RDKV_Media_Validation_01
## TestCase Name
RDKV_CERT_MVS_Animation_Operations
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Animation application via AppManager and perform some operations to change the animation state

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | WPE Framework Running | Wpeframework process should be up and running in the device. | Ensure that Wpeframework process is active and running on the device. |
| 2 | Animation BOLT App Available | Lightning Animation BOLT app package must be available for download via AppManager.<br>MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages<br>hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/).<br>MediaValidationVariables.animation_app_download_url is derived from this base path and must<br>resolve to the BOLT app package (e.g.<br>http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.animation-app+0.1.0.bolt). | Ensure that BOLT app package is available and accessible for download via AppManager. |
| 3 | Operation Max Interval Configured | MediaValidationVariables.operation_max_interval should be set to the maximum operation interval<br>value (in seconds). | Ensure that MediaValidationVariables.operation_max_interval is configured with the required<br>value. |
| 4 | AppManager App Installation Check | AppManager should check if the BOLT app is already installed using :<br>List packages: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}`<br>If it is not already installed then download and install the BOLT package.<br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/animation-app"}}`<br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.animation-app", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | BOLT app is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Pause, play, stop, replay from beginning, stop immediately, start<br>playback, stop.<br>Build the test URL for the Animation app.<br>Store the constructed URL in PersistentStore for AppManager launch.<br>Sample URL:<br>`http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/animations/build/index.html`<br>`?operations=pause,play,stop,replay,stopNow,start,stop&autotest=true` | Ensure that playback operations are configured correctly: Pause, play, stop, replay from<br>beginning, stop immediately, start playback, stop. Ensure the URL is stored in PersistentStore<br>(MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.animation-app"}}'` | Ensure the app (com.rdkcentral.animation-app) is launched successfully and should be listed in<br>the loaded apps. |
| 3 | Perform Configured Operations and Validate Events | App performs the provided operations and validates each operation using events | Ensure that the provided operations and validates each operation using events completes<br>successfully without errors. |
| 4 | Validate Event Result and Update Test Status | Monitor animation progress. Validates the 'pause, play, stop, replay, stopNow, start, stop'<br>event (animation completes successfully) and retrieves the validation result with average CPU<br>load value. Get the event validation result from the app and update the test script status | Ensure that the 'pause, play, stop, replay, stopNow, start, stop' event is received and<br>animation completes successfully. Ensure that the validation result and average CPU load value<br>are retrieved. |
| 5 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId:com.rdkcentral.animation-app)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.animation-app"}}'` | Ensure the test environment is restored successfully. Ensure that the app<br>(com.rdkcentral.animation-app) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>