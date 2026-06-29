## TestCase ID
RDKV_PERFORMANCE_20
## TestCase Name
RDKV_CERT_PVS_Functional_ValidateIPAddress

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the device under test has a valid IP address on its active network interface (Ethernet or WiFi), by retrieving the IP address via SSH and confirming it conforms to the configured IP address type (IPv4 or IPv6).

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure ETHERNET_INTERFACE or WIFI_INTERFACE in device config | `ETHERNET_INTERFACE` or `WIFI_INTERFACE` must be set in the device config file corresponding to the active interface. | The correct interface name should be configured. |
| 4 | Configure DEVICE_IP_ADDRESS_TYPE in device config | `DEVICE_IP_ADDRESS_TYPE` must be set to either `ipv4` or `ipv6` in the device config file. | The IP address type should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Determine the active network interface | Check the current active network interface of the DUT (eth0 or wlan0) using the NetworkManager plugin to determine which interface config key to use. | The active network interface should be identified as either eth0 (Ethernet) or wlan0 (WiFi). |
| 2 | Establish SSH connection to device | Obtain SSH connection parameters and retrieve the interface name and IP address type from the device config file. | SSH parameters, interface name, and IP address type should all be retrieved successfully. |
| 3 | Retrieve the IP address of the active interface | SSH into the device and execute the command to retrieve the IP address for the active interface based on the configured IP address type. <br>For IPv4: `/sbin/ip -o -4 addr list <interface_name> \| awk '{print $4}' \| cut -d/ -f1` <br>For IPv6: `/sbin/ip -o -6 addr list <interface_name> \| awk '{print $4}' \| cut -d/ -f1` | The command should return the IP address of the active interface without an exception. |
| 4 | Validate the IP address format | Parse the IP address from the command output and verify that it is a valid address conforming to the configured IP address type (IPv4 or IPv6). | The device should have a valid IP address on the active interface. The IP address should be non-empty and must be a valid IPv4 or IPv6 address as configured. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M91<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
