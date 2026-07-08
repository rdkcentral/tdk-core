## TestCase ID
RDKV_PERFORMANCE_49
## TestCase Name
RDKV_CERT_PVS_Apps_WiFi_ResourceUsage_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the CPU and memory resource usage of the device while launching the Lightning/Unified Player application over a WiFi network connection and verify that resource usage is within acceptable limits.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is operational | The WPEFramework process must be running on the device before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS setting | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot (if configured) and be ready for test execution. |
| 3 | Confirm the device is connected to WiFi | The DUT must be connected to a WiFi access point before executing this test. The device should not be connected via Ethernet (eth0). The `DEVICE_IP_ADDRESS_TYPE` key must be configured in the device configuration file. | The device should be connected to a WiFi network, and the primary interface should not be eth0. |
| 4 | Confirm LOGGING_METHOD configuration | The `LOGGING_METHOD` key in the device configuration file must be set to either `REST_API` or `WEB_INSPECT`. | The device configuration file should contain a valid `LOGGING_METHOD` value. |
| 5 | Confirm PACKAGEMANAGER_FILE_LOCATOR configuration | The `PACKAGEMANAGER_FILE_LOCATOR` key must be set in the device configuration file. | The `PACKAGEMANAGER_FILE_LOCATOR` configuration key should be set with a valid path. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Retrieve device configuration and logging method | Read the device configuration file to obtain the `LOGGING_METHOD` setting. | The device configuration file should be read successfully and the `LOGGING_METHOD` value should be retrieved. |
| 2 | Verify the active network interface is WiFi | Check the current primary network interface by activating org.rdk.NetworkManager (if needed) and querying it: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.NetworkManager"}}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.NetworkManager.1.GetPrimaryInterface"}` <br>If the returned interface is "eth0", the test must not proceed. | The primary network interface should not be "eth0". The device should be connected via WiFi. |
| 3 | Verify and configure required plugin states | Retrieve the current status of DeviceInfo and org.rdk.PersistentStore plugins: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.PersistentStore"}` <br>If any plugin is not activated, activate it: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.PersistentStore"}}` | Both DeviceInfo and org.rdk.PersistentStore plugins should report an activated status. |
| 4 | Build and store video test URL in PersistentStore | Construct the unified player test application URL with the DASH H264 video URL (`video_src_url_dash_h264`), close operation, and logging arguments. Store it in PersistentStore: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PersistentStore.setValue","params":{"namespace":"MVS","key":"lightningURL","value":"<test_app_url>"}}` | The video test URL should be stored successfully in PersistentStore under namespace MVS with key lightningURL. |
| 5 | Verify if the unified player application is installed | Query the package manager to check if the unified player application bundle is already installed: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The list of installed packages should be retrieved. If the app is already installed, the installation steps should be skipped. |
| 6 | Activate app management plugins and install the application | If the unified player app is not installed, activate org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager, then download and install: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<app_bundle_name>"}}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.install","params":{"packageId":"<app_name>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator_path>"}}` | The application bundle should be downloaded and installed successfully. |
| 7 | Launch the unified player application over WiFi | Launch the application via AppManager: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` <br>Verify the application is active: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps"}` | The application should be launched successfully and appear in the loaded apps list with APP_STATE_ACTIVE. |
| 8 | Monitor application log for launch confirmation over WiFi | Monitor the application log (via REST_API log file or WEB_INSPECT WebSocket console) for the "URL Info:" message indicating the Lightning application has loaded the URL from PersistentStore over the WiFi connection. | The "URL Info:" confirmation message should appear in the application log, confirming the application has launched over the WiFi network. |
| 9 | Validate resource usage after application launch over WiFi | After receiving the "URL Info:" confirmation, validate the CPU and memory usage using the resource validation step, which internally invokes `DeviceInfo.1.systeminfo`: <br>`{"jsonrpc":"2.0","id":1,"method":"DeviceInfo.1.systeminfo"}` | The CPU and memory usage should be within the expected threshold limits. The resource usage validation should return SUCCESS with no ERROR status. |
| 10 | Terminate the unified player application | Terminate the launched application: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | The application should be terminated successfully. |
| 11 | Revert plugin states to original configuration | If any plugins were modified during test setup, restore their original states: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.deactivate","params":{"callsign":"<plugin_name>"}}` | All plugin states should be restored to their original configuration as captured before the test began. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15 mins

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
