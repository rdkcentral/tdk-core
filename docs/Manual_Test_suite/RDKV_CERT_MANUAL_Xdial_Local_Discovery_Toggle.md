## TestCase ID
RDKV_MANUAL_XDIAL_01
## TestCase Name
RDKV_CERT_MANUAL_Xdial_Local_Discovery_Toggle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the XDial feature can be disabled and re-enabled on the DUT using the Local Device Discovery setting in the RDK UI. This test confirms that the DUT is not discoverable when the setting is disabled and becomes discoverable again when re-enabled, ensuring XDial Local Device Discovery toggle behavior meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and connect HDMI display | The DUT shall be powered on with a display connected to the correct HDMI input source. | The DUT should be powered on and the RDK UI should be visible on the TV/display.|
| 2 | Connect DUT and two smartphones to same network | The DUT and the external device (smartphone) shall be connected to the same network. | The DUT and both smartphones should be on the same network and reachable from each other.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Privacy settings screen | Navigate to Settings > Other Settings > Privacy on the RDK UI. | The Privacy settings screen should be displayed with the following options: Local Device Discovery, USB Media Devices, Audio Input, Clear Cookies and App Data, Privacy Policy, and License.|
| 2 | Disable Local Device Discovery and verify | Disable the Local Device Discovery radio button on the Privacy settings screen. Then validate the DUT name visibility in the XDial casting option of the mobile YouTube application. | The Local Device Discovery radio button should be turned off. The DUT name should no longer be visible in the XDial casting device list of the mobile YouTube application.|
| 3 | Re-enable Local Device Discovery and verify | Re-enable the Local Device Discovery radio button on the Privacy settings screen. Then validate the DUT name visibility in the XDial casting option of the mobile YouTube application. | The Local Device Discovery radio button should be turned on. The DUT name should be visible in the XDial casting device list of the mobile YouTube application.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
