## TestCase ID
RDKV_PERFORMANCE_125
## TestCase Name
RDKV_CERT_PVS_Apps_TimeTo_Video_Playback_Vorbis
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the unified Vorbis video player launches successfully and begins playback within the configured time threshold by measuring the elapsed time between the WPE load-committed and Video Player Playing timestamps.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-test reboot behavior | Configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip the reboot. | The device should follow the configured reboot behavior before the test starts. |
| 2 | Verify the performance test module loads | Ensure that the `rdkv_performance` test component is available and that the device is reachable at the configured IP address and port. | The performance module should load successfully and the device connection should be established. |
| 3 | Configure Vorbis playback inputs | Configure the Vorbis source URL, the configured `vp9_url_type`, the `codec_ogg` player selection, and the unified player application bundle URL used to construct the playback request. | The test should be able to construct a valid Vorbis player URL and identify the application bundle to install or launch. |
| 4 | Configure REST API logging | Set the device configuration key `LOGGING_METHOD` to `REST_API`. | The application log should provide the WPE load committed and Video Player Playing timestamps required for measurement. |
| 5 | Configure playback thresholds | Set the device configuration keys `VIDEO_PLAYBACK_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` to numeric millisecond values. | Both threshold values should be available for the time-to-playback comparison. |
| 6 | Configure application package installation | Set the device configuration key `PACKAGEMANAGER_FILE_LOCATOR` to the package locator prefix required by the device. | The downloaded application package should have a valid installation file locator. |
| 7 | Activate required service plugins | Ensure that `DeviceInfo` and `org.rdk.PersistentStore` are activated. | Both required plugins should report the `activated` state. |
| 8 | Prepare application-management plugins | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` can be activated when the unified player is not already installed. | The application download, installation, and launch services should be available. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check the required plugin states | Query `DeviceInfo` and `org.rdk.PersistentStore` with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@DeviceInfo"}` and `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.PersistentStore"}`. | Each required plugin should return the `activated` state. |
| 2 | Activate unavailable required plugins | If either required plugin is not activated, request activation with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}`, then query its status again. | Each required plugin should report `activated` after the activation request. |
| 3 | Select the Vorbis codec player | Split `codec_ogg` into the configured player identifiers and use `video_src_url_vorbis` with the configured `vp9_url_type`. | The selected player list should correspond to the Vorbis source. |
| 4 | Build the Vorbis player test URL | Combine the Vorbis source URL, configured URL type, selected `codec_ogg` player, execution identifiers, logging information, pause and play operations, and `autotest: "true"` into the unified player test URL. | A complete Vorbis player test URL should be generated. |
| 5 | Store the player URL in PersistentStore | Set the MVS `lightningURL` value with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.PersistentStore.setValue","params":{"namespace":"MVS","key":"lightningURL","value":"<generated Vorbis player test URL>"}}`. | The Vorbis player URL should be stored successfully in PersistentStore. |
| 6 | Check whether the unified player is installed | Request the installed package list with `org.rdk.AppPackageManager.1.listPackages` and inspect the returned installed package IDs for the derived application ID. | The application should be identified as installed, or the flow should proceed to download and install it. |
| 7 | Check application-management plugin availability | Query `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` using `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@<plugin>"}`. Activate any unavailable plugin with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}`. | All application-management plugins should report the `activated` state before package installation. |
| 8 | Download the unified player bundle | Request the configured application bundle with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<configured application download URL>/<bundle name>"}}`. | The application bundle should download successfully and return package details for installation. |
| 9 | Install the unified player bundle | Install the downloaded package with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.install","params":{"packageId":"<application ID>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<configured locator><download result>"}}`. | The bundle should install successfully. |
| 10 | Verify the installed application | Query `org.rdk.AppPackageManager.1.listPackages` again and check that the derived application ID is present in the installed package list. | The application ID should appear in the installed package list. |
| 11 | Launch the unified player | Launch the installed application with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<application ID>","intent":"","launchArgs":""}}`. | The launch request should return success. |
| 12 | Verify the application is active | Query loaded applications with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps"}` and locate the application ID with lifecycle state `APP_STATE_ACTIVE`. | The unified player should appear as an active loaded application. |
| 13 | Capture the Video Player Playing timestamp | Monitor the REST API application log until an entry containing `Video Player Playing` is received, then extract its timestamp. | A valid Video Player Playing timestamp should be captured. |
| 14 | Capture the WPE load committed timestamp | Obtain the application storage path with `grep DEFAULT_APP_STORAGE_PATH /etc/device.properties \| cut -d'=' -f2`, then read the latest timestamp with `grep -i 'wpe load committed' <application log> \| tail -n 1 \| cut -d' ' -f2 \| sed 's/:$//'`. | A valid WPE load committed timestamp should be captured from the application log. |
| 15 | Calculate time to Vorbis playback | Convert both timestamps to milliseconds and calculate `Video Player Playing - WPE load committed`. | The elapsed time should be calculated as a positive millisecond value. |
| 16 | Validate the playback threshold | Read `VIDEO_PLAYBACK_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` from the device configuration and verify that `0 < elapsed time < VIDEO_PLAYBACK_THRESHOLD_VALUE + THRESHOLD_OFFSET`. | The time to Vorbis playback should be within the configured threshold; otherwise the test should fail. |
| 17 | Terminate the unified player | Terminate the application with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<application ID>"}}`. | The unified player should terminate successfully. |
| 18 | Restore modified plugin states | If the test changed plugin states, restore `DeviceInfo` and `org.rdk.PersistentStore` to their original states with the corresponding `Controller.1.activate` or `Controller.1.deactivate` request. | The plugins should be restored to their states before test execution. |
| 19 | Record the execution summary and unload the module | Record the threshold values, captured timestamps, and measured time-to-playback result, then unload the `rdkv_performance` module. | The execution summary should be available and the test module should unload successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M153<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>