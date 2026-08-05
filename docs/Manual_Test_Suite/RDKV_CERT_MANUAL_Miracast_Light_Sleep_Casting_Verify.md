## TestCase ID
RDKV_MANUAL_MIRACAST_12
## TestCase Name
RDKV_CERT_MANUAL_Miracast_Light_Sleep_Casting_Verify

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an active Miracast casting session is preserved when the DUT enters and exits Light Sleep mode. This test confirms that the DUT wakes up successfully and Miracast screen mirroring resumes without interruption or loss, ensuring Miracast resilience across power state transitions meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Connect DUT to Application Catalog | Navigate to the Settings screen on the RDK UI and connect the DUT to the Application Catalog if it is not already connected. | The DUT should be connected to the Application Catalog successfully. |
| 3 | Enable Miracast on DUT | Ensure that Miracast is enabled on the DUT. | Miracast should be enabled and functional on the DUT.|
| 4 | Enable Wi-Fi on both devices | Ensure that Wi-Fi is enabled on both the smartphone and the DUT. | Wi-Fi should be active on both the smartphone and the DUT.|
| 5 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 6 | Configure Energy Saver for Light Sleep | Ensure the Energy Saver toggle is set to OFF from Settings > Other Settings > Energy Saver. | The Energy Saver toggle should be set to OFF, activating Light Sleep mode.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Enable Miracast on smartphone | Enable Miracast on the smartphone. | Miracast should be enabled on the smartphone.|
| 2 | Search for Miracast devices from smartphone | Search for Miracast-enabled devices from the smartphone. | The DUT should appear in the list of discoverable Miracast-enabled devices on the smartphone.|
| 3 | Select DUT from discovered devices list | Select the DUT from the discovered devices list. | The DUT should be selectable from the list.|
| 4 | Accept Miracast connection request | Accept the Miracast connection request on both the smartphone and the DUT. | The smartphone should connect to the DUT successfully via Miracast.|
| 5 | Initiate screen mirroring from smartphone | Initiate screen mirroring from the smartphone. | The smartphone screen should be visible on the DUT via the connected display.|
| 6 | Play video content and verify mirroring on DUT | Play any video content on the smartphone. | The video should stream correctly on the DUT without errors.|
| 7 | Put DUT into Light Sleep mode | Press the Power key on the Bluetooth-paired remote to put the DUT into Light Sleep mode. | The DUT display should turn off as it enters Light Sleep mode.|
| 8 | Wake DUT from Light Sleep mode | Press the Power key on the Bluetooth-paired remote to wake the DUT from Light Sleep mode. | The DUT should wake up successfully and the Miracast screen casting session should resume without any interruption or loss.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
