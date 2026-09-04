## TestCase ID
RDKV_STABILITY_22
## TestCase Name
RDKV_CERT_RVS_AppManager_Metadata_Lifecycle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the AppPackageManager reports consistent and accurate package metadata (version, digest, and size in KB) upon each application installation, and to confirm that the metadata remains identical across repeated install and uninstall cycles, with the onAppInstallationStatus event correctly emitted for each installation and uninstallation.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Verify device CPU and memory usage are within limits | The device CPU and memory usage must be within the acceptable range before the test begins. The DeviceInfo plugin is activated if needed to retrieve resource usage metrics. | CPU and memory usage should be within the expected acceptable range on the device. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle filename. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. The full download URL is constructed as `app_download_url + "/" + google_bundle`. | The app_download_url should point to a reachable and valid hosting location. |
| 6 | Configure AppManager_test_count in StabilityTestVariables | `AppManager_test_count` must be set to the desired number of install/uninstall metadata verification iterations in StabilityTestVariables (default: 100). | The AppManager_test_count variable should be configured with a valid integer value. |
| 7 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific configuration file. |
| 8 | Confirm required plugins are available | The following plugins must be available and activatable on the device: org.rdk.DownloadManager, org.rdk.AppPackageManager, and org.rdk.AppManager. | All required plugins should be present and activatable on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration key. If set to Yes, the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should come back online successfully if reboot was configured. |
| 2 | Validate device resource usage state | Check the activation state of the DeviceInfo plugin and activate it if needed, then validate that the device CPU and memory usage are within the acceptable range before proceeding. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}` | Device CPU and memory usage should be within the expected range, confirming the device is in a healthy state before testing. |
| 3 | Verify and activate required plugins | Retrieve the current activation state of org.rdk.DownloadManager, org.rdk.AppPackageManager, and org.rdk.AppManager. Activate any plugin that is not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All three required plugins should be in the activated state before test execution proceeds. |
| 4 | Subscribe to onAppInstallationStatus event | Register a WebSocket event listener to subscribe to the onAppInstallationStatus event from org.rdk.AppPackageManager. Wait 3 seconds after registration. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.1.register", "params": {"event": "onAppInstallationStatus", "id": "client.events.1"}}` | The onAppInstallationStatus event subscription should be established successfully and the WebSocket event listener should be active. |
| 5 | Clear event buffer (Per Iteration) | For each of the `AppManager_test_count` (100) iterations, clear the event listener buffer to discard any stale events before the install operations for that iteration. | The event buffer should be cleared successfully at the start of each iteration. |
| 6 | Check if application is pre-installed and uninstall if present (Per Iteration) | Query the installed package list to check whether com.rdkcentral.google is already installed. If present, uninstall it and wait for the onAppInstallationStatus event with status UNINSTALLED before proceeding with the download. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.1.listPackages"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.uninstall", "params": {"packageId": "com.rdkcentral.google"}}` | If pre-installed, the application should be uninstalled successfully and the onAppInstallationStatus event with UNINSTALLED status should be received before proceeding. |
| 7 | Download application bundle (Per Iteration) | Initiate the download of the application bundle from the configured download URL using the DownloadManager download API. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The application bundle download should complete successfully and return a valid download ID. |
| 8 | Install application on the device (Per Iteration) | Retrieve the `PACKAGEMANAGER_FILE_LOCATOR` device configuration key to construct the installation file path, then install the downloaded application bundle using the AppPackageManager install API. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.install", "params": {"packageId": "com.rdkcentral.google", "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/<download_id>"}}` | The install API should return SUCCESS and initiate the installation of the application for each iteration. |
| 9 | Verify onAppInstallationStatus INSTALLED event received (Per Iteration) | Monitor the event buffer for up to 120 seconds to verify that an onAppInstallationStatus event with INSTALLED status is received for com.rdkcentral.google. <br>`{"jsonrpc": "2.0", "method": "client.events.1.onAppInstallationStatus", "params": {"appId": "com.rdkcentral.google", "status": "INSTALLED"}}` | The onAppInstallationStatus event with INSTALLED status should be received for com.rdkcentral.google within the monitoring period. |
| 10 | Retrieve installed package list and extract metadata (Per Iteration) | Query the AppPackageManager package list to retrieve the entry for com.rdkcentral.google and extract the package metadata fields: version, digest, and sizeKb. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.1.listPackages"}` | The package list should be retrieved successfully and the com.rdkcentral.google entry should contain non-empty version, digest, and sizeKb fields. |
| 11 | Capture or verify metadata consistency (Per Iteration) | On the first iteration, capture the retrieved metadata (version, digest, sizeKb) as the baseline expected metadata. On all subsequent iterations, compare the retrieved metadata fields against the captured baseline values to verify consistency. | For the first iteration, the baseline metadata should be captured successfully. For all subsequent iterations, the retrieved version, digest, and sizeKb values should exactly match the baseline, confirming metadata consistency across installs. |
| 12 | Uninstall application from the device (Per Iteration) | Uninstall com.rdkcentral.google from the device using the AppPackageManager uninstall API. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.uninstall", "params": {"packageId": "com.rdkcentral.google"}}` | The uninstall API should return SUCCESS and the application should be removed for each iteration. |
| 13 | Verify application is removed from package list (Per Iteration) | Query the installed package list to confirm that com.rdkcentral.google no longer appears as an installed package after uninstallation. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.1.listPackages"}` | The com.rdkcentral.google package should not be present in the installed packages list after uninstallation. |
| 14 | Repeat metadata verification for all iterations | Repeat Steps 5 through 13 for all `AppManager_test_count` (100) configured iterations. | Every iteration should successfully install the application, receive the onAppInstallationStatus event, retrieve metadata with consistent version, digest, and sizeKb values matching the baseline, and confirm successful removal from the package list after uninstallation. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 170 minutes

**Priority** : High

**Release Version** : M151<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
