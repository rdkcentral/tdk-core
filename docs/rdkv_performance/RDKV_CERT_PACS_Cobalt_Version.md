## TestCase ID
RDKV_PERFORMANCE_37
## TestCase Name
RDKV_CERT_PACS_Cobalt_Version
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the installed version of the Cobalt application matches the expected current version configured in the device config file.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|SSH access to the DUT should be functional.|
|3|`CURRENT_COBALT_VERSION` must be configured in the device config file.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Get SSH Parameters | Retrieve SSH connection parameters (method, credentials) required to access the DUT. | SSH parameters retrieved successfully. |
| 3 | Check Cobalt Version via SSH | Execute the Cobalt version command on the DUT via SSH and parse the output: <br>`cobalt_bin --version \| grep Cobalt` | Cobalt version string is returned in the output. |
| 4 | Validate Cobalt Version | Compare the retrieved Cobalt version string to the `CURRENT_COBALT_VERSION` value in the device config file. If the version command does not return output, launch Cobalt via RDKShell and check wpeframework logs for the version: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | The Cobalt version matches the configured `CURRENT_COBALT_VERSION`. |
| 5 | Revert Plugin Status | Restore original plugin states if Cobalt was launched during validation. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M88<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
