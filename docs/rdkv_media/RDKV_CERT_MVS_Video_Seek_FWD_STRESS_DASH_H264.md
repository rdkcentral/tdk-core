## TestCase ID
RDKV_Media_Validation_120
## TestCase Name
RDKV_CERT_MVS_Video_Seek_FWD_STRESS_DASH_H264
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Video player application through AppManager and perform video seek forward operation of DASH H264 video codec content repeatedly for given number of times in provided interval

<a name="head.Precondition"></a>
## Preconditions
|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | Ensure that WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.unified_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.seekfwd_interval should be set to the seek-forward interval value (in seconds). | Ensure that the required configuration value is set correctly. |
| 5 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.seekfwd_check_interval should be set to the seek-forward check interval (in seconds). | Ensure that the required configuration value is set correctly. |
| 6 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.operation_max_interval should be set to the maximum operation interval value (in seconds). | Ensure that the required configuration value is set correctly. |
| 7 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.repeat_count_stress should be set to the repeat count for stress tests. | Ensure that the required configuration value is set correctly. |
| 8 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 9 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 10 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Set playback operations for the scenario. | Set playback operations: Seek forward, repeat. | Ensure playback operations are set as specified. |
| 2 | Build the test URL using video_src_url_dash_h264. | Build the test URL with the video_src_url_dash_h264 (DASH stream). | Verify that the test URL is built using video_src_url_dash_h264. |
| 3 | Store the launch URL in PersistentStore. | Store the constructed URL in PersistentStore for AppManager launch. | Ensure that the launch URL is stored in PersistentStore. |
| 4 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 5 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps by sending the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.lightning-unified-player is present in the loaded apps list. |
| 6 | Execute operations and validate media events. | App performs the provided operations and validates each operation using media events ('Video Player seeked'). | Ensure that expected media events are observed for the configured operations. |
| 7 | Validate observed events and set pass/fail status. | If expected event seeking and seeked occurs for each seekfwd operation, then the app reports SUCCESS; otherwise, it reports FAILURE. | Ensure that pass/fail status matches observed event validation. |
| 8 | Update test result based on validation. | Update the test script result as SUCCESS/FAILURE based on event validation result from the app and proc check status (if applicable). | Ensure that the final test result is updated based on validation and proc-check status. |
| 9 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |
<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: RPI-Client, Video_Accelerator

**Estimated duration**: 10

**Priority**: High

**Release Version**: M90<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
















