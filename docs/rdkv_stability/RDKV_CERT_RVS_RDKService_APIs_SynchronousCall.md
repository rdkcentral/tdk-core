## TestCase ID
RDKV_STABILITY_1
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
To validate that the DUT handles multiple RDK Service API calls invoked simultaneously and repeatedly without failure, confirming the device remains stable under stress conditions across all configured iterations.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure iterations in StabilityTestVariables | `iterations` must be set to the desired number of stress test cycles in StabilityTestVariables (default: "200"). | The iterations variable should be configured with a valid integer string value. |
| 3 | Configure methods list in StabilityTestVariables | `methods` must be populated with the list of RDK Service API method names to be invoked simultaneously per iteration in StabilityTestVariables (e.g., org.rdk.System.getDeviceInfo, org.rdk.DisplaySettings.getConnectedAudioPorts, org.rdk.DisplaySettings.getMuted, org.rdk.DisplaySettings.getVolumeLevel, org.rdk.NetworkManager.1.GetPublicIP). | The methods list should contain at least one valid RDK Service method name. |
| 4 | Configure reboot wait time in StabilityTestVariables | `rebootwaitTime` must be set to the number of seconds to wait for the device to come back online after the pre-requisite reboot (default: 150 seconds). | The rebootwaitTime variable should be configured with a valid integer value. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot device before stress test | Reboot the device as a pre-requisite before starting the synchronous call stress test. The device is rebooted by invoking the Thunder Controller harakiri method and the script waits for `rebootwaitTime` (150) seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should reboot successfully and come back online within the configured wait time. |
| 2 | Verify required test variables are configured | Check that `iterations` and `methods` are present and non-empty in StabilityTestVariables. If either is missing or empty, the test is marked as FAILURE and aborted. | Both `iterations` and `methods` variables should be properly configured before proceeding. |
| 3 | Invoke all configured API methods simultaneously (Per Iteration) | For each iteration, invoke all methods from the configured `methods` list as concurrent synchronous JSON-RPC requests using gevent. Each method is called as: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.getDeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DisplaySettings.getConnectedAudioPorts"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DisplaySettings.getMuted"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DisplaySettings.getVolumeLevel"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.NetworkManager.1.GetPublicIP"}` | All API calls should return SUCCESS for each iteration. Any failed methods are recorded. |
| 4 | Record failed requests | If any method invocation fails in an iteration, the failed method names and their failure count are recorded in a tracking dictionary. The total failure count and per-method failure details are accumulated across all iterations. | Failed request details should be captured accurately for post-test reporting. |
| 5 | Repeat simultaneous API invocations for all iterations | Repeat Step 3 and Step 4 for all `iterations` (200) cycles as configured in StabilityTestVariables. | All 200 iterations should complete. Failed iterations and methods are tracked. |
| 6 | Report stress test summary | After completing all iterations, print the total iteration count, total failure count, per-method failure counts, and the full list of failed requests. | Summary report should correctly reflect total iterations executed, total failures, and per-API failure details. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M135<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
