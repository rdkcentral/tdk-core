## TestCase ID
RDKV_MANUAL_BLUETOOTH_08
## TestCase Name
RDKV_CERT_MANUAL_BTRemote_Power_Press

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the POWER key press on the paired Bluetooth remote correctly toggles the DUT display state. This test confirms that the display turns on and the RDK UI Home screen launches successfully, ensuring Bluetooth remote power key functionality meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the DUT to an active network via Ethernet prior to the test. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 2 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 3 |  Ensure bluetooth remote already paired  | Ensure the Bluetooth remote is successfully paired with the DUT prior to the test. | The Bluetooth remote should be paired and functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Press power key to turn off  | Press the Power key on the remote. | The RDK UI should turn off (display/UI should enter standby state).|
| 2 |  Press power key to turn on  | Press the Power key again on the remote. | The RDK UI should turn on and the RDK UI Home screen should launch successfully.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
