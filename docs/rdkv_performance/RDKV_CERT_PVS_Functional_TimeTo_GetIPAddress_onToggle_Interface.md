## TestCase ID
RDKV_PERFORMANCE_96
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_GetIPAddress_onToggle_Interface
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to obtain an IP address after toggling the network interface is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Both Ethernet and WiFi interfaces must be available on the device.|
|3|`IP_ADDRESS_THRESHOLD` must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Toggle Start Time | Record UTC timestamp before toggling the network interface. | Start time recorded. |
| 3 | Toggle Network Interface | Disable current active interface and enable the other (Ethernet → WiFi or WiFi → Ethernet). | Interface toggle initiated. |
| 4 | Wait for IP Address | Monitor until a valid IP address is obtained on the new interface. | IP address obtained. |
| 5 | Record IP Obtained Time | Record UTC timestamp when IP address is obtained. | End time recorded. |
| 6 | Validate Time | Calculate time to get IP after toggle = end timestamp - start timestamp. Compare against threshold. | Time to obtain IP address after interface toggle is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 12

**Priority** : High

**Release Version** : M96<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
