## TestCase ID
RDKV_CERT_RVS_2
## TestCase Name
RDKV_CERT_RVS_Reboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by rebooting the device a configured number of times and verifying that uptime, plugin count, plugin activation state, Ethernet interface availability, and Controller UI accessibility are all within expected bounds after each reboot.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure repeatCount in StabilityTestVariables | `repeatCount` must be set to the desired number of reboot iterations in StabilityTestVariables (default: 1000). | The repeatCount variable should be configured with a valid integer value. |
| 3 | Configure rebootwaitTime in StabilityTestVariables | `rebootwaitTime` must be set to the number of seconds to wait for the device to come back online after each reboot (default: 150 seconds). | The rebootwaitTime variable should be correctly configured. |
| 4 | Configure EthernetInterface in StabilityTestVariables | `EthernetInterface` must be set to the network interface name used on the device (default: "eth0"). | The EthernetInterface variable should match the actual interface on the DUT. |
| 5 | Configure REBOOT_PLUGINS in device config | `REBOOT_PLUGINS` must be configured in the device-specific config file with the list of plugins expected to be in activated or resumed state after every reboot. | The REBOOT_PLUGINS key should contain a valid plugin list in the device config. |
| 6 | Configure validation flags in StabilityTestVariables | Validation flags `ValidateUptime`, `ValidateInterface`, `ValidatePluginStatus`, `ValidateControllerUI`, `ValidateNoOfPlugins`, `ValidateActivatedPlugins` should be set to "Yes" to enforce strict per-iteration validation. | All validation flags should be correctly configured before test execution. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot device as pre-requisite | Reboot the device once before starting the stress test loop. The device is rebooted by invoking the Thunder Controller harakiri method and the script waits for `rebootwaitTime` (150 seconds) for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully after the pre-requisite reboot. |
| 2 | Retrieve baseline plugin count | Retrieve the total count of plugins registered in WPEFramework before any reboot iteration begins. This count is stored as the baseline for per-iteration comparison. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status"}` | Plugin count should be greater than zero and stored as baseline. |
| 3 | Retrieve baseline plugin statuses | Retrieve the name, state, and autostart flag of every registered plugin before the first reboot iteration. This snapshot is used as the baseline for post-reboot status comparison. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status"}` | Plugin status list should be retrieved successfully and must not be empty. |
| 4 | Reboot device (Per Iteration) | For each of the `repeatCount` (1000) iterations, trigger a device reboot by invoking the Controller harakiri method and wait for the device to come back online within `rebootwaitTime` (150) seconds. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should reboot and come back online within the configured wait time for every iteration. |
| 5 | Validate system uptime after reboot | After each reboot, retrieve the system uptime from DeviceInfo.1.systeminfo and verify that the uptime is less than 200 seconds, confirming a fresh reboot occurred. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | System uptime should be less than 200 seconds, confirming a fresh reboot was performed. |
| 6 | Validate plugin count after reboot | Retrieve the count of registered plugins after each reboot via Controller.1.status and compare with the pre-reboot baseline count. A mismatch is logged and the iteration is marked as FAILURE if ValidateNoOfPlugins is set to "Yes". <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status"}` | Plugin count after reboot should equal the baseline count recorded before the first iteration. |
| 7 | Validate plugin statuses after reboot | Retrieve statuses of all plugins after each reboot via Controller.1.status and compare them against the pre-reboot baseline. Any mismatch is logged with the changed plugin details. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status"}` | All plugin states should match the pre-reboot baseline snapshot. |
| 8 | Verify autostart plugins are activated | Read the `REBOOT_PLUGINS` list from the device-specific config file and verify each listed plugin is in activated or resumed state after every reboot. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<plugin_name>"}` | All plugins listed under REBOOT_PLUGINS in the device config should be in activated or resumed state after every reboot. |
| 9 | Check Ethernet interface status | Verify that the Ethernet interface (eth0) is in ENABLED state after each reboot. For non-port-80 builds, the NetworkManager.1.GetInterfaceState method is used. For Thunder port-80 builds, the NetworkControl.1.up method is queried. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "eth0"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "NetworkControl.1.up@eth0"}` | Ethernet interface should be in ENABLED state after every reboot. |
| 10 | Check Controller UI accessibility | Verify that the WPEFramework Controller UI is accessible via HTTP after each reboot. An HTTP GET request is made to the Controller UI endpoint and the response code is verified to be 200 (ACCESSIBLE). | Controller UI should return HTTP status 200 (ACCESSIBLE) after every reboot. |
| 11 | Repeat reboot validation for all iterations | Repeat Steps 4 through 10 for all `repeatCount` (1000) configured iterations. | All iterations should complete successfully with all validation checks passing. |
| 12 | Print test summary | After all iterations are completed or on early exit due to validation failure, print the total reboot count and per-category failure counts for Uptime, Interface, Controller UI, Plugin Count, Plugin Status, and Activated Plugins validations. | Summary should accurately report the number of successful and failed iterations per validation category. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 4000 mins

**Priority** : High

**Release Version** : M82<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
