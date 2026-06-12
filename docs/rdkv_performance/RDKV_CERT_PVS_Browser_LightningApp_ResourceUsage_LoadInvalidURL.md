## TestCase ID
RDKV_PERFORMANCE_143
## TestCase Name
RDKV_CERT_PVS_Browser_LightningApp_ResourceUsage_LoadInvalidURL
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that resource usage remains acceptable and no crash is observed when an invalid URL is loaded in the LightningApp plugin.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|LightningApp plugin should be available and activatable on the device.|
|3|An invalid URL must be configured in `BrowserPerformanceVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Verify and activate LightningApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@LightningApp"}` | LightningApp plugin is in activated state. |
| 3 | Load Invalid URL in LightningApp | Set an invalid URL in LightningApp: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"LightningApp.1.url","params":{"url":"<invalid_url>"}}` | URL set (load may fail gracefully). |
| 4 | Validate Resource Usage | Capture and validate CPU load and memory usage after loading the invalid URL. | Resource usage is within acceptable limits. |
| 5 | Validate LightningApp Stability | Verify LightningApp plugin is still in activated and responsive state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@LightningApp"}` | LightningApp is stable and no crash is observed. |
| 6 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M123<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
