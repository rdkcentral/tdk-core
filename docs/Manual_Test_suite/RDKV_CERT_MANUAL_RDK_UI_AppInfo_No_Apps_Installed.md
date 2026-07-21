## TestCase ID
RDKV_MANUAL_RDKUI_18
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_AppInfo_No_Apps_Installed

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the RDK UI App Info page behavior when no DAC apps are installed on the DUT. This test confirms that the appropriate message is displayed and the user is returned to the home screen, ensuring the no-apps-installed UI state meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Ensure no apps installed on DUT | Ensure no apps are installed on the DUT prior to this test (fresh flash or factory reset state). | The DUT should have no installed apps.|
| 2 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT | The DUT should come up with the RDK UI Home screen.|
| 2 | Navigate to App Info page | navigate to the left side of the RDK UI Home screen and click on the App Info button. Observe if there is error message displayed | Error message should be displayed which states 'No Apps installed'. The overlay windows should have 60% opacity, allowing partial transparency so that the underlying page<br>remains visible.|
| 3 | Press on the ok button in | Press on the OK button in the error overlay | The error message should close and return the user to user home screen|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
