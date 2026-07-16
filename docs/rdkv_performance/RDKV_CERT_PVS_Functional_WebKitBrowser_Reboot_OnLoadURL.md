## TestCase ID
RDKV_PERFORMANCE_21
## TestCase Name
RDKV_CERT_PVS_Functional_WebKitBrowser_Reboot_OnLoadURL

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an application can successfully load a URL before and after a device reboot, confirming that the device remains stable following a reboot and the application is capable of relaunching and loading the URL again.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure REBOOT_WAIT_TIME in device config | `REBOOT_WAIT_TIME` must be set in the device config file to define the wait period after a reboot for the device to come back online. | The reboot wait time should be configured correctly. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Install and launch the application (pre-reboot) | Download, install, and launch the application bundle (com.rdkcentral.google) on the device before rebooting. <br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br><br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` <br><br>Launch: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should be installed and launched successfully before the reboot. |
| 2 | Reboot the device | Trigger a device reboot via the Controller harakiri method and wait for the device to come back online within the configured `REBOOT_WAIT_TIME`. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should reboot and come back online successfully within the configured wait time. |
| 3 | Validate device uptime after reboot | After the device comes back online, verify that the device uptime is less than 280 seconds, confirming it is a fresh boot. | The device uptime should be less than 280 seconds, confirming a successful cold reboot. |
| 4 | Install and launch the application (post-reboot) | After device recovery, repeat the install and launch procedure for the application to verify that the device is stable and the application can launch again after reboot. <br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br><br>Launch: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should relaunch successfully after the device reboot, confirming device stability. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 8 mins

**Priority** : High

**Release Version** : M95<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
