## TestCase ID
RDKV_MANUAL_HDCP_COMP_06
## TestCase Name
RDKV_CERT_MANUAL_HDCP_Comp_Version_Info_Verify

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT correctly reports the supported, receiver, and current HDCP versions via the HDCP Profile API. This test exercises the `org.rdk.HdcpProfile` plugin and the HDMI output manager to validate HDCP handshake and content-protection compliance on the connected display. The test confirms that the application should terminate gracefully and the RDK UI Home screen should be visible on the display.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned.|
| 3 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 4 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|
| 5 | Install required application | Navigate to the Recommended Apps row on the RDK UI Home screen (or the More Apps tab if the required application is not visible), select the required application tile, and press Enter/OK on the remote. Verify that a buffering/loading indicator appears on the tile, indicating that the app bundle download and installation has started. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The required application should be installed successfully on the DUT.|
| 6 | Verify app listed on home screen | Verify that the installed application is listed under the My Apps section/row and on the App Info page of the RDK UI Home screen, confirming it is ready to launch. | The installed application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 7 | Sign in to premium application | If the installed application is a premium application (such as YouTube or Amazon Prime), sign in with valid user credentials and verify A/V playback is functional prior to test execution. | Sign-in should succeed and A/V playback should be functional in the installed application.|
| 8 | Verify all apps launch correctly | Verify that all installed applications launch correctly from the RDK UI, and that any purchased content and premium features are accessible prior to test execution. | All installed applications should launch correctly and purchased content and premium features should be accessible.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT and enable DSMgr logs | Reboot the DUT and execute the following command in the DUT serial console or SSH terminal to enable DSMgr logs prior to the test.<br>Command: `journalctl -fu dsmgr &` | The DUT should reboot successfully and the RDK UI Home screen should be displayed.|
| 2 | Disconnect and reconnect HDMI cable | Once the DUT is up with the RDK UI, disconnect the HDMI cable from the DUT and then reconnect it. | The TV/display should not show the RDK UI while the HDMI cable is unplugged. The RDK UI should be restored on the display after reconnection.|
| 3 | Launch YouTube or Amazon Prime app | Select the YouTube or Amazon Prime application tile from the My Apps / Recommended Apps section of the RDK UI Home screen and press Enter/OK on the remote. | The selected application should launch successfully (cold launch or hot launch based on the app's previous state).|
| 4 | Initiate A/V stream playback | Immediately initiate A/V stream playback from the launched application. | The selected A/V stream should play with proper audio and video output.|
| 5 | Query HDCP version information via API | Immediately after initiating playback, execute the following curl command to query the HDCP status.<br>Command: `curl --data-binary '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.HdcpProfile.getHDCPStatus", "params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The `getHDCPStatus` API should return a successful response, and the supported HDCP version, receiver HDCP version, and current HDCP version should all be reported correctly in the response.|
| 6 | Exit the application | Exit the application by pressing the Back key on the remote. | The application should terminate gracefully and the RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
