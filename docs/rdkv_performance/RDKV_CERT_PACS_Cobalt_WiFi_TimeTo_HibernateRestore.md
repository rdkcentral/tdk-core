## TestCase ID
RDKV_PERFORMANCE_147
## TestCase Name
RDKV_CERT_PACS_Cobalt_WiFi_TimeTo_HibernateRestore
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to hibernate and restore the Cobalt application while connected to a WiFi network is within the expected threshold limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|The DUT should be connected to a WiFi Access Point or WiFi IP should be configured in Test Manager.|
|3|A Lightning application for IP-change detection should be hosted and available.|
|4|`COBALT_HIBERNATE_TIME_THRESHOLD_VALUE` and `COBALT_RESTORE_TIME_THRESHOLD_VALUE` must be configured in the device config file.|
|5|Time in Test Manager and DUT should be in sync.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Current Interface | Determine the current active network interface (eth0 or wlan0) using the IP-change detection utility. | Current interface is identified. |
| 3 | Switch to WiFi (if needed) | If the current interface is Ethernet (eth0), switch to WiFi by enabling the wlan0 interface: connect to SSID, launch IP-change detection Lightning app in WebKitBrowser, and set WiFi as the default interface. | DUT is connected via WiFi; IP-change detection app confirms connection. |
| 4 | Check Plugin Status | Check the current state of Cobalt plugin and ensure it is in resumed state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Plugin state retrieved. |
| 5 | Subscribe to onHibernated and onRestored Events | Register a WebSocket listener for both `onHibernated` and `onRestored` events from RDKShell: <br>`{"jsonrpc":"2.0","id":7,"method":"org.rdk.RDKShell.1.register","params":{"event":"onHibernated","id":"client.events.1"}}`<br>`{"jsonrpc":"2.0","id":8,"method":"org.rdk.RDKShell.1.register","params":{"event":"onRestored","id":"client.events.1"}}` | Event subscriptions established. |
| 6 | Hibernate Cobalt (Timed) | Save current system time and suspend Cobalt to initiate hibernation over WiFi: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"suspended"}` | Suspend call sent; hibernate start time recorded. |
| 7 | Validate Hibernated State | Verify Cobalt transitions to hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `hibernated`. |
| 8 | Capture Hibernate Time | Retrieve the `onHibernated` event from the listener and validate the time taken to hibernate against `COBALT_HIBERNATE_TIME_THRESHOLD_VALUE`. | Hibernate time is within the configured threshold. |
| 9 | Restore Cobalt (Timed) | Save current system time and restore Cobalt from hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"resumed"}` | Restore call sent; restore start time recorded. |
| 10 | Validate Suspended State | Verify Cobalt transitions to suspended state after restore: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `suspended`. |
| 11 | Capture Restore Time | Retrieve the `onRestored` event and validate the restore time against `COBALT_RESTORE_TIME_THRESHOLD_VALUE`. | Restore time is within the configured threshold. |
| 12 | Revert Network Interface | Restore the original network interface if it was changed. | Network interface reverted. |
| 13 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
