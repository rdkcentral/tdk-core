## TestCase ID
RDKV_PERFORMANCE_130
## TestCase Name
RDKV_CERT_PVS_Apps_Successive_Playback_DASH_H264
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate successive playback of a DASH H.264 video stream in the HTML DASH video application, where the same stream URL is queued once per iteration and played back-to-back, each playback ending with the configured close operation, for the number of iterations set in `Succesive_playback_iterations`. The test also validates that every stream plays successfully, that resource usage stays within limits after the last playback, and that the application terminates cleanly.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-test reboot behavior | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot before test execution. | The device should follow the configured reboot behavior before the test starts. |
| 2 | Check WPEFramework availability | Confirm that the TDK performance module can connect to the device and that WPEFramework returns a successful module-load status. | The performance module should load successfully and the device connection should be available. |
| 3 | Configure media test logging | Set the device configuration key `LOGGING_METHOD` to `REST_API`. | The test should use REST API application logging for successive-playback validation. |
| 4 | Configure the package file locator | Set `PACKAGEMANAGER_FILE_LOCATOR` in the device configuration to the filesystem location used by AppPackageManager for downloaded bundles. | The package file locator should be present and usable for application installation. |
| 5 | Configure the DASH H.264 media resources | Configure the HTML DASH test application URL, the DASH video source URL, the HTML player application bundle URL, and set `Succesive_playback_iterations` in the performance test variables to the number of times the stream must be played in succession. | All required DASH H.264 media URLs and the playback iteration count should be available to the test. |
| 6 | Confirm required plugins are activated | Verify the status of `DeviceInfo` and `org.rdk.PersistentStore` using `Controller.1.status@DeviceInfo` and `Controller.1.status@org.rdk.PersistentStore`. | Both plugins should report the `activated` state. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check the required plugin states | Query `DeviceInfo` and `org.rdk.PersistentStore` with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@DeviceInfo"}` and `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.PersistentStore"}`. | Each required plugin should return the `activated` state. |
| 2 | Activate unavailable required plugins | If either required plugin is not activated, request activation with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}`, then query its status again. | Each required plugin should report `activated` after the activation request. |
| 3 | Build the DASH H.264 successive-playback test URLs | Combine the configured DASH video source URL, execution identifiers, logging information, the close operation, and `autotest: "true"` into the HTML DASH player test URL. Generate one such URL per iteration, where the number of iterations is `Succesive_playback_iterations`; every URL carries the same stream, so the stream is played that many times in succession. | A list of DASH H.264 player test URLs should be generated whose length equals `Succesive_playback_iterations`, with each entry pointing to the same stream. |
| 4 | Store the player URLs in PersistentStore | Set the MVS `lightningURL` value with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.PersistentStore.setValue","params":{"namespace":"MVS","key":"lightningURL","value":"<generated DASH H.264 successive-playback URL list>"}}`. The player application reads this list and plays the URLs one after another. | The URL list should be stored successfully in PersistentStore. |
| 5 | Check whether the HTML player is installed | Request the installed package list with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.1.listPackages"}` and inspect the returned installed package IDs for the derived application ID. | The application should be identified as installed, or the flow should proceed to download and install it. |
| 6 | Check application-management plugin availability | Query `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` using `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@<plugin>"}`. Activate any unavailable plugin with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}`. | All application-management plugins should report the `activated` state before package installation. |
| 7 | Download the HTML player bundle | Request the configured application bundle with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<configured application download URL>/<bundle name>"}}`. | The application bundle should download successfully and return package details for installation. |
| 8 | Install the HTML player bundle | Install the downloaded package with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.install","params":{"packageId":"<application ID>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<configured locator><download result>"}}`. | The bundle should install successfully. |
| 9 | Verify the installed application | Query `org.rdk.AppPackageManager.1.listPackages` again and check that the derived application ID is present in the installed package list. | The application ID should appear in the installed package list. |
| 10 | Launch the HTML player | Launch the installed application with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<application ID>","intent":"","launchArgs":""}}`. | The launch request should return success. |
| 11 | Verify the application is active | Query loaded applications with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps"}` and locate the application ID with lifecycle state `APP_STATE_ACTIVE`. | The HTML player should appear as an active loaded application. |
| 12 | Validate the successive DASH H.264 playback | Monitor the REST API application log until the final test result is reported. Count the entries containing `Video Player Playing` (one per playback), collect each `STREAM <number> PLAYBACK RESULT : SUCCESS` or `FAILURE` entry, and check the final `TEST RESULT` entry. | The number of `Video Player Playing` entries should equal `Succesive_playback_iterations`, every `STREAM <number>` entry from 1 to that count should report `SUCCESS`, and the final result should be `TEST RESULT: SUCCESS`. |
| 13 | Validate the post-playback resource usage | After successful playback, run the resource-usage validation and evaluate the returned CPU load and memory usage. | CPU load and memory usage should be returned and should remain within the configured limits. |
| 14 | Terminate the HTML player | Terminate the application with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<application ID>"}}`. | The HTML player should terminate successfully. |
| 15 | Restore modified plugin states | If the test changed plugin states, restore `DeviceInfo` and `org.rdk.PersistentStore` to their original states with the corresponding `Controller.1.activate` or `Controller.1.deactivate` request. | The plugins should be restored to their states before test execution. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 15 min

**Priority** : High

**Release Version** : M154<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
