## TestCase ID
RDKV_PERFORMANCE_5
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
To validate the network connectivity and ping performance of the device under test by confirming there is zero packet loss and that the average round-trip time to the configured destination is within the acceptable threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure ping_test_destination in PerformanceTestVariables | `ping_test_destination` must be set to the IP address or hostname to ping in PerformanceTestVariables. | The ping test destination should be configured with a valid and reachable host. |
| 4 | Configure TRIPTIME_THRESHOLD_VALUE in device config | `TRIPTIME_THRESHOLD_VALUE` must be set in the device config file to define the acceptable average round-trip time in milliseconds. | The threshold value should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate the Network plugin | Query the org.rdk.Network plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.Network"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Network"}}` | The org.rdk.Network plugin should be in the activated state. |
| 2 | Execute ping to configured destination | Send 10 ICMP ping packets to the configured `ping_test_destination` using the Network plugin ping method. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Network.1.ping", "params": {"endpoint": "<ping_test_destination>", "packets": 10}}` | The ping request should be accepted and a response containing packet loss and trip time metrics should be returned. |
| 3 | Validate packet loss | Parse the `packetLoss` field from the ping response and verify it equals zero. | Packet loss should be 0%, confirming uninterrupted connectivity to the destination. |
| 4 | Validate average round-trip time | Parse the `tripAvg` field from the ping response and compare it against the configured `TRIPTIME_THRESHOLD_VALUE` from the device config file. | The average round-trip time should be less than the configured `TRIPTIME_THRESHOLD_VALUE` milliseconds. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M97<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
