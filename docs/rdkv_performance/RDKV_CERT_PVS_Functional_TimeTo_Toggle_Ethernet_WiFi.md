## TestCase ID
RDKV_PERFORMANCE_47
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_Toggle_Ethernet_WiFi
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to toggle between Ethernet and 2.4GHz WiFi network interfaces is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Both Ethernet and 2.4GHz WiFi interfaces must be available and configured on the device.|
|3|`TOGGLE_INTERFACE_THRESHOLD` must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Ethernet to WiFi Toggle Start Time | Record UTC timestamp before disabling Ethernet. | Start time recorded. |
| 3 | Disable Ethernet, Enable WiFi | Toggle the network interface from Ethernet to 2.4GHz WiFi. | WiFi active. |
| 4 | Record Toggle Completion Time | Record UTC timestamp after WiFi connection is established. | End time recorded. |
| 5 | Record WiFi to Ethernet Toggle Start Time | Record UTC timestamp before disabling WiFi. | Start time recorded. |
| 6 | Disable WiFi, Enable Ethernet | Toggle the network interface from WiFi to Ethernet. | Ethernet active. |
| 7 | Record Toggle Completion Time | Record UTC timestamp after Ethernet connection is established. | End time recorded. |
| 8 | Validate Toggle Times | Compare both toggle times against threshold. | Times to toggle between Ethernet and 2.4GHz WiFi are within the expected thresholds. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 20

**Priority** : High

**Release Version** : M89<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
