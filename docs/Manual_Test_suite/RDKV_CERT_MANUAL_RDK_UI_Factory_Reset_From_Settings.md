## TestCase ID
RDKV_MANUAL_RDKUI_14
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Factory_Reset_From_Settings

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a Factory Reset can be performed from the RDK UI Settings and that all user settings and installed apps are restored to factory defaults after the reset. This test confirms that all previously configured settings revert to their default values and the device state is fully reset, ensuring the factory reset behavior meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 3 | Connect DUT to Wi-Fi | Connect the DUT to a Wi-Fi network with active internet access. | The DUT should be connected to Wi-Fi with active internet access.|
| 4 | Sign in to streaming apps | Ensure YouTube, Amazon Prime Video, and Netflix (whichever the platform supports) are signed in with valid user credentials. | All specified streaming applications should be signed in with valid user credentials.|
| 5 | Change display resolution and audio mode to non-default | Change the display resolution and audio output mode to non-default values. | The display resolution and audio output mode should be set to non-default values.|
| 6 | Configure multiple settings to non-default values | Configure the following settings to non-default values: Sleep Timer (15 min), Screen Saver (5 min), Energy Saver (Deep Sleep), Language (Spanish), Local Device Discovery (Off), USB Media Devices (Off), and CEC Control (Off). | All specified settings should be configured to the stated non-default values.|
| 7 | Install streaming apps if not present | If YouTube, Amazon Prime Video, or Netflix are not already available in the My Apps section, install them from the Recommended Apps row. | The specified streaming apps should be installed and available in the My Apps section.|
| 8 | Verify installed apps listed on home screen | Validate that the installed apps are listed under the My Apps section/row and App Info page of the RDK UI Home screen. | The installed apps should be visible in the My Apps section and on the App Info page, ready to launch.|
| 9 | Verify app launch and content access | Validate that the installed apps launch successfully from the RDK UI and that content is accessible. | All installed apps should launch correctly and content should be accessible.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Device settings screen | Navigate to Settings / Other Settings / Advanced Settings / Device screen | Screen should launch and it should have Factory Reset button|
| 2 | Click Factory Reset button | Click on Factory Reset | A Factory Reset confirmation dialog should appear.|
| 3 | Click Cancel in confirmation dialog | Click on Cancel | The confirmation dialog should close and the screen should return to Settings → Other Settings → Advanced Settings → Device.|
| 4 | Click Factory Reset button | Click on Factory Reset | A Factory Reset confirmation dialog should appear.|
| 5 | Click Confirm to proceed with reboot | Click on Confirm | A loading indicator should appear briefly and the DUT should reboot and come up with the RDK splash screen followed by the RDK UI initial setup/pairing screens.|
| 6 | Validate if the values changed are restored to default | Validate if the values changed in precondition(2 to 7 ) are restored to default | All of the values set to non default values prior to Factory reset, should be reverted to default values.<br>The YouTube, Prime Video and Netflix logins should be signed out.<br>Wifi connection should be lost<br>Bluetooth should not be in paired state<br>All installed Apps should be uninstalled or deleted and My Apps section itself could be removed from RDK UI Homepage|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
