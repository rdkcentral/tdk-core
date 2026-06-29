## TestCase ID
RDKV_PERFORMANCE_01
## TestCase Name
RDKV_CERT_PVS_Browser_Octane
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the browser performance score obtained from the Octane JavaScript benchmark test by installing and launching the Octane application bundle and confirming the main score and subcategory scores meet the configured threshold values.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify WPEFramework status | WPEFramework process must be up and running on the device before test execution begins. | WPEFramework process should be active and accessible on the device. |
| 2 | Configure pre-requisite reboot | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | Device should be in a clean state prior to performance test execution. |
| 3 | Configure Octane app bundle name and download URL | `octane_app_bundle_name` (default: `com.rdkcentral.octane+0.1.0.bolt`) and `app_download_url` must be configured in BrowserPerformanceVariables. | The Octane application bundle must be accessible from the configured download URL. |
| 4 | Configure threshold values in device config | `OCTANE_THRESHOLD_VALUE` and `OCTANE_SUBCATEGORY_THRESHOLD_VALUES` must be set in the device-specific configuration file with thresholds for the main score and subcategories (Crypto, EarleyBoyer, Splay, SplayLatency, pdf.js, CodeLoad). `PACKAGEMANAGER_FILE_LOCATOR` must also be configured with the correct path where downloaded packages are stored on the DUT. | All threshold values and file locator path should be available and non-empty for score validation. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot device as pre-requisite | If `PRE_REQ_REBOOT_PVS` is configured as Yes, reboot the device by issuing the harakiri command and wait 150 seconds for reboot to complete: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should reboot successfully and come back online within the wait period. |
| 2 | Check if Octane application is installed | Query the list of installed packages to determine if the Octane app (com.rdkcentral.octane) is already present on the device: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully. If com.rdkcentral.octane is already installed, the installation workflow is skipped. |
| 3 | Activate required AppManager plugins | If the Octane app is not installed, verify and activate the required plugin stack — org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}`<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}`<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}` | All three plugins should be in activated state before download and installation proceed. |
| 4 | Download Octane application bundle | Download the Octane application bundle from the configured URL: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/com.rdkcentral.octane+0.1.0.bolt"}}` | The Octane bundle should be downloaded successfully and a download ID should be returned. |
| 5 | Install Octane application bundle | Install the downloaded Octane bundle using PackageManagerRDKEMS with the file locator from device configuration: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.octane", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The Octane app bundle should be installed successfully. |
| 6 | Verify Octane application is installed | Confirm the Octane app appears in the installed packages list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | com.rdkcentral.octane should appear in the installed packages list. |
| 7 | Launch Octane application | Launch the Octane application using AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.octane", "intent": "", "launchArgs": ""}}` | The Octane application should launch successfully. |
| 8 | Verify Octane application is running | Confirm the launched app appears in the active loaded apps list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | com.rdkcentral.octane should be listed as an active loaded application. |
| 9 | Wait for Octane benchmark to complete | Wait 300 seconds (5 minutes) for the Octane JavaScript benchmark to execute to completion before retrieving results. | The Octane benchmark should complete execution within the wait period. |
| 10 | Retrieve Octane benchmark score | Connect to the WebKit webinspect page and extract the main Octane score along with subcategory scores for Crypto, EarleyBoyer, Splay, SplayLatency, pdf.js, and CodeLoad. | Main Octane score and all subcategory scores should be successfully retrieved and must not contain the value "Unable to get the browser score" or "Running Octane". |
| 11 | Validate Octane main score against threshold | Compare the retrieved main Octane score against `OCTANE_THRESHOLD_VALUE` from the device configuration file. | The main Octane score should be greater than the configured `OCTANE_THRESHOLD_VALUE`. |
| 12 | Validate Octane subcategory scores | Compare each subcategory score against its corresponding threshold from the comma-separated `OCTANE_SUBCATEGORY_THRESHOLD_VALUES` device configuration key for all subcategories: Crypto, EarleyBoyer, Splay, SplayLatency, pdf.js, and CodeLoad. | All subcategory scores should be greater than or equal to their respective configured threshold values. |
| 13 | Terminate Octane application | Terminate the Octane application after score validation: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminate", "params": {"appId": "com.rdkcentral.octane"}}` | The Octane application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M82<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
