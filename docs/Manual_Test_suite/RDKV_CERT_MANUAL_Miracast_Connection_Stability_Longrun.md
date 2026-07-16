## TestCase ID
RDKV_MANUAL_MIRACAST_07
## TestCase Name
RDKV_CERT_MANUAL_Miracast_Connection_Stability_Longrun

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Miracast connection between the smartphone and the DUT remains stable and without interruption over an extended period of time. This test exercises the RDK Miracast Wi-Fi Display service, the P2P Wi-Fi connection stack, and the Miracast settings in the RDK UI to validate screen-mirroring connectivity. The test confirms that the Miracast connection should remain stable throughout the duration without any disconnections or significant lag.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Enable Miracast on DUT | Ensure that Miracast is enabled on the DUT. | Miracast should be enabled and functional on the DUT.|
| 3 | Enable Wi-Fi on both devices | Ensure that Wi-Fi is turned on on both the smart phone and the DUT. | Wi-Fi should be active on both the smart phone and the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Enable Miracast on smart phone | Enable Miracast on the smart phone device. | Miracast should be enabled on the smart phone.|
| 2 | Search for Miracast devices from smart phone | Search for Miracast-enabled devices from the smart phone. | The DUT should appear in the list of discoverable Miracast-enabled devices on the smart phone.|
| 3 | Select DUT from discovered devices list | Select the DUT from the discovered devices list. | The DUT should be selectable from the list.|
| 4 | Accept Miracast connection request | Accept the Miracast connection request on both the smart phone and the DUT. | The smart phone should connect to the DUT successfully via Miracast.|
| 5 | Initiate screen mirroring from smart phone | Initiate screen mirroring from the smart phone. | The smart phone screen should be visible on the DUT via the connected display.|
| 6 | Maintain connection for extended period | Keep the Miracast connection active for an extended period (e.g., 1 hour). | The Miracast connection should remain stable throughout the duration without any disconnections or significant lag.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
