## TestCase ID
RDKV_PERFORMANCE_14
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_GetKeys

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to receive key input from RDKWindowManager to the running application is within the configured acceptable threshold, by measuring the average key delivery time across 15 consecutive key generation iterations.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure keytest_bundle in PerformanceTestVariables | `keytest_bundle` must be set to the key test application bundle filename in PerformanceTestVariables. | The keytest_bundle variable should be configured with a valid bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure GET_KEY_THRESHOLD_VALUE in device config | `GET_KEY_THRESHOLD_VALUE` must be set to the acceptable key delivery time in milliseconds in the device config file. | The threshold value should be configured correctly. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Install and launch the key test application | Download, install, and launch the key test application bundle (com.rdkcentral.keytest). <br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<keytest_bundle>"}}` <br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.keytest", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` <br>Launch: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.keytest", "intent": "", "launchArgs": ""}}` | The key test application should be installed and launched successfully. |
| 2 | Retrieve the application instance ID | Query the AppManager for the list of loaded applications to obtain the app instance ID of the running keytest application. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | The loaded apps list should be returned and the app instance ID for com.rdkcentral.keytest should be extractable from the response. |
| 3 | Send key input and measure delivery time — 15 iterations | In a loop of 15 iterations, send keyCode 50 to the application using the RDKWindowManager generateKey method, record the system time before each send, then check the dacapp log to find the key receipt timestamp. Calculate the delivery time as the difference between send time and log timestamp. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.RDKWindowManager.generateKey", "params": {"client": "<appinstanceid>", "keys": "{\"keys\":[{\"keyCode\":50,\"modifiers\":[],\"delay\":0}]}"}}` <br>Log verification via SSH: `cat /opt/logs/dacapp.log \| grep -inr KeyCode \| tail -1` | Each of the 15 key generation calls should return success. The KeyCode log entry should be present in dacapp.log after each iteration, and the delivery time should be calculable from the timestamps. |
| 4 | Calculate and validate average key delivery time | After completing all 15 iterations, calculate the average key delivery time. Compare the average against the configured `GET_KEY_THRESHOLD_VALUE` from the device config file. | All 15 iterations should have completed successfully. The average key delivery time should be less than `GET_KEY_THRESHOLD_VALUE` milliseconds. |
| 5 | Terminate the key test application | Send a terminate request to clean up the application after the measurement. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.keytest"}}` | The application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 7 mins

**Priority** : High

**Release Version** : M98<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
