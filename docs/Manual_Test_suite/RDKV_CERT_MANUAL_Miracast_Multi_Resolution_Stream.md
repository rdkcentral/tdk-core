## TestCase ID
RDKV_MANUAL_MIRACAST_10
## TestCase Name
RDKV_CERT_MANUAL_Miracast_Multi_Resolution_Stream

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT can stream Miracast content correctly at different video resolutions including 720p, 1080p, and 4K. This test confirms that video streams correctly at each resolution without errors or quality degradation, ensuring Miracast multi-resolution streaming meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Enable Miracast on DUT | Ensure that Miracast is enabled on the DUT. | Miracast should be enabled and functional on the DUT.|
| 3 | Enable Wi-Fi on both devices | Ensure that Wi-Fi is enabled on both the smartphone and the DUT. | Wi-Fi should be active on both the smartphone and the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Enable Miracast on smartphone | Enable Miracast on the smartphone. | Miracast should be enabled on the smartphone.|
| 2 | Search for Miracast devices from smartphone | Search for Miracast-enabled devices from the smartphone. | The DUT should appear in the list of discoverable Miracast-enabled devices on the smartphone.|
| 3 | Select DUT from discovered devices list | Select the DUT from the discovered devices list. | The DUT should be selectable from the list.|
| 4 | Accept Miracast connection request | Accept the Miracast connection request on both the smartphone and the DUT. | The smartphone should connect to the DUT successfully via Miracast.|
| 5 | Initiate screen mirroring from smartphone | Initiate screen mirroring from the smartphone. | The smartphone screen should be visible on the DUT via the connected display.|
| 6 | Play video at different resolutions | Play video content on the smartphone at different resolutions (e.g., 720p, 1080p, 4K). | The video should stream correctly on the DUT at each resolution without errors or quality degradation.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
