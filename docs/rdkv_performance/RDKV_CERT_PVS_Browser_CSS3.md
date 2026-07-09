## TestCase ID
RDKV_PERFORMANCE_52
## TestCase Name
RDKV_CERT_PVS_Browser_CSS3
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the browser performance score obtained from the CSS3 benchmark test by installing and launching the CSS3 application bundle and confirming the main score and subcategory scores meet the configured threshold values.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify WPEFramework status | WPEFramework process must be up and running on the device before test execution begins. | WPEFramework process should be active and accessible on the device. |
| 2 | Configure pre-requisite reboot | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | Device should be in a clean state prior to performance test execution. |
| 3 | Configure CSS3 app bundle name and download URL | `css3_app_bundle_name` (default: `com.rdkcentral.css3+0.1.0.bolt`) and `app_download_url` must be configured in BrowserPerformanceVariables with valid values pointing to the hosted application bundle. | CSS3 application bundle must be accessible from the configured download URL. |
| 4 | Configure threshold values in device config | `CSS3_THRESHOLD_VALUE` and `CSS3_SUBCATEGORY_THRESHOLD_VALUES` must be set in the device-specific configuration file. `PACKAGEMANAGER_FILE_LOCATOR` must also be configured with the correct path where downloaded packages are stored on the DUT. | All threshold values and the file locator path should be available and non-empty for installation and score validation. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot device as pre-requisite | If `PRE_REQ_REBOOT_PVS` is configured as Yes, reboot the device by issuing the harakiri command and wait 150 seconds for the reboot to complete: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should reboot successfully and come back online within the wait period. |
| 2 | Check if CSS3 application is installed | Query the list of installed packages to determine if the CSS3 app (com.rdkcentral.css3) is already present on the device: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully. If com.rdkcentral.css3 is already installed, the installation workflow is skipped. |
| 3 | Activate required AppManager plugins | If the CSS3 app is not installed, verify and activate the required plugin stack — org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}` | All three plugins should be in activated state before the download and installation proceed. |
| 4 | Download CSS3 application bundle | Download the CSS3 application bundle from the configured URL using the DownloadManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/com.rdkcentral.css3+0.1.0.bolt"}}` | The CSS3 application bundle should be downloaded successfully and a download ID should be returned. |
| 5 | Install CSS3 application bundle | Install the downloaded CSS3 bundle using PackageManagerRDKEMS with the file locator path from device configuration: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.css3", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The CSS3 app bundle should be installed successfully. |
| 6 | Verify CSS3 application is installed | Confirm the CSS3 app appears in the installed packages list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | com.rdkcentral.css3 should appear in the installed packages list. |
| 7 | Launch CSS3 application | Launch the CSS3 application using AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.css3", "intent": "", "launchArgs": ""}}` | The CSS3 application should launch successfully. |
| 8 | Verify CSS3 application is running | Confirm the launched app appears in the active loaded apps list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | com.rdkcentral.css3 should be listed as an active loaded application. |
| 9 | Retrieve CSS3 benchmark score | Wait 20 seconds for the CSS3 benchmark to execute, then connect to the WebKit webinspect page and extract the main CSS3 score and all subcategory scores across the CSS3 test categories. | Main CSS3 score and all subcategory scores should be successfully retrieved from the webinspect page and must not contain the value "Unable to get the browser score". |
| 10 | Validate CSS3 main score against threshold | Compare the retrieved main CSS3 score against `CSS3_THRESHOLD_VALUE` from the device configuration file. | The main CSS3 score should be greater than the configured `CSS3_THRESHOLD_VALUE`. |
| 11 | Validate CSS3 subcategory scores | Compare each subcategory score against its corresponding threshold from the comma-separated `CSS3_SUBCATEGORY_THRESHOLD_VALUES` device configuration key, iterating over all CSS3 subcategories. | All subcategory scores should be greater than or equal to their respective configured threshold values. |
| 12 | Terminate CSS3 application | Terminate the CSS3 application after score validation: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.css3"}}` | The CSS3 application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M82<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
