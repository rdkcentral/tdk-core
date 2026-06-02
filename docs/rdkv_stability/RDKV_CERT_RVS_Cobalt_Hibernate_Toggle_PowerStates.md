## TestCase ID
RDKV_STABILITY_68
## TestCase Name
RDKV_CERT_RVS_Cobalt_Hibernate_Toggle_PowerStates
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt hibernate state persistence across power state toggles by placing Cobalt in hibernate state and repeatedly toggling the device between standby and on power states, verifying Cobalt remains hibernated and CPU/memory usage stays within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin and org.rdk.System plugin must be available in the supported plugins list.|
|3|max_power_state_changes must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt and hibernate | Launch Cobalt via `launch_plugin`. Hibernate Cobalt via `org.rdk.RDKShell.1.suspend`. Verify Cobalt status is "suspended" (hibernated). | Cobalt should launch and enter hibernated state. |
| 4 | Power state toggle loop (repeat for max_power_state_changes iterations) | For each iteration: <br>Set preferred standby mode to LIGHT SLEEP: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPreferredStandbyMode","params":{"standbyMode":"LIGHT_SLEEP"}}` <br>Set device to standby: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"STANDBY","standbyReason":"TDKTest"}}` <br>Get power state and verify it is "STANDBY". <br>Set device back to ON: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"ON","standbyReason":"TDKTest"}}` <br>Verify Cobalt is still in hibernated/suspended state via `rdkservice_getPluginStatus`. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Power state transitions should complete successfully. Cobalt should remain in hibernated state across power toggles. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the power state stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 360

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
