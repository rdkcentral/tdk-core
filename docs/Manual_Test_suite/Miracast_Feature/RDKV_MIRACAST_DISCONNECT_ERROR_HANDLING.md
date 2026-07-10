## TestCase ID
RDKV_MANUAL_MIRACAST_09
## TestCase Name
RDKV_CERT_MANUAL_MIRACAST_DISCONNECT_ERROR_HANDLING

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT handles Miracast session errors and disconnections gracefully, including Wi-Fi disruption and re-connection after casting termination.

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
| 6 | Disconnect Wi-Fi on mobile device | Disconnect the Wi-Fi SSID on the mobile device. | The Miracast session should not be terminated. |
| 7 | Reconnect Wi-Fi on mobile device | Reconnect to the Wi-Fi SSID on the mobile device. | The Miracast session should not be terminated. |
| 8 | Stop casting session from mobile | Stop the casting session from the mobile device. | The Miracast connection should terminate and the DUT should return to its default state (RDK UI Home screen). |
| 9 | Repeat steps with other devices/conditions | Re-initiate Miracast from the same mobile device (repeat Steps 2–5). | The Miracast connection should be re-established successfully and screen mirroring should resume. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
