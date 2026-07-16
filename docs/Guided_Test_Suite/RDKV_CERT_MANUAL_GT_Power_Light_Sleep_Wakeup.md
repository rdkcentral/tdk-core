## TestCase ID
RDKV_MANUAL_GT_POWER_01
## TestCase Name
RDKV_CERT_MANUAL_GT_Power_Light_Sleep_Wakeup

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT correctly transitions to the LIGHT SLEEP power state and subsequently wakes up to the ON state with functional AV playback restored. This test confirms the complete LIGHT SLEEP power management cycle — state entry, state verification, and wake-up recovery — meets RDK power management certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`POWER_MGMT_Automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `POWER_MGMT_Automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Connect HDMI display to DUT | Connect an HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV should be connected to the DUT and the RDK UI should be visible on the screen. |
| 3 | Verify and sign in to YouTube app | Verify that the YouTube (Cobalt) app is installed on the DUT and sign in with a valid user account prior to the test. | The YouTube (Cobalt) app must be installed on the DUT and signed in with a valid user account, with AV playback accessible, prior to test execution. |
| 4 | Verify DUT powerstate is ON | Execute the getPowerState API to verify the DUT is in ON state and the RDK UI homepage is visible on the TV. The script then prompts: *"Is RDK UI Homepage visible on TV [yes/no]:"* — respond `yes` if the RDK UI homepage is visible.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The DUT should be in ON state, the getPowerState API should return powerState=ON, and the RDK UI homepage should be visible on the TV display. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Select light sleep in Energy Saver | A visual alert blinks on the screen: *"PLEASE SELECT LIGHT SLEEP FROM ENERGY SAVER TO PROCEED TEST!!!"* — navigate manually to **Settings → Other Settings → Energy Saver** on the DUT and select **Light Sleep**. The script then prompts: *"Is Light sleep is in ticked state on Settings/Other Settings/Energy Saver [yes/no]:"* — respond `yes` once Light Sleep is selected. | Light Sleep should be selected and ticked in the Energy Saver settings on the DUT. |
| 2 | Set powerstate to LIGHT_SLEEP via API | Execute the curl command to set the DUT powerstate to LIGHT_SLEEP via the System API.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.setPowerState","params":{"powerState":"LIGHT_SLEEP","standbyReason":"For Testing"}}' http://127.0.0.1:9998/jsonrpc` | The setPowerState API should return success=true, confirming the DUT has been set to LIGHT_SLEEP state. |
| 3 | Verify DUT is in light sleep state | Execute the getPowerState API to verify the DUT is in LIGHT_SLEEP state. The script then prompts: *"Is RDK UI Homepage visible on TV [yes/no]:"* — respond `no` since the screen should be off in light sleep mode.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The getPowerState API should confirm the DUT is in LIGHT_SLEEP or STANDBY state, and the RDK UI homepage should NOT be visible on the TV display (screen off). |
| 4 | Set powerstate to ON via API | Execute the curl command to set the DUT powerstate back to ON (wake up) via the System API.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.setPowerState","params":{"powerState":"ON","standbyReason":"For Testing"}}' http://127.0.0.1:9998/jsonrpc` | The setPowerState API should return success=true, confirming the DUT has been set to ON state. |
| 5 | Verify DUT woke up successfully | Execute the getPowerState API to verify the DUT has returned to ON state. The script then prompts: *"Is RDK UI Homepage visible on TV [yes/no]:"* — respond `yes` if the RDK UI homepage is visible on the TV.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The getPowerState API should return powerState=ON and the RDK UI homepage should be visible on the TV display, confirming the DUT has woken up successfully. |
| 6 | Start immediate AV playback via YouTube | Launch the YouTube application with immediate AV playback via the AppManager launchApp API using the configured playback URL (`<yt_URL>`):<br>Command: `curl -d '{"jsonrpc":"2.0","id":2,"method":"org.rdk.AppManager.launchApp","params":{"appId":"com.rdkcentral.youtube","intent":"playback","launchArgs":"<yt_URL>"}}' http://localhost:9998/jsonrpc` | The YouTube application should launch successfully and AV playback should start immediately, confirming the DUT is fully operational after waking up from LIGHT SLEEP. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
