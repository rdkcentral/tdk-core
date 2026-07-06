## TestCase ID
RDKV_PERFORMANCE_53
## TestCase Name
RDKV_CERT_PVS_Browser_Kraken
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the browser performance score obtained from the Kraken JavaScript benchmark test by installing and launching the Kraken application bundle and confirming the score is within the expected low-score (better performance) threshold value.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify WPEFramework status | WPEFramework process must be up and running on the device before test execution begins. | WPEFramework process should be active and accessible on the device. |
| 2 | Configure pre-requisite reboot | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | Device should be in a clean state prior to performance test execution. |
| 3 | Configure Kraken app bundle name and download URL | `kraken_app_bundle_name` (default: `com.rdkcentral.kraken+0.1.0.bolt`) and `app_download_url` must be configured in BrowserPerformanceVariables. | The Kraken application bundle must be accessible from the configured download URL. |
| 4 | Configure threshold value in device config | `KRAKEN_THRESHOLD_VALUE` must be configured in the device-specific configuration file. Note that for the Kraken benchmark a lower score indicates better performance, so the score must be less than the threshold. `PACKAGEMANAGER_FILE_LOCATOR` must also be set with the correct path where downloaded packages are stored on the DUT. | Threshold value and file locator path should be available and non-empty for installation and score validation. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot device as pre-requisite | If `PRE_REQ_REBOOT_PVS` is configured as Yes, reboot the device by issuing the harakiri command and wait 150 seconds for reboot to complete: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should reboot successfully and come back online within the wait period. |
| 2 | Check if Kraken application is installed | Query the list of installed packages to determine if the Kraken app (com.rdkcentral.kraken) is already present: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully. If com.rdkcentral.kraken is already installed, the installation workflow is skipped. |
| 3 | Activate required AppManager plugins | If the Kraken app is not installed, verify and activate the required plugin stack — org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}` | All three plugins should be in activated state before download and installation proceed. |
| 4 | Download Kraken application bundle | Download the Kraken application bundle from the configured URL: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/com.rdkcentral.kraken+0.1.0.bolt"}}` | The Kraken bundle should be downloaded successfully and a download ID should be returned. |
| 5 | Install Kraken application bundle | Install the downloaded Kraken bundle using PackageManagerRDKEMS with the file locator from device configuration: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.kraken", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The Kraken app bundle should be installed successfully. |
| 6 | Verify Kraken application is installed | Confirm the Kraken app appears in the installed packages list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | com.rdkcentral.kraken should appear in the installed packages list. |
| 7 | Launch Kraken application | Launch the Kraken application using AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.kraken", "intent": "", "launchArgs": ""}}` | The Kraken application should launch successfully. |
| 8 | Verify Kraken application is running | Confirm the launched app appears in the active loaded apps list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | com.rdkcentral.kraken should be listed as an active loaded application. |
| 9 | Wait for Kraken benchmark to complete | Wait 900 seconds (15 minutes) for the Kraken JavaScript benchmark to complete all its test iterations before retrieving results. | The Kraken benchmark should complete execution within the wait period. |
| 10 | Retrieve Kraken benchmark score | Connect to the WebKit webinspect page and extract the main Kraken score from the benchmark test results. | The Kraken score should be successfully retrieved and must not contain the value "Unable to get the browser score". |
| 11 | Validate Kraken score against threshold | Compare the retrieved Kraken score against `KRAKEN_THRESHOLD_VALUE` from the device configuration file. For the Kraken benchmark, a lower score indicates better JavaScript performance, so the score must be less than the threshold and greater than zero. | The Kraken benchmark score should be greater than 0 and less than the configured `KRAKEN_THRESHOLD_VALUE`. |
| 12 | Terminate Kraken application | Terminate the Kraken application after score validation: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminate", "params": {"appId": "com.rdkcentral.kraken"}}` | The Kraken application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 20 mins

**Priority** : High

**Release Version** : M102<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
