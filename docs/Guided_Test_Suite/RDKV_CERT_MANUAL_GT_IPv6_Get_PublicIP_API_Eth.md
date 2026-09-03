## TestCase ID
RDKV_MANUAL_GT_IPV6_08
## TestCase Name
RDKV_CERT_MANUAL_GT_IPv6_Get_PublicIP_API_Eth

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Preconditions](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the NetworkManager GetPublicIP API correctly resolves and returns a valid public IPv6 address when explicitly queried for the Ethernet interface in a dual-network (WiFi + Ethernet) configuration. This test confirms the API respects the interface-specific parameter and returns the correct public IPv6 address for the Ethernet path independently of the active WiFi connection.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`IPv6_Automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `IPv6_Automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 3 | Connect DUT to IPv6 WiFi SSID | Connect the DUT to an IPv6-supported WiFi SSID configured as `<ipv6_conf_SSID>`. | The DUT should be connected to the configured IPv6-supported WiFi SSID and a valid IPv6 address should be assigned to the wlan0 interface. |
| 4 | Connect Ethernet cable to DUT | Connect the Ethernet cable to the DUT and ensure a valid IPv4 address is assigned to the eth0 interface. | The Ethernet interface (eth0) should have a valid IPv4 address assigned on the DUT. |
| 5 | Verify IPv6 SSID and Ethernet connection | Verify the DUT is connected to the correct IPv6 SSID and Ethernet is active using the NetworkManager API.<br>Command: `curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.GetConnectedSSID"}' http://127.0.0.1:9998/jsonrpc` | The DUT should be connected to `<ipv6_conf_SSID>`, a valid IPv6 address should be present on wlan0, and eth0 should have a valid IPv4 address. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify GetPublicIP API with explicit interface | Execute the GetPublicIP API with the Ethernet interface explicitly specified as a parameter, while both the IPv6-supported WiFi (wlan0) and Ethernet (eth0) interfaces are simultaneously active on the DUT:<br>`curl -d '{"jsonrpc":"2.0","id":42,"method":"org.rdk.NetworkManager.1.GetPublicIP","params":{"interface":"eth0","ipversion":"IPv6"}}' http://127.0.0.1:9998/jsonrpc` | The GetPublicIP API should return `success: true` with `interface: eth0` and a valid public IPv6 address, confirming the API correctly resolves the IPv6 address for the explicitly specified Ethernet interface. If the Ethernet interface does not have a public IPv6 address assigned, the API should return `success: false`, confirming the API handles the interface-specific query gracefully without error. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
