## TestCase ID
RDKV_MANUAL_HDCP_COMP_05
## TestCase Name
RDKV_CERT_GT_HDCP_ENABLED_STATUS

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that HDCP is enabled on the DUT and correctly reported via the `org.rdk.HdcpProfile.getHDCPStatus` API during active AV playback, as tested by the `HDCP_COMPLIANCE_AUTOMATED.sh` script. The test launches YouTube AV playback via `org.rdk.AppManager.launchApp` and then queries `getHDCPStatus` to confirm `isHDCPEnabled=true`, verifying that HDCP content protection is active on the HDMI output. This test ensures the DUT's HDCP enable state is correctly reflected in the HdcpProfile API under real playback conditions.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Ensure the test script (`HDCP_COMPLIANCE_AUTOMATED.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) are present in the working directory of the DUT before executing the test. The `device.conf` file must be configured with the correct values required for this specific test prior to execution. | The files `HDCP_COMPLIANCE_AUTOMATED.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
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
| 3 | Verify HDCP is enabled | Execute the curl command to verify that HDCP is enabled on the DUT via the getHDCPStatus API.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":3,"method":"org.rdk.HdcpProfile.getHDCPStatus","params":{}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The API response should return `isHDCPEnabled=true` and `success=true`, confirming HDCP is enabled on the DUT. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
