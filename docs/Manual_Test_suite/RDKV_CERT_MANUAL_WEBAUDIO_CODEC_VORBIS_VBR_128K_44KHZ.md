## TestCase ID
RDKV_MANUAL_WEBAUDIO_13
## TestCase Name
RDKV_CERT_MANUAL_WEBAUDIO_CODEC_VORBIS_VBR_128K_44KHZ

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT can successfully decode a Vorbis audio file (VBR 128 kbps, 44 kHz) using the WebAudio API and report the correct codec metadata.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned. |
| 3 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 4 | Upload WebAudio test files and bolt package to server | Copy all the WebAudio HTML test files and the WebAudio Test bolt package to an accessible server (replace <Server_URL> with the actual server address available in your test environment). | The WebAudio HTML test files and WebAudio Test bolt package should be available and accessible on the server. |
| 5 | Download WebAudio test package via API | Download the WebAudio Test bolt package from the server using the PackageManagerRDKEMS.download API.<br>Command: `curl -d '{ "jsonrpc": 2.0, "id": 2, "method": "org.rdk.PackageManagerRDKEMS.download", "params": { "url": "<Bolt_Package_URL>" } }' http://127.0.0.1:9998/jsonrpc` | The download API request should succeed and the WebAudio Test bolt package should be downloaded to the DUT. |
| 6 | Verify package in /opt/CDL/ | Verify that the downloaded package is available in the /opt/CDL/ directory of the DUT.<br>Command: `ls -lh /opt/CDL/` | The downloaded WebAudio Test bolt package should be listed in the /opt/CDL/ directory of the DUT. |
| 7 | List packages and get package ID | Verify that the package is listed on the DUT and obtain the package ID from the response.<br>Command: `curl -d '{ "jsonrpc": 2.0, "id": 8, "method": "org.rdk.PackageManagerRDKEMS.listPackages" }' http://127.0.0.1:9998/jsonrpc` | The WebAudio Test package should be listed and the package ID should be retrievable from the response. |
| 8 | Install WebAudio test package | Install the downloaded WebAudio Test package using the PackageManagerRDKEMS.install API.<br>Command: `curl -d '{ "jsonrpc": 2.0, "id": 7, "method": "org.rdk.PackageManagerRDKEMS.install", "params": { "packageId": "<package_id>", "version": "0.1.0", "additionalMetadata": [ {"name": "type", "value": "native/dac-app"} ], "fileLocator": "/opt/CDL/<package_name>" } }' http://127.0.0.1:9998/jsonrpc` | The WebAudio Test package should be installed successfully on the DUT. |
| 9 | Verify package state as INSTALLED | Verify that the installed package state is "INSTALLED".<br>Command: `curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 8, "method": "org.rdk.PackageManagerRDKEMS.packageState", "params": {"packageId": "<package_id>", "version": "<version>"}}' http://127.0.0.1:9998/jsonrpc` | The package state should be reported as "INSTALLED" in the API response. |
| 10 | Verify WebAudio test app on home screen | Verify that the WebAudio Test App is available and listed under the My Apps section/row of the RDK UI Home screen, ready to launch. | The WebAudio Test App should be visible in the My Apps section of the RDK UI Home screen and ready to launch. |
| 11 | Launch app if not visible | If the WebAudio Test App is not visible in the My Apps section, launch the installed app using the org.rdk.AppManager.1.launchApp API.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":"3","method": "org.rdk.AppManager.1.launchApp", "params":{"appId":"<App_id>"}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The WebAudio Test App should launch successfully and be accessible from the RDK UI Home screen. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch WebAudio test app | Select the WebAudio Test App tile from the My Apps section of the RDK UI Home screen and press Enter/OK. If the tile is not visible, launch via the org.rdk.AppManager.1.launchApp API.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":"3","method":"org.rdk.AppManager.1.launchApp","params":{"appId":"<App_id>"}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The WebAudio Test App should launch successfully on top of the RDK UI Home screen with the default WebAudio Test page. The API response should be: {"jsonrpc":"2.0","id":3,"result":null} |
| 2 | Navigate to TC_WEBAUDIO_MANUAL_13 tab and verify codec info | Navigate to the TC_WEBAUDIO_MANUAL_13 tab using the Tab key and press Enter. | The TC_WEBAUDIO_MANUAL_13 HTML page should load correctly, displaying the decoded audio codec information. Expected output: Audio Codec Information: Sample Rate: 44100 Hz, Channels: 1, Duration: 0.2510657596371882 seconds |
| 3 | Close WebAudio test app | Close the WebAudio Test App by pressing the Back key on the remote. If Back key does not close it, terminate using the terminateApp API.<br>Command: `curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 15, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<App_Id>"}}' http://127.0.0.1:9998/jsonrpc` | The WebAudio Test App should terminate gracefully and the RDK UI Home screen should be visible on the display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
