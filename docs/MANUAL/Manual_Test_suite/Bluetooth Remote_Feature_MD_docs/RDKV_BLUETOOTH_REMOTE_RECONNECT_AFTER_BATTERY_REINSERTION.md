## TestCase ID
RDKV_MANUAL_BLUETOOTH_10
## TestCase Name
RDKV_CERT_MANUAL_BLUETOOTH_REMOTE_RECONNECT_AFTER_BATTERY_REINSERTION

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a paired Bluetooth remote automatically restores its connection to the DUT after the remote battery is removed and re-inserted.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the DUT to an active network via Ethernet prior to the test. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT. |
| 2 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 3 |  Conduct test in isolated environment  | Conduct the test in an isolated environment free of other VA/Bluetooth devices to prevent unintended Bluetooth interference. | The test environment should be free of Bluetooth interference from other devices. |
| 4 |  Ensure bluetooth remote already paired  | Ensure the Bluetooth remote is successfully paired with the DUT and all key presses are confirmed to be functioning correctly prior to the test. | The Bluetooth remote should be paired and all key presses should be functional on the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Remove and re-insert battery  | Remove the battery from the paired remote, wait a few seconds, then re-insert the battery. After a few seconds, perform key presses using the remote. | The Bluetooth connection should be restored automatically after battery re-insertion. All key presses should respond correctly, confirming that the pairing has been re-established. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
