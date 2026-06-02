## TestCase ID
RDKV_STABILITY_14
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
To validate device stability by continuously toggling the power state between ON and STANDBY for a configured number of iterations, verifying the power state change event is received and resource usage remains within acceptable limits after each toggle.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`max_power_state_changes` must be configured in StabilityTestVariables with the desired number of power state toggle iterations (default: 1000).|
|3|org.rdk.System and DeviceInfo plugins should be available in the build. Plugins present in `SUPPORTED_PLUGINS` in the device-specific config file will be used.|
|4|`SUPPORTED_PLUGINS` must be configured in the device-specific config file to indicate which plugins are available on the DUT.|
|5|Device should be rebooted before test execution if `PRE_REQ_REBOOT` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pre-requisite Reboot | Conditionally reboot the device before the test. `pre_requisite_reboot()` reads the `PRE_REQ_REBOOT` key from the device-specific config file. If set to "Yes", the device is rebooted via `Controller.1.harakiri` and the script waits 150 seconds for it to come back online. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"} | Device should come back online successfully if reboot was triggered. |
| 2 | Check Device Pre-condition State | Validate initial CPU and memory resource usage before the stress test begins using `check_device_state()`. The DeviceInfo plugin is activated if not already active, `rdkservice_validateResourceUsage` is invoked to check resource usage, and the plugin state is reverted afterward. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_validateResourceUsage"} | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Check and Activate Required Plugins | Read `SUPPORTED_PLUGINS` from device-specific config to determine which of org.rdk.System and DeviceInfo are present on the DUT. Check the status of each applicable plugin. If any are not in the required activated state, activate them via `rdkservice_setPluginStatus`. Original states are saved for revert on exit. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.System"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}} | org.rdk.System and DeviceInfo (where supported) should be in activated state. |
| 4 | Register for Power State Change Event | Create a WebSocket event listener to subscribe to the `onSystemPowerStateChanged` event from org.rdk.System. The listener connects to the device's Thunder JSON-RPC endpoint and registers using the event registration payload. <br>{"jsonrpc": "2.0", "id": 5, "method": "org.rdk.System.1.register", "params": {"event": "onSystemPowerStateChanged", "id": "client.events.1"}} | Event listener should be registered and active, ready to receive power state change notifications. |
| 5 | Get Current Power State | Retrieve the current power state of the device before starting the toggle loop. This value is stored as the initial state for revert at the end of the test. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.getPowerState"} | Current power state should be retrieved successfully (e.g., ON, STANDBY, LIGHT_SLEEP, or DEEP_SLEEP). |
| 6 | Toggle Power State (Per Iteration) | For each of the `max_power_state_changes` (1000) iterations, determine the new target state: if the current state is STANDBY, DEEP_SLEEP, or LIGHT_SLEEP, toggle to ON; otherwise toggle to STANDBY. Set the new power state via `org.rdk.System.1.setPowerState` and wait up to 60 seconds for the `onSystemPowerStateChanged` event to be received from the event listener. If the expected event is not received within 60 seconds, the iteration is marked as FAILURE and the loop exits. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "STANDBY", "standbyReason": "APIUnitTest"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "ON", "standbyReason": "APIUnitTest"}} | setPowerState should return SUCCESS and the `onSystemPowerStateChanged` event with the expected new power state should be received within 60 seconds for every iteration. |
| 7 | Verify New Power State | After the power state change event is confirmed, verify the actual current power state by querying `org.rdk.System.1.getPowerState` and confirming it matches the expected new state. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.getPowerState"} | The reported power state should match the newly set target state (ON or STANDBY). |
| 8 | Validate Resource Usage (Per Iteration) | After each successful power state toggle and verification, invoke `rdkservice_validateResourceUsage` to measure current CPU load and memory usage. The values are recorded per iteration and written to a JSON log file (`CPUMemoryInfo.json`) at the end of the test. If resource usage returns an ERROR, the test is marked FAILURE and the loop exits. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_validateResourceUsage"} | CPU and memory usage should be within the acceptable threshold in every iteration. |
| 9 | Revert Power State | After completing all iterations (or on early exit), if the current power state differs from the initial power state recorded in Step 5, revert the device to its original power state. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "<initial_power_state>", "standbyReason": "APIUnitTest"}} | Device power state should be successfully restored to its initial value. |
| 10 | Revert Plugin Statuses | If any plugins were activated during Step 3, revert them back to their original states using `set_plugins_status`. The event listener WebSocket connection is also disconnected. | Plugin states should be restored to their pre-test values and the event listener should be cleanly disconnected. |
| 11 | Check Device Post-condition State | Validate CPU and memory resource usage after the stress test completes using `check_device_state()` to confirm the device remains in a healthy state. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_validateResourceUsage"} | CPU and memory usage should be within the expected range after all power state toggle iterations complete. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 360

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
