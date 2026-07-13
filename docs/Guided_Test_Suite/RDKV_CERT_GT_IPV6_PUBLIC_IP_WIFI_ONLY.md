## TestCase ID
RDKV_MANUAL_IPV6_03
## TestCase Name
RDKV_CERT_GT_IPV6_PUBLIC_IP_WIFI_ONLY

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT correctly reports a valid public IPv6 address via the WiFi interface (wlan0) when operating in a WiFi-only configuration with Ethernet disconnected, as tested by the `IPv6_Automated.sh` script. The test exercises the `org.rdk.NetworkManager.1.GetIPSettings` API to retrieve the public IPv6 address assigned to the wlan0 interface and verifies the address is non-empty and in valid IPv6 format. This test confirms the DUT's IPv6 address resolution and reporting capability via the WiFi interface under Ethernet-disconnected conditions.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 2 | Connect DUT to IPv6 WiFi SSID | Connect the DUT to an IPv6-supported WiFi SSID configured as `<ipv6_conf_SSID>`. | The DUT should be connected to the configured IPv6-supported WiFi SSID and a valid IPv6 address should be assigned to the wlan0 interface. |
| 3 | Disconnect Ethernet cable | Disconnect the Ethernet cable from the DUT to ensure only WiFi connectivity is active. | The Ethernet interface (eth0) should have no IPv4 address assigned on the DUT. |
| 4 | Verify IPv6 SSID connection | Verify the DUT is connected to the correct IPv6 SSID using the NetworkManager API.<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | The DUT should be connected to `<ipv6_conf_SSID>`, a valid IPv6 address should be present on wlan0, and Ethernet should be disconnected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Get public IPv6 IP via WiFi interface | Execute the curl command to retrieve the public IPv6 IP address via the WiFi interface (wlan0).<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.GetPublicIP","params":{"ipversion":"IPv6"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return interface=wlan0, a valid IPv6 public address, and success=true. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
