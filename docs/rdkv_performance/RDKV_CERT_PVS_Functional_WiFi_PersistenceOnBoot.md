## TestCase ID
RDKV_PERFORMANCE_64
## TestCase Name
RDKV_CERT_PVS_Functional_WiFi_PersistenceOnBoot
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the device maintains its WiFi connection configuration and automatically reconnects to the previously connected WiFi network after a reboot.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WiFi adapter must be available and enabled on the device.|
|3|A target WiFi network must be in range and the device must have been previously connected to it.|
|4|WiFi credentials must be configured in device config.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Verify Initial WiFi Connection | Confirm the device is connected to the configured WiFi network and has a valid IP address. | Initial WiFi connection confirmed. |
| 3 | Reboot Device | Reboot the device: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.harakiri"}` | Device reboots. |
| 4 | Wait for Device to Come Online | Wait for WPEFramework to restart after reboot. | Device comes back online. |
| 5 | Verify WiFi Reconnection | Verify that the device has automatically reconnected to the same WiFi network with a valid IP address. | Device successfully reconnected to the WiFi network after reboot, confirming WiFi persistence on boot. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
