## TestCase ID
RDKV_PERFORMANCE_214
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_StandbyToOn

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for the device to transition its power state from STANDBY to ON is within the configured acceptable threshold, by measuring the duration between the setPowerState API call and the onSystemPowerStateChanged event timestamp.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm org.rdk.System plugin is available | The org.rdk.System plugin must be present and activatable in the device build. | The System plugin should be available in the build. |
| 3 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 4 | Synchronize Test Manager time with UTC | The time in the Test Manager must be in sync with UTC time for accurate timestamp comparison. | Test Manager time and device time should be synchronized. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate the System plugin | Query the System plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.System"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}` | The org.rdk.System plugin should be in the activated state. |
| 2 | Subscribe to power state changed event | Register an event listener for the onSystemPowerStateChanged event to capture the transition timestamp. <br>`{"jsonrpc": "2.0", "id": 5, "method": "org.rdk.System.1.register", "params": {"event": "onSystemPowerStateChanged", "id": "client.events.1"}}` | The event registration should succeed and the listener should be active. |
| 3 | Get current power state and ensure device is in ON state | Retrieve the current power state and set it to ON if it is not already ON. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.getPowerState"}` <br>Set to ON if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "ON", "standbyReason": "APIUnitTest"}}` | The device should be in the ON state before proceeding. |
| 4 | Set power state to STANDBY | Set the device power state to STANDBY in preparation for the STANDBY-to-ON transition measurement. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "LIGHT_SLEEP", "standbyReason": "APIUnitTest"}}` | The device should transition to STANDBY state successfully. |
| 5 | Set power state to ON and record start time | Record the current system time, then send the request to transition the device power state from STANDBY to ON. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "ON", "standbyReason": "APIUnitTest"}}` | The setPowerState request should be accepted and the power state transition to ON should begin. |
| 6 | Capture event timestamp and validate transition time | Retrieve the onSystemPowerStateChanged event from the event buffer and parse its timestamp. Calculate the STANDBY-to-ON transition time as the difference between the event timestamp and the recorded start time. Compare against the configured threshold. | The onSystemPowerStateChanged event should be received with the ON state. The transition time should be within the configured acceptable threshold. |
| 7 | Revert plugin state if changed | If the System plugin was activated for this test, deactivate it to revert to the original state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.System"}}` | Plugin state should be reverted to the original configuration if it was changed during precondition setup. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M85<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
