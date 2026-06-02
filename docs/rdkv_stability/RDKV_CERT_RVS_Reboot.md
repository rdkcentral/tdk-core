## TestCase ID
RDKV_STABILITY_02
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
To validate device stability by rebooting the device a configured number of times and verifying uptime, plugin count, plugin status, autostart plugin activation, Ethernet interface availability, and Controller UI accessibility after each reboot.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`repeatCount` in StabilityTestVariables should be set to the desired number of reboot iterations (default: 1000).|
|3|`rebootwaitTime` in StabilityTestVariables should be configured with the number of seconds to wait for the device to come back online after each reboot (default: 150 seconds).|
|4|`EthernetInterface` in StabilityTestVariables should be set to the correct network interface name used on the device (default: "eth0").|
|5|`REBOOT_PLUGINS` must be configured in the device-specific config file with the list of plugins expected to be in activated or resumed state after every reboot.|
|6|Validation flags in StabilityTestVariables (`ValidateUptime`, `ValidateInterface`, `ValidatePluginStatus`, `ValidateControllerUI`, `ValidateNoOfPlugins`, `ValidateActivatedPlugins`) should be set to "Yes" to enforce strict per-iteration validation.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pre-requisite Reboot | Reboot the device once as a pre-requisite before starting the stress test loop. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_rebootDevice", "params": {"waitTime": 150}} | Device should come back online successfully after the pre-requisite reboot. |
| 2 | Get Baseline Plugin Count | Retrieve the total number of plugins registered in WPEFramework before any reboot iteration begins. This count is stored as the baseline for per-iteration comparison. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status"} | Plugin count should be greater than zero. |
| 3 | Get Baseline Plugin Statuses | Retrieve the name, state, and autostart flag of every registered plugin before the first reboot iteration. This snapshot is used as the baseline for post-reboot status comparison. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status"} | Plugin status list should be retrieved successfully and must not be empty. |
| 4 | Reboot Device (Per Iteration) | For each of the `repeatCount` (1000) iterations, trigger a device reboot and wait for the device to come back online. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "rdkservice_rebootDevice", "params": {"waitTime": 150}} | Device should reboot and come back online within the configured wait time (150 seconds). |
| 5 | Validate Uptime After Reboot | After each reboot, retrieve the system uptime from DeviceInfo to confirm the device has performed a fresh reboot. The `validateUptime()` function checks that uptime is between 0 and 200 seconds. If `ValidateUptime` is "Yes", the test exits on failure. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | System uptime should be less than 200 seconds, confirming a fresh reboot. |
| 6 | Validate Plugin Count After Reboot | Retrieve the number of registered plugins after each reboot and compare with the pre-reboot baseline using `validateNoOfPlugins()`. If `ValidateNoOfPlugins` is "Yes", the test exits when a mismatch is found. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status"} | Plugin count after reboot should equal the baseline count recorded before the first iteration. |
| 7 | Validate Plugin Statuses After Reboot | Retrieve statuses of all plugins after each reboot and compare them against the pre-reboot baseline using `validatePluginStatus()`. Any mismatch is logged with details of changed plugins. If `ValidatePluginStatus` is "Yes", the test exits on mismatch. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status"} | All plugin states should match the pre-reboot baseline snapshot. |
| 8 | Verify Autostart Plugins Are Activated | Read the `REBOOT_PLUGINS` list from the device-specific config file and verify each listed plugin is in "activated" or "resumed" state using `checkPluginsActivated()`. If `ValidateActivatedPlugins` is "Yes", the test exits on failure. | All plugins listed under REBOOT_PLUGINS in device config should be in activated or resumed state after every reboot. |
| 9 | Check Ethernet Interface Status | Verify that the Ethernet interface (eth0) is up after each reboot using `getIFStatus()`. For non-port-80 builds: queries `org.rdk.NetworkManager.1.GetInterfaceState`. For Thunder port-80 builds: queries `NetworkControl.1.up@eth0`. If `ValidateInterface` is "Yes", the test exits when the interface is not enabled. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.NetworkManager.1.GetInterfaceState", "params": {"interface": "eth0"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "NetworkControl.1.up@eth0"} | Ethernet interface should be in ENABLED state after every reboot. |
| 10 | Check Controller UI Accessibility | Verify that the WPEFramework Controller UI is accessible via HTTP after each reboot using `getUIStatus()`. An HTTP GET is made to `http://<deviceIP>:<port>/Service/Controller/UI` and the response code is checked. If `ValidateControllerUI` is "Yes", the test exits when not accessible. | Controller UI should return HTTP status 200 (ACCESSIBLE) after every reboot. |
| 11 | Print Test Summary | After all `repeatCount` (1000) iterations are completed, or upon early exit due to validation failure, `getSummary()` prints the total reboots completed and the number of failures per validation category: Uptime, Interface, Controller UI, Plugin Count, Plugin Status, and Activated Plugins. | Summary should report the number of successful and failed iterations for each validation check. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 4000

**Priority** : High

**Release Version** : M82<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
