## TestCase ID
RDKV_MANUAL_XDIAL_09
## TestCase Name
RDKV_CERT_MANUAL_XDIAL_DUAL_DEVICE_CAST

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the DUT behavior when two external devices (smartphones) simultaneously establish a YouTube XDial casting session to the same DUT.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and connect HDMI display | The DUT shall be powered on with a display connected to the correct HDMI input source. | The DUT should be powered on and the RDK UI should be visible on the TV/display. |
| 2 | Connect DUT and two smartphones to same network | The DUT and two external devices (smartphones) shall be connected to the same network. | The DUT and both smartphones should be on the same network and reachable from each other. |
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
| 1 | Verify YouTube app is installed | Validate that the YouTube application is installed and available in the My Apps/Recommended Apps section/row of the RDK UI Home Page. If not installed, install it as per the Apps Installation preconditions (Preconditions 4–7). | The YouTube application should be installed and its tile should be available. |
| 2 | Launch YouTube on both smartphones | Launch YouTube on both smartphones simultaneously and tap the cast icon at the top of each screen. | The DUT should be listed in the cast devices popup on both smartphones. |
| 3 | Connect Smartphone 1 to DUT | Select the DUT from Smartphone 1's cast devices popup. | Smartphone 1 should display "Connecting to <VA Device Name>" followed by "Connected to <VA Device Name>". The YouTube Home screen should load on the TV. A "New Device Connected" notification should appear in the top corner of YouTube on the TV. |
| 4 | Open cast options on Smartphone 1 | Tap the Cast icon again on Smartphone 1. | A popup should appear on Smartphone 1 with the DUT name, volume control, Voice Search, Remote, Close, and Disconnect options. |
| 5 | Select Remote option from popup | Select the Remote option from the popup on Smartphone 1. | A remote control screen should appear on Smartphone 1 with navigation and playback controls. |
| 6 | Select video and initiate playback | Select a video and press the OK (Play/Pause) button on Smartphone 1's remote control screen to initiate playback. | The selected video should start playing on the TV. |
| 7 | Connect Smartphone 2 to DUT | Select the DUT from Smartphone 2's cast devices popup. | Smartphone 2 should display "Connecting to <VA Device Name>" followed by "Connected to <VA Device Name>". The YouTube Home screen should also reflect the connected state on the TV. |
| 8 | Open cast options on Smartphone 2 | Tap the Cast icon again on Smartphone 2. | A popup should appear on Smartphone 2 with the DUT name, volume control, Voice Search, Remote, Close, and Disconnect options. |
| 9 | Select Remote option from popup | Select the Remote option from the popup on Smartphone 2. | A remote control screen should appear on Smartphone 2 with navigation and playback controls. |
| 10 | Verify dual-device cast and control | Validate that the same YouTube content is displayed on both smartphones and the TV (DUT), and attempt to control playback using Smartphone 2's remote control screen. | Both smartphones should display the same cast content simultaneously. Smartphone 2 should be able to perform remote navigation and playback operations on the YouTube interface displayed on the TV. |
| 11 | Close YouTube app via Back key | Close/exit the YouTube application by pressing the Back key on the remote. | The YouTube application should terminate gracefully. The RDK UI Home Page should be displayed on the TV, and the casting sessions on both smartphones should be closed. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
