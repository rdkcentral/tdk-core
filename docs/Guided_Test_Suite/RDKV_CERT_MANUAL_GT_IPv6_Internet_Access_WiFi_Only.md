## TestCase ID
RDKV_MANUAL_GT_IPV6_05
## TestCase Name
RDKV_CERT_MANUAL_GT_IPv6_Internet_Access_WiFi_Only

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Preconditions](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT has functional IPv6 internet access via the WiFi interface and supports AV media playback when operating in a WiFi-only configuration with the Ethernet interface physically disconnected. This test confirms the DUT's WiFi IPv6 path is fully operational for internet connectivity and media streaming without any Ethernet dependency.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`IPv6_Automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `IPv6_Automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 3 | Connect DUT to IPv6 WiFi SSID | Connect the DUT to an IPv6-supported WiFi SSID configured as `<ipv6_conf_SSID>`. | The DUT should be connected to the configured IPv6-supported WiFi SSID and a valid IPv6 address should be assigned to the wlan0 interface. |
| 4 | Disconnect Ethernet cable | Disconnect the Ethernet cable from the DUT to ensure only WiFi connectivity is active. | The Ethernet interface (eth0) should have no IPv4 address assigned on the DUT. |
| 5 | Verify and sign in to YouTube app | Verify that the YouTube app is installed on the DUT and sign in with a valid user account prior to the test. | The YouTube app must be installed on the DUT and signed in with a valid user account, with AV playback accessible, prior to test execution. |
| 6 | Verify IPv6 SSID connection | Verify the DUT is connected to the correct IPv6 SSID using the NetworkManager API.<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | The DUT should be connected to `<ipv6_conf_SSID>`, a valid IPv6 address should be present on wlan0, and Ethernet should be disconnected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify IPv6 connectivity via WiFi | Execute the curl command to verify IPv6 internet connectivity via the WiFi interface (wlan0).<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.IsConnectedToInternet","params":{"ipversion":"IPv6"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return interface=wlan0, connected=true, and status=FULLY_CONNECTED, confirming IPv6 internet connectivity via WiFi. |
| 2 | Start immediate AV playback via YouTube | Launch the YouTube application with immediate AV playback via the AppManager launchApp API using the configured playback URL (`<yt_URL>`):<br>Command: `curl -d '{"jsonrpc":"2.0","id":2,"method":"org.rdk.AppManager.launchApp","params":{"appId":"com.rdkcentral.youtube","intent":"playback","launchArgs":"<yt_URL>"}}' http://localhost:9998/jsonrpc` | The YouTube application should launch successfully and AV playback should start immediately on the DUT. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
