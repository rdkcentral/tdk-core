## TestCase ID
RDKV_MANUAL_SYSTEM_03
## TestCase Name
RDKV_CERT_MANUAL_System_Wpeframework_Process_Status

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the WPEFramework processes are running and operating as expected on the DUT. This test confirms that the WPEFramework processes are active in the process list without errors, ensuring WPEFramework service health meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Ensure console access to DUT  | Ensure that either SSH or serial console access to the DUT is available to execute commands. | SSH or serial console access should be available and functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Access device serial console  | Access the device serial console from the PC/laptop using the configured serial terminal utility. | The serial console should be accessible, and the device prompt should be displayed.|
| 2 |  Validate WPE process status  | Execute the command to validate the WPE process status.<br>Command: `ps -ef \| grep "WPE"` | All the required WPE processes should be running:<br>- WPEProcess<br>- WPEFramework<br>- WPENetworkProcess<br>- WPEWebProcess|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
