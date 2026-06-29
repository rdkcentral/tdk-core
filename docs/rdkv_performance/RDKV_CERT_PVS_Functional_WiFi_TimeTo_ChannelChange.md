## TestCase ID
RDKV_PERFORMANCE_23
## TestCase Name
RDKV_CERT_PVS_Functional_WiFi_TimeTo_ChannelChange

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for channel change in the channel change application is within the configured threshold when the device is connected to a WiFi network, by measuring and averaging the channel change duration across 5 consecutive channel changes.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure channelchange_bundle in PerformanceTestVariables | `channelchange_bundle` must be set to the channel change application bundle filename in PerformanceTestVariables. | The channelchange_bundle variable should be configured with a valid bundle name. |
| 4 | Ensure WiFi network is available | Either the DUT should already be connected and configured with a WiFi IP in the Test Manager, or a WiFi Access Point with the same IP address range should be available. A Lightning application for IP change detection should be hosted. | A WiFi network should be available and accessible for the DUT to connect to. |
| 5 | Configure CHANNEL_CHANGE_TIME_THRESHOLD_VALUE and THRESHOLD_OFFSET | Both values must be set in the device config file for the channel change time validation. | Threshold values should be configured correctly. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check and establish WiFi connection | Check the current active network interface of the DUT. If the interface is already WiFi (wlan0), proceed directly. If it is Ethernet (eth0), switch to WiFi by enabling the WiFi interface, connecting to the configured SSID, launching a Lightning IP change detection app in WebKitBrowser, and setting WiFi as the default interface. | The DUT should be connected to the WiFi network and the active interface should be wlan0. |
| 2 | Install and launch the channel change application | Download, install, and launch the channel change application bundle (com.rdkcentral.channelchange) over the WiFi connection. <br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<channelchange_bundle>"}}` <br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.channelchange", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` <br>Launch: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.channelchange", "intent": "", "launchArgs": ""}}` | The channel change application should be installed and launched successfully over WiFi. |
| 3 | Wait for channel tuning and verify playback | Allow 60 seconds for the application to initialize. Verify tuning activity and playback by checking device logs via SSH: <br>`cat /opt/logs/dacapp.log \| grep -nr "Tuning to channel" \| tail -1` <br>`cat /opt/logs/dacapp.log \| grep -nr Playing \| head -n1` | Tuning and Playing log entries should be present in dacapp.log, confirming the channel change app is active. |
| 4 | Capture channel change times and calculate average | Retrieve all channel change timing entries from the device logs and parse the time for each of the 5 channel changes: <br>`cat /opt/logs/dacapp.log \| grep -nr "channel change:"` <br>Calculate the average time across 5 iterations. | The log should contain 5 channel change time entries. The average channel change time should be calculated successfully. |
| 5 | Validate channel change time against threshold | Compare the average channel change time against the configured threshold (`CHANNEL_CHANGE_TIME_THRESHOLD_VALUE` + `THRESHOLD_OFFSET`). | The average channel change time over WiFi should be within the range: 0 < average_time < (CHANNEL_CHANGE_TIME_THRESHOLD_VALUE + THRESHOLD_OFFSET) milliseconds. |
| 6 | Terminate the application and revert interface | Send a terminate request for the application and revert the network interface to its original state if it was changed. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.channelchange"}}` | The application should be terminated successfully and the network interface should be reverted to its original configuration. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 12 mins

**Priority** : High

**Release Version** : M85<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
