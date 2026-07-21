## TestCase ID
RDKV_MANUAL_HDCP_COMP_02
## TestCase Name
RDKV_CERT_MANUAL_HDCP_Comp_Auth_Initiation_Verify

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that HDCP authentication is correctly initiated when the HDMI cable is reconnected to the DUT without any active A/V stream. This test confirms that the HDCP handshake completes and the authentication status is correctly reported in the system logs, ensuring HDCP content protection compliance meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display.|
| 2 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned.|
| 3 | Ensure no A/V stream is playing | Ensure that no A/V stream is playing on the DUT during the test. | No A/V stream should be active on the DUT.|
| 4 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT and enable DSMgr logs | Reboot the DUT and execute the following command in the DUT serial console or SSH terminal to enable DSMgr logs prior to the test.<br>Command: `journalctl -fu dsmgr &` | The DUT should reboot successfully and the RDK UI Home screen should be displayed.|
| 2 | Disconnect and reconnect HDMI cable | Once the DUT is up with the RDK UI, disconnect the HDMI cable from the DUT and then reconnect it. | The TV/display should not show the RDK UI while the HDMI cable is unplugged. The RDK UI should be restored on the display after reconnection.|
| 3 | Query HDCP status without A/V playback | Without initiating any A/V playback, execute the following curl command to query the HDCP status.<br>Command: `curl --data-binary '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.HdcpProfile.getHDCPStatus", "params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The response should indicate successful HDCP authentication.|
| 4 | Review DSMgr console logs | Review the device console logs for the expected log entries. | The following log entries should be present in the console logs: "Updated hotplug to CONNECTED" and "Updated hdcp_status to AUTHENTICATED"|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
