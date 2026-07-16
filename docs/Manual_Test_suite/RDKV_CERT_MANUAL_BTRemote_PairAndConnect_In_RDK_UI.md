## TestCase ID
RDKV_MANUAL_BLUETOOTH_09
## TestCase Name
RDKV_CERT_MANUAL_BTRemote_PairAndConnect_In_RDK_UI

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a Bluetooth remote can be successfully paired and connected to the DUT while the RDK UI is active. This test exercises the RDK Bluetooth pairing stack, the remote-control key-mapping service, and the RDK UI to validate remote-control button behaviour. The test confirms that all navigation key presses should function correctly, confirming that the remote is successfully paired and connected to the DUT.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the DUT to an active network via Ethernet prior to the test. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 2 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 3 |  Conduct test in isolated environment  | Conduct the test in an isolated environment free of other VA/Bluetooth devices to prevent unintended Bluetooth interference. | The test environment should be free of Bluetooth interference from other devices.|
| 4 |  Ensure remote is not currently paired  | Ensure the remote to be paired is not currently paired or connected to any DUT. If the remote is already paired to a DUT, clear the pairing information by pressing and holding the CH UP and VOL DOWN keys simultaneously for a few seconds before starting the test. | The remote should have no existing pairing and should be ready for a fresh pairing with the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Put remote into pairing mode  | Put the remote into pairing mode by pressing and holding the OK and CH UP keys simultaneously for a few seconds. | The red LED on the remote should blink continuously, indicating that the remote has entered pairing mode.|
| 2 |  Wait for auto-pairing with DUT  | Wait for the DUT to detect and pair with the remote automatically. | The remote should pair automatically with the DUT.|
| 3 |  Validate key presses after pairing  | Perform navigation key presses using the newly paired remote. | All navigation key presses should function correctly, confirming that the remote is successfully paired and connected to the DUT.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
