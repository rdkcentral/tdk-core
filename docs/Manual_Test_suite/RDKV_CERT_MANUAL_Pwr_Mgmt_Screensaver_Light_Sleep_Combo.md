## TestCase ID
RDKV_MANUAL_POWER_12
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Screensaver_Light_Sleep_Combo

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the DUT behavior when both the Screen Saver and Light Sleep inactivity timers are configured concurrently via the RDK UI settings. This test confirms that the screen saver activates first followed by the DUT entering Light Sleep, and that the RDK UI resumes correctly after wake-up, ensuring the combined screensaver and Light Sleep timer behavior meets certification requirements.

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
| 1 | Navigate to Energy Saver settings | In RDK UI, navigate to Settings → Other Settings → Energy Saver. | The Energy Saver screen should load successfully and display two options: Deep Sleep and Light Sleep.|
| 2 | Validate and select Light Sleep mode | Validate that the Light Sleep option is selected (indicated by a tick mark). If not, select Light Sleep. | Light Sleep should be the default sleep mode after a fresh flash. A tick mark should appear next to the Light Sleep option upon selection.|
| 3 | Navigate to Sleep Timer settings | In RDK UI, navigate to Settings → Other Settings → Sleep Timer. | The Sleep Timer screen should load and display the available time frame options: OFF, 15 Minutes, 30 Minutes, 45 Minutes, and 1 Hour.|
| 4 | Select 15 Minutes sleep timer | Select the 15 Minutes radio button and press the Back button. | The 15 Minutes option should be selected and the Settings → Other Settings screen should launch.|
| 5 | Validate Screen Saver setting | Validate the Screen Saver value in Settings → Other Settings. | The Screen Saver value should be set to Off by default (unless previously changed).|
| 6 | Open Screen Saver timer options | Select the Screen Saver option. | The available time frame options should be listed: Off, 5 Minutes, 15 Minutes, 30 Minutes, and 60 Minutes.|
| 7 | Select 5 Minutes screensaver timer | Select the 5 Minutes time frame and press the Home button. | The 5 Minutes option should be selected and upon pressing the Home key, the RDK UI Home screen should launch.|
| 8 | Remain idle to trigger screensaver and sleep | Remain idle on the RDK UI Home screen for 15 minutes without any key presses or actions. | After 5 minutes of inactivity, the screen saver should start playing. 10 minutes after the screen saver starts (i.e., at the 15-minute mark), the DUT should enter Light Sleep mode. The RDK UI should turn off.|
| 9 | Wake DUT via Power key on remote | Press the Power key on the Bluetooth-paired remote to wake up the DUT from Light Sleep mode. | The DUT should wake up from Light Sleep mode. The RDK UI should come up again. The DUT should be accessible via SSH and internet should be accessible.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
