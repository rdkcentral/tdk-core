## TestCase ID
RDKV_STABILITY_37
## TestCase Name
RDKV_CERT_RVS_Toggle_2.4GHz_5GHz
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly switching the WiFi connection between 2.4GHz and 5GHz frequency bands for max_ssid_changes iterations while streaming content, verifying CPU and memory usage remains within expected limits after each switch.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be in resumed state; org.rdk.NetworkManager (or org.rdk.Wifi) and DeviceInfo plugins must be activated.|
|3|Both 2.4GHz and 5GHz WiFi access points must be available and configured in StabilityTestVariables (ssid_24ghz, password_24ghz, ssid_5ghz, password_5ghz).|
|4|max_ssid_changes must be configured in StabilityTestVariables.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, org.rdk.NetworkManager, and DeviceInfo plugins. Set required states: WebKitBrowser=resumed, org.rdk.NetworkManager=activated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Check current interface and switch to WiFi if needed | Check the current default network interface via `check_current_interface`. If the device is on Ethernet, switch to WiFi: connect to the 2.4GHz SSID via org.rdk.NetworkManager. | Device should be connected via WiFi interface. |
| 4 | Get LightningApp URL and launch | Get the lightning app URL configured in StabilityTestVariables. Launch the LightningApp. | LightningApp should launch successfully. |
| 5 | Check current SSID frequency | Verify which frequency band (2.4GHz or 5GHz) the device is currently connected to. | Current SSID and frequency should be determined. |
| 6 | Toggle 2.4GHz/5GHz loop (repeat for max_ssid_changes iterations) | For each iteration: <br>Connect to the opposite frequency WiFi network (if on 2.4GHz, switch to 5GHz, and vice versa) via org.rdk.NetworkManager: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.NetworkManager.1.WiFiConnect","params":{"ssid":"<new_ssid>","passphrase":"<password>","security":4}}` <br>Wait for the connection to be established. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | WiFi band should switch successfully in each iteration. CPU load and memory usage should remain within expected limits. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 8 | Revert network and plugins | Restore the original network interface settings and revert plugins to their original state. | Network settings and plugins should be restored to pre-test state. |
| 9 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the WiFi toggle stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 3000

**Priority** : High

**Release Version** : M89<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
