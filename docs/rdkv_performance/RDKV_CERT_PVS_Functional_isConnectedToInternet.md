## TestCase ID
RDKV_PERFORMANCE_55
## TestCase Name
RDKV_CERT_PVS_Functional_isConnectedToInternet
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the device can successfully connect to the internet and retrieve a valid response from a configured internet connectivity check endpoint.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Device must be connected to a network (Ethernet or WiFi) with internet access.|
|3|Internet connectivity check URL must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Verify Network Interface | Confirm device has an active network interface with a valid IP address. | Network interface active. |
| 3 | Check Internet Connectivity | Send an HTTP request to the configured internet connectivity check endpoint (e.g., a known URL). | HTTP response received. |
| 4 | Validate Internet Connection | Verify the HTTP response indicates successful internet connectivity. | Device is connected to the internet and can reach the configured endpoint. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 20

**Priority** : High

**Release Version** : M90<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
