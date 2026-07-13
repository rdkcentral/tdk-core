## TestCase ID
RDKV_MANUAL_HDCP_COMP_02
## TestCase Name
RDKV_CERT_GT_HDCP_AUTH_INITIATED_STATUS

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that HDCP authentication initiation is correctly triggered and logged by the DUT after an HDMI hotplug event, as tested by the `HDCP_COMPLIANCE_AUTOMATED.sh` script. The test exercises the `org.rdk.HdcpProfile.getHDCPStatus` API to verify `isHDCPInitiated=true` following the hotplug, and checks the device log at `<hdcp_logs_path>` for the expected authentication initiation entries. This test confirms that the HDCP subsystem on the DUT correctly begins the authentication handshake upon HDMI connection and records the event appropriately in the system logs.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Ensure the test script (`HDCP_COMPLIANCE_AUTOMATED.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) are present in the working directory of the DUT before executing the test. The `device.conf` file must be configured with the correct values required for this specific test prior to execution. | The files `HDCP_COMPLIANCE_AUTOMATED.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 3 | Verify active HDMI connection | Execute the DisplaySettings API to verify an active HDMI connection is present on the DUT.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":3,"method":"org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The API should return `connectedVideoDisplays=HDMI0`, confirming an active HDMI connection is present. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Hotplug HDMI cable on DUT | A visual alert blinks on the screen: *"PLEASE DISCONNECT HDMI CABLE AND CONNECT IT BACK TO DUT TO PROCEED TEST!!!"* — physically disconnect the HDMI cable from the DUT and then reconnect it. The script then prompts: *"Is HDMI cable hotplugged from DUT and RDK UI showing on TV [yes/no]:"* — respond `yes` once the HDMI is reconnected and the RDK UI is visible on the TV. | The HDMI cable should be hotplugged and the RDK UI should be visible on the TV display after reconnection. |
| 2 | Verify HDMI connected via getHDCPStatus | Execute the curl command to verify the HDMI connection status via the HdcpProfile API after the hotplug operation.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":3,"method":"org.rdk.HdcpProfile.getHDCPStatus","params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The API response should return `isConnected=true` and `success=true`, confirming the DUT has detected the HDMI reconnection. |
| 3 | Verify HDCP authentication logs | Execute the commands to check the device log file for both the HDMI connect and HDCP authentication events.<br>Command 1: `tail -n 500 $hdcp_logs_path \| grep -F -i -o "Updated hotplug to CONNECTED" \| tail -n 1`<br>Command 2: `tail -n 500 $hdcp_logs_path \| grep -F -i -o "Updated hdcp_status to AUTHENTICATED" \| tail -n 1` | The log file should contain both `"Updated hotplug to CONNECTED"` and `"Updated hdcp_status to AUTHENTICATED"`, confirming that HDCP authentication was successfully initiated after the hotplug operation. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
