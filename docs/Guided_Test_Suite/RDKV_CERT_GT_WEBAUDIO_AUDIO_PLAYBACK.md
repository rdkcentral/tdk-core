## TestCase ID
RDKV_MANUAL_WEBAUDIO_06
## TestCase Name
RDKV_CERT_GT_WEBAUDIO_AUDIO_PLAYBACK

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Webaudio_manual App can initiate audio playback via the Web Audio API by activating the [play] button, producing an audible alarm sound on the DUT, as exercised by the `WEBAUDIO_manual_automated.sh` script. The test uses `org.rdk.RDKWindowManager.generateKey` navigation (Tab×6 → Enter×1 → Tab×4 → Enter×1) to select the audio playback test and activate the [play] button, with tester confirmation of audible alarm output. This test confirms that the DUT's Web Audio API audio synthesis and playback pipeline is functional through the Webaudio_manual application.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Ensure the test script (`WEBAUDIO_manual_automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) are present in the working directory of the DUT before executing the test. The `device.conf` file must be configured with the correct values required for this specific test prior to execution. | The files `WEBAUDIO_manual_automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Verify DUT connected to network | Ensure the DUT is connected to an active network (WiFi or Ethernet) prior to test execution. | The DUT must have active network connectivity so that the WebAudio App and the hosted audio files and HTML pages are accessible during the test. |
| 3 | Connect HDMI display to DUT | Connect the HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV must be connected to the DUT and the RDK UI must be visible on the screen prior to test execution. |
| 4 | Host audio files and HTML pages on server | Ensure the required audio files and inner HTML pages used by the WebAudio App are hosted and accessible on `<app_download_server>`. | The required audio test files and inner HTML pages must be hosted on the same server where the WebAudio App bundle is hosted at `<app_download_server>`, accessible from the DUT. |
| 5 | Verify WebAudio App installed | The `WEBAUDIO_manual_automated.sh` script automatically verifies if the Webaudio_manual App is installed via `AppManager.getInstalledApps` and `AppManager.isInstalled`. If not installed, the script downloads bundle `<webaudio_app_bundle>` from `<app_download_server>` and installs it via `PackageManagerRDKEMS.install`. | The Webaudio_manual App must be installed on the DUT and confirmed present in `AppManager.getInstalledApps` before the test steps execute. |
| 5 | Kill existing WebAudio App instance | The script checks for any active instance of the Webaudio_manual App via `AppManager.getLoadedApps`. If an active instance is found, it is terminated via `AppManager.killApp` before the test starts. | Any previously active instance of the Webaudio_manual App must be terminated to ensure the test starts from a clean app state. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch WebAudio App | The script launches the Webaudio_manual App via `AppManager.launchApp` with empty intent and launchArgs:<br>`curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "<isAppInstalled_appid>", "intent": "", "launchArgs": "" }}' http://localhost:9998/jsonrpc`<br><br>The script then prompts: *"Is Webaudio_manual App launched successfully [yes/no]:"* — the tester must respond `yes` to confirm. | The `AppManager.launchApp` API should return `"result":null` and the tester should confirm that the Webaudio_manual App launched successfully on the DUT. |
| 2 | Navigate to audio playback test and click play | The script sets focus on the Webaudio_manual App via `org.rdk.RDKWindowManager.setFocus`, then sends the following key sequence via `org.rdk.RDKWindowManager.generateKey`:<br>**Tab×6 → Enter×1** to select the audio playback test case<br>**Tab×4 → Enter×1** to click the **[play]** button to start audio playback | The app should navigate to the audio playback test case and the [play] button should be activated successfully. |
| 3 | Verify audio playback output | The script prompts: *"Is an (alarm sound) Audio heard when play button is pressed on Webaudio_manual App [yes/no]:"* — the tester must listen and respond `yes` if an alarm sound is audible. | The tester should confirm with `yes` that an alarm sound audio is audible when the [play] button is pressed on the Webaudio_manual App. |
| 4 | Terminate WebAudio App | The script terminates the Webaudio_manual App via `AppManager.terminateApp`:<br>`curl -H "Content-Type: application/json" --data-binary '{"jsonrpc": 2.0, "id": 15, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<isAppInstalled_appid>"}}' http://127.0.0.1:9998/jsonrpc` | The `AppManager.terminateApp` API should return `"result":null` confirming the Webaudio_manual App instance has been closed successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
