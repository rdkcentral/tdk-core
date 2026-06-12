## TestCase ID
RDKV_PERFORMANCE_07
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_Ethernet_InterfaceUp
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for the Ethernet interface to come up and obtain an IP address is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Ethernet port must be connected to a network.|
|3|`ETHERNET_INTERFACE_UP_THRESHOLD` must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Disable Ethernet Interface | Disable the Ethernet interface on the device. | Ethernet interface down. |
| 3 | Record Start Time | Record UTC timestamp before enabling Ethernet interface. | Start time recorded. |
| 4 | Enable Ethernet Interface | Enable the Ethernet interface. | Ethernet interface enabling started. |
| 5 | Wait for Interface Up | Monitor until Ethernet interface is up and an IP address is assigned. | Ethernet interface active with IP address. |
| 6 | Record Interface Up Time | Record UTC timestamp when interface is confirmed up. | End time recorded. |
| 7 | Validate Time | Calculate Ethernet interface up time = end timestamp - start timestamp. Compare against threshold. | Time for Ethernet interface to come up is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 7

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
