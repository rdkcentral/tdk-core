## TestCase ID
RDKV_MANUAL_HDMIHOTPLUG_01
## TestCase Name
RDKV_CERT_MANUAL_HDMI_Hotplug_UI_Restore_On_Reconnect_Home_Screen

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the RDK UI Home screen is correctly restored on the display after an HDMI cable reconnect. This test exercises the RDK HDMI hotplug detection service and display manager to validate display connection and disconnection event handling. The test confirms that upon HDMI reconnection, the TV/display should restore and correctly display the RDK UI Home screen without any manual intervention.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned.|
| 2 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 3 | Connect HDMI cable and select source | Connect the HDMI cable between the DUT and the TV/display, with the correct input source selected. | The HDMI cable should be connected and the correct input source should be selected on the TV/display.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT and verify home screen | Reboot the DUT and wait for it to fully boot up. | The DUT should boot up successfully and the RDK UI Home screen should be visible on the TV/display.|
| 2 | Disconnect and reconnect HDMI cable | Disconnect the HDMI cable from the DUT. Wait approximately 10 seconds, then reconnect the HDMI cable to the DUT. | Upon HDMI reconnection, the TV/display should restore and correctly display the RDK UI Home screen without any manual intervention.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
