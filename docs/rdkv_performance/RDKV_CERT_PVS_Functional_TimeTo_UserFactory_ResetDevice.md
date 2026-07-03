## TestCase ID
RDKV_PERFORMANCE_19
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_UserFactory_ResetDevice

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to perform a user factory reset of the device via the org.rdk.Warehouse resetDevice method is within the configured acceptable threshold, and that the reset operation completes successfully as evidenced by the deletion of a test file and a warehousereset reboot reason.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Synchronize Test Manager and device time | The time in the Test Manager and DUT should be in sync for accurate timestamp comparison. | Times should be synchronized. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate the org.rdk.Warehouse and org.rdk.System plugins. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.Warehouse"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.System"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | Both Warehouse and System plugins should be in the activated state. |
| 2 | Create a test file in /opt/ directory | SSH into the device and create a test file in the /opt/ directory. This file will be used to verify that the reset operation has cleared the partition. | The test file should be created successfully in the /opt/ directory. |
| 3 | Subscribe to factory reset done event | Register an event listener for the resetDone event to capture the time when the reset completes. <br>`{"jsonrpc": "2.0", "id": 6, "method": "org.rdk.Warehouse.1.register", "params": {"event": "resetDone", "id": "client.events.1"}}` | The event registration should succeed and the listener should be active. |
| 4 | Initiate device factory reset and record start time | Record the current system time, then send the resetDevice request via the Warehouse plugin to perform a userfactory reset. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.Warehouse.1.resetDevice", "params": {"suppressReboot": false, "resetType": "USERFACTORY"}}` | The resetDevice request should be accepted and the factory reset operation should begin. |
| 5 | Capture resetDone event and calculate reset time | Retrieve the resetDone event from the event buffer and parse its timestamp. Calculate the reset time as the difference between the event timestamp and the recorded start time. Compare against the configured threshold. | The resetDone event should be received and the time taken for the factory reset should be within the configured acceptable threshold. |
| 6 | Verify reset completion | SSH into the device and verify that the test file previously created in /opt/ has been deleted, confirming the reset was effective. Also verify the previous reboot reason is warehousereset. | The test file should no longer exist in /opt/ after the factory reset, confirming the reset was completed successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
