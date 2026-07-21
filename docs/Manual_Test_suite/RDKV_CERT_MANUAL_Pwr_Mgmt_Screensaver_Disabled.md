## TestCase ID
RDKV_MANUAL_POWER_10
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Screensaver_Disabled

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the screen saver does not activate on the DUT when the Screen Saver option is set to Off in the RDK UI settings. This test confirms that the DUT UI remains on the RDK UI Home screen throughout the inactivity period without any screensaver activation, ensuring the screen saver disable behavior meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired with the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Ensure RDK UI is accessible | Ensure the RDK UI is visible and accessible on the DUT. | The RDK UI should be visible and accessible on the DUT.|
| 3 | Copy Screensaver.mp4 to DUT | Copy the Screensaver.mp4 file to the DUT at the location /home/root/lxresui/static/images. | The Screensaver.mp4 file should be available at the specified location on the DUT.|
| 4 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 5 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT. | The DUT should reboot and come up with the RDK UI displaying as expected.|
| 2 | Validate Screen Saver setting | In RDK UI, navigate to Settings → Other Settings and validate the Screen Saver value. | The Screen Saver value should be set to Off by default (unless previously changed).|
| 3 | Open Screen Saver timer options | Select the Screen Saver option. | The available time frame options should be listed: Off, 5 Minutes, 15 Minutes, 30 Minutes, and 60 Minutes.|
| 4 | Select Off screensaver option | Select the Off option and press the Home button. | The Off option should be selected and upon pressing the Home key, the RDK UI Home screen should launch.|
| 5 | Remain idle to activate screensaver | Remain idle on the RDK UI Home screen for 5 minutes without any key presses. | After 5 minutes of inactivity, the screen saver should not activate. The DUT UI should remain on the RDK UI Home screen.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
