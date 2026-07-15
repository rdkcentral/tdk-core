## TestCase ID
RDKV_MANUAL_BLUETOOTH_05
## TestCase Name
RDKV_CERT_MANUAL_BTRemote_Home_Press

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the HOME key press on the paired Bluetooth remote navigates back to the RDK UI Home screen. This test exercises the RDK Bluetooth pairing stack, the remote-control key-mapping service, and the RDK UI to validate remote-control button behaviour. The test confirms that the RDK UI Home screen should launch successfully.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the DUT to an active network via Ethernet prior to the test. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT. |
| 2 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 3 |  Ensure bluetooth remote already paired  | Ensure the Bluetooth remote is successfully paired with the DUT prior to the test. | The Bluetooth remote should be paired and functional on the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Open application via OK key  | On the RDK UI Home screen, use the remote navigation keys to navigate to any functional application or Settings button, then press OK. | The selected application or Settings screen should open successfully. |
| 2 |  Press HOME key  | Press the HOME key on the remote. | The RDK UI Home screen should launch successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
