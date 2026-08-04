## TestCase ID
RDKV_MANUAL_XDIAL_13
## TestCase Name
RDKV_CERT_MANUAL_Xdial_Cast_Reconnect_Same_Device

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an XDial casting session can be successfully re-established using the same smartphone after a previous casting session has been properly disconnected. This test confirms that the re-established session initiates video playback correctly on the DUT, ensuring XDial re-connection from the same device meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and connect HDMI display | The DUT shall be powered on with a display connected to the correct HDMI input source. | The DUT should be powered on and the RDK UI should be visible on the TV/display.|
| 2 | Connect DUT and two smartphones to same network | The DUT and the external device (smartphone) shall be connected to the same network. | The DUT and both smartphones should be on the same network and reachable from each other.|
| 3 | Enable Local Device Discovery | Local Device Discovery shall be enabled in Settings > Other Settings > Privacy on the RDK UI. | Local Device Discovery should be enabled in Settings > Other Settings > Privacy on the RDK UI.|
| 4 | Install YouTube application | Select the YouTube tile on the Recommended Apps row (or navigate to the More Apps tab if not visible) and press Enter/OK on the remote. A loading/buffering indicator should appear on the tile, followed by a green tick icon upon successful installation. | The YouTube application should be installed successfully on the DUT.|
| 5 | Verify YouTube app listed on home screen | Validate that the installed YouTube application is listed under the My Apps section/row and App Info page of the RDK UI Home Page, ready to launch. | The YouTube application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 6 | Sign in to YouTube and verify A/V playback | Since YouTube is a premium application, sign in with valid user credentials and validate AV playback prior to test execution. | Sign-in should succeed and A/V playback should be functional in the YouTube application.|
| 7 | Verify YouTube launch and premium features | Validate that YouTube launches from the RDK UI and that purchased contents and premium features are accessible. | The YouTube application should launch correctly from the RDK UI and purchased content and premium features should be accessible.|
| 8 | Pair Bluetooth remote | The Bluetooth remote shall be paired and connected to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify YouTube app is installed | Validate that the YouTube application is installed and available in the My Apps/Recommended Apps section/row of the RDK UI Home Page. If not installed, install it as per the Apps Installation preconditions (Preconditions 4–7). | The YouTube application should be installed and its tile should be available.|
| 2 | Launch YouTube on smartphone and tap cast icon | Launch YouTube on the smartphone and tap the cast icon at the top of the screen. | The DUT should be listed in the cast devices popup along with other available devices.|
| 3 | Select DUT from cast devices popup | Select the DUT from the cast devices popup. | The smartphone should display "Connecting to <VA Device Name>" followed by "Connected to <VA Device Name>". The YouTube Home screen should load on the TV with a "New Device Connected" notification.|
| 4 | Tap Cast icon on smartphone for options | Tap the Cast icon again on the smartphone. | A popup should appear with the DUT name, volume control, Voice Search option, Remote option, and Close/Disconnect options.|
| 5 | Select Remote option from popup | Select the Remote option from the popup. | A remote control screen should appear with navigation and playback controls.|
| 6 | Select video and initiate playback | Select a video and press the OK (Play/Pause) button to initiate playback. | The selected video should start playing on the TV.|
| 7 | Tap Cast icon on smartphone for options | Close the remote popup and tap the Cast icon again on the smartphone. | A popup should appear again with the DUT name, volume control, Voice Search option, Remote option, and Close/Disconnect options.|
| 8 | Disconnect casting session | Press the Disconnect option in the popup. | A "Device Disconnected" notification should be displayed on the TV. The YouTube Home screen on the TV should exit to a user list screen.|
| 9 | Select DUT from cast devices popup | Using the same smartphone, re-launch YouTube, tap the cast icon, and select the DUT from the cast devices popup again. | The casting session should be re-established successfully with the same smartphone. The selected video content on the smartphone should start playing on the TV.|
| 10 | Close YouTube app via Back key | Close/exit the YouTube application by pressing the Back key on the remote. | The YouTube application should terminate gracefully. The RDK UI Home Page should be displayed on the TV, and the casting session should be closed.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
