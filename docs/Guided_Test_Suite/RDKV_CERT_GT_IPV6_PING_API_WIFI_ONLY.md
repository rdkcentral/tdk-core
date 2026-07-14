## TestCase ID
RDKV_MANUAL_IPV6_07
## TestCase Name
RDKV_CERT_GT_IPV6_PING_API_WIFI_ONLY

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the `org.rdk.NetworkManager.1.Ping` API successfully transmits and receives IPv6 ICMP packets to a configured IPv6 endpoint (`<ipv6_ping_endpoint>`) with zero packet loss via the WiFi interface when Ethernet is disconnected, as tested by the `IPv6_Automated.sh` script. The test calls the Ping API with an IPv6 target and verifies the response reports 0% packet loss, confirming IPv6 ICMP reachability over the WiFi-only network path. This test ensures the RDK NetworkManager's IPv6 Ping functionality is operational and the DUT's IPv6 WiFi path has reliable bidirectional packet delivery.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`IPv6_Automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `IPv6_Automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 3 | Connect DUT to IPv6 WiFi SSID | Connect the DUT to an IPv6-supported WiFi SSID configured as `<ipv6_conf_SSID>`. | The DUT should be connected to the configured IPv6-supported WiFi SSID and a valid IPv6 address should be assigned to the wlan0 interface. |
| 4 | Disconnect Ethernet cable | Disconnect the Ethernet cable from the DUT to ensure only WiFi connectivity is active. | The Ethernet interface (eth0) should have no IPv4 address assigned on the DUT. |
| 5 | Verify IPv6 SSID connection | Verify the DUT is connected to the correct IPv6 SSID using the NetworkManager API.<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | The DUT should be connected to `<ipv6_conf_SSID>`, a valid IPv6 address should be present on wlan0, and Ethernet should be disconnected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify ping API to IPv6 endpoint | Execute the curl command to ping the IPv6 endpoint `2001:4860:4860::8888` with 10 packets.<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.Ping","params":{"endpoint":"2001:4860:4860::8888","ipversion":"IPv6","packets":10}}' http://127.0.0.1:9998/jsonrpc` | The ping API response should return packetLoss=0, packetsTransmitted greater than 0, packetsReceived greater than 0, and success=true, confirming successful IPv6 ping with zero packet loss. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
