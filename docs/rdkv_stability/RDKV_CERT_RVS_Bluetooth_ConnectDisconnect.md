## TestCase ID
RDKV_STABILITY_25
## TestCase Name
RDKV_CERT_RVS_Bluetooth_ConnectDisconnect
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by continuously connecting and disconnecting a Bluetooth device for a minimum of 1000 iterations, verifying CPU and memory usage remains within expected limits after each operation.

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
| 2 | Check and set plugin preconditions | Get the status of org.rdk.Bluetooth and DeviceInfo plugins via `rdkservice_getPluginStatus`. Activate any plugin not in the required state using `rdkservice_setPluginStatus`. Required states: org.rdk.Bluetooth=activated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Prepare Bluetooth emulator | SSH to the Bluetooth emulator device and execute `bluetoothctl`, `agent NoInputNoOutput`, `default-agent`, and `discoverable on` to make the emulator discoverable. | Bluetooth emulator should be discoverable. |
| 4 | Enable Bluetooth on DUT | Enable Bluetooth on the DUT using the Bluetooth plugin API.<br>{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.enable"} | Bluetooth should be enabled successfully. |
| 5 | Start scan for devices | Start scanning for Bluetooth devices with a timeout of 30 seconds.<br>{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.startScan","params":{"timeout":"30","profile":"DEFAULT"}} | Scan should start without errors. |
| 6 | Wait and stop scan | Wait 30 seconds for discovery then stop scanning.<br>{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.stopScan"} | Scan should stop successfully. |
| 7 | Get discovered devices | Retrieve the list of discovered Bluetooth devices and find the emulator by BT_EMU_DEVICE_NAME.<br>{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.getDiscoveredDevices"} | The emulator device should appear in the discovered devices list. |
| 8 | Pair device | Pair the DUT with the Bluetooth emulator using the discovered device ID.<br>{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.pair","params":{"deviceID":"<deviceID>"}} | Pairing should complete successfully. |
| 9 | Connect and disconnect loop (repeat for connect_disconnect_max_count iterations) | For each iteration: Connect to the Bluetooth device: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.connect","params":{"deviceID":"<deviceID>"}}` <br>Disconnect from the device: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.disconnect","params":{"deviceID":"<deviceID>"}}` <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage` using DeviceInfo.1.systeminfo. | Connect and disconnect should succeed in each iteration. CPU load and memory usage should be within expected limits. |
| 10 | Unpair device | Unpair the Bluetooth emulator from the DUT.<br>{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Bluetooth.1.unpair","params":{"deviceID":"<deviceID>"}} | Device should be unpaired successfully. |
| 11 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with iteration data. |
| 12 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 13 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 2000

**Priority** : High

**Release Version** : M87<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
