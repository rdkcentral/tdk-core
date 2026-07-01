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
|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | Ensure that WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.multi_animation_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required configuration is set correctly. | MediaValidationVariables.animation_duration should be set to the desired animation duration (in seconds). | Ensure that MediaValidationVariables.animation_duration should be configured with the required value. |
| 5 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 6 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 7 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.multi-animation-app", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Store the launch URL in PersistentStore. | Build the test URL for the Multianimation app. Store the constructed URL in PersistentStore for AppManager launch. Sample URL:<br><code>http://&lt;TM_IP&gt;:&lt;port&gt;/tdkservice/fileStore/lightning-apps/multianimations/build/index.html?autotest=true</code>. | Ensure that the launch URL is stored in PersistentStore. |
| 2 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.multi-animation-app"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 3 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps by sending the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.multi-animation-app is present in the loaded apps list. |
| 4 | Run animation operations and validate outcomes. | App performs animation of multiple objects for multiple object counts one by one for the provided duration. | Ensure that animation of multiple objects for multiple object counts one by one for the provided duration completes successfully without errors. |
| 5 | Verify that app starts with animation of single object for provided duration and collect the fps. | App starts with animation of single object for provided duration and collect the fps for every second, then find the average of collected fps. | Ensure that with animation of single object for provided duration and collect the fps for every second, then find the average of collected fps completes successfully without errors. |
| 6 | Verify that if the average FPS obtained is greater than or equal to expected fps value, then app. | If the average FPS obtained is greater than or equal to expected fps value, then app increases number of objects to. | Ensure that if the average FPS obtained should be greater than or equal to expected fps value, then app increases number of objects to. |
| 7 | Verify that again average fps is calculated and checked, then app decides to proceed for further. | Again average fps is calculated and checked, then app decides to proceed for further more number of objects or not. | Ensure that again average fps should be calculated and checked, then app decides to proceed for further more number of objects or not. |
| 8 | Verify that average fps for single object animation should be as expected. | Average fps for single object animation should be as expected. If this condition is satisfied test result is set as SUCCESS or else FAILURE. | Ensure that average fps for single object animation should be as expected. |
| 9 | Verify that test script finally gives the number of objects the device can animate with expected FPS. | Test script finally gives the number of objects the device can animate with expected FPS. | Ensure that test script finally gives the number of objects the device can animate with expected FPS should be va lidate d. |
| 10 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.multi-animation-app"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |
<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: RPI-Client, Video_Accelerator

**Estimated duration**: 15

**Priority**: High

**Release Version**: M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>

















