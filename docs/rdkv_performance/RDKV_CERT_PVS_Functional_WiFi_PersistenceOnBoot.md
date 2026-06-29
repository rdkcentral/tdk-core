## TestCase ID
RDKV_PERFORMANCE_22
## TestCase Name
RDKV_CERT_PVS_Functional_WiFi_PersistenceOnBoot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the WiFi connection persists after a device reboot — confirming that the device automatically reconnects to the same WiFi SSID after rebooting without any manual reconfiguration.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm org.rdk.NetworkManager plugin is available | The org.rdk.NetworkManager plugin must be present and activatable in the device build. | The NetworkManager plugin should be available in the build. |
| 3 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 4 | Ensure WiFi network is available | Either the DUT's default interface should already be WiFi, or a WiFi SSID with the same IP address range as Ethernet should be available for connection during the test. | A WiFi network should be accessible for the DUT to connect to and persist across reboot. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate the NetworkManager plugin | Query the NetworkManager plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.NetworkManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}` | The org.rdk.NetworkManager plugin should be in the activated state. |
| 2 | Establish WiFi connection | Connect the DUT to the WiFi interface (wlan0). If the device is not already on WiFi, connect to the configured SSID. | The DUT should be successfully connected to the WiFi network. |
| 3 | Record the connected SSID | Retrieve and record the name of the currently connected WiFi SSID to use as the reference for post-reboot verification. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}` | The connected SSID name should be retrieved successfully. |
| 4 | Reboot the device | Trigger a device reboot via the Controller harakiri method and wait for the device to come back online within the configured reboot wait time. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should reboot and come back online successfully. |
| 5 | Verify WiFi persistence after reboot | After the device comes back online, invoke the DeviceInfo systeminfo API to confirm the device has restarted, then check the connected SSID to verify it matches the SSID recorded before the reboot. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.NetworkManager.1.GetConnectedSSID"}` | The device should be automatically reconnected to the same WiFi SSID after reboot without any manual reconfiguration. The connected SSID should match the one recorded before the reboot. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15 mins

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
