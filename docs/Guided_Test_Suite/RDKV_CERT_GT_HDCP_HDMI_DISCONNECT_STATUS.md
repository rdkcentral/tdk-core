## TestCase ID
TC_HDCPCOMPLIANCE_MANUAL_01
## TestCase Name
RDKV_HDCP_HDMI_DISCONNECT_STATUS_GT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the HDMI disconnection is correctly detected by the DUT, reflected in the HdcpProfile status, and logged in the device logs.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 2 | Verify active HDMI connection | Execute the DisplaySettings API to verify an active HDMI connection is present on the DUT.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":3,"method":"org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The API should return `connectedVideoDisplays=HDMI0`, confirming an active HDMI connection is present. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Manually disconnect HDMI cable | A visual alert blinks on the screen: *"PLEASE DISCONNECT HDMI CABLE FROM DUT TO PROCEED TEST!!!"* — physically disconnect the HDMI cable from the DUT. The script then prompts: *"Is HDMI cable disconnected from DUT and RDK UI not showing on TV [yes/no]:"* — respond `yes` once the HDMI cable is disconnected and the TV shows no signal. | The HDMI cable should be disconnected from the DUT and no RDK UI signal should be visible on the TV display. |
| 2 | Verify HDMI disconnected via getHDCPStatus | Execute the curl command to verify the HDMI connection status via the HdcpProfile API.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":3,"method":"org.rdk.HdcpProfile.getHDCPStatus","params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The API response should return `isConnected=false` and `success=true`, confirming the DUT has detected the HDMI disconnection. |
| 3 | Verify disconnect log and HDCP reason | Execute the command to check the device log file for the HDMI disconnect event and verify the HDCP reason code.<br>Command: `tail -n 500 $hdcp_logs_path \| grep -F -i -o "Updated hotplug to DISCONNECTED" \| tail -n 1` | The log file should contain the entry `"Updated hotplug to DISCONNECTED"` and the getHDCPStatus API should return `hdcpReason=0`, confirming the HDMI hotplug disconnection was correctly logged and processed. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
