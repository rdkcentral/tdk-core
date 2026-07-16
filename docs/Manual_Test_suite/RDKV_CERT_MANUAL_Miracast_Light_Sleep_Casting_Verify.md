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
To validate that the Miracast screen casting session is not lost when the DUT enters and exits Light Sleep mode during an active casting session. This test exercises the RDK Miracast Wi-Fi Display service, the P2P Wi-Fi connection stack, and the Miracast settings in the RDK UI to validate screen-mirroring connectivity. The test confirms that the DUT should wake up successfully and the Miracast screen casting session should resume without any interruption or loss.

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
| 5 | Initiate screen mirroring from mobile | Initiate screen mirroring from the mobile device. | The mobile device screen should be visible on the DUT via the connected display. |
| 6 | Play video content and verify mirroring on DUT | Play any video content on the mobile device. | The video should stream correctly on the DUT without errors. |
| 7 | Put DUT into Light Sleep mode | Put the DUT into Light Sleep mode. | The DUT display should turn off as it enters Light Sleep mode. |
| 8 | Wake DUT from Light Sleep mode | Wake the DUT from Light Sleep mode. | The DUT should wake up successfully and the Miracast screen casting session should resume without any interruption or loss. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
