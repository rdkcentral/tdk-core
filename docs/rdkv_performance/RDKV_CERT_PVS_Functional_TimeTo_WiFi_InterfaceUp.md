## TestCase ID
RDKV_PERFORMANCE_29
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_WiFi_InterfaceUp
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for the 2.4GHz WiFi interface to come up and obtain an IP address is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WiFi adapter must support 2.4GHz band and be enabled.|
|3|Target 2.4GHz WiFi access point must be in range.|
|4|WiFi credentials must be configured in device config.|
|5|`WIFI_INTERFACE_UP_THRESHOLD` must be configured in device config.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Disable WiFi Interface | Disable the WiFi interface on the device. | WiFi interface down. |
| 3 | Record Start Time | Record UTC timestamp before enabling WiFi interface. | Start time recorded. |
| 4 | Enable WiFi Interface | Enable the 2.4GHz WiFi interface and connect to the configured SSID. | WiFi enabling started. |
| 5 | Wait for Interface Up and IP | Monitor until WiFi interface is up with a valid IP address. | WiFi interface active with IP address. |
| 6 | Record Interface Up Time | Record UTC timestamp when interface is confirmed up with IP. | End time recorded. |
| 7 | Validate Time | Calculate WiFi up time = end timestamp - start timestamp. Compare against threshold. | Time for 2.4GHz WiFi interface to come up is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 25

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
