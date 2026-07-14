## TestCase ID
RDKV_GT_HDCP_COMP_07
## TestCase Name
RDKV_CERT_GT_HDCP_COMPLIANT_STATUS

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT achieves HDCP compliance status during active AV playback and that the content continues to stream with proper audio and video quality, as tested by the `HDCP_COMPLIANCE_AUTOMATED.sh` script. The test launches YouTube AV playback via `org.rdk.AppManager.launchApp` and verifies HDCP compliance through the `org.rdk.HdcpProfile.getHDCPStatus` API, confirming `isHDCPCompliant=true`, then uses tester-confirmed visual verification to ensure AV playback quality is unaffected. This test confirms end-to-end HDCP compliance on the DUT output with a connected HDMI display during real media streaming.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`HDCP_COMPLIANCE_AUTOMATED.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `HDCP_COMPLIANCE_AUTOMATED.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 3 | Verify and sign in to YouTube app | Verify that the YouTube (Cobalt) app is installed on the DUT and sign in with a valid user account prior to the test. | The YouTube (Cobalt) app must be installed on the DUT and signed in with a valid user account, with AV playback accessible, prior to test execution. |
| 4 | Verify active HDMI connection | Execute the DisplaySettings API to verify an active HDMI connection is present on the DUT.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":3,"method":"org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The API should return `connectedVideoDisplays=HDMI0`, confirming an active HDMI connection is present. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Hotplug HDMI cable on DUT | A visual alert blinks on the screen: *"PLEASE DISCONNECT HDMI CABLE AND CONNECT IT BACK TO DUT TO PROCEED TEST!!!"* — physically disconnect the HDMI cable from the DUT and then reconnect it. The script then prompts: *"Is HDMI cable hotplugged from DUT and RDK UI showing on TV [yes/no]:"* — respond `yes` once the HDMI is reconnected and the RDK UI is visible on the TV. | The HDMI cable should be hotplugged and the RDK UI should be visible on the TV display after reconnection. |
| 2 | Start immediate AV playback via YouTube | Launch the YouTube application with immediate AV playback via the AppManager launchApp API using the configured playback URL (`<yt_URL>`):<br>Command: `curl -d '{"jsonrpc":"2.0","id":2,"method":"org.rdk.AppManager.launchApp","params":{"appId":"com.rdkcentral.youtube","intent":"playback","launchArgs":"<yt_URL>"}}' http://localhost:9998/jsonrpc` | The YouTube application should launch successfully and AV playback should start immediately on the DUT. |
| 3 | Verify HDCP compliant status | Execute the curl command to verify that the DUT is HDCP compliant via the getHDCPStatus API.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":3,"method":"org.rdk.HdcpProfile.getHDCPStatus","params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The API response should return `isHDCPCompliant=true` and `success=true`, confirming the DUT is HDCP compliant. |
| 4 | Confirm continuous AV playback quality | The script prompts: *"Is AV stream playing continuously with proper audio and video in TV [yes/no]:"* — observe the TV display and respond `yes` if AV playback is continuous with proper audio and video quality. | AV playback should be continuous with proper audio and video on the TV display, confirming the DUT maintains HDCP-compliant streaming without interruption. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
