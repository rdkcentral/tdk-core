## TestCase ID
RDKV_PERFORMANCE_221
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_WiFiConnection_5GHZ

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the system CPU load and memory usage remain within acceptable limits after the device is connected to a 5 GHz WiFi Access Point, confirming that the 5 GHz WiFi connection does not introduce excessive resource consumption.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Ensure a 5 GHz WiFi Access Point is available | Either the DUT should already be connected and configured with a 5 GHz WiFi IP in the Test Manager, or a 5 GHz WiFi Access Point with the same IP address range as Ethernet should be available. If the DUT is an RPI, it must be RPI 3B+ or newer to detect 5 GHz SSIDs. | A 5 GHz WiFi network should be available and accessible for the DUT to connect to. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check current interface and SSID frequency | Check the current active network interface of the DUT. If the interface is already WiFi (wlan0), verify the frequency of the connected SSID is 5 GHz. If the interface is Ethernet (eth0), switch to the 5 GHz WiFi SSID by connecting to the configured 5 GHz SSID. | The DUT should be connected to the 5 GHz WiFi network with wlan0 as the active interface and the connected SSID frequency confirmed as 5 GHz. |
| 2 | Verify and activate the DeviceInfo plugin | Query the DeviceInfo plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}` | The DeviceInfo plugin should be in the activated state. |
| 3 | Validate resource usage over 5 GHz WiFi connection | Measure and validate the system CPU and memory usage while the device is connected to the 5 GHz WiFi network. Invoke the DeviceInfo systeminfo API: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. | CPU load and memory usage should be within the configured acceptable limits while the device is connected to the 5 GHz WiFi network. |
| 4 | Revert network interface and plugin state | If the network interface was switched during the test, revert the default interface and any plugin state changes made during setup. | The network interface and plugin state should be reverted to their original configurations. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15 mins

**Priority** : High

**Release Version** : M89<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
