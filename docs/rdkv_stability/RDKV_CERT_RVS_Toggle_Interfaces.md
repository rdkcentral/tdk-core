## TestCase ID
RDKV_STABILITY_17
## TestCase Name
RDKV_CERT_RVS_Toggle_Interfaces
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly toggling the network interface between Ethernet and WiFi (or enabling/disabling an interface) for max_interface_changes iterations while streaming content, verifying CPU and memory usage remains within expected limits after each toggle.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|org.rdk.NetworkManager and DeviceInfo plugins must be activated; WebKitBrowser plugin must be in resumed state.|
|3|Both Ethernet (eth0) and WiFi (wlan0) interfaces must be available; WiFi credentials must be configured in StabilityTestVariables.|
|4|max_interface_changes must be configured in StabilityTestVariables.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, org.rdk.NetworkManager, and DeviceInfo plugins. Set required states: WebKitBrowser=resumed, org.rdk.NetworkManager=activated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Check current interface | Check the current default network interface (Ethernet or WiFi) via `check_current_interface`. Get the current network interface in use by the device. | Current network interface should be determined. |
| 4 | Toggle interface loop (repeat for max_interface_changes iterations) | For each iteration: <br>If on Ethernet: Disable Ethernet and enable WiFi. Connect to WiFi using stored credentials via org.rdk.NetworkManager: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.NetworkManager.1.SetInterfaceState","params":{"interface":"eth0","enabled":false}}` `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.NetworkManager.1.SetInterfaceState","params":{"interface":"wlan0","enabled":true}}` <br>If on WiFi: Disconnect WiFi and enable Ethernet. <br>Verify the interface switch was successful and network is accessible. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Network interface should toggle successfully in each iteration. Device should remain connected after each toggle. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert network and plugins | Restore the original network interface settings and revert plugins to their original state. | Network settings and plugins should be restored to pre-test state. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the interface toggle stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 4000

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
