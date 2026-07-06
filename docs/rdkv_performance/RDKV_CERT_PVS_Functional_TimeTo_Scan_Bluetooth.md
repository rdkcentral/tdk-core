## TestCase ID
RDKV_PERFORMANCE_16
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_Scan_Bluetooth

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to scan and discover a Bluetooth device is within the configured acceptable threshold, by measuring the duration from the start of the scan to when the onDiscoveredDevice event is triggered.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Ensure a Bluetooth emulator is available | A Bluetooth emulator device must be accessible and configurable during the test. Time in the DUT and Test Manager should be in sync. | The Bluetooth emulator should be reachable and its time should be synchronized with the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate the Bluetooth plugin | Query the Bluetooth plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.Bluetooth"}` <br><br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}` | The org.rdk.Bluetooth plugin should be in the activated state. |
| 2 | Make Bluetooth emulator discoverable | SSH into the Bluetooth emulator and execute commands to make it discoverable: `bluetoothctl`, `agent NoInputNoOutput`, `default-agent`, `discoverable on`. | The Bluetooth emulator should be made discoverable successfully. |
| 3 | Subscribe to Bluetooth device discovery event | Register an event listener for the onDiscoveredDevice event to capture the time when the emulator is discovered. <br>`{"jsonrpc": "2.0", "id": 6, "method": "org.rdk.Bluetooth.1.register", "params": {"event": "onDiscoveredDevice", "id": "client.events.1"}}` | The event registration should succeed and the listener should be active. |
| 4 | Enable Bluetooth on the DUT | Enable Bluetooth functionality on the device under test. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.enable"}` | Bluetooth should be enabled successfully on the DUT. |
| 5 | Start Bluetooth scan and record start time | Record the current system time, then start scanning for Bluetooth devices. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": "30", "profile": "DEFAULT"}}` | Bluetooth scan should start successfully. |
| 6 | Stop scan and validate discovery time | Stop the Bluetooth scan and retrieve the onDiscoveredDevice event from the event buffer. Calculate the scan time as the difference between the event timestamp and the recorded start time. Compare against the configured threshold. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Bluetooth.1.stopScan"}` | The onDiscoveredDevice event should be received. The time taken to discover the Bluetooth emulator should be within the configured acceptable threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
