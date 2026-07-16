## TestCase ID
RDKV_MANUAL_APPS_10
## TestCase Name
RDKV_CERT_MANUAL_App_Timezone_Display_Sync

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time displayed on the RDK UI Home screen accurately reflects the timezone configured in the device settings. This test exercises the DAC App Manager service, the RDK UI Home screen Recommended Apps / More Apps tiles, and the App Info page to manage application installation and launch. The test confirms that the Calcutta time zone time should be displayed in the top right corner of the RDK UI Home screen.

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
| 1 | Navigate to Settings | In RDK UI, navigate to Settings → Other Settings → Advanced Settings → Device → Time Zone. | The Time Zone screen should launch successfully.|
| 2 | Select timezone (Asia/Calcutta) | Select the Asia timezone, then select Calcutta (Kolkata), and press OK. | The Calcutta time zone should be set on the DUT and the updated time should be reflected in the top right corner of the RDK UI screen.|
| 3 | Press Home button and verify timezone | Press the Home button from the remote. | The Calcutta time zone time should be displayed in the top right corner of the RDK UI Home screen.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
