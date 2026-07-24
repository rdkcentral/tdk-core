## TestCase ID
RDKV_MANUAL_BLUETOOTH_01
## TestCase Name
RDKV_CERT_MANUAL_BTRemote_Pair_FromStartupScreen

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a Bluetooth remote can be successfully paired with the DUT from the startup pairing screen immediately after a fresh firmware flash. This test confirms that all navigation key presses respond correctly and the selected application launches successfully, ensuring that startup remote pairing meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the DUT to an active network via Ethernet prior to the test. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 2 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 3 |  Conduct test in isolated environment  | Conduct the test in an isolated environment free of other VA/Bluetooth devices to prevent unintended Bluetooth interference. | The test environment should be free of Bluetooth interference from other devices.|
| 4 |  Flash DUT firmware  | Perform the test immediately after flashing the DUT firmware so that the "Pair your remote control" startup screen is presented on boot. | The DUT should be freshly flashed and ready to present the startup pairing screen on the next boot.|
| 5 |  Prepare universal remote  | Use a Universal Remote (Tatlow RDK — display name in RDK UI) as the primary remote for this test. If unavailable, any other supported Bluetooth remote may be used. Note: Key combinations for pairing and clearing pairing info are specific to the Tatlow RDK remote and may differ for other remote models. | The Bluetooth remote should be available and ready for pairing with the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Power on DUT after firmware flash  | Power on the DUT after completing the firmware flash. | The DUT should boot successfully, displaying the RDK splash screen followed by the "Pair your remote control" screen. A 30-second countdown timer should be displayed and repeat continuously.|
| 2 |  Clear remote pairing information  | Clear the existing pairing information from the remote by pressing and holding the CH UP and VOL DOWN keys simultaneously for a few seconds. | The red LED on the remote should blink once and stop, indicating that the pairing information has been successfully cleared from the remote.|
| 3 |  Put remote into pairing mode  | Put the remote into pairing mode by pressing and holding the OK and CH UP keys simultaneously for a few seconds. | The red LED on the remote should blink continuously, indicating that the remote has entered pairing mode.|
| 4 |  Wait for auto-pairing with DUT  | Wait for the DUT to detect and pair with the remote automatically. | The remote should pair automatically with the DUT. A confirmation message such as "Paired with Tatlow RDK remote" should be displayed on screen, and the RDK UI should automatically navigate to the Language selection screen.|
| 5 |  Navigate language selection screen  | Use the remote navigation keys to navigate the Language selection screen. Navigate to the "Continue Setup" button and press OK. | All navigation key presses and the OK button should function correctly. The RDK UI should advance to the Network selection screen.|
| 6 |  Skip network selection  | Navigate to the "Skip" button on the Network selection screen and press OK. | The RDK UI Home screen should launch successfully.|
| 7 |  Validate remote navigation on Home screen  | Perform navigation key presses on the RDK UI Home screen and attempt to open an application such as YouTube using the remote. | All navigation key presses should respond correctly and the selected application should launch successfully.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
