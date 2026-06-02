## TestCase ID
RDKV_STABILITY_48
## TestCase Name
RDKV_CERT_RVS_Bluetooth_PairUnpair
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by continuously pairing and unpairing a Bluetooth emulator device for a minimum of 1000 iterations, verifying CPU and memory usage remains within expected limits after each operation.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|A Bluetooth emulator must be set up and accessible via SSH; BT_EMU_DEVICE_NAME must be configured in the device config file.|
|3|org.rdk.Bluetooth and DeviceInfo plugins must be available in the supported plugins list (SUPPORTED_PLUGINS in device config).|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of org.rdk.Bluetooth and DeviceInfo plugins via `rdkservice_getPluginStatus`. Activate any plugin not in the required state. Required states: org.rdk.Bluetooth=activated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Pair-Unpair loop (repeat for pair_unpair_max_count iterations) | For each iteration: <br>SSH to the Bluetooth emulator and execute `bluetoothctl`, `agent NoInputNoOutput`, `default-agent`, `discoverable on` to make it discoverable. <br>Enable Bluetooth on DUT: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.enable"}` <br>Start scan: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.startScan","params":{"timeout":"30","profile":"DEFAULT"}}` <br>Stop scan: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.stopScan"}` <br>Get discovered devices and find emulator by BT_EMU_DEVICE_NAME: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}` <br>Pair the device: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.pair","params":{"deviceID":"<deviceID>"}}` <br>Verify device appears in pairedDevices list: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.getPairedDevices"}` <br>Unpair the device: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.unpair","params":{"deviceID":"<deviceID>"}}` <br>Verify device no longer appears in pairedDevices list. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Pair and unpair should succeed in each iteration. Device should not appear in pairedDevices after unpairing. CPU load and memory usage should be within expected limits. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 2400

**Priority** : High

**Release Version** : M93<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
