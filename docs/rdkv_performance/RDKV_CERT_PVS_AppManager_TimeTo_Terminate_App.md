## TestCase ID
RDKV_PERFORMANCE_172
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_Terminate_App
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To measure the time taken to terminate an app

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|Wpeframework process should be up and running in the device.|
|2|Time in Test Manager and DUT should be in sync with UTC|
|3|google_bundle should be updated in PerformanceTestVariables|
|4|app_download_url should be updated in PerformanceTestVariables|
|5|PACKAGEMANAGER_FILE_LOCATOR in device specific config file must be updated with correct file path where the app bundle is getting downloaded in the device|
|6|APPMANAGER_TERMINATE_THRESHOLD_VALUE in device specific config file must be updated with correct threshold value|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check the status of org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS and org.rdk.AppManager <br> {"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"} | Should be able to get the current status of org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS and org.rdk.AppManager |
| 2 | Step 2 | If org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS or org.rdk.AppManager is not in activated state, try to activate <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.DownloadManager"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.PackageManagerRDKEMS"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.AppManager"}} | Should be able to activate org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS and org.rdk.AppManager |
| 3 | Step 3 | Check if the configured app is already installed in the device <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"} | Should be able to retrieve the list of apps installed in the device |
| 4 | Step 4 | If the app is not already installed, start downloading the app bundle <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download","params": {"url":"<download url>"}} | The app bundle should get downloaded successfully and the API should return success |
| 5 | Step 5 | If the app is not already installed, install the downloaded app bundle<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install","params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>>"}} | The app should get installed in the device |
| 6 | Step 6 | Launch the app in the device<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp","params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}} | The app should get launched successfully |
| 7 | Step 7 | Verify the app is in launched state<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"} | The response should include com.rdkcentral.google with lifecycleState as APP_STATE_ACTIVE<br>{"appId": "com.rdkcentral.google", "type": "INTERACTIVE_APP", "targetLifecycleState": "APP_STATE_ACTIVE", "lifecycleState": "APP_STATE_ACTIVE"} |
| 8 | Step 8 | Register for the event onAppLifecycleStateChanged to listen for the terminate completion<br>{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}} | Should be able to register for the onAppLifecycleStateChanged event successfully |
| 9 | Step 9 | Save the current time just before initiating the terminate to calculate the time taken for termination<br>start_time = datetime.now(UTC).time() | Should be able to save the current time successfully |
| 10 | Step 10 | Initiate terminate app command to terminate the launched app<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp","params": {"appId":"com.rdkcentral.google"}} | The app should get terminated successfully and the API should return success |
| 11 | Step 11 | Check if the event onAppLifecycleStateChanged is received with state APP_STATE_UNLOADED on terminating the app | Should receive the event successfully<br>{"jsonrpc":"2.0","method":"client.events.1.onAppLifecycleStateChanged","params":{"appId":"com.rdkcentral.google","appInstanceId":"\<appInstanceId\>","newState":"APP_STATE_UNLOADED","oldState":"APP_STATE_ACTIVE","errorReason":"APP_ERROR_NONE"}} |
| 12 | Step 12 | Get the time when the APP_STATE_UNLOADED event is received <br>terminate_time = str(event).split("$$$")[0]<br>time_taken_for_terminate = terminated_time - terminate_start_time | Event: \<HH:MM:SS.ffffff\>$$${"jsonrpc":"2.0","method":"client.events.1.onAppLifecycleStateChanged","params":{"appId":"com.rdkcentral.google","appInstanceId":"\<appInstanceId\>","newState":"APP_STATE_UNLOADED","oldState":"APP_STATE_ACTIVE","errorReason":"APP_ERROR_NONE"}} |
| 13 | Step 13 | Calculate the time taken to terminate the app using the start time and event time | The time taken for termination should be less than the configured threshold value |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
