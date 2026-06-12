## TestCase ID
RDKV_PERFORMANCE_18
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_BluetoothConnection
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when a Bluetooth connection is established on the device.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Bluetooth adapter should be available and enabled on the device.|
|3|A target Bluetooth device should be in range and pairable.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Capture Baseline Resource Usage | Record CPU and memory usage before establishing Bluetooth connection. | Baseline recorded. |
| 3 | Initiate Bluetooth Pairing | Initiate Bluetooth pairing with a target device. | Bluetooth pairing initiated. |
| 4 | Establish Bluetooth Connection | Complete the Bluetooth connection. | Bluetooth connection established. |
| 5 | Capture Resource Usage During Connection | Record CPU and memory usage while Bluetooth connection is active. | Resource data captured. |
| 6 | Validate Resource Usage | Verify CPU load and memory usage during Bluetooth connection are within acceptable limits. | CPU load and memory usage are within the expected limits. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
