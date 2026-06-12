## TestCase ID
RDKV_PERFORMANCE_20
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_WiFiConnection
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges during a WiFi connection establishment on the device.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WiFi adapter should be available and enabled on the device.|
|3|A target WiFi network (2.4GHz) must be reachable.|
|4|WiFi credentials (SSID/password) must be configured in device config.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Capture Baseline Resource Usage | Record CPU and memory usage before establishing WiFi connection. | Baseline recorded. |
| 3 | Initiate WiFi Connection | Connect to the configured 2.4GHz WiFi SSID. | WiFi connection initiated. |
| 4 | Verify WiFi Connection | Confirm device is connected to the WiFi network and has a valid IP address. | WiFi connection established successfully. |
| 5 | Capture Resource Usage During Connection | Record CPU and memory usage while WiFi connection is active. | Resource data captured. |
| 6 | Validate Resource Usage | Verify CPU load and memory usage during WiFi connection are within acceptable limits. | CPU load and memory usage during WiFi connection are within the expected limits. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 13

**Priority** : High

**Release Version** : M85<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
