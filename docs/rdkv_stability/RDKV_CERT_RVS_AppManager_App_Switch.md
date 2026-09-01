## TestCase ID
RDKV_STABILITY_19
## TestCase Name
RDKV_CERT_RVS_AppManager_App_Switch

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the RDKWindowManager application switching functionality by installing and launching two application instances simultaneously, retrieving their initial Z-order values, and repeatedly swapping the Z-order between applications while verifying that each Z-order update is correctly reflected and the Z-order values of both applications remain distinct after each switch operation.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Verify device CPU and memory usage are within limits | The device CPU and memory usage must be within the acceptable range before the test begins. | CPU and memory usage should be within the expected acceptable range on the device. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle filename. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable and valid hosting location. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific configuration file. |
| 7 | Confirm required plugins are available | The following plugins must be available and activatable on the device: org.rdk.DownloadManager, org.rdk.AppPackageManager, and org.rdk.AppManager. | All required plugins should be present and activatable on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration key. If set to Yes, the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should come back online successfully if reboot was configured. |
| 2 | Verify and activate required plugins | Retrieve the current activation state of org.rdk.DownloadManager, org.rdk.AppPackageManager, and org.rdk.AppManager. Activate any plugin that is not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All three required plugins should be in the activated state before test execution proceeds. |
| 3 | Reboot device to establish a clean state | Reboot the device using the Thunder Controller harakiri method to establish a clean application state before installing and launching test applications. The script waits `rebootwaitTime` (150 seconds) for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should reboot and come back online successfully within the configured wait time. |
| 4 | Install and launch Test App 1 | Check if com.rdkcentral.testapp1 is already installed. If not, download and install the application bundle, then launch com.rdkcentral.testapp1 using the AppManager launchApp API. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.1.listPackages"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.install", "params": {"packageId": "com.rdkcentral.testapp1", "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/<download_id>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.testapp1"}}` | Test App 1 (com.rdkcentral.testapp1) should be installed and launched successfully. |
| 5 | Install and launch Test App 2 | Check if com.rdkcentral.testapp2 is already installed. If not, download and install the application bundle, then launch com.rdkcentral.testapp2 using the AppManager launchApp API. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.testapp2"}}` | Test App 2 (com.rdkcentral.testapp2) should be installed and launched successfully. |
| 6 | Retrieve loaded app instance IDs | Retrieve the list of loaded applications and extract the appInstanceId for both com.rdkcentral.testapp1 and com.rdkcentral.testapp2 where lifecycleState is APP_STATE_ACTIVE. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.getLoadedApps"}` | Both application instance IDs should be retrieved successfully from the loaded apps list. |
| 7 | Retrieve initial Z-order for both applications | Retrieve the initial Z-order values for both Test App 1 and Test App 2 using the RDKWindowManager getZOrder API with their respective appInstanceIds. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.RDKWindowManager.getZOrder", "params": {"clientId": "<app_instance_id_1>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.RDKWindowManager.getZOrder", "params": {"clientId": "<app_instance_id_2>"}}` | The initial Z-order values for both applications should be retrieved successfully and should be distinct. |
| 8 | Set Z-order of Test App 1 to swapped value (Per Iteration) | For each of the 3 switching iterations, set the Z-order of Test App 1 to the Z-order value previously held by Test App 2, effectively swapping their display order. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.RDKWindowManager.setZOrder", "params": {"clientId": "<app_instance_id_1>", "zOrder": <swapped_z_order_value>}}` | The setZOrder API should return SUCCESS for Test App 1 for each iteration. |
| 9 | Verify Z-order of Test App 1 after switch (Per Iteration) | Retrieve the updated Z-order of Test App 1 to verify the new value was applied correctly. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.RDKWindowManager.getZOrder", "params": {"clientId": "<app_instance_id_1>"}}` | The Z-order of Test App 1 should reflect the newly assigned value. |
| 10 | Set Z-order of Test App 2 to swapped value (Per Iteration) | Set the Z-order of Test App 2 to the Z-order value previously held by Test App 1 to complete the Z-order swap. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.RDKWindowManager.setZOrder", "params": {"clientId": "<app_instance_id_2>", "zOrder": <swapped_z_order_value>}}` | The setZOrder API should return SUCCESS for Test App 2 for each iteration. |
| 11 | Verify Z-order of both apps are distinct after full switch (Per Iteration) | Retrieve the Z-order of both Test App 1 and Test App 2 and verify that their Z-order values are different from each other after the full swap. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.RDKWindowManager.getZOrder", "params": {"clientId": "<app_instance_id_1>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.RDKWindowManager.getZOrder", "params": {"clientId": "<app_instance_id_2>"}}` | The Z-order values of both Test App 1 and Test App 2 should be distinct after each full switch, confirming successful Z-order swapping. |
| 12 | Repeat app switch validation for all iterations | Repeat Steps 8 through 11 for all `AppManager_test_count` (100) configured iterations. | Every switching iteration should successfully complete the Z-order swap between both applications with distinct final Z-order values, confirming correct application switching behaviour. |
| 13 | Terminate both applications after test | After completing all switching iterations, terminate both com.rdkcentral.testapp1 and com.rdkcentral.testapp2 using the AppManager terminateApp API to clean up the device state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.testapp1"}}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.testapp2"}}` | Both applications should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 250 minutes

**Priority** : High

**Release Version** : M151<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
