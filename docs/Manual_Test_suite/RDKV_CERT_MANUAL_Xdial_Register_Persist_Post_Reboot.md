## TestCase ID
RDKV_MANUAL_XDIAL_04
## TestCase Name
RDKV_CERT_MANUAL_Xdial_Register_Persist_Post_Reboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Dynamic XDial support registration persists on the DUT after a device reboot when an XDial-supported application is already installed. This test exercises the `org.rdk.DialServer` plugin, the DIAL protocol handler, and the application launch bridge to validate the targeted X-DIAL application discovery or launch scenario. The test confirms that the YouTube application should terminate gracefully. The RDK UI Home Page should be displayed on the TV, and the casting session on the smartphone should be closed.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and connect HDMI display | The DUT shall be powered on with a display connected to the correct HDMI input source. | The DUT should be powered on and the RDK UI should be visible on the TV/display. |
| 2 | Connect DUT and two smartphones to same network | The DUT and the external device (smartphone) shall be connected to the same network. | The DUT and both smartphones should be on the same network and reachable from each other. |
| 3 | Enable Local Device Discovery | Local Device Discovery shall be enabled in Settings > Other Settings > Privacy on the RDK UI. | Local Device Discovery should be enabled in Settings > Other Settings > Privacy on the RDK UI. |
| 4 | Install YouTube application | Select the YouTube tile on the Recommended Apps row (or navigate to the More Apps tab if not visible) and press Enter/OK on the remote. A loading/buffering indicator should appear on the tile, followed by a green tick icon upon successful installation. | The YouTube application should be installed successfully on the DUT. |
| 5 | Verify YouTube app listed on home screen | Validate that the installed YouTube application is listed under the My Apps section/row and App Info page of the RDK UI Home Page, ready to launch. | The YouTube application should be visible in the My Apps section and on the App Info page, ready to launch. |
| 6 | Sign in to YouTube and verify A/V playback | Since YouTube is a premium application, sign in with valid user credentials and validate AV playback prior to test execution. | Sign-in should succeed and A/V playback should be functional in the YouTube application. |
| 7 | Verify YouTube launch and premium features | Validate that YouTube launches from the RDK UI and that purchased contents and premium features are accessible. | The YouTube application should launch correctly from the RDK UI and purchased content and premium features should be accessible. |
| 8 | Pair Bluetooth remote | The Bluetooth remote shall be paired and connected to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify YouTube app is installed | Validate that the YouTube application is installed and available in the My Apps/Recommended Apps section/row of the RDK UI Home Page. If not installed, install it as per the Apps Installation preconditions (Preconditions 4–7). | The YouTube application should be installed and its tile should be available in the My Apps/Recommended Apps section/row. |
| 2 | Reboot DUT | Reboot the DUT and wait for the RDK UI Home Page to load completely. | The DUT should reboot successfully and the RDK UI Home Page should be displayed. |
| 3 | Launch the youtube application on the | Launch the YouTube application on the smartphone and tap the cast icon at the top of the screen. | The YouTube application should launch on the smartphone and a popup displaying the list of available cast devices should appear. |
| 4 | Validate that the dut is listed | Validate that the DUT is listed in the cast devices popup. | The DUT should be listed in the cast devices popup along with other available devices. |
| 5 | Select DUT from cast devices popup | Select the DUT from the cast devices popup. | The smartphone should display "Connecting to <VA Device Name>" followed by "Connected to <VA Device Name>". The YouTube Home screen should load on the TV. A "New Device Connected" notification should appear in the top corner of YouTube on the TV. |
| 6 | Close YouTube app via Back key | Close/exit the YouTube application by pressing the Back key on the remote. | The YouTube application should terminate gracefully. The RDK UI Home Page should be displayed on the TV, and the casting session on the smartphone should be closed. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
