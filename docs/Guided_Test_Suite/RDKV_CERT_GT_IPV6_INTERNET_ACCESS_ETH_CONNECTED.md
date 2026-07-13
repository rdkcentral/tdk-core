## TestCase ID
RDKV_MANUAL_IPV6_04
## TestCase Name
RDKV_CERT_GT_IPV6_INTERNET_ACCESS_ETH_CONNECTED

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT has functional IPv6 internet access via the Ethernet interface and that AV playback is operational when both WiFi (IPv6 SSID) and Ethernet are connected simultaneously, as tested by the `IPv6_Automated.sh` script. The test verifies IPv6 internet connectivity via `org.rdk.NetworkManager.1.IsConnectedToInternet` with the eth0 interface, then launches YouTube AV playback via `org.rdk.AppManager.launchApp` and confirms playback via tester input. This test ensures the DUT can access the internet and stream media content over IPv6 via the Ethernet interface in a dual-network configuration.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Ensure the test script (`IPv6_Automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) are present in the working directory of the DUT before executing the test. The `device.conf` file must be configured with the correct values required for this specific test prior to execution. | The files `IPv6_Automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 3 | Connect DUT to IPv6 WiFi SSID | Connect the DUT to an IPv6-supported WiFi SSID configured as `<ipv6_conf_SSID>`. | The DUT should be connected to the configured IPv6-supported WiFi SSID and a valid IPv6 address should be assigned to the wlan0 interface. |
| 4 | Connect Ethernet cable to DUT | Connect the Ethernet cable to the DUT and ensure a valid IPv4 address is assigned to the eth0 interface. | The Ethernet interface (eth0) should have a valid IPv4 address assigned on the DUT. |
| 5 | Verify YouTube app available | Verify that the YouTube (Cobalt) app is available and accessible on the DUT. | The YouTube app should be present and accessible on the DUT. |
| 6 | Sign in to YouTube app | Sign in to the YouTube application on the DUT with a valid user account prior to the test. | YouTube should be signed in with a valid user account and AV playback should be accessible. |
| 7 | Verify IPv6 SSID and Ethernet connection | Verify the DUT is connected to the correct IPv6 SSID and Ethernet is active using the NetworkManager API.<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | The DUT should be connected to `<ipv6_conf_SSID>`, a valid IPv6 address should be present on wlan0, and eth0 should have a valid IPv4 address. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify IPv6 connectivity via Ethernet | Execute the curl command to verify IPv6 internet connectivity via the Ethernet interface (eth0).<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.IsConnectedToInternet","params":{"ipversion":"IPv6"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return interface=eth0, connected=true, and status=FULLY_CONNECTED, confirming IPv6 internet connectivity via Ethernet. |
| 2 | Start immediate AV playback via YouTube | The script launches the YouTube application with immediate AV playback via the AppManager launchApp API using the configured playback URL (`<yt_URL>`).<br>Command: `curl -d '{"jsonrpc":"2.0","id":2,"method":"org.rdk.AppManager.launchApp","params":{"appId":"com.rdkcentral.youtube","intent":"playback","launchArgs":"<yt_URL>"}}' http://localhost:9998/jsonrpc` | The YouTube application should launch successfully and AV playback should start immediately on the DUT. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
