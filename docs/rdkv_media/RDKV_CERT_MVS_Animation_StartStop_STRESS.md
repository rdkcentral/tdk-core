## TestCase ID
RDKV_Media_Validation_02
## TestCase Name
RDKV_CERT_MVS_Animation_StartStop_STRESS
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Animation application through AppManager and perform animation start and stop operation repeatedly for given number of times

<a name="head.Precondition"></a>
## Preconditions
|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | Ensure that WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.animation_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.pause_interval_stress should be set to the pause interval value for stress tests (in sec onds). | Ensure that the required configuration value is set correctly. |
| 5 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.play_interval_stress should be set to the play interval value for stress tests (in secon ds). | Ensure that the required configuration value is set correctly. |
| 6 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.repeat_count_stress should be set to the repeat count for stress tests. | Ensure that the required configuration value is set correctly. |
| 7 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 8 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 9 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.animation-app", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Set playback operations and build the animation app test URL. | Configure the playback operations (stop, start, repeat) and build the test URL for the Animation app. The animation will stop, restart playback, and repeat this cycle for the configured number of times. | Ensure that the playback operations are configured and the test URL is built successfully. |
| 2 | Store the launch URL in PersistentStore. | Store the constructed URL in PersistentStore for AppManager launch. <br>Sample URL: `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/animations/build/index.html?operations=stop,start,repeat&autotest=true`| Ensure that the launch URL is stored in PersistentStore. |
| 3 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.animation-app"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 4 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.animation-app is present in the loaded apps list. |
| 5 | Execute operations and validate media events. | App performs the stop and start operation repeatedly and validates using events. | Ensure that expected media events are observed for the configured operations. |
| 6 | Monitor animation progress. | Monitor animation progress. | Ensure that the 'stop, start, repeat' event should be received and animation completes successfully. Ensure that the validation result and average CPU load value should be retrieved. |
| 7 | Run animation operations and validate outcomes. | Validates the 'stop, start, repeat' event (animation completes successfully) and retrieves the validation result with a verage CPU load value. Get the event validation result from the app and update the test script status. | Ensure that animation operations complete successfully without errors. |
| 8 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.animation-app"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |
<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: RPI-Client, Video_Accelerator

**Estimated duration**: 10

**Priority**: High

**Release Version**: M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>


























