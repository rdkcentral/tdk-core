## TestCase ID
RDKV_MANUAL_WEBAUDIO_09
## TestCase Name
RDKV_CERT_GT_WEBAUDIO_AAC_DECODE_VBR128K

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT's WebKit browser correctly decodes an AAC audio file encoded at VBR-128kbps-44kHz using the Web Audio API's `decodeAudioData` function, and that the Webaudio_manual App displays the resulting decoded codec metadata on an inner HTML page, as exercised by the `WEBAUDIO_manual_automated.sh` script. The test navigates to the AAC decode test using `org.rdk.RDKWindowManager.generateKey` (Tab×9 → Enter×1) and confirms via tester input that decoded audio information is visible on the HTML page loaded from `<app_download_server>`. This test ensures the DUT supports AAC VBR audio decoding via the Web Audio API, which is a key requirement for WebAudio certification compliance.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`WEBAUDIO_manual_automated.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `WEBAUDIO_manual_automated.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Verify DUT connected to network | Ensure the DUT is connected to an active network (WiFi or Ethernet) prior to test execution. | The DUT must have active network connectivity so that the WebAudio App and the hosted audio files and HTML pages are accessible during the test. |
| 3 | Connect HDMI display to DUT | Connect the HDMI display/TV to the DUT and ensure the correct HDMI input source is selected on the display. | The HDMI display/TV must be connected to the DUT and the RDK UI must be visible on the screen prior to test execution. |
| 4 | Host audio files and HTML pages on server | Ensure the required AAC audio file (vbr-128kbps-44khz) and its associated inner HTML page used by the WebAudio App are hosted and accessible on `<app_download_server>`. | The required AAC test audio file and inner HTML page must be hosted on the same server where the WebAudio App bundle is hosted at `<app_download_server>`, accessible from the DUT. |
| 5 | Verify WebAudio App installed | The `WEBAUDIO_manual_automated.sh` script automatically verifies if the Webaudio_manual App is installed via `AppManager.getInstalledApps` and `AppManager.isInstalled`. If not installed, the script downloads bundle `<webaudio_app_bundle>` from `<app_download_server>` and installs it via `PackageManagerRDKEMS.install`. | The Webaudio_manual App must be installed on the DUT and confirmed present in `AppManager.getInstalledApps` before the test steps execute. |
| 6 | Kill existing WebAudio App instance | The `WEBAUDIO_manual_automated.sh` script checks for any active instance of the Webaudio_manual App via `AppManager.getLoadedApps`. If an active instance is found, it is terminated via `AppManager.killApp` before the test starts. | Any previously active instance of the Webaudio_manual App must be terminated to ensure the test starts from a clean app state. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch WebAudio App | The script launches the Webaudio_manual App via `AppManager.launchApp` with empty intent and launchArgs:<br>`curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "<isAppInstalled_appid>", "intent": "", "launchArgs": "" }}' http://localhost:9998/jsonrpc`<br><br>The script then prompts: *"Is Webaudio_manual App launched successfully [yes/no]:"* — the tester must respond `yes` to confirm. | The `AppManager.launchApp` API should return `"result":null` and the tester should confirm that the Webaudio_manual App launched successfully on the DUT. |
| 2 | Navigate to AAC decode test and verify decoded info on HTML page | The script sets focus on the Webaudio_manual App via `org.rdk.RDKWindowManager.setFocus`, then sends the following key sequence via `org.rdk.RDKWindowManager.generateKey`:<br>**Tab×9 → Enter×1** to select the AAC audio decoding test (vbr-128kbps-44khz) and load the inner HTML page.<br><br>The script then prompts: *"Is Audio decoded information of codecs loaded on a html page of Webaudio_manual App [yes/no]:"* — the tester must respond `yes` to confirm the decoded codec info is displayed. | The app should navigate to the AAC decode test, the inner HTML page should load and display the decoded audio codec information for the AAC vbr-128kbps-44khz file, and the tester should confirm with `yes`. |
| 3 | Terminate WebAudio App | The script terminates the Webaudio_manual App via `AppManager.terminateApp`:<br>`curl -H "Content-Type: application/json" --data-binary '{"jsonrpc": 2.0, "id": 15, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<isAppInstalled_appid>"}}' http://127.0.0.1:9998/jsonrpc` | The `AppManager.terminateApp` API should return `"result":null` confirming the Webaudio_manual App instance has been closed successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
