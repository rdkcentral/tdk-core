## TestCase ID
RDKV_MANUAL_XDIAL_23
## TestCase Name
RDKV_CERT_MANUAL_Xdial_Wakeup_From_Network_Standby

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an XDial cast request from a secondary device successfully wakes the DUT from Network Standby mode and initiates content playback on the DUT. This test confirms that the DUT wakes up and content playback begins in response to the cast request, ensuring XDial-triggered wakeup from Network Standby meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Ensure DUT in Network Standby | The DUT shall be in Network Standby mode prior to test execution. | The DUT should be in Network Standby mode prior to test execution.|
| 2 | Connect DUT and two smartphones to same network | The DUT and the secondary device (smartphone/iPad) shall be connected to the same network. | The DUT and both smartphones should be on the same network and reachable from each other.|
| 3 | Ensure DUT in Network Standby | Local Device Discovery shall be enabled in Settings > Other Settings > Privacy on the RDK UI (configured prior to the DUT entering Network Standby). | The DUT should be in Network Standby mode prior to test execution.|
| 4 | Install YouTube application | Select the YouTube tile on the Recommended Apps row (or navigate to the More Apps tab if not visible) and press Enter/OK on the remote. A loading/buffering indicator should appear on the tile, followed by a green tick icon upon successful installation. | The YouTube application should be installed successfully on the DUT.|
| 5 | Verify YouTube app listed on home screen | Validate that the installed YouTube application is listed under the My Apps section/row and App Info page of the RDK UI Home Page, ready to launch. | The YouTube application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 6 | Sign in to YouTube and verify A/V playback | Sign in to YouTube with valid user credentials and validate AV playback prior to test execution. | Sign-in should succeed and A/V playback should be functional in the YouTube application.|
| 7 | Verify YouTube launch and premium features | Validate that YouTube launches from the RDK UI and that purchased contents and premium features are accessible. | The YouTube application should launch correctly from the RDK UI and purchased content and premium features should be accessible.|
| 8 | Pair Bluetooth remote | The Bluetooth remote shall be paired and connected to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify YouTube app is installed | Validate that the YouTube application is installed and available in the My Apps/Recommended Apps section/row of the RDK UI Home Page. This validation should be performed before the DUT enters Network Standby mode. If not installed, install it as per the Apps Installation preconditions (Preconditions 4–7) before entering standby. | The YouTube application should be installed and its tile should be available.|
| 2 | Launch YouTube or Netflix on secondary device | Launch the YouTube or Netflix application on the secondary device (smartphone/iPad). | The YouTube or Netflix application should launch successfully on the secondary device.|
| 3 | Play content on secondary device | Play any video, movie, or series on the secondary device. | The selected content should start playing on the secondary device.|
| 4 | Cast from secondary device and wake DUT | Tap the cast icon on the secondary device and select the DUT from the cast devices list. | The DUT should wake up from Network Standby mode and launch the appropriate application (YouTube or Netflix). The content selected on the secondary device should start playing on the TV via XDial.|
| 5 | Close YouTube app via Back key | Close/exit the YouTube application by pressing the Back key on the remote. | The YouTube application should terminate gracefully. The RDK UI Home Page should be displayed on the TV, and the casting session should be closed.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
