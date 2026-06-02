## TestCase ID
RDKV_STABILITY_75
## TestCase Name
RDKV_CERT_RVS_Cobalt_Hibernate_Toggle_PowerStates_Lifecycle
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt lifecycle management across power state toggles by repeatedly hibernating Cobalt, toggling power states, restoring Cobalt from hibernate, and executing lifecycle operations, verifying stability and resource usage throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin and org.rdk.System plugin must be available in the supported plugins list.|
|3|max_power_state_changes and cobalt_test_url must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt | Launch Cobalt via `launch_plugin` using `org.rdk.RDKShell.1.launch`. | Cobalt should launch successfully. |
| 4 | Hibernate, power toggle, and lifecycle loop (repeat for max_power_state_changes iterations) | For each iteration: <br>Hibernate Cobalt via `org.rdk.RDKShell.1.suspend`. <br>Verify Cobalt is suspended. <br>Set preferred standby mode to LIGHT SLEEP: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPreferredStandbyMode","params":{"standbyMode":"LIGHT_SLEEP"}}` <br>Toggle device to STANDBY: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"STANDBY","standbyReason":"TDKTest"}}` <br>Toggle device back to ON: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"ON","standbyReason":"TDKTest"}}` <br>Restore Cobalt from hibernate via `org.rdk.RDKShell.1.restoreApp`. <br>Execute lifecycle management: launch → set video URL via deeplink → validate proc entry → suspend → resume → destroy. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Power state toggles and Cobalt hibernate/restore/lifecycle should all succeed. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the complex stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 720

**Priority** : High

**Release Version** : M131<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
