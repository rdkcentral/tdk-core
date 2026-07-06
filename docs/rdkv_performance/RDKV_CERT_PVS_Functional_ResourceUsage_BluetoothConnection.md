## TestCase ID
RDKV_PERFORMANCE_6
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_BluetoothConnection

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the system CPU load and memory usage remain within acceptable limits after establishing a Bluetooth connection between the device under test and a Bluetooth emulator.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Ensure a Bluetooth emulator is available | A Bluetooth emulator device must be accessible via SSH and available for pairing during the test execution. | The Bluetooth emulator should be reachable and configurable via SSH. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate the DeviceInfo, org.rdk.Bluetooth, and org.rdk.System plugins. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.Bluetooth"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.System"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All three plugins should be in the activated state. |
| 2 | Make Bluetooth emulator discoverable | SSH into the Bluetooth emulator device and execute the bluetoothctl commands to make it discoverable: `bluetoothctl`, `agent NoInputNoOutput`, `default-agent`, `discoverable on`. | The Bluetooth emulator should be made discoverable successfully. |
| 3 | Enable Bluetooth on the device under test | Enable Bluetooth functionality on the DUT using the Bluetooth plugin. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.enable"}` | Bluetooth should be enabled successfully on the DUT. |
| 4 | Start Bluetooth scan | Start scanning for nearby Bluetooth devices with a 30-second timeout using the default profile. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": "30", "profile": "DEFAULT"}}` | Bluetooth scan should start successfully. |
| 5 | Stop Bluetooth scan | Stop the ongoing Bluetooth scan. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.stopScan"}` | The Bluetooth scan should stop successfully. |
| 6 | Retrieve discovered Bluetooth devices | Retrieve the list of devices discovered during the scan. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}` | The discovered devices list should be returned successfully. The Bluetooth emulator should appear in the list and its device ID should be identified by matching `BT_EMU_DEVICE_NAME`. |
| 7 | Pair with the Bluetooth emulator | Initiate a pairing request to the Bluetooth emulator using the device ID obtained from the discovered devices list. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<device_id>"}}` | The pairing request should be sent successfully. |
| 8 | Verify pairing is successful | Retrieve the list of paired devices and confirm the Bluetooth emulator appears in the list. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.getPairedDevices"}` | The Bluetooth emulator should appear in the paired devices list, confirming that pairing was completed successfully. |
| 9 | Trust DUT Bluetooth MAC on emulator | SSH into the Bluetooth emulator and run the trust command for the DUT's Bluetooth MAC address: `bluetoothctl <<< 'trust <bluetooth_mac>'`. | The trust command should execute successfully on the Bluetooth emulator. |
| 10 | Connect to the Bluetooth emulator | Initiate a Bluetooth connection to the emulator using the paired device ID, device type, and DEFAULT profile. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<device_id>", "deviceType": "<device_type>", "profile": "DEFAULT"}}` | The Bluetooth connection should be established successfully. |
| 11 | Validate resource usage after Bluetooth connection | After the Bluetooth connection is established, measure and validate the system CPU and memory usage. Invoke the DeviceInfo systeminfo API: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. | CPU load and memory usage should be within the configured acceptable limits after establishing the Bluetooth connection. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
