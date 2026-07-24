## TestCase ID
RDKV_MANUAL_BLUETOOTH_03
## TestCase Name
RDKV_CERT_MANUAL_BTRemote_Repair_After_FactoryReset

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Bluetooth remote pairing is cleared after a DUT factory reset and that the remote can be successfully re-paired from the startup pairing screen. This test confirms that all navigation key presses respond correctly after re-pairing, ensuring that remote pairing recovery after factory reset meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the DUT to an active network via Ethernet prior to the test. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 2 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 3 |  Conduct test in isolated environment  | Conduct the test in an isolated environment free of other VA/Bluetooth devices to prevent unintended Bluetooth interference. | The test environment should be free of Bluetooth interference from other devices.|
| 4 |  Ensure bluetooth remote already paired  | Ensure the Bluetooth remote is successfully paired with the DUT and all key presses are confirmed to be functioning correctly prior to the test. | The Bluetooth remote should be paired and all key presses should be functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Navigate to factory reset  | On the DUT, navigate to Settings > Other Settings > Advanced Settings > Device and select "Factory Reset". | All screens in the navigation path should load correctly in sequence. The Factory Reset confirmation screen should be displayed.|
| 2 |  Confirm factory reset  | Select the "Confirm" button on the Factory Reset confirmation screen. | The DUT should initiate the factory reset process and reboot after a few seconds.|
| 3 |  Observe DUT after reboot  | Observe the DUT display after reboot. | The RDK splash screen should be displayed, followed by the "Pair your remote control" startup screen.|
| 4 |  Clear remote pairing information  | Clear the existing pairing information from the remote by pressing and holding the CH UP and VOL DOWN keys simultaneously for a few seconds. | The red LED on the remote should blink once and stop, indicating that the pairing information has been successfully cleared from the remote.|
| 5 |  Put remote into pairing mode  | Put the remote into pairing mode by pressing and holding the OK and CH UP keys simultaneously for a few seconds. | The red LED on the remote should blink continuously, indicating that the remote has entered pairing mode.|
| 6 |  Wait for auto-pairing with DUT  | Wait for the DUT to detect and pair with the remote automatically. | The remote should pair automatically with the DUT. A confirmation message such as "Paired with Tatlow RDK remote" should be displayed on screen, and the RDK UI should automatically navigate to the Language selection screen.|
| 7 |  Navigate language selection screen  | Use the remote navigation keys to navigate the Language selection screen. Navigate to the "Continue Setup" button and press OK. | All navigation key presses and the OK button should function correctly. The RDK UI should advance to the Network selection screen.|
| 8 |  Skip network selection  | Navigate to the "Skip" button on the Network selection screen and press OK. | The RDK UI Home screen should launch successfully.|
| 9 |  Validate remote navigation on Home screen  | Perform navigation key presses on the RDK UI Home screen and attempt to open an application such as YouTube using the remote. | All navigation key presses should respond correctly and the selected application should launch successfully.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
