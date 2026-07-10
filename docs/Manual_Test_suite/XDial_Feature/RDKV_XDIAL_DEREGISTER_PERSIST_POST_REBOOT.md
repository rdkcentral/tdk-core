## TestCase ID
RDKV_MANUAL_XDIAL_05
## TestCase Name
RDKV_CERT_MANUAL_XDIAL_DEREGISTER_PERSIST_POST_REBOOT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Dynamic XDial support is de-registered from the DUT after a device reboot when the XDial-supported application is not installed.

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
| 1 | Navigate to App Info page | If the YouTube application is available in the My Apps/Recommended Apps section/row, navigate to the App Info page using the App Info button on the left side of the RDK UI Home Page and press Enter/OK on the remote. | The RDK UI should open the dedicated App Info page, listing all DAC applications installed on the device. |
| 2 | Select YouTube and click Uninstall | Select the YouTube application icon on the App Info page and click Uninstall. | A confirmation dialog should appear, prompting the user to confirm the uninstallation. |
| 3 | Confirm uninstallation | Click the Yes button to confirm uninstallation. | A loading/buffering indicator should be displayed on the YouTube application tile. The application should subsequently be removed from the list on the App Info page. |
| 4 | Verify YouTube removed from home screen | Press the Home button on the remote and validate that YouTube has been removed from the My Apps row on the RDK UI Home Page. | The RDK UI Home Page should load and the YouTube tile should no longer be visible in the My Apps row. |
| 5 | Reboot DUT | Reboot the DUT and wait for the RDK UI Home Page to load completely. | The DUT should reboot successfully and the RDK UI Home Page should be displayed. |
| 6 | Launch the youtube application on the | Launch the YouTube application on the smartphone and tap the cast icon at the top of the screen. | The YouTube application should launch on the smartphone and a popup displaying the list of available cast devices should appear. |
| 7 | Validate that the dut is not | Validate that the DUT is not listed in the cast devices popup. | The DUT should not be listed in the cast devices popup. |
| 8 | Validate the rdk ui home page | Validate the RDK UI Home Page of the DUT for any unexpected behavior. | The RDK UI Home Page should remain idle without any unexpected behaviors. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
