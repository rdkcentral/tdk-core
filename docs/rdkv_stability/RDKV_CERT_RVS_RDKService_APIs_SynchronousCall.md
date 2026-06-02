## TestCase ID
RDKV_STABILITY_66
## TestCase Name
RDKV_CERT_RVS_RDKService_APIs_SynchronousCall
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the device handles multiple RDK Services API requests invoked simultaneously and repeatedly under stress conditions without failure.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`iterations` must be configured in StabilityTestVariables with the number of stress test repetitions (default: 200).|
|3|`methods` must be configured in StabilityTestVariables with the list of RDK Service API callsigns to be invoked simultaneously (default list: org.rdk.System.getDeviceInfo, org.rdk.DisplaySettings.getConnectedAudioPorts, org.rdk.DisplaySettings.getMuted, org.rdk.DisplaySettings.getVolumeLevel, org.rdk.NetworkManager.1.GetPublicIP).|
|4|`rebootwaitTime` must be configured in StabilityTestVariables with the number of seconds to wait for the device to come back online after the pre-requisite reboot (default: 150 seconds).|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pre-requisite Reboot | Reboot the device once before starting the stress test and wait for it to come back online. `rebootwaitTime` is read from StabilityTestVariables (default: 150 seconds). <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_rebootDevice", "params": {"waitTime": 150}} | Device should reboot and come back online successfully before the stress test begins. |
| 2 | Validate Required Configuration | Check that both `iterations` and `methods` attributes are present and non-empty in StabilityTestVariables. If either is missing, the test is marked as FAILURE and execution stops. | Both `iterations` and `methods` must be configured in StabilityTestVariables. |
| 3 | Invoke RDK Service APIs Simultaneously (Per Iteration) | For each of the `iterations` (default: 200) iterations, invoke all configured API methods simultaneously in a single synchronous request using `rdkservice_synchronous_request`. The following methods are called together in each iteration by default: org.rdk.System.getDeviceInfo, org.rdk.DisplaySettings.getConnectedAudioPorts, org.rdk.DisplaySettings.getMuted, org.rdk.DisplaySettings.getVolumeLevel, org.rdk.NetworkManager.1.GetPublicIP. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_synchronous_request", "params": {"method": ["org.rdk.System.getDeviceInfo", "org.rdk.DisplaySettings.getConnectedAudioPorts", "org.rdk.DisplaySettings.getMuted", "org.rdk.DisplaySettings.getVolumeLevel", "org.rdk.NetworkManager.1.GetPublicIP"]}} | All API methods should return successful responses in each iteration. Any failed methods are recorded. |
| 4 | Track and Report Failures | After all iterations are complete, aggregate the results: collect all failed requests, count the number of failures per API method, and print a summary including total iteration count, total failure count, per-method failure counts, and the list of failed requests. | Summary should be printed showing iteration count (200), total failures, and details of any failed API methods. If all iterations pass, total failure count should be 0. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M135<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
