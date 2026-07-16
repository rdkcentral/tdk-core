## TestCase ID
RDKV_MANUAL_MIRACAST_01
## TestCase Name
RDKV_CERT_MANUAL_Miracast_Device_Connection_Verify

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a mobile device can successfully discover and connect to the DUT using Miracast. This test exercises the RDK Miracast Wi-Fi Display service, the P2P Wi-Fi connection stack, and the Miracast settings in the RDK UI to validate screen-mirroring connectivity. The test confirms that the mobile device should connect to the DUT successfully via Miracast.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Enable Miracast on DUT | Ensure that Miracast is enabled on the DUT. | Miracast should be enabled and functional on the DUT. |
| 3 | Enable Wi-Fi on both devices | Ensure that Wi-Fi is turned on on both the mobile device and the DUT. | Wi-Fi should be active on both the mobile device and the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Enable Miracast on mobile device | Enable Miracast on the mobile device. | Miracast should be enabled on the mobile device. |
| 2 | Search for Miracast devices from mobile | Search for Miracast-enabled devices from the mobile device. | The DUT should appear in the list of discoverable Miracast-enabled devices on the mobile device. |
| 3 | Select DUT from discovered devices list | Select the DUT from the discovered devices list. | The DUT should be selectable from the list. |
| 4 | Accept Miracast connection request | Accept the Miracast connection request on both the mobile device and the DUT. | The mobile device should connect to the DUT successfully via Miracast. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
