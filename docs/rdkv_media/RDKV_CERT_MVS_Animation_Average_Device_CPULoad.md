## TestCase ID
RDKV_Media_Validation_05
## TestCase Name
RDKV_CERT_MVS_Animation_Average_Device_CPULoad
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Animation application via AppManager and check whether the average device CPU load value calculated for 60 sec duration is as expected

<a name="head.Precondition"></a>
## Preconditions
|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | Check that the WPEFramework process is active and stable on the device before test execution. | Ensure that WPEFramework should be active and running before continuing. |
| 2 | Confirm that the Animation BOLT package server path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:/images/signed-packages/`) | Confirm that the package host path is configured and reachable. |
| 3 | Verify that the Animation app download URL resolves to the BOLT package. | Check that MediaValidationVariables.animation_app_download_url resolves to com.rdkcentral.animation-app+0.1.0.bolt from the configured host path. | Ensure that the Animation BOLT package should be accessible for AppManager download. |
| 4 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is already installed on the device. |
| 5 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/animation-app"}}</code>. | Ensure that the BOLT package is downloaded successfully. |
| 6 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.animation-app", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the BOLT app is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Configure the animation playback operation for the test scenario. | Configure the `stop(60)` operation: the animation app will run for 60 seconds and then stop automatically. | Ensure that the configured operation should be Stop (60s). |
| 3 | Store the launch URL in PersistentStore. | Set the MVS/lightningURL in PersistentStore with the generated URL before app launch. <br>Sample URL: `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/animations/build/index.html?operations=stop(60)&autotest=true`| Ensure that the launch URL is stored in PersistentStore. |
| 4 | Launch the app through AppManager. | Launch the app using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId":"com.rdkcentral.animation-app"}}</code>. Then register for required events. | Ensure that the app launches successfully via AppManager. |
| 5 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.animation-app is present in the loaded apps list. |
| 6 | Verify that the animation runs for 60 seconds and validate completion behavior. | Run the animation and confirm that playback stops automatically after 60 seconds. | Ensure that the animation should complete without runtime errors. |
| 7 | Monitor stop events and collect validation output with CPU metrics. | Monitor the stop event and retrieve the validation result along with the average CPU load value. | Confirm that the stop event is received and CPU metrics are captured. |
| 8 | Validate that the measured average CPU load stays below the threshold. | Compare the reported average CPU value against the threshold and check that it is less than 90. | Ensure that the average CPU load should be less than 90. |
| 9 | Terminate app and restore test environment. | Terminate the app using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId":"com.rdkcentral.animation-app"}}</code>. | Ensure that the app is terminated and the test environment is restored. |
| 10 | Verify that the test environment is restored to default. | Verify that the app unloaded event is received and confirm that the test environment is restored to default after app termination. | Ensure that the app unload is confirmed and the environment should return to default. |
<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: RPI-Client, Video_Accelerator

**Estimated duration**: 3

**Priority**: High

**Release Version**: M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
















