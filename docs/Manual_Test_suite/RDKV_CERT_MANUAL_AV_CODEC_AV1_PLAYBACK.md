## TestCase ID
RDKV_MANUAL_AV_14
## TestCase Name
RDKV_CERT_MANUAL_AV_Codec_AV1_Playback

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that AV1 stream playback is functional on the DUT. This test exercises the RDK media pipeline, AV decoder plugins, and the video player application to drive codec-specific playback scenarios. The test confirms that the AV1 asset should play with proper audio and video without any artifacts or errors.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Upload MVT test bolt package to server | Copy the MVT Test bolt package into the server (e.g., https://<your_app_bundle_server>/ or any accessible server). | The MVT Test bolt package should be available and accessible on the server. |
| 2 | Download MVT test package via API | Download the MVT Test bolt package from the server using the PackageManagerRDKEMS.download API.<br>Command: `curl -d '{ "jsonrpc": 2.0, "id": 2, "method": "org.rdk.PackageManagerRDKEMS.download", "params": { "url": "<Bolt_Package_URL>" } }' http://127.0.0.1:9998/jsonrpc` | The download API request should succeed and the MVT Test bolt package should be downloaded to the DUT. |
| 3 | Check whether packages are downloaded | Validate that the downloaded package is available in the <PACKAGEMANAGER_FILE_LOCATOR> directory of the DUT.<br>Command: `ls -lh <PACKAGEMANAGER_FILE_LOCATOR>` | The downloaded MVT Test bolt package should be listed in the <PACKAGEMANAGER_FILE_LOCATOR> directory of the DUT. |
| 4 | List packages and get package ID | Validate that the package is listed on the DUT and obtain the package ID from the response.<br>Command: `curl -d '{ "jsonrpc": 2.0, "id": 8, "method": "org.rdk.PackageManagerRDKEMS.listPackages" }' http://127.0.0.1:9998/jsonrpc` | The MVT Test package should be listed and the package ID should be retrievable from the response. |
| 5 | Install MVT test package | Install the downloaded MVT Test package using the PackageManagerRDKEMS.install API.<br>Command: `curl -d '{ "jsonrpc": 2.0, "id": 7, "method": "org.rdk.PackageManagerRDKEMS.install", "params": { "packageId": "<package_id>", "version": "<PACKAGEMANAGER_APP_VERSION>", "additionalMetadata": [ {"name": "type", "value": "native/dac-app"} ], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>" } }' http://127.0.0.1:9998/jsonrpc` | The MVT Test package should be installed successfully on the DUT. |
| 6 | Verify package state as INSTALLED | Validate that the installed package state is "INSTALLED".<br>Command: `curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 8, "method": "org.rdk.PackageManagerRDKEMS.packageState", "params": {"packageId": "<package_id>", "version": "<version>"}}' http://127.0.0.1:9998/jsonrpc` | The package state should be reported as "INSTALLED" in the API response. |
| 7 | Verify MVT test app on home screen | Validate that the installed MVT Test App is available in the My Apps section/row of the RDK UI Homepage. | The MVT Test App should be visible in the My Apps section of the RDK UI Homepage and ready to launch. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch MVT test app | Select the MVT Test App tile under the My Apps section/row of the RDK UI Homepage and press the Enter/OK button on the remote. | The MVT Test App should be launched successfully on top of the RDK UI Homepage. |
| 2 | Navigate to AV1 section and initiate playback | Navigate to the section in the MVT App where the AV1 asset is present and initiate playback of the asset. | The AV1 asset should play with proper audio and video without any artifacts or errors. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
