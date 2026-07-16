## TestCase ID
RDKV_MANUAL_POWER_09
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Screensaver_On_Inactivity

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the screen saver activates on the DUT after the configured period of user inactivity. This test exercises the `org.rdk.PowerManager` plugin and the RDK power-state machine (including standby, deep-sleep, and wake triggers) to validate power-mode transitions. The test confirms that the screen saver should stop and the RDK UI Home screen should launch.

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
| 1 | Reboot the DUT | Reboot the DUT using reboot command. | The DUT should reboot and come up with the RDK UI displaying as expected.|
| 2 | Validate Screen Saver setting | In RDK UI, navigate to Settings → Other Settings and validate the Screen Saver value. | The Screen Saver value should be set to Off by default (unless previously changed).|
| 3 | Open Screen Saver timer options | Select the Screen Saver option. | The available time frame options should be listed: Off, 5 Minutes, 15 Minutes, 30 Minutes, and 60 Minutes.|
| 4 | Select 5 Minutes screensaver timer | Select the 5 Minutes time frame and press the Home button. | The 5 Minutes option should be selected and upon pressing the Home key, the RDK UI Home screen should launch.|
| 5 | Remain idle to activate screensaver | Remain idle on the RDK UI Home screen for 5 minutes without any key presses. | After 5 minutes of inactivity, the screen saver should start playing.|
| 6 | Press any key to dismiss screensaver | Press any key on the remote. | The screen saver should stop and the RDK UI Home screen should launch.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
