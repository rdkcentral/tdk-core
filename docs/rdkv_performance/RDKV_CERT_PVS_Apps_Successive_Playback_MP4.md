## TestCase ID
RDKV_PERFORMANCE_136
## TestCase Name
RDKV_CERT_PVS_Apps_Successive_Playback_MP4
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate successive playback of MP4 video streams through the HTML video application, including application installation and launch, playback result reporting, resource usage validation, and application termination.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-test reboot behavior | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot before test execution. | The device should follow the configured reboot behavior before the test starts. |
| 2 | Check WPEFramework availability | Confirm that the TDK performance module can connect to the device and that WPEFramework returns a successful module-load status. | The performance module should load successfully and the device connection should be available. |
| 3 | Configure media test logging | Set the device configuration key `LOGGING_METHOD` to `REST_API`. | The test should use REST API application logging for successive-playback validation. |
| 4 | Configure the package file locator | Set `PACKAGEMANAGER_FILE_LOCATOR` in the device configuration to the filesystem location used by AppPackageManager for downloaded bundles. | The package file locator should be present and usable for application installation. |
| 5 | Configure the MP4 media resources | Configure the HTML video test application URL, the MP4 source URL, the HTML player application bundle URL, and the successive-playback iteration count referenced by the performance and media validation configuration. | All required MP4 media URLs and the playback iteration count should be available to the test. |
| 6 | Confirm required plugins are activated | Verify the status of `DeviceInfo` and `org.rdk.PersistentStore` using `Controller.1.status@DeviceInfo` and `Controller.1.status@org.rdk.PersistentStore`. | Both plugins should report the `activated` state. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Load the performance module | Establish the TDK connection to the device and read the module-load result. | The module-load result should be `SUCCESS`. |
| 2 | Read the device logging configuration | Read the device configuration key `LOGGING_METHOD` and apply the selected device configuration file. | The logging method should be read successfully and the configuration should be applied. |
| 3 | Build the MP4 playback URLs | Set the execution ID, execution device ID, result ID, logging mode, test-manager URL, MP4 video source URL, automatic-test flag, and close operation in the HTML video test URL arguments. Generate one complete test URL for each configured successive-playback iteration. | The test should produce a complete MP4 URL list containing one URL per configured playback iteration. |
| 4 | Check required plugin states | Query the required plugin states using `{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@DeviceInfo"}` and `{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@org.rdk.PersistentStore"}`. | Both plugin-status requests should succeed and return the required plugin states. |
| 5 | Activate required plugins | If either required plugin is not activated, activate it using `{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}` and `{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"org.rdk.PersistentStore"}}`, then query both statuses again. | The required plugins should report `activated` after the status is rechecked. |
| 6 | Store the MP4 playback URLs | Set the generated URL list in PersistentStore under namespace `MVS` and key `lightningURL` using the JSON-RPC request `{"jsonrpc":"2.0","id":1,"method":"org.rdk.PersistentStore.setValue","params":{"namespace":"MVS","key":"lightningURL","value":"<generated MP4 successive-playback URL list>"}}`. | PersistentStore should accept the MP4 URL value successfully. |
| 7 | Check application installation state | Query installed packages using `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppPackageManager.1.listPackages"}` and determine whether the HTML player application package is already installed. | The package list should be returned successfully and the installation state should be identified. |
| 8 | Activate application-management plugins | When installation is required, verify and activate `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` using the corresponding `Controller.1.status@<callsign>` and `Controller.1.activate` requests. | All application-management plugins should report `activated`. |
| 9 | Download the player application bundle | Download the configured player bundle using `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<application bundle download URL>"}}`. | The application bundle should download successfully. |
| 10 | Install the player application | Install the downloaded bundle using `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppPackageManager.install","params":{"packageId":"<application name>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<configured package file locator plus downloaded file details>"}}`. | The application should install successfully. |
| 11 | Verify the installed application package | Query `org.rdk.AppPackageManager.1.listPackages` again and check that the player application is listed as installed. | The player application should appear in the installed package list. |
| 12 | Launch the player application | Launch the installed application using `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<application name>","intent":"","launchArgs":""}}`. | The launch request should succeed. |
| 13 | Verify the active application state | Read loaded applications using `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.getLoadedApps"}` and confirm that the player application has an active lifecycle state. | The player application should be present in the loaded-applications response with an active state. |
| 14 | Validate successive MP4 playback | Monitor the REST API application log until the final test result is reported. Count `Video Player Playing` events, collect each `STREAM <number> PLAYBACK RESULT : SUCCESS` or `FAILURE` entry, and validate that every expected stream reports success and the final result contains `TEST RESULT: SUCCESS`. | All expected MP4 streams should start playback, complete successfully, and produce a successful final test result. |
| 15 | Validate post-playback resource usage | Execute the resource-usage validation test after successful playback and evaluate the returned CPU-load and memory-usage values. | CPU load and memory usage should be returned and should remain within the configured expected limits. |
| 16 | Terminate the player application | Terminate the application using `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<application name>"}}`. | The application should terminate successfully. |
| 17 | Restore modified plugin states | If plugin states were changed for this test, restore the original `DeviceInfo` and `org.rdk.PersistentStore` states using the corresponding `Controller.1.activate` or `Controller.1.deactivate` requests. | The original plugin states should be restored before test completion. |
| 18 | Unload the performance module | Unload the performance module and write the execution summary, including `MP4` codec, expected streams, observed play events, successful streams, failed streams, CPU load, and memory usage. | The module should unload cleanly and the execution summary should be recorded. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 15 min

**Priority** : High

**Release Version** : M154<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
