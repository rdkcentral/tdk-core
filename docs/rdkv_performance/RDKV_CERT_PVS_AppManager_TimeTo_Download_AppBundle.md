## TestCase ID
RDKV_PERFORMANCE_194
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_Download_AppBundle
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To measure the time taken to download an app bundle

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|Wpeframework process should be up and running in the device.|
|2|Time in Test Manager and DUT should be in sync with UTC|
|3|google_bundle should be updated in PerformanceTestVariables|
|4|app_download_url should be updated in PerformanceTestVariables|
|5|APPMANAGER_DOWNLOAD_THRESHOLD_VALUE in device specific config file must be updated with correct threshold value|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check the status of org.rdk.DownloadManager
 {"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"} | Should be able to get the current status of org.rdk.DownloadManager  |
| 2 | Step 2  | If org.rdk.DownloadManager is not in activated state, try to activate
{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate" , "params":{"callsign":"org.rdk.DownloadManager"} | Should be able to activate org.rdk.DownloadManager |
| 3 | Step 3  | Register for the thunder event onAppDownloadStatus
{"jsonrpc": "2.0","id": 2,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.1" }} | Should be able to register for the onAppDownloadStatus event successfully |
| 4 | Step 4 | Save the current time just before starting the download to calculate the time taken for downloading the bundle
start_time = datetime.now(UTC).time() | Should save the current time  |
| 5 | Step 5 | Download the configured app bundle from the configured download url 
{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download","params": {"url":"<download url>"}}
 | The app bundle should get downloaded successfully and the API should return success |
| 6 | Step 6 | Check if onAppDownloadStatus event is received on success download of the bundle | Should receive the event successfully
{"jsonrpc":"2.0","method":"client.events.1.onAppDownloadStatus","params":{"downloadStatus":"[{\\"downloadId\\":\\"2001\\",\\"fileLocator\\":<PACKAGEMANAGER_FILE_LOCATOR>}]"}} |
| 7 | Step 7 | Get the time when the event is received 
time_taken_for_download = downloaded_time - download_start_time | Event: 03:13:54.408570$$${"jsonrpc":"2.0","method":"client.events.1.onAppDownloadStatus","params":{"downloadStatus":"[{\\"downloadId\\":\\"2001\\",\\"fileLocator\\":<PACKAGEMANAGER_FILE_LOCATOR>"}]"}} |
| 8 | Step 8 | Calculate the time taken to download the app bundle using the start time and event time
 | The time taken for download should be less than the configured threshold value |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
