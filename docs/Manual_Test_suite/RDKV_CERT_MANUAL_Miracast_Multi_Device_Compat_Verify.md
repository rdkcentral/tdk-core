## TestCase ID
RDKV_MANUAL_MIRACAST_08
## TestCase Name
RDKV_CERT_MANUAL_Miracast_Multi_Device_Compat_Verify

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Miracast compatibility with different smartphones and operating systems including Android and iOS. This test confirms that screen casting is established successfully with each device type and results are consistent across all tested platforms, ensuring Miracast multi-device compatibility meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Enable Miracast on DUT | Ensure that Miracast is enabled on the DUT. | Miracast should be enabled and functional on the DUT.|
| 3 | Enable Wi-Fi on both devices | Ensure that Wi-Fi is enabled on both the smartphone and the DUT. | Wi-Fi should be active on both the smartphone and the DUT.|
| 4 | Connect smartphone to Wi-Fi SSID | Connect the smartphone to a Wi-Fi SSID prior to the test. | The smartphone should be connected to a Wi-Fi SSID with a valid IP address assigned.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Enable Miracast on smartphone | Enable Miracast on the smartphone. | Miracast should be enabled on the smartphone.|
| 2 | Search for Miracast devices from smartphone | Search for Miracast-enabled devices from the smartphone. | The DUT should appear in the list of discoverable Miracast-enabled devices on the smartphone.|
| 3 | Select DUT from discovered devices list | Select the DUT from the discovered devices list. | The DUT should be selectable from the list.|
| 4 | Accept Miracast connection request | Accept the Miracast connection request on both the smartphone and the DUT. | The smartphone should connect to the DUT successfully via Miracast.|
| 5 | Initiate screen mirroring from smartphone | Initiate screen mirroring from the smartphone. | The smartphone screen should be visible on the DUT via the connected display.|
| 6 | Repeat steps with other devices/conditions | Repeat Steps 1–5 with other smartphones (Android and iOS). | Miracast screen casting should establish successfully with each different smartphone. The results for Steps 1–5 should be consistent across all tested device types.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
