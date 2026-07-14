## TestCase ID
RDKV_PERFORMANCE_11
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_ChangeResolution

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to change the display resolution via the DisplaySettings plugin is within the acceptable configured threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure CHANGE_RESOLUTION_VALUE in device config | `CHANGE_RESOLUTION_VALUE` must be set to the target resolution (e.g., 1080p) to change to during the test in the device-specific config file. | The resolution value should be configured and must differ from the current active resolution. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate the DisplaySettings plugin | Query the DisplaySettings plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DisplaySettings"}` <br><br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}` | The org.rdk.DisplaySettings plugin should be in the activated state. |
| 2 | Retrieve connected video displays | Get the list of connected video displays to identify the active display for resolution change. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}` | The connected video displays list should be returned successfully. |
| 3 | Get current resolution of the display | Retrieve the current resolution of the first connected display to confirm it differs from the target resolution. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<first_connected_display>"}}` | The current resolution of the display should be returned successfully. |
| 4 | Subscribe to resolutionChanged event | Register an event listener for the resolutionChanged event to capture the timestamp when the resolution change is applied. <br>`{"jsonrpc": "2.0", "id": 6, "method": "org.rdk.DisplaySettings.1.register", "params": {"event": "resolutionChanged", "id": "client.events.1"}}` | The event registration should succeed and the listener should be active. |
| 5 | Set the new resolution and measure time | Record the current system time, then set the display resolution to the configured `CHANGE_RESOLUTION_VALUE`. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<first_connected_display>", "resolution": "<CHANGE_RESOLUTION_VALUE>"}}` | The resolution change request should be accepted successfully. |
| 6 | Validate resolution change time | Capture the timestamp from the resolutionChanged event and calculate the time taken as the difference between the event timestamp and the start time recorded before the resolution set call. Compare against the configured threshold. | The time taken to change resolution should be within the configured acceptable threshold limit. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M96<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
