## TestCase ID
RDKV_MANUAL_IMG_FORMAT_01
## TestCase Name
RDKV_CERT_MANUAL_Img_Format_PNG_Support_Verify

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the PNG image format is correctly rendered and displayed by the DUT via the Browser Test application. This test exercises the WPE browser image rendering pipeline and the SVG/HTML test page to validate decoding and display of the target image format. The test confirms that the Browser Test App should terminate gracefully and the RDK UI Home screen should be visible on the TV/display.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 2 |  Pair bluetooth remote  | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 3 |  Connect DUT to network  | Connect the DUT to an active network via Wi-Fi or Ethernet. | The DUT should be connected to an active network with a valid IP address assigned. |
| 4 |  Upload browser test app to server  | Copy the Browser Test HTML application and the Browser Test bolt package to an accessible server (replace `<Server_URL>` with the actual server address available in your test environment). | The Browser Test HTML application and Browser Test bolt package should be available and accessible on the server. |
| 5 |  Download bolt package via API  | Download the Browser Test bolt package from the server using the PackageManagerRDKEMS.download API.<br>Command: `curl -d '{ "jsonrpc": 2.0, "id": 2, "method": "org.rdk.PackageManagerRDKEMS.download", "params": { "url": "<Bolt_Package_URL>" } }' http://127.0.0.1:9998/jsonrpc` | The download API request should succeed and the Browser Test bolt package should be downloaded to the DUT. |
| 6 |  Verify package in /opt/cdl/  | Verify that the downloaded package is available in the /opt/CDL/ directory of the DUT.<br>Command: `ls -lh /opt/CDL/` | The downloaded Browser Test bolt package should be listed in the /opt/CDL/ directory of the DUT. |
| 7 |  List packages and get package ID  | Verify that the Browser Test package is listed on the DUT and obtain the package ID from the response.<br>Command: `curl -d '{ "jsonrpc": 2.0, "id": 8, "method": "org.rdk.PackageManagerRDKEMS.listPackages" }' http://127.0.0.1:9998/jsonrpc` | The Browser Test package should be listed and the package ID should be retrievable from the response. |
| 8 |  Install browser test package  | Install the downloaded Browser Test package using the PackageManagerRDKEMS.install API.<br>Command: `curl -d '{ "jsonrpc": 2.0, "id": 7, "method": "org.rdk.PackageManagerRDKEMS.install", "params": { "packageId": "<package_id>", "version": "0.1.0", "additionalMetadata": [ {"name": "type", "value": "native/dac-app"} ], "fileLocator": "/opt/CDL/<package_name>" } }' http://127.0.0.1:9998/jsonrpc` | The Browser Test package should be installed successfully on the DUT. |
| 9 |  Verify package state as INSTALLED  | Verify that the installed package state is "INSTALLED".<br>Command: `curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 8, "method": "org.rdk.PackageManagerRDKEMS.packageState", "params": {"packageId": "<package_id>", "version": "<version>"}}' http://127.0.0.1:9998/jsonrpc` | The package state should be reported as "INSTALLED" in the API response. |
| 10 |  Verify browser test app on Home screen  | Verify that the Browser Test App is available and listed under the My Apps section/row of the RDK UI Home screen, ready to launch. | The Browser Test App should be visible in the My Apps section of the RDK UI Home screen and should be ready to launch. |
| 11 |  Launch app if not visible  | If the Browser Test App is not visible in the My Apps section, launch the installed app using the org.rdk.AppManager.1.launchApp API.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":"3","method": "org.rdk.AppManager.1.launchApp", "params":{"appId":"<App_id>"}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The Browser Test App should launch successfully and be accessible from the RDK UI Home screen. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Launch browser test app  | Select the Browser Test App tile under the My Apps section/row of the RDK UI Home screen and press Enter/OK on the remote. If the tile is not visible, launch the app using the org.rdk.AppManager.1.launchApp API.<br>Command: `curl --data-binary '{"jsonrpc":"2.0","id":"3","method":"org.rdk.AppManager.1.launchApp","params":{"appId":"<App_id>"}}' -H 'content-type:text/plain;' http://127.0.0.1:9998/jsonrpc` | The Browser Test App should launch successfully on top of the RDK UI Home screen, displaying the default Browser Test page. The API response should be: {"jsonrpc":"2.0","id":3,"result":null} |
| 2 |  Navigate to PNG image tile  | Use the Tab key on the keyboard to navigate to the PNG IMAGE tile under the Image Formats section and press Enter to load the image file. | The PNG IMAGE tile should load correctly. The .png image file should be displayed on the RDK UI without errors. |
| 3 |  Close browser test app  | Close the Browser Test App by pressing the Back key on the remote. If the Back key does not close the app, terminate it using the org.rdk.AppManager.terminateApp API.<br>Command: `curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 15, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<App_Id>"}}' http://127.0.0.1:9998/jsonrpc` | The Browser Test App should terminate gracefully and the RDK UI Home screen should be visible on the TV/display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
