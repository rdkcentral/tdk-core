## TestCase ID
RDKV_PERFORMANCE_171
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_Launch_App
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To measure the time taken to launch an app

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|Wpeframework process should be up and running in the device.|
|2|Time in Test Manager and DUT should be in sync with UTC|
|3|google_bundle should be updated in PerformanceTestVariables|
|4|app_download_url should be updated in PerformanceTestVariables|
|5|PACKAGEMANAGER_FILE_LOCATOR in device specific config file must be updated with correct file path where the app bundle is getting downloaded in the device|
|6|APPMANAGER_LAUNCH_THRESHOLD_VALUE in device specific config file must be updated with correct threshold value|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check the status of org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS and org.rdk.AppManager <br> {"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"} | Should be able to get the current status of org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS and org.rdk.AppManager |
| 2 | Step 2 | If org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS or org.rdk.AppManager is not in activated state, try to activate <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.DownloadManager"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.PackageManagerRDKEMS"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.AppManager"}} | Should be able to activate org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS and org.rdk.AppManager |
| 3 | Step 3 | Check if the configured app is already installed in the device <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"} | Should be able to retrieve the list of apps installed in the device |
| 4 | Step 4 | If the app is already installed in the device, uninstall the app from the device <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "com.rdkcentral.google"}} | The app should get uninstalled successfully |
| 5 | Step 5 | Start downloading the app bundle to install in the device <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download","params": {"url":"<download url>"}} | The app bundle should get downloaded successfully and the API should return success |
| 6 | Step 6 | Initiate install app command to install the downloaded app bundle<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install","params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"/opt/CDL/package2001"}} | The app should get installed in the device |
| 7 | Step 7 | Register for the event onAppLifecycleStateChanged to listen for the launch completion<br>{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}} | Should be able to register for the onAppLifecycleStateChanged event successfully |
| 8 | Step 8 | Save the current time just before initiating the launch to calculate the time taken for launch<br>start_time = datetime.now(UTC).time() | Should be able to save the current time successfully |
| 9 | Step 9 | Initiate launch app command to launch the installed app<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.launch", "params": {"appId": "com.rdkcentral.google"}} | The app should get launched in the device |
| 10 | Step 10 | Check if the event onAppLifecycleStateChanged is received with state APP_STATE_ACTIVE on launching the app | Should receive the event successfully<br>{"jsonrpc":"2.0","method":"client.events.1.onAppLifecycleStateChanged","params":{"appId":"com.rdkcentral.google","state":"APP_STATE_ACTIVE"}} |
| 11 | Step 11 | Get the time when the APP_STATE_ACTIVE event is received <br>launch_time = str(event).split("$$$")[0]<br>time_taken_for_launch = launched_time - launch_start_time | Event: \<HH:MM:SS.ffffff\>$$${"jsonrpc":"2.0","method":"client.events.1.onAppLifecycleStateChanged","params":{"appId":"com.rdkcentral.google","state":"APP_STATE_ACTIVE"}} |
| 12 | Step 12 | Calculate the time taken to launch the app using the start time and event time | The time taken for launch should be less than the configured threshold value |
| 13 | Step 13 | Terminate the launched app<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminate", "params": {"appId": "com.rdkcentral.google"}} | The app should get terminated successfully |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
