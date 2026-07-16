## TestCase ID
RDKV_MANUAL_XDIAL_18
## TestCase Name
RDKV_CERT_MANUAL_Xdial_Cast_Yt_Shorts_Playback

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the behavior when a YouTube Short is selected from the TV during an active XDial casting session, and that the Short plays correctly after the casting session is disconnected. This test exercises the `org.rdk.DialServer` plugin, the DIAL protocol handler, and the application launch bridge to validate the targeted X-DIAL application discovery or launch scenario. The test confirms that the YouTube application should terminate gracefully. The RDK UI Home Page should be displayed on the TV, and the casting session should be closed.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and connect HDMI display | The DUT shall be powered on with a display connected to the correct HDMI input source. | The DUT should be powered on and the RDK UI should be visible on the TV/display.|
| 2 | Connect DUT and two smartphones to same network | The DUT and the external device (smartphone) shall be connected to the same network. | The DUT and both smartphones should be on the same network and reachable from each other.|
| 3 | Terminate any previous XDial session | Any previous XDial casting session shall be properly terminated using the Disconnect option prior to this test execution. | Any previous XDial casting session should be properly terminated.|
| 4 | Enable Local Device Discovery | Local Device Discovery shall be enabled in Settings > Other Settings > Privacy on the RDK UI. | Local Device Discovery should be enabled in Settings > Other Settings > Privacy on the RDK UI.|
| 5 | Install YouTube application | Select the YouTube tile on the Recommended Apps row (or navigate to the More Apps tab if not visible) and press Enter/OK on the remote. A loading/buffering indicator should appear on the tile, followed by a green tick icon upon successful installation. | The YouTube application should be installed successfully on the DUT.|
| 6 | Verify YouTube app listed on home screen | Validate that the installed YouTube application is listed under the My Apps section/row and App Info page of the RDK UI Home Page, ready to launch. | The YouTube application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 7 | Sign in to YouTube and verify A/V playback | Since YouTube is a premium application, sign in with valid user credentials and validate AV playback prior to test execution. | Sign-in should succeed and A/V playback should be functional in the YouTube application.|
| 8 | Verify YouTube launch and premium features | Validate that YouTube launches from the RDK UI and that purchased contents and premium features are accessible. | The YouTube application should launch correctly from the RDK UI and purchased content and premium features should be accessible.|
| 9 | Pair Bluetooth remote | The Bluetooth remote shall be paired and connected to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify YouTube app is installed | Validate that the YouTube application is installed and available in the My Apps/Recommended Apps section/row of the RDK UI Home Page. If not installed, install it as per the Apps Installation preconditions (Preconditions 5–8). | The YouTube application should be installed and its tile should be available.|
| 2 | Launch YouTube on smartphone and tap cast icon | Launch YouTube on the smartphone and tap the cast icon at the top of the screen. | The DUT should be listed in the cast devices popup along with other available devices.|
| 3 | Select DUT from cast devices popup | Select the DUT from the cast devices popup. | The smartphone should display "Connecting to <VA Device Name>" followed by "Connected to <VA Device Name>". The YouTube Home screen should load on the TV with a "New Device Connected" notification.|
| 4 | Tap Cast icon on smartphone for options | Tap the Cast icon again on the smartphone. | A popup should appear with the DUT name, volume control, Voice Search option, Remote option, and Close/Disconnect options.|
| 5 | Navigate to YouTube Shorts and select | Navigate to YouTube Shorts on the TV and select any Short to play. | A popup should appear on the TV with the message: "Disconnect Device to watch this Short".|
| 6 | Disconnect and play YouTube Short | Press the Disconnect button on the popup. | The YouTube Short should start playing on the TV. The XDial casting session should be terminated and playback should resume on the smartphone independently.|
| 7 | Close YouTube app via Back key | Close/exit the YouTube application by pressing the Back key on the remote. | The YouTube application should terminate gracefully. The RDK UI Home Page should be displayed on the TV, and the casting session should be closed.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
