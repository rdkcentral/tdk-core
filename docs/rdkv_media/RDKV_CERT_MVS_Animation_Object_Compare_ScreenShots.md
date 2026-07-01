## TestCase ID
RDKV_Media_Validation_42
## TestCase Name
RDKV_CERT_MVS_Animation_Object_Compare_ScreenShots
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Objects Animation application through AppManager to render a rectangle and validate animation operation using screen shot comparison

<a name="head.Precondition"></a>
## Preconditions
|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | Ensure that WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.object_animation_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required configuration is set correctly. | MediaValidationVariables.image_upload_dir should be set to the directory path for image uploads. | Ensure that MediaValidationVariables.image_upload_dir should be configured with the required value. |
| 5 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 6 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 7 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.object-animation-app", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Store the launch URL in PersistentStore. | Build the test URL for the Objects Animation app. Store the constructed URL in PersistentStore for AppManager launch. Sample URL:<br><code>http://&lt;TM_IP&gt;:&lt;port&gt;/tdkservice/fileStore/lightning-apps/objectanimations/build/index.html?autotest=true</code>. | Ensure that the launch URL is stored in PersistentStore. |
| 2 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.object-animation-app"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 3 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps by sending the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.object-animation-app is present in the loaded apps list. |
| 4 | Run animation operations and validate outcomes. | App performs animation to render single rectangle object for provided duration. | Ensure that animation to render single rectangle object for provided duration completes successfully without errors. |
| 5 | Verify that using screenshot plugin, capture screenshots at regular interval and upload to the. | Using screenshot plugin, capture screenshots at regular interval and upload to the configured url. | Ensure that the URL should be stored in PersistentStore (MVS/lightningURL) successfully. |
| 6 | Verify that compare the captured screenshots among them and check whether they are same or different. | compare the captured screenshots among them and check whether they are same or different. | Ensure that they should be same or different as expected. |
| 7 | Verify that if the screenshots are different, then its because of animation which moves the object. | If the screenshots are different, then its because of animation which moves the object. | Ensure that the screenshots should be different. Ensure that the test result should be updated as SUCCESS. |
| 8 | Verify that if the screenshots matches, then object is not animated properly. | If the screenshots matches, then object is not animated properly. update the test result as SUCCESS, if screenshots are different or else FAILURE if screenshots matches. | Ensure that the screenshots should be different. Ensure that the test result should be updated as SUCCESS. |
| 9 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.object-animation-app"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |
<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: Video_Accelerator

**Estimated duration**: 5

**Priority**: High

**Release Version**: M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>

















