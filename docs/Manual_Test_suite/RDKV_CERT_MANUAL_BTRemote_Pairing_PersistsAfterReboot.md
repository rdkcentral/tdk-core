## TestCase ID
RDKV_MANUAL_BLUETOOTH_02
## TestCase Name
RDKV_CERT_MANUAL_BTRemote_Pairing_PersistsAfterReboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Bluetooth remote pairing is preserved and key presses remain functional after a DUT reboot. This test exercises the RDK Bluetooth pairing stack, the remote-control key-mapping service, and the RDK UI to validate remote-control button behaviour. The test confirms that all key presses should respond correctly, confirming that the remote pairing has persisted across the reboot.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the DUT to an active network via Ethernet prior to the test. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 2 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 3 |  Ensure bluetooth remote already paired  | Ensure the Bluetooth remote is successfully paired with the DUT and all key presses are confirmed to be functioning correctly prior to the test. | The Bluetooth remote should be paired and all key presses should be functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Reboot DUT  | Reboot the DUT. | The DUT should reboot successfully and the RDK UI Home screen should be displayed upon boot.|
| 2 |  Validate key presses after reboot  | Perform key presses using the same paired remote that was validated before the reboot. | All key presses should respond correctly, confirming that the remote pairing has persisted across the reboot.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
