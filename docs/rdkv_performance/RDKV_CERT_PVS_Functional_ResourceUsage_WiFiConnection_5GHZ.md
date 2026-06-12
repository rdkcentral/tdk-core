## TestCase ID
RDKV_PERFORMANCE_45
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_WiFiConnection_5GHZ
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges during a 5GHz WiFi connection establishment on the device.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WiFi adapter must support 5GHz band and be enabled on the device.|
|3|A target 5GHz WiFi network must be reachable.|
|4|WiFi 5GHz credentials (SSID/password) must be configured in device config.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Capture Baseline Resource Usage | Record CPU and memory usage before establishing 5GHz WiFi connection. | Baseline recorded. |
| 3 | Initiate 5GHz WiFi Connection | Connect to the configured 5GHz WiFi SSID. | 5GHz WiFi connection initiated. |
| 4 | Verify 5GHz WiFi Connection | Confirm device is connected to the 5GHz WiFi network and has a valid IP address. | 5GHz WiFi connection established successfully. |
| 5 | Capture Resource Usage During Connection | Record CPU and memory usage while 5GHz WiFi connection is active. | Resource data captured. |
| 6 | Validate Resource Usage | Verify CPU load and memory usage during 5GHz WiFi connection are within acceptable limits. | CPU load and memory usage during 5GHz WiFi connection are within the expected limits. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M89<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
