## TestCase ID
RDKV_STABILITY_34
## TestCase Name
RDKV_CERT_RVS_AppManager_Install_Uninstall_AppStates
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that application installation state, loaded state, the AppManager uninstall event, and query results remain consistent before and after terminating and uninstalling the application.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the device connection | Configure the target device IP address and port so that the stability test framework can connect to the device. | The test framework should connect to the target device successfully. |
| 2 | Configure the reboot policy | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot policy should be applied according to the configured value. |
| 3 | Check WPEFramework and device status | Load the `rdkv_stability` module and verify that the device is available before starting the test. | The framework module and device status should report success. |
| 4 | Activate the required application services | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` are activated. | All required application services should be in the activated state. |
| 5 | Configure the application package | Configure the Google application bundle and a valid application download base URL. The application identifier must be `com.rdkcentral.google`. | The application package should be available for installation and its application identifier should be configured correctly. |
| 6 | Configure the stability iteration count | Configure the application manager stability test count used for repeated state-consistency validation. | A valid positive iteration count should be available for the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate the required application services | Query the device application service states and activate any service that is not already active: `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager`. | The required application services should be activated successfully. |
| 2 | Subscribe to the uninstall event | Register for the AppManager uninstall event using: `{"jsonrpc": "2.0","id": 1,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppUninstalled", "id": "client.events.1" }}`. | The `onAppUninstalled` event subscription should be registered successfully. |
| 3 | Install the application under test | Download and install the configured Google application bundle for `com.rdkcentral.google` without launching it. | The application should be installed successfully and should be available for state validation. |
| 4 | Capture the initial installed-applications snapshot | Query installed applications using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getInstalledApps","params":{}}`. | The query should return success and the initial snapshot should contain `com.rdkcentral.google`. |
| 5 | Check the initial installation state | Query the application installation state using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.isInstalled","params":{"appId":"com.rdkcentral.google"}}`. | The query should return success and indicate that `com.rdkcentral.google` is installed. |
| 6 | Capture the initial loaded-applications snapshot | Query loaded applications using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps","params":{}}`. | The query should return success and the application should not be loaded before launch. |
| 7 | Launch the application | Submit a launch request for `com.rdkcentral.google`. | The launch request should return success. |
| 8 | Terminate the application | Terminate the launched application using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.terminateApp","params":{"appId":"com.rdkcentral.google"}}`. | The termination request should return success. |
| 9 | Uninstall the terminated application | Submit an uninstall request for `com.rdkcentral.google`. | The uninstall request should return success. |
| 10 | Validate the uninstall event | Read the event buffer for up to 120 seconds until an event containing `onAppUninstalled` and `com.rdkcentral.google` is received. | The `onAppUninstalled` event should be received for the expected application. |
| 11 | Capture the final installed-applications snapshot | Query installed applications again using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getInstalledApps","params":{}}`. | The query should return success and the final snapshot should not contain `com.rdkcentral.google`. |
| 12 | Check the final installation state | Query the final installation state using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.isInstalled","params":{"appId":"com.rdkcentral.google"}}`. | The query should return success and indicate that `com.rdkcentral.google` is not installed. |
| 13 | Capture the final loaded-applications snapshot | Query loaded applications again using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps","params":{}}`. | The query should return success and the final snapshot should not contain `com.rdkcentral.google`. |
| 14 | Verify cross-surface state consistency | Compare the initial and final installed-applications snapshots, `isInstalled` results, loaded-applications snapshots, and the uninstall event. The initial state must be installed, reported as installed, and not loaded; the final state must be absent from all query surfaces and accompanied by the matching uninstall event. | All query surfaces and the event stream should agree on the application state before and after uninstall. |
| 15 | Reinstall the application for the next iteration | Reinstall the configured application bundle without launching it before beginning the next iteration. | The application should be installed successfully and ready for the next consistency check. |
| 16 | Repeat the state-consistency validation | Repeat the initial snapshots, launch, termination, uninstall, event validation, final snapshots, consistency comparison, and reinstall actions for the configured application manager test count. | Every configured iteration should maintain consistent installed, loaded, and event states across the uninstall transition. |
| 17 | Disconnect the event listener and test module | Disconnect the uninstall event listener and unload the `rdkv_stability` test module after all iterations complete. | The event listener and test module should be disconnected and unloaded cleanly. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 300 seconds

**Priority** : High

**Release Version** : M153<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
