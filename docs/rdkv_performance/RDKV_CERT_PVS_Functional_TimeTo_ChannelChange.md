## TestCase ID
RDKV_PERFORMANCE_12
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_ChannelChange

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for channel change in the channel change application is within the configured threshold limit, by measuring and averaging the channel change duration across 5 consecutive channel changes.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure channelchange_bundle in PerformanceTestVariables | `channelchange_bundle` must be set to the channel change application bundle filename in PerformanceTestVariables. | The channelchange_bundle variable should be configured with a valid bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure CHANNEL_CHANGE_TIME_THRESHOLD_VALUE in device config | `CHANNEL_CHANGE_TIME_THRESHOLD_VALUE` must be set to the acceptable channel change time in milliseconds in the device config file. | The threshold value should be configured correctly. |
| 6 | Configure THRESHOLD_OFFSET in device config | `THRESHOLD_OFFSET` must be set in the device config file to allow a tolerance margin for the threshold comparison. | The threshold offset should be configured correctly. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Install and launch the channel change application | Download, install, and launch the channel change application bundle (com.rdkcentral.channelchange). <br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<channelchange_bundle>"}}` <br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.channelchange", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` <br>Launch: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.channelchange", "intent": "", "launchArgs": ""}}` | The channel change application should be installed and launched successfully. |
| 2 | Wait for channel tuning to begin | Allow 60 seconds for the application to initialize and begin channel tuning. Verify tuning activity by checking device logs via SSH: <br>`cat /opt/logs/dacapp.log \| grep -nr "Tuning to channel" \| tail -1` | The tuning log entry should be present in dacapp.log confirming the channel change app is actively tuning. |
| 3 | Verify playback has started | Confirm that video playback has started after tuning by checking the device logs via SSH: <br>`cat /opt/logs/dacapp.log \| grep -nr Playing \| head -n1` | A Playing log entry should be present, confirming video playback has commenced. |
| 4 | Capture channel change times for 5 channel changes | Retrieve all channel change timing entries from the device logs via SSH and parse the time for each of the 5 channel changes: <br>`cat /opt/logs/dacapp.log \| grep -nr "channel change:"` | The log should contain 5 channel change time entries that can be parsed successfully. |
| 5 | Calculate and validate average channel change time | Calculate the average channel change time across 5 iterations and compare it against the configured threshold (`CHANNEL_CHANGE_TIME_THRESHOLD_VALUE` + `THRESHOLD_OFFSET`) from the device config file. | The average channel change time should be within the range: 0 < average_time < (CHANNEL_CHANGE_TIME_THRESHOLD_VALUE + THRESHOLD_OFFSET) milliseconds. |
| 6 | Terminate the channel change application | Send a terminate request to clean up the application after the measurement. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.channelchange"}}` | The application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
