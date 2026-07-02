## TestCase ID
RDKV_STABILITY_4
## TestCase Name
RDKV_CERT_RVS_Toggle_PowerStates

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by continuously toggling the power state between ON and STANDBY for a configured number of iterations, verifying that the onSystemPowerStateChanged event is received and that CPU and memory resource usage remain within acceptable limits after each power state toggle.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure max_power_state_changes in StabilityTestVariables | `max_power_state_changes` must be set to the desired number of power state toggle iterations in StabilityTestVariables (default: 1000). | The max_power_state_changes variable should be configured with a valid integer value. |
| 4 | Configure SUPPORTED_PLUGINS in device config | `SUPPORTED_PLUGINS` must be configured in the device-specific config file listing which plugins are available on the DUT. Required plugins org.rdk.System and DeviceInfo must be present. | The SUPPORTED_PLUGINS list should include org.rdk.System and DeviceInfo. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration key from the device-specific config file. If set to "Yes", the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully if reboot was configured. |
| 2 | Validate device resource usage before test | Check device state and resource usage before starting the stress test. The DeviceInfo plugin is queried, activated if needed, and DeviceInfo.1.systeminfo is invoked to measure CPU and memory usage. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Verify and activate required plugins | Read `SUPPORTED_PLUGINS` from the device-specific config to determine which of org.rdk.System and DeviceInfo are present. Check the current activation state of each applicable plugin and activate any that are not in the required state. Original states are saved for revert on exit. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.System"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}` | org.rdk.System and DeviceInfo (where supported) should be in activated state before the test loop begins. |
| 4 | Subscribe to power state change event | Create a WebSocket event listener to subscribe to the onSystemPowerStateChanged event from org.rdk.System. <br>`{"jsonrpc": "2.0", "id": 5, "method": "org.rdk.System.1.register", "params": {"event": "onSystemPowerStateChanged", "id": "client.events.1"}}` | Event subscription should be established successfully. |
| 5 | Retrieve current power state | Retrieve the current power state of the device before starting the toggle loop. The value is stored as the initial state for revert at test completion. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.getPowerState"}` | Current power state should be retrieved successfully (e.g., ON, STANDBY, LIGHT_SLEEP, or DEEP_SLEEP). |
| 6 | Toggle power state to new target state (Per Iteration) | For each of the `max_power_state_changes` (1000) iterations, determine the new target state: if the current state is STANDBY, DEEP_SLEEP, or LIGHT_SLEEP, toggle to ON; otherwise toggle to STANDBY. Set the new power state via org.rdk.System.1.setPowerState. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "STANDBY", "standbyReason": "APIUnitTest"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "ON", "standbyReason": "APIUnitTest"}}` | setPowerState should return SUCCESS for each iteration. |
| 7 | Validate onSystemPowerStateChanged event received | Wait up to 60 seconds for the onSystemPowerStateChanged event to be received from the WebSocket event listener. The expected event content is checked to confirm the new power state (STANDBY/LIGHT_SLEEP or ON) is reported. If not received within 60 seconds, the iteration is marked as FAILURE and the loop exits. | The onSystemPowerStateChanged event should be received within 60 seconds with the correct new power state value. |
| 8 | Verify new power state via getPowerState | After the power state change event is confirmed, query org.rdk.System.1.getPowerState to verify the device is reporting the expected new power state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.getPowerState"}` | The reported power state should match the newly set target state (ON or STANDBY). |
| 9 | Validate resource usage after power state toggle | After each successful power state toggle and verification, measure the current CPU load and memory usage via DeviceInfo.1.systeminfo. The result is recorded per iteration and written to a CPUMemoryInfo JSON log file. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the acceptable threshold after every power state toggle iteration. |
| 10 | Repeat power state toggle for all iterations | Repeat Steps 6 through 9 for all `max_power_state_changes` (1000) configured iterations. | All iterations should complete successfully with the power state toggle event received and resource usage within acceptable limits. |
| 11 | Revert power state to initial value | After completing all iterations or on early exit, if the current power state differs from the initial state recorded in Step 5, revert the device to its original power state via org.rdk.System.1.setPowerState. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "<initial_power_state>", "standbyReason": "APIUnitTest"}}` | Device power state should be successfully restored to its initial value. |
| 12 | Revert plugin statuses | If any plugins were activated during Step 3, revert them back to their original states via the Controller API. The event listener WebSocket connection is also disconnected. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.deactivate", "params": {"callsign": "<plugin_name>"}}` | Plugin states should be restored to their pre-test values and the event listener should be cleanly disconnected. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 360 mins

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
