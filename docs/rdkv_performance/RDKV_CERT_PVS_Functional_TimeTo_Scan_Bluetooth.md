## TestCase ID
RDKV_PERFORMANCE_65
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_Scan_Bluetooth
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to complete a Bluetooth scan and discover nearby devices is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Bluetooth adapter must be available and enabled on the device.|
|3|At least one Bluetooth device should be in discovery range.|
|4|`BLUETOOTH_SCAN_THRESHOLD` must be configured in device config.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Scan Start Time | Record UTC timestamp before initiating Bluetooth scan. | Start time recorded. |
| 3 | Initiate Bluetooth Scan | Start Bluetooth device discovery scan. | Bluetooth scan started. |
| 4 | Wait for Scan Completion | Monitor until the scan completes or devices are discovered. | Bluetooth devices discovered. |
| 5 | Record Scan End Time | Record UTC timestamp after scan completes. | End time recorded. |
| 6 | Validate Time | Calculate scan time = end timestamp - start timestamp. Compare against threshold. | Time to complete Bluetooth scan is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
