## TestCase ID
RDKV_PERFORMANCE_13
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_ColdBoot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for a cold boot of the device — measured from the moment of reboot initiation to when WPEFramework starts — is within the configured acceptable threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure COLDBOOT_IDLE_WAIT_TIME in device config | `COLDBOOT_IDLE_WAIT_TIME` must be set in seconds in the device config file to define how long to keep the device idle before rebooting. | The idle wait time should be configured correctly. |
| 4 | Configure REBOOT_WAIT_TIME in device config | `REBOOT_WAIT_TIME` must be set in seconds in the device config file to allow the device to come back online after the reboot. | The reboot wait time should be configured correctly. |
| 5 | Configure COLDBOOT_TIME_THRESHOLD_VALUE in device config | `COLDBOOT_TIME_THRESHOLD_VALUE` must be set to the acceptable cold boot duration in milliseconds in the device config file. | The threshold value should be configured correctly. |
| 6 | Configure THRESHOLD_UPTIME and THRESHOLD_OFFSET in device config | `THRESHOLD_UPTIME` and `THRESHOLD_OFFSET` must be configured in the device config file. | Both values should be configured correctly. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Keep device in idle state | Allow the device to remain idle for the configured `COLDBOOT_IDLE_WAIT_TIME` seconds before triggering the cold boot. | The device should remain in idle state for the configured duration. |
| 2 | Reboot the device and record start time | Record the current system time, then trigger a device reboot via the Controller harakiri method and wait for the device to come back online within `REBOOT_WAIT_TIME`. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should reboot and come back online successfully within the configured wait time. |
| 3 | Validate device uptime after reboot | Verify that the device uptime is less than the configured `THRESHOLD_UPTIME`, confirming the device has undergone a cold boot. | The device uptime should be less than `THRESHOLD_UPTIME` seconds, confirming a successful cold boot. |
| 4 | Extract WPEFramework start time from system log | SSH into the device and retrieve the log line containing WPEFramework start information from the system log: <br>`cat /opt/logs/system.log \| grep -inr Started.*wpeframework \| head -n 1` | The WPEFramework started log entry should be present in the system log after the cold boot. |
| 5 | Calculate and validate cold boot time | Parse the timestamp from the WPEFramework start log entry and calculate the cold boot time as the difference between the WPEFramework start time and the system start time recorded before reboot. Compare against (`COLDBOOT_TIME_THRESHOLD_VALUE` + `THRESHOLD_OFFSET`). | The cold boot time should be within the configured threshold limit (`COLDBOOT_TIME_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` milliseconds). |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 360 mins

**Priority** : High

**Release Version** : M96<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
