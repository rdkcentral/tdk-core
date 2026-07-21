## TestCase ID
RDKV_MANUAL_APPS_09
## TestCase Name
RDKV_CERT_MANUAL_App_Home_Screen_Focus_Left_Pane

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the RDK UI Home screen focus is correctly restored when the Home icon in the left pane is selected on the DUT. This test confirms that focus navigates to the last accessed section of the Home screen, ensuring that pane-based navigation behaves correctly for certification.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and ensure RDK UI is accessible | Ensure the DUT is powered on and the RDK UI is visible and accessible on the display. | The DUT should be powered on and the RDK UI should be visible and accessible on the display.|
| 2 | Pair Bluetooth remote | Ensure a Bluetooth-paired remote control is available and functional for DUT navigation. | The Bluetooth remote should be paired and functional for DUT navigation.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Home icon in left panel | Navigate to the left panel of the RDK UI Home screen, select the Home icon (first icon in the left pane), and press OK. | The focus should move to the last accessed section in the RDK UI Home screen.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
