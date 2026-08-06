## TestCase ID
RDKV_PERFORMANCE_2
## TestCase Name
RDKV_CERT_PVS_Functional_Device_MaxResponseTime

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the maximum API response time for a configured WPEFramework method is within the expected acceptable limit, measured across 5 consecutive API calls.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure method in PerformanceTestVariables | `method` must be set to the JSON-RPC method name to be benchmarked in PerformanceTestVariables. Eg: `org.rdk.AppManager.1.getInstalledApps` | The method variable should be configured with a valid WPEFramework API method name. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Measure API response time — 5 iterations | Execute the configured method 5 times consecutively and measure the response time for each call. The test measures the round-trip time from when the JSON-RPC request is dispatched to when the response is received. The configured method from `PerformanceTestVariables.method` is used as the target API for all 5 measurements. | Each of the 5 API calls should return a valid response time value successfully. The response time for each call should be recorded for analysis. |
| 2 | Validate maximum response time | After collecting 5 response time samples, identify the maximum response time and validate it against the configured threshold. The maximum value from all 5 measurements must not exceed the expected response time limit. | The maximum API response time across all 5 iterations should be within the configured acceptable limit. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M116<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
