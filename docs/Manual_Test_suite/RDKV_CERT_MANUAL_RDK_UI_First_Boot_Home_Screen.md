## TestCase ID
RDKV_MANUAL_RDKUI_16
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_First_Boot_Home_Screen

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that on the very first boot, the RDK UI Home screen displays only the Recommended Apps and Video on Demand rows with no My Apps row, since no apps are installed. This test confirms that the initial home screen layout is correctly rendered without the My Apps section, ensuring the first-boot home screen display meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Ensure no apps installed on DUT | Ensure no apps are installed on the DUT prior to this test (fresh flash or factory reset state). | The DUT should have no installed apps.|
| 2 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT after flashing | The DUT should come up with the First Time Installation (FTI) screen.|
| 2 | Complete or skip FTI setup screens | Either Put remote in pairing mode and pair the remote, select language and select network interface<br>OR<br>Skip the FTI screens | The RDK UI Home screen should launch with or without pairing the remote|
| 3 | Observe and validate RDK UI Home screen layout | Observe the RDK UI Home screen page | The UI should have only two rows. The top row should display Recommended Apps, while the<br>bottom row should display Video on Demand (VoD) apps. My Apps row should be hidden as there are no DAC apps<br>installed yet.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
