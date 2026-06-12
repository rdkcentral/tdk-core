## TestCase ID
RDKV_PERFORMANCE_62
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_Scan_WiFi
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to complete a WiFi network scan and discover available access points is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WiFi adapter must be available and enabled on the device.|
|3|At least one WiFi access point should be in range.|
|4|`WIFI_SCAN_THRESHOLD` must be configured in device config.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Scan Start Time | Record UTC timestamp before initiating WiFi scan. | Start time recorded. |
| 3 | Initiate WiFi Scan | Start WiFi network scan to discover available access points. | WiFi scan started. |
| 4 | Wait for Scan Completion | Monitor until the WiFi scan completes and access points are listed. | WiFi access points discovered. |
| 5 | Record Scan End Time | Record UTC timestamp after scan completes. | End time recorded. |
| 6 | Validate Time | Calculate WiFi scan time = end timestamp - start timestamp. Compare against threshold. | Time to complete WiFi scan is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
