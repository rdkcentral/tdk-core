## TestCase ID
RDKV_MANUAL_HDCP_COMP_06
## TestCase Name
RDKV_CERT_GT_HDCP_VERSION_VERIFY

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT reports consistent HDCP version information across all three version parameters — supported, received, and current — as verified via the `org.rdk.HdcpProfile.getHDCPStatus` API during active AV playback, as tested by the `HDCP_COMPLIANCE_AUTOMATED.sh` script. The test launches YouTube AV playback via `org.rdk.AppManager.launchApp` and queries `getHDCPStatus` to confirm that `supportedHDCPVersion`, `receiverHDCPVersion`, and `currentHDCPVersion` all return `2.2`. This test ensures HDCP 2.2 version negotiation between the DUT and the connected HDMI display is functioning correctly.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`HDCP_COMPLIANCE_AUTOMATED.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `HDCP_COMPLIANCE_AUTOMATED.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 3 | Verify YouTube app available | Verify that the YouTube (Cobalt) app is available and accessible on the DUT. | The YouTube app should be present and accessible on the DUT. |
| 4 | Sign in to YouTube app | Sign in to the YouTube application on the DUT with a valid user account prior to the test. | YouTube should be signed in with a valid user account and AV playback should be accessible. |
| 5 | Verify active HDMI connection | Execute the DisplaySettings API to verify an active HDMI connection is present on the DUT.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":3,"method":"org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The API should return `connectedVideoDisplays=HDMI0`, confirming an active HDMI connection is present. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Hotplug HDMI cable on DUT | A visual alert blinks on the screen: *"PLEASE DISCONNECT HDMI CABLE AND CONNECT IT BACK TO DUT TO PROCEED TEST!!!"* — physically disconnect the HDMI cable from the DUT and then reconnect it. The script then prompts: *"Is HDMI cable hotplugged from DUT and RDK UI showing on TV [yes/no]:"* — respond `yes` once the HDMI is reconnected and the RDK UI is visible on the TV. | The HDMI cable should be hotplugged and the RDK UI should be visible on the TV display after reconnection. |
| 2 | Start immediate AV playback via YouTube | The script launches the YouTube application with immediate AV playback via the AppManager launchApp API using the configured playback URL (`<yt_URL>`).<br>Command: `curl -d '{"jsonrpc":"2.0","id":2,"method":"org.rdk.AppManager.launchApp","params":{"appId":"com.rdkcentral.youtube","intent":"playback","launchArgs":"<yt_URL>"}}' http://localhost:9998/jsonrpc` | The YouTube application should launch successfully and AV playback should start immediately on the DUT. |
| 3 | Verify supported, receiver and current HDCP versions | Execute the curl command to retrieve and verify all HDCP version fields from the getHDCPStatus API.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":3,"method":"org.rdk.HdcpProfile.getHDCPStatus","params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The API response should return `supportedHDCPVersion=2.2`, `receiverHDCPVersion=2.2`, and `currentHDCPVersion=2.2` — all three values should be equal and set to 2.2, and `success=true`. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
