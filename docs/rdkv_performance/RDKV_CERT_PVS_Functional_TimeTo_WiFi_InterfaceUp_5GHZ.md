## TestCase ID
RDKV_PERFORMANCE_50
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_WiFi_InterfaceUp_5GHZ
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for the 5GHz WiFi interface to come up and obtain an IP address is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WiFi adapter must support 5GHz band and be enabled.|
|3|Target 5GHz WiFi access point must be in range.|
|4|5GHz WiFi credentials must be configured in device config.|
|5|`WIFI_INTERFACE_UP_5GHZ_THRESHOLD` must be configured in device config.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Disable WiFi Interface | Disable the WiFi interface on the device. | WiFi interface down. |
| 3 | Record Start Time | Record UTC timestamp before enabling 5GHz WiFi interface. | Start time recorded. |
| 4 | Enable 5GHz WiFi Interface | Enable the 5GHz WiFi interface and connect to the configured SSID. | 5GHz WiFi enabling started. |
| 5 | Wait for Interface Up and IP | Monitor until 5GHz WiFi interface is up with a valid IP address. | 5GHz WiFi interface active with IP address. |
| 6 | Record Interface Up Time | Record UTC timestamp when interface is confirmed up with IP. | End time recorded. |
| 7 | Validate Time | Calculate 5GHz WiFi up time = end timestamp - start timestamp. Compare against threshold. | Time for 5GHz WiFi interface to come up is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M89<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
