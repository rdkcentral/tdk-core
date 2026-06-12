## TestCase ID
RDKV_PERFORMANCE_101
## TestCase Name
RDKV_CERT_PVS_Functional_Ping_Performance
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the network ping performance (round-trip time) of the device is within acceptable thresholds.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Device must be connected to an active network.|
|3|`PING_PERFORMANCE_THRESHOLD` must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Ping Target Host | Send ICMP ping requests to a configured target host and record round-trip times. | Ping responses received. |
| 3 | Calculate Average RTT | Average the round-trip times from multiple ping requests. | Average RTT calculated. |
| 4 | Validate Ping Performance | Compare average RTT against `PING_PERFORMANCE_THRESHOLD` configured in device config. | Average ping round-trip time is within acceptable threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M97<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
