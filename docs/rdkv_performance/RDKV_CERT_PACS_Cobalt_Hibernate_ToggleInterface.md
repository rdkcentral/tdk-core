## TestCase ID
RDKV_PERFORMANCE_145
## TestCase Name
RDKV_CERT_PACS_Cobalt_Hibernate_ToggleInterface
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Cobalt application persists in the Hibernated state even after the network interface is toggled between WiFi and Ethernet.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|The DUT should be connected and configured with a WiFi IP, or a WiFi Access Point with the same IP range must be available.|
|3|A Lightning application for IP-change detection should be already hosted and its URL configured in `PerformanceTestVariables` as `ip_change_app_url`.|
|4|Test Manager credentials (`tm_username`, `tm_password`) must be configured.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt and WebKitBrowser plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states are retrieved successfully. |
| 3 | Launch Cobalt | Launch Cobalt via RDKShell and verify it is in the foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launches and is in the foreground. |
| 4 | Hibernate Cobalt | Suspend Cobalt to put it into a hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"suspended"}` | Cobalt transitions to hibernated state. |
| 5 | Validate Hibernated State | Confirm Cobalt is in the hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is reported as `hibernated`. |
| 6 | Check Current Network Interface | Identify the currently active network interface (eth0 or wlan0) using the IP-change detection utility via `org.rdk.NetworkManager.1.getActiveInterface` or equivalent network status API. | Current network interface is determined. |
| 7 | Toggle Network Interface | Toggle the network interface from the current one to the other (e.g., WiFi to Ethernet or vice versa) using `org.rdk.Network.1.setInterfaceEnabled` API: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.Network.1.setInterfaceEnabled","params":{"interface":"<new_interface>","enabled":true}}` | Network interface toggle is initiated and confirmed. |
| 8 | Validate Hibernated State Persists | After the network interface toggle, re-check Cobalt state to confirm it remained hibernated: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt remains in `hibernated` state after interface toggle. |
| 9 | Revert Network Interface | Restore the original network interface setting. | Network interface reverted to original state. |
| 10 | Deactivate Cobalt | Deactivate the Cobalt plugin to clean up: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Cobalt is deactivated successfully. |
| 11 | Revert Plugin Status | Restore original plugin states as captured before the test. | Plugins reverted to their original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 20

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
