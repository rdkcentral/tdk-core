## TestCase ID
RDKV_MANUAL_HDCPCOMPLIANCE_01
## TestCase Name
RDKV_CERT_MANUAL_HDCP_COMP_CABLE_HOTPLUG_VERIFY

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that HDMI cable disconnect and connect events are correctly detected and reported by the DUT via the HDCP Profile API and system logs.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned. |
| 3 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT and enable DSMgr logs | Reboot the DUT and execute the following command in the DUT serial console or SSH terminal to enable DSMgr logs prior to the test.<br>Command: `journalctl -fu dsmgr &` | The DUT should reboot successfully and the RDK UI Home screen should be displayed. |
| 2 | Disconnect HDMI cable from DUT | Once the DUT is up with the RDK UI, disconnect the HDMI cable from the DUT. | The TV/display should no longer show the RDK UI after the HDMI cable is disconnected. |
| 3 | Query HDCP status via API | Execute the following curl command in the DUT SSH terminal or serial console to query the HDCP status.<br>Command: `curl --data-binary '{"jsonrpc":"2.0", "id":3, "method":"org.rdk.HdcpProfile.getHDCPStatus", "params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The response should indicate HDMI disconnection. Expected response: {"jsonrpc":"2.0","id":3,"result":{"HDCPStatus":{"isConnected":false,"isHDCPCompliant":false,"isHDCPEnabled":false,"hdcpReason":0,"supportedHDCPVersion":"2.2","receiverHDCPVersion":"1.4","currentHDCPVersion":"1.4"},"success":true}} |
| 4 | Review DSMgr console logs | Review the device console logs for the expected log entries. | The following log entry should be present in the console logs: "Updated hotplug to DISCONNECTED" or "hdcpReason":0 |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
