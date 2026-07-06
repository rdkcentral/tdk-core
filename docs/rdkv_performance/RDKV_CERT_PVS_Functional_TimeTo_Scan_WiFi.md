## TestCase ID
RDKV_PERFORMANCE_17
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_Scan_WiFi

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to scan and discover the configured WiFi SSID is within the acceptable configured threshold, by measuring the duration from the start of the WiFi scan to when the onAvailableSSIDs event is triggered.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure WIFI_SSID_NAME in device config | `WIFI_SSID_NAME` must be set to the target WiFi SSID to scan for in the device-specific config file. | The SSID name should be configured correctly. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate the NetworkManager plugin | Query the NetworkManager plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.NetworkManager"}` <br><br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}` | The org.rdk.NetworkManager plugin should be in the activated state. |
| 2 | Subscribe to available SSIDs event | Register an event listener for the onAvailableSSIDs event to capture the time when the SSID list becomes available. <br>`{"jsonrpc": "2.0", "id": 6, "method": "org.rdk.NetworkManager.1.register", "params": {"event": "onAvailableSSIDs", "id": "client.events.1"}}` | The event registration should succeed and the listener should be active. |
| 3 | Start WiFi scan and record start time | Obtain SSH parameters, then record the current system time and initiate a WiFi scan for the configured SSID. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.NetworkManager.1.StartWiFiScan", "params": {"ssid": "<WIFI_SSID_NAME>"}}` | The WiFi scan should start successfully and begin searching for available SSIDs. |
| 4 | Capture event and validate scan time | Wait up to 60 seconds for the onAvailableSSIDs event from the event buffer. Calculate the scan time as the difference between the event receipt time and the recorded start time. Compare against the configured threshold. | The onAvailableSSIDs event should be received within 60 seconds. The time taken to scan and discover the SSID details should be within the configured acceptable threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
